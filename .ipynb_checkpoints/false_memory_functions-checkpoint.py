import xarray as xr
import numpy as np
from ptsa.data.timeseries import TimeSeries

def add_mirror_buffer_adjusted(eeg_ptsa, duration):
    """
    Return a time series with mirrored data added to both ends of this
    time series (up to specified length/duration).
    The new series total time duration is:
        ``original duration + 2 * duration * samplerate``
    Parameters
    ----------
    duration : float
        Buffer duration in seconds.
    Returns
    -------
    New time series with added mirrored buffer.
    """
    samplerate = float(eeg_ptsa['samplerate'])
    samples = int(np.ceil(float(eeg_ptsa['samplerate']) * duration))   

    if samples > len(eeg_ptsa['time']):
        raise ValueError("Requested buffer time is longer than the data")

    data = eeg_ptsa.data

    mirrored_data = np.concatenate(
        (data[..., 1:samples + 1][..., ::-1], data,
         data[..., -samples - 1:-1][..., ::-1]), axis=-1)

    start_time = eeg_ptsa['time'].data[0] - (duration*1000) # Noa's edit
    t_axis = (np.arange(mirrored_data.shape[-1]) * (1000 / samplerate))+start_time #Noa's edit
    coords = {dim_name:eeg_ptsa.coords[dim_name]
              for dim_name in eeg_ptsa.dims[:-1]}
    coords['time'] = t_axis
    coords['samplerate'] = float(eeg_ptsa['samplerate'])

    return TimeSeries(mirrored_data, dims=eeg_ptsa.dims, coords=coords)

def add_output_position(evs):
    '''
    This function adds an 'output position' column to events dataframe.
    The input is the event strcture (the result of: evs = reader.load('task_events'))
    The output is the same event structure with an additional column for output position of each recalled word.
'''
    import numpy as np
    
    output_position=np.zeros(len(evs))*np.nan
    for session in evs['session'].unique():
        session_evs=evs[evs['session']==session]
        for list in session_evs['list'].unique()[session_evs['list'].unique()>=0]:
            list_evs=session_evs[session_evs['list']==list]
            rec_evs=list_evs[list_evs['type']=='REC_WORD']
            list_output_position=np.arange(1,len(rec_evs)+1)
            rec_evs_indx=list_evs[list_evs['type']=='REC_WORD'].index
            serial_ind=np.zeros(len(rec_evs_indx))*np.nan
            i=0
            for index_val in rec_evs_indx:
                bool_mat=evs.index==index_val
                assert sum(bool_mat)==1
                serial_ind[i]=np.where(bool_mat==True)[0]
                i=i+1
            assert len(rec_evs_indx)==len(list_output_position)
            output_position[serial_ind.astype(int)]=list_output_position
    evs['output position']=output_position # ADD COLUMN
    assert all(np.isnan(evs[evs['type']!='REC_WORD']['output position'])),'error in creating a mask for recall events'
    pos_list_evs=evs[evs['list']>0]
    assert any(np.isnan(pos_list_evs[pos_list_evs['type']=='REC_WORD']['output position']))==False,'error in creating a mask for recall events'
    return evs

# import numpy as np
def add_rec_ISI(evs): 
    '''
    This function adds an 'ISI' column to the events dataframe.
    The input is the event strcture (the result of: evs = reader.load('task_events'))
    The output is the same event structure with an additional column for the ISI of each recalled word (i.e. time between recalled words).'''
    rec_ISI=np.full(len(evs),np.nan)
    rec_words_index=evs[evs['type']=='REC_WORD'].index # recalled words' index
    ISI=np.full(len(evs),np.nan)
    for i in rec_words_index:
        diff=evs['rectime'].loc[i]-evs['rectime'].loc[i-1] # time diff between recalls
        for j in range(0,len(evs)):
            if sum(evs.iloc[j]==evs.loc[i])==len(evs.columns):
                ISI[j]=diff
    evs['ISI']=ISI # ADD COLUMN    
    return evs

