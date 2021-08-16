from .su_trace_header import SUTraceHeader

class SUTrace(SUTraceHeader):
    def __init__(self, data: bytes) -> None:
        super().__init__(data=data)