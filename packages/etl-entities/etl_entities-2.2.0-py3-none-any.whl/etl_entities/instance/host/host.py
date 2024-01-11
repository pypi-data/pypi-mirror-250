#  Copyright 2022 MTS (Mobile Telesystems)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from __future__ import annotations

from pydantic import AnyUrl, ConstrainedStr, parse_obj_as


class Host(ConstrainedStr):
    """Generic host representation"""

    min_length = 1

    @classmethod
    def validate(cls, value: str) -> str:
        url = parse_obj_as(AnyUrl, f"http://{value}")  # NOSONAR
        if url.host != value:
            raise ValueError(f"Invalid host {value}")

        return value