def categorized_words(evs,list_n):
    '''create a df with the encoded semantic categories (3 categories in catFR) and their related words (four words per category) for each list'''
    import pandas as pd
    assert list_n>=0, 'list number is negative'
    category_words=pd.DataFrame([])
    encoding_evs=evs[evs['type']=='WORD']
    list_evs=encoding_evs[encoding_evs['list']==list_n]
    if len(list_evs)==0: # if no events exist
        category_words=category_words.append({'category':[],'words':[]},ignore_index=True)
    else:
        #    A specific problem with sub R1488T that has 22 encoded words
        if list_evs['eegfile'].iloc[0][0:6]=='R1488T' and list_evs['list'].unique()[0]==11 and list_evs['session'].unique()[0]==0:
            list_evs=list_evs.iloc[10:]
        if len(list_evs)>0:
            if len(list_evs)==12:
    #           print('wrong number of words in list:', list_n,'subject:', evs['eegfile'][0][0:6]) # words number
                categories=list_evs['category'].unique()
                if len(categories)!=3:
                    print('wrong number of words in list:', list_n,'subject:', evs['eegfile'][0][0:6])# categories number
                for category in categories:
                    category_evs=list_evs[list_evs['category']==category]
                    assert len(category_evs['item_name'].tolist())==4 # 4 words per category
                    category_words=category_words.append({'category':category,'words':category_evs['item_name'].tolist()},ignore_index=True)
    return category_words


import pandas as pd
# change path to excel file:
categorized_ELIs_list = pd.read_excel('/home1/noaherz/Long2017/code_sharing/ELI_words_catFR_comparison_final.xlsx',engine="openpyxl")

def add_semantic_relatedness(evs):
    '''Add sematic relatedness column (1= the intrusion belong to the same semantic category as the ones in encoding, 0 = intrusion does not belong to any semantic category in the encoded list).
    The input is the event structure, as produced by reader.load('task_events').
    The output is the same event structure with a new sematic relatedness column'''
    import numpy as np
    if any(evs.columns=='item_name'): # in the pyFR and FR/catFR this column has a different name 
            item='item_name'
    elif any(evs.columns=='item'):
            item='item'
 
    evs_reset=evs.reset_index(drop=True) # I added this line at a ater stage of the analysis

    semantic_relatedness=np.zeros(len(evs_reset))*np.nan
    for session in evs['session'].unique():
        session_evs=evs_reset[evs_reset['session']==session]
        for list_n in session_evs['list'].unique()[session_evs['list'].unique()>=0]:
            list_evs=session_evs[session_evs['list']==list_n]
            rec_evs=list_evs[list_evs['type']=='REC_WORD']
            rec_evs_index=rec_evs.index
            
            # check what were the three list semantic categories:
            encoded_categories = categorized_words(evs,list_n)
            if len(encoded_categories)>1:
                encoded_categories = list(encoded_categories['category'])

                for row in rec_evs_index:
                    if rec_evs['intrusion'].loc[row]==0: # correct recalls
                        semantic_category=rec_evs['category'].loc[row]
                        semantic_relatedness_bool=semantic_category in encoded_categories
                        semantic_relatedness[row]=semantic_relatedness_bool
                    elif rec_evs['intrusion'].loc[row]>0: # PLIs
                        intruded_list=rec_evs['intrusion'].loc[row]
                        word=rec_evs[item].loc[row]
                        word=word.upper()
                        bool_list=evs[evs['list']==list_n-intruded_list][item]==word
                        semantic_category=list(evs[evs['list']==list_n-intruded_list][bool_list]['category'])[0]
                        semantic_relatedness_bool=semantic_category in encoded_categories
                        semantic_relatedness[row]=semantic_relatedness_bool
                    elif rec_evs['intrusion'].loc[row]==-1: # ELIs
                        word=rec_evs[item].loc[row]
                        word=word.upper()

                        # Extract the manual coding of the semantic category for ELI:
                        word_indx=categorized_ELIs_list[categorized_ELIs_list['Rater 1']==word].index
                        assert list(categorized_ELIs_list.loc[word_indx]['Rater 1'])==list(categorized_ELIs_list.loc[word_indx]['Rater 2'])
                        
                        if any(word_indx):
                            semantic_bool=[]
                            if int(categorized_ELIs_list.loc[word_indx]['Camparison'])==0: # if raters did not agree on semantic category
                                semantic_relatedness[row]=False
                            elif int(categorized_ELIs_list.loc[word_indx]['Camparison'])==1: # if there was agreement between raters 
                                for category_n in encoded_categories:
                                    semantic_bool.append(any(categorized_ELIs_list.loc[word_indx]==category_n))
                                semantic_relatedness_bool=any(semantic_bool)
                                semantic_relatedness[row]=semantic_relatedness_bool
    evs['semantic_relatedness']=semantic_relatedness
    return evs

