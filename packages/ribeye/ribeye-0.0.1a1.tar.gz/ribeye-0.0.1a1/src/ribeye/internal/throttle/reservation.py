#  Copyright 2023 The Beef Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.


from dataclasses import dataclass

from beef.internal.time_ import Time

Tokens = float


@dataclass()
class Reservation:
    tokens: Tokens
    ready_at: Time
