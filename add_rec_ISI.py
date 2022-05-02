import numpy as np
def add_rec_ISI(evs): 
    '''
    This function adds an 'ISI' column to the events dataframe.
    The input is the event strcture (the result of: evs = reader.load('task_events'))
    The output is the same event structure with an additional column for the ISI of each recalled word (i.e. time between recalled words).'''
    rec_ISI=np.full(len(evs),np.nan)
    rec_words_index=evs[evs['type']=='REC_WORD'].index # recalled words' index
    ISI=np.full(len(evs),np.nan)
    for i in rec_words_index:
        ISI[i]=evs['rectime'].iloc[i]-evs['rectime'].iloc[i-1] # time diff between recalls
    evs['ISI']=ISI # ADD COLUMN    
    return evs