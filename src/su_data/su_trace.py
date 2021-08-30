# =============================================================================
# Copyright (c) 2021 SeisSpark (https://github.com/kdeyev/SeisSpark).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
from typing import List

from su_data.segy_trace_header import SEGYTraceHeaderEntryType

from .encoding import get_values
from .su_trace_header import SUTraceHeader


class SUTrace(SUTraceHeader):
    def __init__(self, buffer: bytes) -> None:
        super().__init__(buffer=buffer)

    @property
    def body(self) -> List[float]:
        return get_values(buffer=self.buffer, index=240, type=SEGYTraceHeaderEntryType.float, number=self.num_samples)[0]