def add_output_position(evs):
    '''
    This function adds an 'output position' column to events dataframe.
    The input is the event strcture (the result of: evs = reader.load('task_events'))
    The output is the same event structure with an additional column for output position of each recalled word.
'''
    import numpy as np
    
    output_position=np.zeros(len(evs))*np.nan
    for session in evs['session'].unique():
        session_evs=evs[evs['session']==session]
        for list in session_evs['list'].unique()[session_evs['list'].unique()>=0]:
            list_evs=session_evs[session_evs['list']==list]
            rec_evs=list_evs[list_evs['type']=='REC_WORD']
            list_output_position=np.arange(1,len(rec_evs)+1)
            rec_evs_indx=list_evs[list_evs['type']=='REC_WORD'].index
            serial_ind=np.zeros(len(rec_evs_indx))*np.nan
            i=0
            for index_val in rec_evs_indx:
                bool_mat=evs.index==index_val
                assert sum(bool_mat)==1
                serial_ind[i]=np.where(bool_mat==True)[0]
                i=i+1
            assert len(rec_evs_indx)==len(list_output_position)
            output_position[serial_ind.astype(int)]=list_output_position
    evs['output position']=output_position # ADD COLUMN
    assert all(np.isnan(evs[evs['type']!='REC_WORD']['output position'])),'error in creating a mask for recall events'
    pos_list_evs=evs[evs['list']>0]
    assert any(np.isnan(pos_list_evs[pos_list_evs['type']=='REC_WORD']['output position']))==False,'error in creating a mask for recall events'
    return evs

# compute means
def average_tilt(long_df,condition,column_string):
    '''
    Compute average for each event type (correcl recall/intrusion/deliberation) as well as the difference between correct recalls and intrusions
    column_string can be: 'HFA_LFA_diff'/'LFA'/'HFA'/'Low_theta'
    condition can be: 'all'/'related'/'nonrelated'
    exmaple: average_tilt(long_df,'all','HFA_LFA_diff')
    '''
    
    import pandas as pd
    if condition == 'all':
        pass
    elif condition == 'related': 
        long_df = long_df[long_df['semantic_relatedness']==1]
    elif condition == 'nonrelated':        
        intrusions_index=long_df[long_df['event_type'].isin(['intrusion','PLI','ELI'])].index
        intrusions_only=long_df.loc[intrusions_index]
        intrusions_related=intrusions_only[intrusions_only['semantic_relatedness']==1].index
        long_df = long_df.drop(labels=list(intrusions_related))
    else:
        print('Wrong condition parameter. Options are: "all"/"related" or "nonrelated" ')
        
    diff=pd.DataFrame([])
    correct_recall_mean_tilt=[]
    intrusion_mean_tilt=[]
    deliberation_mean_tilt=[]
    ELI_mean_tilt=[]
    PLI_mean_tilt=[]
    for sub in long_df['subject'].unique():
        subj_mean=long_df[long_df['subject']==sub]
        try:
            assert 'correct recall' in subj_mean['event_type'].unique(),f'correct recall missing for subject {sub}'
            assert 'intrusion' in subj_mean['event_type'].unique(),f'intrusions missing for subject {sub}'
            assert 'deliberation' in subj_mean['event_type'].unique(),f'deliberations missing for subject {sub}'
            if 'PLI' in subj_mean['event_type'].unique():
                sub_num=subj_mean['subject'].unique()
                assert 'ELI' in subj_mean['event_type'].unique(), f'problem with subject {sub_num}'
            
            for event in subj_mean['event_type'].unique():
                mean_tilt=np.mean(subj_mean[subj_mean['event_type']==event][column_string])
                if event=='correct recall':
                    correct_recall_mean_tilt.append(mean_tilt)
                elif event=='intrusion':
                    intrusion_mean_tilt.append(mean_tilt)
                elif event=='deliberation':
                    deliberation_mean_tilt.append(mean_tilt)
                elif event=='PLI':
                    PLI_mean_tilt.append(mean_tilt)
                elif event=='ELI':
                    ELI_mean_tilt.append(mean_tilt) 

            for sess in subj_mean['sessions'].unique():
                sess_data=subj_mean[subj_mean['sessions']==sess]
                correct_rec=np.mean(sess_data[sess_data['event_type']=='correct recall'][column_string])
                intrusion=np.mean(sess_data[sess_data['event_type']=='intrusion'][column_string])
    #             tilt_diff.append(correct_r_tilt - intrusion_tilt)
                diff=diff.append({'subject': sub, 'session':sess,'correct_intrusion_diff': correct_rec - intrusion},ignore_index=True)
        except: 
            pass
    return diff,correct_recall_mean_tilt,intrusion_mean_tilt,deliberation_mean_tilt,PLI_mean_tilt,ELI_mean_tilt



# from imports import *
# import pandas as pd

