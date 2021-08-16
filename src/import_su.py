

from typing import Any, List

from su_data.su_pipe import su_process_pipe

output_traces = su_process_pipe(["suplane"], [])

output_traces = su_process_pipe(["sufilter", "f1=10,f2=20,f3=30,f4-40"], output_traces)


for trace in output_traces:
    print(trace.data)
# from obspy.io.segy.segy import iread_segy, iread_su

# def su_to_array(filename: str) -> List[Any]:
#     for trace in iread_su(filename):
#         print(trace)
    
# if __name__ == "__main__":
#     su_to_array('synth.su')
