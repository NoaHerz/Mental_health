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
categorized_ELIs_list = pd.read_excel('/home1/noaherz/word2vec/ELI_words_catFR_comparison_final.xlsx',engine="openpyxl")

def add_semantic_relatedness(evs):
    '''Add sematic relatedness column (1= intrusion belong to the same semantic category as the ones in encoding, 0 = intrusion does not belong to any semantic category in the encoded list).
    The input is the event structure, as produced by reader.load('task_events').
    The output is the same event structure with a new sematic relatedness column'''
    import numpy as np
    if any(evs.columns=='item_name'): # in the pyFR and FR/catFR this column has a different name 
            item='item_name'
    elif any(evs.columns=='item'):
            item='item'
 
    semantic_relatedness=np.zeros(len(evs))*np.nan
    for session in evs['session'].unique():
        session_evs=evs[evs['session']==session]
        for list_n in session_evs['list'].unique()[session_evs['list'].unique()>=0]:
            list_evs=session_evs[session_evs['list']==list_n]
            rec_evs=list_evs[list_evs['type']=='REC_WORD']
            rec_evs_index=rec_evs.index
#             print(list_n)
            # check what were the three list semantic categories:
            encoded_categories = categorized_words(evs,list_n)
#             print(list_n)
#             print(encoded_categories)
            if len(encoded_categories)>1:
                encoded_categories = list(encoded_categories['category'])

                for row in rec_evs_index:
                    if rec_evs['intrusion'].loc[row]==0: # correct recalls
                        semantic_category=rec_evs['category'].loc[row]
                        semantic_relatedness_bool=semantic_category in encoded_categories
                        semantic_relatedness[row]=semantic_relatedness_bool
                    elif rec_evs['intrusion'].loc[row]>0: # PLIs
                        intruded_list=rec_evs['intrusion'].loc[row]
        #                 list(categorized_words(evs,list_n-intruded_list)['category'])
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
