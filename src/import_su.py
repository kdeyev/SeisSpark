

from typing import Any, List

from obspy.io.segy.segy import iread_segy, iread_su

def su_to_array(filename: str) -> List[Any]:
    for trace in iread_su(filename):
        print(trace)
    
if __name__ == "__main__":
    su_to_array('synth.su')