def ms2WindowNumber(start_ms,end_ms,window_length_ms,sliding_window_ms):
    ''' This function creates a dataframe connecting time windows in ms to the time window number
    # window_length_ms: window length in ms. e.g., 100.
    # start_ms: start of time window relative to stimulus in ms. e.g., -4500.
    # end_ms: end of time window relative to stimulus in ms. e.g., 1000.
    # sliding_window_ms: sliding window in ms. e.g., 50. 
    '''
    ms_to_windows=[(i, i + window_length_ms) for i in range(int(start_ms),int(end_ms-window_length_ms+1),int(sliding_window_ms))]
    ms_to_windows_df=pd.Series(ms_to_windows)
    ms_to_windows_df=pd.DataFrame({'ms (start,end)':ms_to_windows_df,'time window number':np.arange(1,len(ms_to_windows_df)+1)})
    return ms_to_windows_df  

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


# list of subjects that their eeg is misaligned
def correctEEGsubjects(sub):
    import re
    sub_num = [int(s) for s in re.findall(r'\d+',sub)]
    if sub_num[0]>=1397:
        in_list = True
    elif sub in ['R1379E','R1385E','R1387E','R1394E','R1402E','R1404E','R1396T','R1396T','R1395M','R1389J']:
        in_list = True
    else:
        in_list = False
    return in_list


def event_type_index(chosen_data):   
    '''the input ("chosen_data") is the event structure that containes the words I want to seperate to correct/intrusions/deliberation. ...
    The Output is the index array of each event type (which can be then used to extract the associated items from the initial "chosen_data" df)'''
    
    import pandas as pd
    # define output variables
    events_index=pd.DataFrame([])
    correct_recall_serial_index=[] ;ELI_serial_index=[]; PLI_serial_index=[];all_intrusions_serial_index=[]
    deliberation_serial_index=[];related_intrusions_serial_index=[]; nonrelated_intrusions_serial_index=[]
    related_PLI_serial_index=[] ; nonrelated_PLI_serial_index = []; related_ELI_serial_index=[]; nonrelated_ELI_serial_index=[]
    
    if 'semantic_relatedness' in chosen_data.columns:
        semantic_columns_exist=True
    else:
        semantic_columns_exist=False
        
    if any(chosen_data.columns=='item_name'): # in the pyFR and FR/catFR this column has a different name 
            item='item_name'
    elif any(chosen_data.columns=='item'):
            item='item'
    for ii in range(0,len(chosen_data)):
        intrusion_value=chosen_data['intrusion'].iloc[ii]
        if semantic_columns_exist==True:
            semantic_boolean=chosen_data['semantic_relatedness'].iloc[ii]
        word=chosen_data[item].iloc[ii]
        if intrusion_value==0:
            correct_recall_serial_index.append(ii)
            deliberation_serial_index.append(ii)
        elif intrusion_value==-1 and word!='<>': 
            ELI_serial_index.append(ii)
            all_intrusions_serial_index.append(ii)
            deliberation_serial_index.append(ii)
            if semantic_columns_exist==True:
                if semantic_boolean==1:
                    related_intrusions_serial_index.append(ii)
                    related_ELI_serial_index.append(ii)
                elif semantic_boolean==0:
                    nonrelated_intrusions_serial_index.append(ii)
                    nonrelated_ELI_serial_index.append(ii)
            elif semantic_columns_exist==False:
                related_intrusions_serial_index=[];nonrelated_intrusions_serial_index=[];

        elif intrusion_value==-1 and word=='<>': 
            deliberation_serial_index.append(ii)
        elif intrusion_value>0:
            PLI_serial_index.append(ii)
            all_intrusions_serial_index.append(ii)
            deliberation_serial_index.append(ii)
            if semantic_columns_exist==True:
                if semantic_boolean==1:
                    related_intrusions_serial_index.append(ii)
                    related_PLI_serial_index.append(ii)
                elif semantic_boolean==0:
                    nonrelated_intrusions_serial_index.append(ii)
                    nonrelated_PLI_serial_index.append(ii)
            elif semantic_columns_exist==False:
                related_intrusions_serial_index=[];nonrelated_intrusions_serial_index=[];
                
    assert len(chosen_data)>=len(PLI_serial_index+ELI_serial_index+correct_recall_serial_index),'there is an error in the calculation of events serial index' 
    assert len(all_intrusions_serial_index)==len(ELI_serial_index)+len(PLI_serial_index),'error in All_intrusions_serial_index calculation'
    assert len(chosen_data)==len(deliberation_serial_index),'error in deliberation_serial_index calculation'
    
    events_index=events_index.append({'correct_recall_serial_index':correct_recall_serial_index,'ELI_serial_index':ELI_serial_index,'PLI_serial_index':PLI_serial_index,
                         'all_intrusions_serial_index':all_intrusions_serial_index,'deliberation_serial_index':deliberation_serial_index,
                         'related_intrusions_serial_index':related_intrusions_serial_index,'nonrelated_intrusions_serial_index':nonrelated_intrusions_serial_index,'related_PLI_serial_index': related_PLI_serial_index, 'nonrelated_PLI_serial_index':nonrelated_PLI_serial_index,'related_ELI_serial_index':related_ELI_serial_index,'nonrelated_ELI_serial_index':nonrelated_ELI_serial_index},ignore_index=True)

    return events_index

