def correctEEGoffset(sub,session,exp,reader,events):
    # The EEG for many FR subjects (FR1 and catFR1 in particular) does not align with the events since the 
    # implementation of Unity. This is a temporary fix for the EEG alignment for these subjects before
    # the data is corrected in Rhino. Subject-by-subject details are here:
    # https://docs.google.com/spreadsheets/d/1co5f7-dPOktGIXZJ7uptv0SwBJhf36TuhVSMFqRC0X8/edit?usp=sharing
    # JS 2020-09-22
    # Update 2020-09-29 accounting for sampling rate and raising error if eeg events don't exist
    
    ## Inputs ##
    # sub: subject name (type str)
    # session: session number (type int)
    # exp: experiment, typically 'FR1' or 'catFR1' (type str)
    # reader: typical output from CMLReader function (see cmlreaders documentation)
    # events: dataFrame from reader.load('task_events') for your events of choice
    
    import re
    import numpy as np
    
    sub_num = [int(s) for s in re.findall(r'\d+',sub)] # extract number for sub   
    
    corrected_evs= events.copy(deep=True)
    temp_eeg = reader.load_eeg(events=corrected_evs, rel_start=0, rel_stop=100) # just to get sampling rate
    sr = temp_eeg.samplerate
    sr_factor = 1000/sr
    
    if sum(events.eegoffset==-1)>0:
        raise Exception('Events without EEG (those with events.eegoffset=-1) should be removed before calling correctEEGoffset')
 
    if (sub in ['R1379E','R1385E','R1387E','R1394E','R1402E']) or \
        (sub=='R1404E' and session==0 and exp=='catFR1'): 
        # first 5 true for catFR1 and FR1. R1404E only one catFR1 session has partial beep 
        # for these subs there is a partial beep and 500 ms of eeg lag (see "History of issues 2020-09-08" for examples)
        
        # add time (in units of samples) since the events are already ahead of the eeg
        corrected_evs.eegoffset = corrected_evs.eegoffset+int(np.round(500/sr_factor)) 
        #'rectime' is the time, in ms, when a word was recalled relative to the start of the recall period for that list.
        #corrected_evs.loc[corrected_evs.loc[:,'rectime']>=0,'rectime'] = corrected_evs.loc[corrected_evs.loc[:,'rectime']>=0,'rectime'] + 500
        
    # subs where unity was implemented for some sessions but not others
    elif (sub=='R1396T' and exp=='catFR1') or (sub=='R1396T' and session==1) or \
         (sub=='R1395M' and exp=='catFR1') or (sub=='R1395M' and exp=='FR1' and session>0):
        corrected_evs.eegoffset = corrected_evs.eegoffset+int(np.round(1000/sr_factor))
        #corrected_evs.loc[corrected_evs.loc[:,'rectime']>=0,'rectime'] = corrected_evs.loc[corrected_evs.loc[:,'rectime']>=0,'rectime'] + 1000
        
    # do nothing since these sessions were pyEPL so the offset is okay
    elif (sub=='R1406M' and session==0) or (sub=='R1415T' and session==0 and exp=='FR1') or (sub=='R1422T' and exp=='FR1'):
        pass 
    
    # remaining unity subs
    elif sub_num[0]>=1397 or sub == 'R1389J': 
        corrected_evs.eegoffset = corrected_evs.eegoffset+int(np.round(1000/sr_factor))
        #corrected_evs.loc[corrected_evs.loc[:,'rectime']>=0,'rectime'] = corrected_evs.loc[corrected_evs.loc[:,'rectime']>=0,'rectime'] + 1000
        
    return corrected_evs