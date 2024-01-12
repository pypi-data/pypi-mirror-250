# Copyright (C) 2022 Bjarne von Horn (vh at igh dot de).
#
# This file is part of the PdCom library.
#
# The PdCom library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# The PdCom library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more .
#
# You should have received a copy of the GNU Lesser General Public License
# along with the PdCom library. If not, see <http://www.gnu.org/licenses/>.

from asyncio import Event, Future, get_event_loop
from . import _PdComWrapper as PdComWrapper
from .Variable import Variable
from datetime import timedelta
from numbers import Number
from typing import Optional, Union, AsyncContextManager
from weakref import WeakSet
import numpy


class _Subscription(PdComWrapper.Subscription):
    def __init__(
        self,
        subscriber: "SubscriberBase",
        variable: Union[str, PdComWrapper.Variable],
        fut: Future,
        selector: Optional[PdComWrapper.Selector],
    ):
        if isinstance(variable, str):
            super().__init__(
                subscriber._subscriber,
                subscriber._subscriber._process._process,
                variable,
                selector,
            )
        else:
            super().__init__(subscriber._subscriber, variable._v, selector)
        self._pending_subscription_future = fut
        self._value_queue = []

    def _push_value_queue(self):
        self._value_queue.append(self.value)

    def _pop_value_queue(self):
        if len(self._value_queue) > 0:
            self._value_queue.pop(0)

    def current_value(self):
        if len(self._value_queue) > 0:
            return self._value_queue[0]
        return self.value


class Subscription:
    State = PdComWrapper.Subscription.State
    """State enum of a subscription"""

    def __init__(
        self,
        subscriber: "SubscriberBase",
        variable: Union[str, PdComWrapper.Variable],
        fut: Future,
        selector: Optional[PdComWrapper.Selector],
    ):
        self.subscriber = subscriber
        self._subscription = _Subscription(subscriber, variable, fut, selector)
        subscriber._subscriber._subscriptions.add(self)
        # trigger process to call callbacks in case subscription is already ready
        subscriber._subscriber._process._process.callPendingCallbacks()

    def cancel(self):
        """Cancel a subscription."""
        if self._subscription is not None:
            self._subscription.cancel()
            self._subscription = None

    async def poll(self):
        """Poll an existing subscription.

        This can for example be used to refresh an event-based subscription.
        """
        # FIXME(vh) in case of event or periodic subscription,
        # newValues() may be called prematurely
        self._subscription.poll()
        async with self.subscriber.newValues():
            return self.value

    async def read(self):
        """Wait for an update and return the new value.

        :return: tuple of (value, timestamp)
        """
        async with self.subscriber.newValues() as ts:
            return (self.value, ts)

    @property
    def value(self):
        """The current value."""
        v = self._subscription.current_value()
        if v.shape == (1,):
            return v[0]
        else:
            return v

    @property
    def variable(self):
        """The corresponding variable."""
        return Variable(self._subscription.variable)

    @property
    def state(self) -> "Subscription.State":
        """The current state of the subscription."""
        return self._subscription.state

    def __iter__(self):
        """Iterate Row-wise over values."""
        return numpy.nditer(self._subscription.current_value(), order="C")


