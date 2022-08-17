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