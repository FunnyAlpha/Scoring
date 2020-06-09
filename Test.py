from dateutil import parser
import re
import pandas as pd
#from Parse import *

v_time =parser.parse('03.10.2012 00:00:00', dayfirst=True)
#print(v_time.month)

#print(v_time)

# data=c|ApprovalCharacteristics[48].variation|1
# n|ApprovalCharacteristics[49].integerValue|0

# regex = re.compile(r'(.*?)\|ApprovalCharacteristics\[(\d+)\]\.(.*)\|(.*?)\s*$')

# for line in data.split('\n'):    

#     print(re.findall(regex,line)[0])



# v_dict = parse_vct_str(test_str,df_dict,rx_dict)
# print(v_dict['APPROVALCHARACTERISTIC'])
# df = get_df_txt('APPROVALCHARACTERISTIC',v_dict)


d = {'option1': ['1', '0', '1', '1'], 'option2': ['0', '0', '1', '0'], 'option3': ['1', '1', '0', '0']}
df = pd.DataFrame(d)
print(df)

for index,row in df.iterrows():
    #print (row['option1'])
    if index == 1:
        df1 = {'1':[df.loc[index,'option1']],'2':[df.loc[index,'option2']]}
        print (row['option1'])

print(pd.DataFrame(df1))