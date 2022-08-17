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