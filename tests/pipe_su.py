

from typing import Any, List

from su_data.su_pipe import su_process_pipe

output_traces = su_process_pipe(["suplane"], [])

output_traces = su_process_pipe(["sufilter", "f1=10,f2=20,f3=30,f4-40"], output_traces)

for trace in output_traces:
    print(trace.body)