def getBadChannels(pairs,elec_cats,remove_soz_ictal):
    ''' load information on seizure onset zone and bad electrodes'''
    import numpy as np
    bad_bp_mask = np.zeros(len(pairs))
    if elec_cats != []:
        if remove_soz_ictal == True:
            bad_elecs = elec_cats['bad_channel'] + elec_cats['soz'] + elec_cats['interictal']
        else:
            bad_elecs = elec_cats['bad_channel']
        for row_num in range(0,len(pairs)): 
            labels=pairs.iloc[row_num]['label']
            elec_labels = labels.split('-')
            if elec_labels[0] in bad_elecs or elec_labels[1] in bad_elecs:
                bad_bp_mask[row_num] = 1
    return bad_bp_mask

def getElecCats(reader):  
    try:
        elec_cats = reader.load('electrode_categories') # contains info about seizure onset zone, interictal spiking, broken leads.
        bad_elec_status=str(len(elec_cats))+' electrode categories'
    except:
        bad_elec_status= 'failed loading electrode categories'
        elec_cats = []
    return elec_cats,bad_elec_status       
    
    
def getMTLregions(MTL_labels):
    ''' see brain_labels.py for MTL_labels ''' 
    HPC_labels = [MTL_labels[i] for i in [0,1,2,3,4,9,10,11,12,13,25,30,35,40,45,46,49,52,53,56]] # all labels within HPC
    ENT_labels = [MTL_labels[i] for i in [6,15,21,24,29,34,39,47,54]] # all labels within entorhinal
    PHC_labels = [MTL_labels[i] for i in [7,16,20,26,31,36,41,48,55]] # all labels within parahippocampal
    return HPC_labels,ENT_labels,PHC_labels  

# Compare models :
from scipy import stats

def lrtest(llmin, llmax,df = 1):
    lr = 2 * (llmax - llmin)
    if llmax<llmin:
        raise ValueError('Check assumptions.')
    stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)
    p = stats.chisqprob(lr, df) 
    return lr, p

def missing_channels(pairs,exp,sub): 
    '''
    This function specifies subjects that need manual removal of electrodes.
    This should be, in the future, implemanted as part of the lab's data loading process.
'''
    row_indx=[]
    delete_chans=[]
    missing_chans=[]
    if sub == 'R1350D':
        missing_chans= ['LAHCMD2-LAHCMD3', 'LAHCMD4-LAHCMD5', 'LAHCMD6-LAHCMD7', 'LAHCMD8-LAHCMD1', 'LPHCMD2-LPHCMD3', 'LPHCMD4-LPHCMD5', 'LPHCMD6-LPHCMD7', 'LPHCMD8-LPHCMD1']
    elif sub == 'R1354E':
        missing_chans= ['5Ldm1-5Ldm2', '5Ldm2-5Ldm3', '5Ldm3-5Ldm4', '5Ldm4-5Ldm5', '5Ldm5-5Ldm6', '5Ldm6-5Ldm7', '5Ldm7-5Ldm8', '5Ldm8-5Ldm9', '5Ldm9-5Ldm1', '25Ldm1-25Ldm2', '25Ldm2-25Ldm3', '25Ldm3-25Ldm4', '25Ldm4-25Ldm5', '25Ldm5-25Ldm6', '25Ldm6-25Ldm7', '25Ldm7-25Ldm8', '25Ldm8-25Ldm9', '25Ldm9-25Ldm1']
    elif sub == 'R1368T':
        missing_chans=['LBMicro1-LBMicro2', 'LBMicro2-LBMicro3', 'LBMicro3-LBMicro4', 'LBMicro4-LBMicro5', 'LBMicro5-LBMicro6', 'LBMicro6-LBMicro7', 'LBMicro7-LBMicro8', 'LBMicro8-LBMicro1']
    elif sub=='R1387E':
        missing_chans=['5Ld8-5Ld9', '5Ld10-5Ld11', '5Ld12-5Ld1', '5Ld14-5Ld15', '5Ld16-5Ld13']
    elif sub=='R1393T' and exp=='catFR1':
        missing_chans=['LBMI2-LBMI3', 'LBMI4-LBMI5', 'LBMI6-LBMI7', 'LBMI8-LBMI1', 'LBMI10-LBMI11', 'LBMI12-LBMI13', 'LBMI14-LBMI15', 'LBMI16-LBMI9']
    elif sub == 'R1492J' and exp=='catFR1':
        missing_chans=['LQA7-LQA8']
    elif sub == 'R1525J' and exp=='catFR1':
        missing_chans= ['RQ6-RQ7', 'LC10-LC11']
    for row in range(0,len(pairs)):
        labels=pairs['label'][row]
        if labels in missing_chans:
            delete_chans.append(row)
            row_indx.append(row)
    pairs=pairs.drop(axis=0,labels=delete_chans)
    return pairs,row_indx

