from typing import List

from .su_trace import SUTrace

class SUGather:
    def __init__(self) -> None:
        self.traces: List[SUTrace] = []