from .encoding import get_value
from .segy_trace_header import SEGYTraceHeaderEntry, SEGY_TRACE_HEADER_ENTRYS, SEGYTraceHeaderEntryName

NS_ENTRY: SEGYTraceHeaderEntry = SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.ns]

class SUTraceHeader:
    def __init__(self, data: bytes) -> None:
        self.data = data

    def get_header_value(self, entry: SEGYTraceHeaderEntry):
        return get_value(data=self.data, index=entry.position, type=entry.type)

    @property 
    def num_samples(self) -> int: 
        return self.get_header_value(NS_ENTRY)