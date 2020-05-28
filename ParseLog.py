from pyparsing import *
import pandas as pd
import re
from tabulate import tabulate


#############
test_list = []

with open('sample_vector_cb.txt',encoding='utf-8') as file:
    line = file.readline()
    while line:
        result = re.split(r'[|]',re.sub(r'\n','',line))
        result1 = ['data_type','as_full_path','value']
        dictObj = dict(zip(result1,result))
        test_list.append(dictObj)
        #print(dictObj)
        line = file.readline()


#print(test_list)      

test_df = pd.DataFrame(test_list)

id_credit = test_df.loc[test_df['as_full_path'].isin(['idCredit']),'value'].values[0]

print(tabulate(test_df, headers='keys',tablefmt='psql',disable_numparse=True))

df_output_list = {'idCredit':id_credit}
df_output_dict = []
# parse

cb_path = 'credit.creditBureau.creditData'
ArrIndPrev = '[0]'

for row in test_df.itertuples():

    regex = re.compile(cb_path)
    match = re.search(regex, row.as_full_path)
    if match:
        #print('Found "{}" in "{}"'.format(cb_path,row.as_full_path))
        #print(row.as_full_path.split('.')[3])
        ArrInd = re.findall(r'.[\d]]',row.as_full_path)[0]
        
        if ArrInd == ArrIndPrev:
            df_output_list[row.as_full_path.split('.')[3]] = row.value
            ArrIndPrev = ArrInd

        else:
            df_output_dict.append(df_output_list)
            df_output_list  = {'idCredit':id_credit}
            df_output_list[row.as_full_path.split('.')[3]] = row.value
            ArrIndPrev = ArrInd
        #df_output_list[row.as_full_path] = row.value
        #pass

    else:
        df_output_list[row.as_full_path] = row.value
    #print (row.as_full_path)

#print(df_output_dict)

#df_output = pd.DataFrame([df_output_list])
df_output = pd.DataFrame(df_output_dict)

print(tabulate(df_output[['idCredit','creditCurrency','creditDate','creditDayOverdue','creditEndDate','creditEndDateFact','creditJoint']], headers='keys',tablefmt='psql',disable_numparse=True))

#print(df_output[['idCredit','creditCurrency','creditDate','creditDayOverdue','creditEndDate','creditEndDateFact','creditJoint']])
#print('id_credit = ',id_credit)

#print(df_output)




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



import re
import pandas as pd
from dateutil.parser import parse

'''
df_output_list  = {}
df_output_dict  = []
match_counter = 1


with open('sample_car.txt',encoding='utf-8') as file:
    line = file.readline()
    while line:

        result = re.split(r'\|',line.rstrip())
        result2 = re.findall(r'.(?<=\[)(\d+)(?=\])',result[1])

        regex = re.compile('vechicle.car.characteristics.')
        match = re.search(regex, result[1])
        if match:

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

        line = file.readline()
    df_output_dict.append(df_output_list)
#print(df_output_dict)
df_output = pd.DataFrame(df_output_dict)
print(df_output)


'''

'''
df = pd.read_csv('sample_car.txt', sep='|', header=None)

print(df.iloc[:,1])

columns = df.iloc[:,1].str.split('.').str[-1].unique()

df_out = pd.DataFrame(df.iloc[:,-1].to_numpy().reshape(-1,len(columns)), columns=columns)

print(df_out)

'''
'''

import pandas as pd
from io import StringIO

res = (pd.read_csv('sample_car.txt', sep="|", header = None)
       #extract the numbers from col 1
       .assign(number = lambda x: x[1].str.extract(r"(\d+)"),
               #get the tail of the string in column 1
               headers = lambda x: x[1].str.split(r"\[\d+\]\.").str[-1],
               datatype = lambda x: x[0].values
              )
        #set numbers and headers as index 
        #and keep only the last column, which is relevant
       .set_index(['number','headers','datatype'])
       #.filter([2])
        #unstacking here ensures the headers
       # are directly on top of each related data in column 2
       #.unstack()
        #some cleanups
       #.droplevel(0,axis=1)
       #.rename_axis(None,axis=1)
       #.rename_axis(None)
      )

#print(res)      


rx = re.compile(r'(.*?)\|vechicle\.car\.characteristics\[(\d+)\]\.(.*)\|(.*?)\s*$')

df = pd.DataFrame([rx.match(line).groups() for line in open('sample_car.txt',encoding='utf-8')])

#df=df.drop(0,1)
#print(df)

column = df[2].unique()     # store the column names in file order

#df = df.set_index([1, 2])

#print(df)

df = df.drop(0,1).set_index([1, 2]).unstack().droplevel(0, axis=1).rename_axis(
    index=None, columns=None).reindex(column, axis=1)

#print(df)


some_list = ['1',2,'ssss']

ls = [type(item) for item in some_list]
print(ls)


'''

def set_vct_data_type(p_list):

    p_list[2] = p_list[2].upper()

    if p_list[0]=='d':
        p_list[3] = parse(p_list[3])
    elif p_list[0]=='n':
        p_list[3] = float(p_list[3])
    else:
        p_list[3] = str(p_list[3])
    pass    


rx_dict = {
    re.compile(r'(.*?)\|credit\.creditBureau\.creditData\[(\d+)\]\.(.*)\|(.*?)\s*$'):'CREDITBUREAU',
    re.compile(r'(.*?)\|documents\[(\d+)\]\.(.*)\|(.*?)\s*$'):'DOCUMENTS',
    re.compile(r'(.*?)\|persons\[(\d+)\]\.(\w*)\|(.*?)\s*$'):'APPLICATION'
}


df_output_dict  = {
    'CREDITBUREAU':[],
    'APPLICATION':[],
    'DOCUMENTS':[]
}

with open('sample_vector_cb.txt',encoding='utf-8') as file:
    line = file.readline()
    while line:

        #rx = re.compile(r'(.*?)\|credit\.creditBureau\.creditData\[(\d+)\]\.(.*)\|(.*?)\s*$')
        #rx = re.compile(r'(.*?)\|documents\[(\d+)\]\.(.*)\|(.*?)\s*$')

        for rx,val in rx_dict.items():

            match = re.search(rx, line)
            if match:
                temp_list = list(re.findall(rx,line)[0])
                #print(temp_list)
                set_vct_data_type(temp_list)
                '''
                if temp_list[0]=='d':
                    print(temp_list[3])
                    temp_list[3] = parse(temp_list[3])
                elif temp_list[0]=='n':
                    temp_list[3] = float(temp_list[3])
                else:
                    temp_list[3] = str(temp_list[3])    
                '''    
                #print(type(df_output_dict['cb']))
                df_output_dict[val].append(temp_list)
                #print(type(df_output_dict['cb']))

                #ls = [type(item) for item in temp_list]
                #print(ls)

        line = file.readline()

print(df_output_dict['APPLICATION'])


get
df = pd.DataFrame(df_output_dict['APPLICATION'])
#print(df)
column = df[2].unique()
df = df.drop(0,1).set_index([1, 2]).unstack().droplevel(0, axis=1).rename_axis(
    index=None, columns=None).reindex(column, axis=1)

print(df)
#print(df['published'])
