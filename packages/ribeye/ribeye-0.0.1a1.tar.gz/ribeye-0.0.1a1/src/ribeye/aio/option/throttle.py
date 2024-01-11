#  Copyright 2023 The Beef Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.


import asyncio
import time as sys_time
from typing import Awaitable, Callable

from beef.aio import Client, Context
from beef.aio.internal import EndpointDescriptor
from beef.internal.types import PT, T


class ThrottleOption:
    __PRIORITY = 80

    def __init__(
        self, tokens: float, sleep_func: Callable[[float], Awaitable[None]] = asyncio.sleep
    ) -> None:
        self.tokens = tokens
        self.sleep_func = sleep_func

    def __call__(self, descriptor: EndpointDescriptor[PT, T]) -> None:
        if self.tokens > 0.0:
            descriptor.register_operator(ThrottleOption.__PRIORITY, self.__operator)

    async def __operator(self, ctx: Context[Client, T]) -> T:
        current_time = sys_time.monotonic()
        reservation = ctx.client.limiter.reserve_at(current_time, self.tokens)
        delay = reservation.ready_at - current_time
        if delay > 0:
            await self.sleep_func(delay)

        return await ctx.proceed()
