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