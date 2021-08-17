

from typing import Any, List

from su_data.su_pipe import su_process_pipe

output_buffers = su_process_pipe(["suplane"], [])

output_buffers = su_process_pipe(["sufilter", "f1=10,f2=20,f3=30,f4-40"], output_buffers)

for buffer in output_buffers:
    print(buffer)
