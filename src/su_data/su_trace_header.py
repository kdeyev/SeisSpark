from typing import Any

from .encoding import get_value
from .segy_trace_header import SEGY_TRACE_HEADER_ENTRIES, SEGYTraceHeaderEntry, SEGYTraceHeaderEntryName

NS_ENTRY: SEGYTraceHeaderEntry = SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.ns]


class SUTraceHeader:
    def __init__(self, buffer: bytes) -> None:
        self.buffer = buffer

    def get_header_value(self, entry: SEGYTraceHeaderEntry) -> Any:
        return get_value(self.buffer, index=entry.position, type=entry.type)

    @property
    def num_samples(self) -> int:
        return self.get_header_value(NS_ENTRY)


def get_header_value(buffer: bytes, entry: SEGYTraceHeaderEntry) -> Any:
    return get_value(buffer, index=entry.position, type=entry.type)
