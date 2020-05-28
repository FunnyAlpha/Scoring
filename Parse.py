import re
import pandas as pd
from dateutil.parser import parse


rx_dict = {
    re.compile(r'(.*?)\|credit\.creditBureau\.creditData\[(\d+)\]\.(.*)\|(.*?)\s*$'):'CREDITBUREAU',
    re.compile(r'(.*?)\|sourceData\.behaviourData\.persons\[(\d+)\]\.(.*)\|(.*?)\s*$'):'BEHAVIOURDATA',
    re.compile(r'(.*?)\|applicantData\.previousApplications\.persons\[(\d+)\]\.(.*)\|(.*?)\s*$'):'PREVAPPLICATION',
    re.compile(r'(.*?)\|documents\[(\d+)\]\.(.*)\|(.*?)\s*$'):'DOCUMENTS',
    re.compile(r'(.*?)\|persons\[(\d+)\]\.(\w*)\|(.*?)\s*$'):'PERSONS',
    re.compile(r'(.*?)\|(.\w*)\|(.*?)\s*$'):'APPLICATION',
    re.compile(r'(.*?)\|(idCredit)\|(.*?)\s*$'):'SK_APPLICATION'
}


df_dict  = {
    'CREDITBUREAU':[],
    'BEHAVIOURDATA':[],
    'APPLICATION':[],
    'PREVAPPLICATION':[],
    'DOCUMENTS':[],
    'PERSONS':[],
    'SK_APPLICATION':[]
}



def set_vct_data_type(p_list):

    if len(p_list) == 3:
        p_list.insert(1,0)

    p_list[2] = p_list[2].upper()

    if p_list[0]=='d':
        p_list[3] = parse(p_list[3])
    elif p_list[0]=='n' and p_list[2]=='IDCREDIT':
        p_list[3] = int(p_list[3])
    elif p_list[0]=='n':
        p_list[3] = float(p_list[3])    
    else:
        p_list[3] = str(p_list[3])
    pass    


def parse_vct(p_input,p_dict,p_rx_dict):

    with open(p_input,encoding='utf-8') as file:
        line = file.readline()
        while line:

            for rx,val in p_rx_dict.items():

                if re.search(rx, line):
                    #make list from line
                    temp_list = list(re.findall(rx,line)[0])
                    #set data types
                    set_vct_data_type(temp_list)
                    #append list element to dictionary 
                    p_dict[val].append(temp_list)

            line = file.readline()

    return p_dict

def get_df_txt(p_type,p_dict):

    df = pd.DataFrame(p_dict[p_type])
    #get column name
    column = df[2].unique()
    #unstack and clean dataframe
    df = df.drop(0,1).set_index([1, 2]).unstack().droplevel(0, axis=1).rename_axis(
        index=None, columns=None).reindex(column, axis=1)
    df['SK_APPLICATION'] = p_dict['SK_APPLICATION'][0][3]     
    return df
'''
v_dict = parse_vct('sample_vector_cb.txt',df_dict,rx_dict)
print(v_dict['APPLICATION'])
df = get_df_txt('APPLICATION',v_dict)
print(df['SYSDATE'])
'''