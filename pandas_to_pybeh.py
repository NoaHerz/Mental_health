import pandas as pd
import numpy as np
import scipy as sp
from pybeh.make_recalls_matrix import make_recalls_matrix
from pybeh.crp import crp
from pybeh.sem_crp import sem_crp
from pybeh.temp_fact import temp_fact
from pybeh.dist_fact import dist_fact

def get_itemno_matrices(evs, itemno_column='itemno', list_index=['subject', 'session', 'list']):
    """Expects as input a dataframe (df) for one subject"""
    evs.loc[:, itemno_column] = evs.loc[:, itemno_column].astype(int)
    evs['pos'] = evs.groupby(list_index).cumcount()
    itemnos_df = pd.pivot_table(evs, values=itemno_column, 
                                 index=list_index, 
                                 columns='pos', fill_value=0)
    itemnos = itemnos_df.values
    return itemnos

def pd_crp(df, lag_num=5, itemno_column='itemno', list_index=['subject', 'session', 'list']):
    """Expects as input a dataframe (df) for one subject"""
    pres_itemnos = get_itemno_matrices(df.query('type == "WORD"'), 
                                       itemno_column=itemno_column, 
                                       list_index=list_index)
    rec_itemnos = get_itemno_matrices(df.query('type == "REC_WORD"'), 
                                       itemno_column=itemno_column, 
                                       list_index=list_index)
    recalls = make_recalls_matrix(pres_itemnos, rec_itemnos)

    prob = crp(recalls=recalls,
                  subjects=['_'] * recalls.shape[0],
                  listLength=pres_itemnos.shape[1],
                  lag_num=lag_num)
    crp_dict = {'prob': prob[0], 
                'lag': np.arange(-lag_num, (lag_num+1))}
    return pd.DataFrame(crp_dict)

def get_sim_mat(df, itemno_column, sim_columns, method=sp.spatial.distance.euclidean):
    sem_sim_df = df.pivot_table(values='pref_rating', columns='item_num', 
                                              index='subject')
    # https://stackoverflow.com/questions/29723560/distance-matrix-for-rows-in-pandas-dataframe
    sem_sims = sem_sim_df.apply(lambda col1: sem_sim_df.apply(
        lambda col2: method(col1, col2))).values
    return sem_sims

def pd_sem_crp(df, itemno_column='itemno', 
                list_index=['subject', 'session', 'list'], sim_columns=None,
                sem_sims=None, method=sp.spatial.distance.euclidean, n_bins=10):
    """Expects as input a dataframe (df) for one subject"""
    pres_itemnos = get_itemno_matrices(df.query('type == "WORD"'), 
                                       itemno_column=itemno_column, 
                                       list_index=list_index)
    rec_itemnos = get_itemno_matrices(df.query('type == "REC_WORD"'), 
                                       itemno_column=itemno_column, 
                                       list_index=list_index)
    recalls = make_recalls_matrix(pres_itemnos, rec_itemnos)
    if sem_sims is None:
        sem_sims = get_sim_mat(df.query('type == "WORD_VALS"'), itemno_column, 
                               sim_columns, method=method)
    
    bin_means, crp = sem_crp(recalls=recalls, 
                   recalls_itemnos=rec_itemnos, 
                   pres_itemnos=pres_itemnos, 
                   subjects=['_'] * recalls.shape[0], 
                   sem_sims=sem_sims, 
                   n_bins=n_bins, 
                   listLength=pres_itemnos.shape[1])
    crp_dict = {'prob': crp[0], 
                'sem_bin_mean': bin_means[0],
                'sem_bin': np.arange(n_bins)
               }
    return pd.DataFrame(crp_dict).query('prob == prob') #remove bins with no data

def pd_temp_fact(df, skip_first_n=0, itemno_column='itemno', list_index=['subject', 'session', 'list']):
    """Expects as input a dataframe (df) for one subject"""
    pres_itemnos = get_itemno_matrices(df.query('type == "WORD"'), 
                                       itemno_column=itemno_column, 
                                       list_index=list_index)
    rec_itemnos = get_itemno_matrices(df.query('type == "REC_WORD"'), 
                                       itemno_column=itemno_column, 
                                       list_index=list_index)
    recalls = make_recalls_matrix(pres_itemnos, rec_itemnos)

    temp_fact_arr = temp_fact(recalls=recalls, 
                  subjects=['_']*recalls.shape[0],
                  listLength=pres_itemnos.shape[1],
                  skip_first_n=skip_first_n)
    
    return temp_fact_arr[0]

def pd_dist_fact(df, rec_itemnos=None, itemno_column='itemno', 
                 list_index=['subject', 'session', 'list'], 
                 dist_mat=None, is_similarity=False, 
                 dist_columns=None,
                 skip_first_n=0,
                 method=sp.spatial.distance.euclidean
                ):
    pres_itemnos = get_itemno_matrices(df.query('type == "WORD"'), 
                                       itemno_column=itemno_column, 
                                       list_index=list_index)
    rec_itemnos = get_itemno_matrices(df.query('type == "REC_WORD"'), 
                                       itemno_column=itemno_column, 
                                       list_index=list_index)
    recalls = make_recalls_matrix(pres_itemnos, rec_itemnos)
    
    if dist_mat is None:
        dist_mat = get_sim_mat(df.query('type == "WORD_VALS"'), itemno_column, 
                               dist_columns, method=method)
    
    dist_fact_arr = dist_fact(rec_itemnos=rec_itemnos, 
              pres_itemnos=pres_itemnos, 
              subjects=['_'] * recalls.shape[0],
              dist_mat=dist_mat, is_similarity=is_similarity, 
              skip_first_n=skip_first_n)
    return dist_fact_arr[0]