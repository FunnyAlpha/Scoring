import re
import pandas as pd
from io import StringIO
from datetime import datetime


def parse_line(p_type,str_list,index_arr):
    
    global match_counter
    global df_output_list
    global df_output_dict
    global ArrInd
    global cb_path

    if p_type == 'cb':
        cb_path = re.compile('credit.creditBureau.creditData.')
    else:
        cb_path = re.compile('credit.creditBureau.creditData.')

    match = re.search(cb_path, str_list[1])
    if match:
        #print('Found "{}" in "{}"'.format('creditBureau',result[1]))
        #print(row.as_full_path.split('.')[3])
        if match_counter == 1:
            ArrInd = 0
        match_counter+=1
        #print(match_counter)
        if ArrInd == int(index_arr[0]):
            if str_list[1].split('.')[3].upper() == 'CREDITTYPE':
                df_output_list[str_list[1].split('.')[3].upper()] = int(str_list[2])
            elif str_list[1].split('.')[3].upper() == 'CREDITJOINT':
                df_output_list[str_list[1].split('.')[3].upper()] = int(str_list[2])
            elif str_list[1].split('.')[3].upper() == 'CREDITDATE':
                df_output_list[str_list[1].split('.')[3].upper()] = datetime.strptime(str_list[2], '%d.%m.%Y %H:%M:%S') 
            else:
                df_output_list[str_list[1].split('.')[3].upper()] = str(str_list[2])    
            ArrInd = int(index_arr[0])
        else:
            df_output_dict.append(df_output_list)
            df_output_list  = {}
            df_output_list[str_list[1].split('.')[3].upper()] = str_list[2]
            ArrInd = int(index_arr[0])

def get_df(p_type):
    
    global match_counter
    global df_output_list
    global df_output_dict
    global ArrInd
    global cb_path

    df_output_list  = {}
    df_output_dict  = []
    match_counter = 1
    ArrInd = 1

    with open('sample_vector_cb.txt',encoding='utf-8') as file:
        line = file.readline()

        while line:
            #result = re.split(r'\|',re.sub(r'\n','',line))
            result = re.split(r'\|',line.rstrip())
            result2 = re.findall(r'.(?<=\[)(\d+)(?=\])',result[1])
            parse_line(p_type,result,result2)

            if result[1] == 'idCredit':
                sk_application = result[2]

            line = file.readline()
        df_output_dict.append(df_output_list)
    df_output = pd.DataFrame(df_output_dict)
    df_output['SK_APPLICATION'] = sk_application

    return df_output

#df_output = get_df('cb')
#print(df_output)

'''
df_output_list  = {}
df_output_dict  = []
match_counter = 1

with open('sample_vector_cb.txt',encoding='utf-8') as file:
    line = file.readline()
    while line:
        #result = re.split(r'\|',re.sub(r'\n','',line))
        result = re.split(r'\|',line.rstrip())
        result2 = re.findall(r'.(?<=\[)(\d+)(?=\])',result[1])

        #print(result2)

        cb_path = re.compile('credit.creditBureau.creditData.')
        match = re.search(cb_path, result[1])
        if match:
            #print('Found "{}" in "{}"'.format('creditBureau',result[1]))
        #print(row.as_full_path.split('.')[3])
            if match_counter == 1:
                ArrInd = 0
            match_counter+=1
            #print(df_output_list)
            if ArrInd == int(result2[0]):
                df_output_list[result[1].split('.')[3]] = result[2]
                ArrInd = int(result2[0])

            else:
                df_output_dict.append(df_output_list)
                df_output_list  = {}
                df_output_list[result[1].split('.')[3]] = result[2]
                ArrInd = int(result2[0])
                #print(ArrInd)
        #df_output_list[row.as_full_path] = row.value
        #pass
        #print(result)
        line = file.readline()

#print(df_output_dict)
df_output = pd.DataFrame(df_output_dict)
print(df_output)
'''