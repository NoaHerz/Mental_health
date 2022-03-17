from imports import *
import pandas as pd

def convertMstoWindowNumber(period_ms,start_ms,end_ms,window_length_ms,sliding_window_ms):
    '''Convert time in ms to time-window. 
    The output is the number of time window corresponding to a specific ms, after averaging the data using a sliding window.
    example: time_window_number = convertMstoWindowNumber(-4490,-4500,1000,100,50) 
    will yield the time window for -4490 ms for a data reshaped with 100ms bins, with sliding window of 50 ms, beginning from -4500ms and up to 1000ms
    relative to vocalization. '''
    # PERIOD_ms is the begining of the time window I'm interested in, in ms.
    ms_to_windows_df=ms2WindowNumber(start_ms,end_ms,window_length_ms,sliding_window_ms)
    assert (period_ms/sliding_window_ms).is_integer(),'period start time is not rounded according to the sliding window'
    time_window_counter=-1
    for start,end in ms_to_windows_df['ms (start,end)']: 
        time_window_counter=time_window_counter+1
        if start==period_ms:
            break
    return time_window_counter  

def ms2WindowNumber(start_ms,end_ms,window_length_ms,sliding_window_ms):
    # This function creates a dataframe connecting time windows in ms to the time window number
    # window_length_ms: window length in ms. e.g., 100.
    # start_ms: start of time window relative to stimulus in ms. e.g., -4500.
    # end_ms: end of time window relative to stimulus in ms. e.g., 1000.
    # sliding_window_ms: sliding window in ms. e.g., 50.    
    ms_to_windows=[(i, i + window_length_ms) for i in range(int(start_ms),int(end_ms-window_length_ms+1),int(sliding_window_ms))]
    ms_to_windows_df=pd.Series(ms_to_windows)
    ms_to_windows_df=pd.DataFrame({'ms (start,end)':ms_to_windows_df,'time window number':np.arange(1,len(ms_to_windows_df)+1)})
    return ms_to_windows_df     