import numpy
def Loc2PairsTranslation(pairs,localizations):
    # localizations is all the possible contacts and bipolar pairs locations
    # pairs is the actual bipolar pairs recorded (plugged in to a certain montage of the localization)
    # this finds the indices that translate the localization pairs to the pairs/tal_struct

    loc_pairs = localizations.type.pairs
    loc_pairs = numpy.array(loc_pairs.index)
    split_pairs = [pair.upper().split('-') for pair in pairs.label] # pairs.json is usually upper anyway but things like "micro" are not
    pairs_to_loc_idxs = []
    for loc_pair in loc_pairs:
        loc_pair = [loc.upper() for loc in loc_pair] # pairs.json is always capitalized so capitalize location.pairs to match (e.g. Li was changed to an LI)
        loc_pair = list(loc_pair)
        idx = (numpy.where([loc_pair==split_pair for split_pair in split_pairs])[0])
        if len(idx) == 0:
            loc_pair.reverse() # check for the reverse since sometimes the electrodes are listed the other way
            idx = (numpy.where([loc_pair==split_pair for split_pair in split_pairs])[0])
            if len(idx) == 0:
                idx = ' '
        pairs_to_loc_idxs.extend(idx)

    return pairs_to_loc_idxs # these numbers you see are the index in PAIRS frame that the localization.pairs region will get put

def get_elec_regions(localizations,pairs): 
    # 2020-08-13 new version after consulting with Paul 
    # suggested order to use regions is: stein->das->MTL->wb->mni
    
    # 2020-08-26 previous version input tal_struct (pairs.json as a recArray). Now input pairs.json and localizations.json like this:
    # pairs = reader.load('pairs')
    # localizations = reader.load('localization')
    
    regs = []    
    atlas_type = []
    pair_number = []
    has_stein_das = 0
    
    # if localization.json exists get the names from each atlas
    if len(localizations) > 1: 
        # pairs that were recorded and possible pairs from the localization are typically not the same.
        # so need to translate the localization region names to the pairs...which I think is easiest to just do here

        # get an index for every pair in pairs
        loc_translation = Loc2PairsTranslation(pairs,localizations)
        loc_dk_names = ['' for _ in range(len(pairs))]
        loc_MTL_names = copy(loc_dk_names) 
        loc_wb_names = copy(loc_dk_names)
        for i,loc in enumerate(loc_translation):
            if loc != ' ': # set it to this when there was no localization.pairs
                if 'atlases.mtl' in localizations: # a few (like 5) of the localization.pairs don't have the MTL atlas
                    loc_MTL_names[loc] = localizations['atlases.mtl']['pairs'][i] # MTL field from pairs in localization.json
                    has_MTL = 1
                else:
                    has_MTL = 0 # so can skip in below
                loc_dk_names[loc] = localizations['atlases.dk']['pairs'][i]
                loc_wb_names[loc] = localizations['atlases.whole_brain']['pairs'][i]   
    for pair_ct in range(len(pairs)):
        try:
            pair_number.append(pair_ct) # just to keep track of what pair this was in subject
            pair_atlases = pairs.iloc[pair_ct] #tal_struct[pair_ct].atlases
            if 'stein.region' in pair_atlases: # if 'stein' in pair_atlases.dtype.names:
                test_region = str(pair_atlases['stein.region'])
                if (test_region is not None) and (len(test_region)>1) and \
                   (test_region not in 'None') and (test_region != 'nan'):
                    regs.append(test_region.lower())
