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
