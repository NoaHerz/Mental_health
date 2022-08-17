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
    '/home1/noaherz/word2vec/GoogleNews-vectors-negative300.bin.gz', binary=True)

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
#                         this_word.append(word2vec.similarity(word, j))
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