#             if 'stein' in pair_atlases.dtype.names:  ### OLD WAY FROM TAL_STRUCT...leaving as example
#                 if (pair_atlases['stein']['region'] is not None) and (len(pair_atlases['stein']['region'])>1) and \
#                    (pair_atlases['stein']['region'] not in 'None') and (pair_atlases['stein']['region'] != 'nan'):
#                     regs.append(pair_atlases['stein']['region'].lower())
                    atlas_type.append('stein')
                    has_stein_das = 1 # temporary thing just to see where stein/das stopped annotating
                    continue # back to top of for loop
                else:
                    pass # keep going in loop
            if 'das.region' in pair_atlases:
                test_region = str(pair_atlases['das.region'])
                if (test_region is not None) and (len(test_region)>1) and \
                   (test_region not in 'None') and (test_region != 'nan'):
                    regs.append(test_region.lower())
                    atlas_type.append('das')
                    has_stein_das = 1
                    continue
                else:
                    pass
            if len(localizations) > 1 and has_MTL==1:             # 'MTL' from localization.json
                if loc_MTL_names[pair_ct] != '' and loc_MTL_names[pair_ct] != ' ':
                    if str(loc_MTL_names[pair_ct]) != 'nan': # looking for "MTL" field in localizations.json
                        regs.append(loc_MTL_names[pair_ct].lower())
                        atlas_type.append('MTL_localization')
                        continue
                    else:
                        pass
                else:
                    pass
            if len(localizations) > 1:             # 'whole_brain' from localization.json
                if loc_wb_names[pair_ct] != '' and loc_wb_names[pair_ct] != ' ':
                    if str(loc_wb_names[pair_ct]) != 'nan': # looking for "MTL" field in localizations.json
                        regs.append(loc_wb_names[pair_ct].lower())
                        atlas_type.append('wb_localization')
                        continue
                    else:
                        pass
                else:
                    pass
            if 'wb.region' in pair_atlases:
                test_region = str(pair_atlases['wb.region'])
                if (test_region is not None) and (len(test_region)>1) and \
                   (test_region not in 'None') and (test_region != 'nan'):
                    regs.append(test_region.lower())
                    atlas_type.append('wb')
                    continue
                else:
                    pass
            if len(localizations) > 1:             # 'dk' from localization.json
                if loc_dk_names[pair_ct] != '' and loc_dk_names[pair_ct] != ' ':
                    if str(loc_dk_names[pair_ct]) != 'nan': # looking for "dk" field in localizations.json
                        regs.append(loc_dk_names[pair_ct].lower())
                        atlas_type.append('dk_localization')
                        continue
                    else:
                        pass
                else:
                    pass
            if 'dk.region' in pair_atlases:
                test_region = str(pair_atlases['dk.region'])
                if (test_region is not None) and (len(test_region)>1) and \
                   (test_region not in 'None') and (test_region != 'nan'):
                    regs.append(test_region.lower())
                    atlas_type.append('dk')
                    continue
                else:
                    pass
            if 'ind.corrected.region' in pair_atlases: # I don't think this ever has a region label but just in case
                test_region = str(pair_atlases['ind.corrected.region'])
                if (test_region is not None) and (len(test_region)>1) and \
                   (test_region not in 'None') and (test_region not in 'nan'):
                    regs.append(test_region.lower())
                    atlas_type.append('ind.corrected')
                    continue
                else:
                    pass  
            if 'ind.region' in pair_atlases:
                test_region = str(pair_atlases['ind.region'])
                if (test_region is not None) and (len(test_region)>1) and \
                   (test_region not in 'None') and (test_region != 'nan'):
                    regs.append(test_region.lower())
                    atlas_type.append('ind')
                    # [tal_struct[i].atlases.ind.region for i in range(len(tal_struct))] # if you want to see ind atlases for comparison to above
                    # have to run this first though to work in ipdb: globals().update(locals())                  
                    continue
                else:
                    regs.append('No atlas')
                    atlas_type.append('No atlas')
            else: 
                regs.append('No atlas')
                atlas_type.append('No atlas')
        except AttributeError:
            regs.append('error')
            atlas_type.append('error')
    return numpy.array(regs),numpy.array(atlas_type),numpy.array(pair_number),has_stein_das

def brain_label():
    from getMTLregions import getMTLregions
    MTL_stein = ['left ca1','left ca2','left ca3','left dg','left sub','left prc','left ec','left phc','left mtl wm',
             'right ca1','right ca2','right ca3','right dg','right sub','right prc','right ec','right phc','right mtl wm',
             'left amy','right amy'] # including amygdala in MTL
    MTL_ind = ['parahippocampal','entorhinal','temporalpole',   
               ' left amygdala',' left ent entorhinal area',' left hippocampus',' left phg parahippocampal gyrus',' left tmp temporal pole', # whole-brain names
               ' right amygdala',' right ent entorhinal area',' right hippocampus',' right phg parahippocampal gyrus',' right tmp temporal pole',
               'left amygdala','left ent entorhinal area','left hippocampus','left phg parahippocampal gyrus','left tmp temporal pole',
               'right amygdala','right ent entorhinal area','right hippocampus','right phg parahippocampal gyrus','right tmp temporal pole',
               '"ba35"','"ba36"','"ca1"', '"dg"', '"erc"', '"phc"', '"sub"',
               'ba35', 'ba36','ca1','dg','erc','phc','sub']
    MTL_labels = MTL_stein+MTL_ind

    HPC_labels,ENT_labels,PHC_labels =getMTLregions(MTL_labels)
    PHG_labels=ENT_labels+PHC_labels+['prc', 'ba35', 'ba36','left prc','right prc']
    return HPC_labels,PHG_labels


