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
