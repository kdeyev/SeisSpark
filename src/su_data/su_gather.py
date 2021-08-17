from typing import List, Any, Tuple

from su_data.segy_trace_header import SEGYTraceHeaderEntry

from .su_trace import SUTrace

class SUGather:
    def __init__(self, key: Any = None, traces: List[SUTrace] = []) -> None:
        self.key = key
        self.traces: List[SUTrace] = traces

    @property
    def trace_count(self) -> int:
        return len(self.traces)

    
    def get_header_entry_values(self, header_entry: SEGYTraceHeaderEntry) -> List[Any]:
        return list([trace.get_header_value(header_entry) for trace in self.traces])