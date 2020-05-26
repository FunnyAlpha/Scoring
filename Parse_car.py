import re
import pandas as pd

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