class _Subscriber(PdComWrapper.Subscriber):
    def __init__(self, process, transmission: PdComWrapper.Transmission):
        if isinstance(transmission, timedelta):
            transmission = PdComWrapper.Transmission(transmission)
        elif isinstance(transmission, Number):
            transmission = PdComWrapper.Transmission(timedelta(seconds=transmission))
        super().__init__(transmission)
        self._process = process
        process._process._subscribers.add(self)
        self._newvalues_event: Event = Event()
        self._process_exception = None
        self._subscriptions: WeakSet[Subscription] = WeakSet()
        self._synchronizer_count = 0
        self._cached_timestamps: list[timedelta] = []

    def stateChanged(self, s: PdComWrapper.Subscription) -> None:
        if s.state == s.State.Active and s._pending_subscription_future is not None:
            if not s._pending_subscription_future.cancelled():
                s._pending_subscription_future.set_result(None)
            s._pending_subscription_future = None
        elif s.state == s.State.Invalid and s._pending_subscription_future is not None:
            if not s._pending_subscription_future.cancelled():
                s._pending_subscription_future.set_exception(
                    PdComWrapper.InvalidSubscription()
                )
            s._pending_subscription_future = None

    def newValues(self, time: timedelta) -> None:
        # this is a virtual function called by C++ PdCom5
        if self._synchronizer_count > 0:
            # caching values requested because of "synchronizeNewValues"
            for subscription in self._subscriptions:
                if subscription is not None:
                    subscription._subscription._push_value_queue()
            self._cached_timestamps.append(time)
            self._process_exception = None
            self._newvalues_event.set()

    async def synchronizerEnter(self) -> timedelta:
        await self._newvalues_event.wait()
        # raise exception passed by Process._cancel_all_futures
        if self._process_exception is not None:
            raise self._process_exception
        return self._cached_timestamps[0]

    async def synchronizerExit(self):
        # user is done processing current values, so close the window
        self._synchronizer_count -= 1
        if self._synchronizer_count == 0:
            for sub in self._subscriptions:
                if sub is not None:
                    sub._subscription._pop_value_queue()
            self._cached_timestamps.pop(0)
            if len(self._cached_timestamps) == 0:
                self._newvalues_event.clear()


class NewValuesSynchronizer:
    def __init__(self, sub: "_Subscriber"):
        self._subscriber = sub
        if self._subscriber._synchronizer_count != 0:
            raise ValueError("do not use the same subscription in multiple tasks")
        self._subscriber._synchronizer_count += 1

    async def __aenter__(self) -> timedelta:
        return await self._subscriber.synchronizerEnter()

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._subscriber.synchronizerExit()
        return False


class SubscriberBase:
    def __init__(self, process, transmission: PdComWrapper.Transmission):
        self._subscriber = _Subscriber(process, transmission)

    def newValues(self) -> AsyncContextManager[timedelta]:
        """Entry point for library users to process incoming data.

        This function return an asynchronous context manager.
        In the body of the context manager, the values of the subscriptions
        assigned to this subscriber are guaranteed to not change.
        The handle returned by the context manager (:code:`async with ... as ts`)
        is the timestamp of the values as timedelta instance.

        The following example shows how to subscribe to two variables with
        a period of one second.

        .. code-block:: python

            import pdcom5
            process = pdcom5.Process()
            await process.connect("msr://localhost")
            subscriber = process.create_subscriber(1.0)
            cos = await subscriber.subscribe("/osc/cos")
            sin = await subscriber.subscribe("/osc/sin")
            running = True
            while running:
                async with subscriber.newValues() as timestamp:
                    print(f"At {timestamp}, cos was {cos.value}" +
                            f" and sin was {sin.value}.")

        Please do not do any blocking operations in the body of the context
        manager, like sleeping for a long time. The reason is that the library
        has to cache the incoming values in some cases to make sure no data is
        skipped. Also, using the same subscription in multiple concurrent tasks
        is not allowed, for the same reason. Just create one subscriber per task.
        """
        return NewValuesSynchronizer(self._subscriber)


class Subscriber(SubscriberBase):
    """Variable subscriber.

    This class manages how variables are subscribed and the callback when new
    values are received.

    :param process: Process instance
    :param transmission: Kind of subscription (poll, event based, periodic)
    """

    def __init__(self, process, transmission: PdComWrapper.Transmission):
        super().__init__(process, transmission)

    async def subscribe(
        self,
        variable: Union[str, PdComWrapper.Variable],
        selector: Optional[PdComWrapper.Selector] = None,
    ) -> Subscription:
        """Subscribe to a variable.

        :param variable: Variable to subscribe.
        :param selector: Optional selector to create a view on multidimensional data.

        :return: a Subscription instance.
        """
        fut = get_event_loop().create_future()
        ans = Subscription(self, variable, fut, selector)
        await fut
        return ans