def categorized_words(evs,list_n):
    '''create a df with the encoded semantic categories (3 categories in catFR) and their related words (four words per category) for each list'''
    import pandas as pd
    assert list_n>=0, 'list number is negative'
    category_words=pd.DataFrame([])
    encoding_evs=evs[evs['type']=='WORD']
    list_evs=encoding_evs[encoding_evs['list']==list_n]
    if len(list_evs)==0: # if no events exist
        category_words=category_words.append({'category':[],'words':[]},ignore_index=True)
    else:
        #    A specific problem with sub R1488T that has 22 encoded words
        if list_evs['eegfile'].iloc[0][0:6]=='R1488T' and list_evs['list'].unique()[0]==11 and list_evs['session'].unique()[0]==0:
            list_evs=list_evs.iloc[10:]
        if len(list_evs)>0:
            if len(list_evs)==12:
    #           print('wrong number of words in list:', list_n,'subject:', evs['eegfile'][0][0:6]) # words number
                categories=list_evs['category'].unique()
                if len(categories)!=3:
                    print('wrong number of words in list:', list_n,'subject:', evs['eegfile'][0][0:6])# categories number
                for category in categories:
                    category_evs=list_evs[list_evs['category']==category]
                    assert len(category_evs['item_name'].tolist())==4 # 4 words per category
                    category_words=category_words.append({'category':category,'words':category_evs['item_name'].tolist()},ignore_index=True)
    return category_words

import gensim.models as models
word2vec = models.KeyedVectors.load_word2vec_format(
    '/home1/noaherz/Long2017/code_sharing/GoogleNews-vectors-negative300.bin.gz', binary=True)

def case_insensitive_similarity(word1,word2):
    ''' enable word2vec to compute similarity between words regardless of them being upper/lower case. If more than one format of the word exist, it computes the average over all words formats'''
    import numpy
    this_word=[]
    try:
        this_word.append(word2vec.similarity(word1.lower(),word2.lower()))
    except:
        pass
    try:
        this_word.append(word2vec.similarity(word1.lower(),word2.upper()))
    except:
        pass
    try:
        this_word.append(word2vec.similarity(word1.upper(),word2.lower()))
    except:
        pass
    try:
        this_word.append(word2vec.similarity(word1.upper(),word2.upper()))
    except:
        pass
    
    return numpy.mean(this_word)

def add_semantic_similarity(evs):
    ''' Use word2vec to extract semantic similarity between each recalled word and the encoded words of that list.
    The input is the event structure, as produced by reader.load('task_events').
    The output is the same event structure with a new column, indicating the mean semantic similarity of each word with all words encoded in that list.'''
    import numpy
    mean_semantic_similarity=numpy.zeros(len(evs))*numpy.nan
    for session in evs['session'].unique():
        session_evs=evs[evs['session']==session]
        for list_n in session_evs['list'].unique()[session_evs['list'].unique()>=0]:
            list_evs=session_evs[session_evs['list']==list_n]
            rec_evs=list_evs[list_evs['type']=='REC_WORD']
            rec_evs_index=rec_evs.index
            for row in rec_evs_index:
                word=rec_evs['item_name'].loc[row]
                word=word.lower()
                # compute similarity vector
                category_words = categorized_words(evs,list_n) 
                word_list=category_words['words'][0]+category_words['words'][1]+category_words['words'][2]
                lowerC_word_list=[word_fromlist.lower() for word_fromlist in word_list]
                this_word = []
                for j in lowerC_word_list:
                    try:
                        this_word.append(case_insensitive_similarity(word,j))
                    except:   
                        print('word ',j,'or ', word,'not in vocabulary')
                        print('session ',session,'list ', list_n,' row ',row)
                        continue
                if len(this_word)>=10: #if more than two words are missing in vocabolary do not compute mean similarity
                    this_word_array=numpy.array(this_word)
                    mean_sim=numpy.mean(this_word_array[this_word_array!=1])
                    mean_semantic_similarity[row]=mean_sim
    evs['semantic_similarity']=mean_semantic_similarity
    return evs


