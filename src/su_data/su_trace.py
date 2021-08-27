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
