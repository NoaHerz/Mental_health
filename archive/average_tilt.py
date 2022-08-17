# compute means
# column_string: 'HFA_LFA_diff'/'LFA'/'HFA'
# condition: 'all'/'related'/'nonrelated'
# exmaple: average_tilt(long_df,'all','HFA_LFA_diff'):
def average_tilt(long_df,condition,column_string):
    '''
    Compute average for each event type (correcl recall/intrusion/deliberation) as well as the difference between correct recalls and intrusions
    column_string can be: 'HFA_LFA_diff'/'LFA'/'HFA'
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
       