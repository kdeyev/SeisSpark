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
from typing import Any, List

from su_data.segy_trace_header import SEGYTraceHeaderEntry

from .su_trace import SUTrace


class SUGather:
    def __init__(self, key: int, traces: List[SUTrace] = []) -> None:
        self.key = key
        self.traces: List[SUTrace] = traces

    @property
    def trace_count(self) -> int:
        return len(self.traces)

    def get_header_entry_values(self, header_entry: SEGYTraceHeaderEntry) -> List[Any]:
        return [trace.get_header_value(header_entry) for trace in self.traces]

    def get_data_array(self) -> List[List[float]]:
        return [trace.body for trace in self.traces]
