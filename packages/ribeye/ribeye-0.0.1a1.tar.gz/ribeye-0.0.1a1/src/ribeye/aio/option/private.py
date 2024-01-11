#  Copyright 2023 The Beef Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.


from beef.aio import Client, Context
from beef.aio.internal import EndpointDescriptor
from beef.internal.types import PT, T


class PrivateOption:
    __PRIORITY = 50

    def __call__(self, descriptor: EndpointDescriptor[PT, T]) -> None:
        descriptor.register_operator(PrivateOption.__PRIORITY, PrivateOption.__operator)

    @staticmethod
    async def __operator(ctx: Context[Client, T]) -> T:
        await ctx.client.authenticate(ctx.request)
        return await ctx.proceed()


Instance = PrivateOption()
