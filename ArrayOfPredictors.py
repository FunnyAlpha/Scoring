class PredictorsTest():
    def __init__(self,key,value,typeVal):
        self.key = key
        self.value = value
        self.typeVal = typeVal

PredictorsTestObj1 = PredictorsTest('CB_MAXAGRMNTHS_1_3','1','n')
PredictorsTestObj2 = PredictorsTest('CB_MAXAGRMNTHS_2_3','2','n')
PredictorsTestObj3 = PredictorsTest('CB_MAXAGRMNTHS_3_3','3','n')
PredictorsTestObj4 = PredictorsTest('SEX','m','c')


arrayOfPredictors = []
arrayOfPredictors.append(PredictorsTestObj1)
arrayOfPredictors.append(PredictorsTestObj2)
arrayOfPredictors.append(PredictorsTestObj3)
arrayOfPredictors.append(PredictorsTestObj4)

def getPredictorArray():
    return arrayOfPredictors

# print(getPredictorArray())    

import pandas as pd
import re

class Reading:

   def __init__(self, h, p):
       self.HourOfDay = h 
       self.Percentage = p 

df = pd.DataFrame({
     'SK_APPLICATION': [12345678],
     'MAXAGRMNTHS1_3': [1],
     'MAXAGRMNTHS2_3': [2],
     'MAXAGRMNTHS3_3': [3],
     'EDUCATION': ['2']
})

# print(df)
# print(df.dtypes)

# listOfReading= [(PredictorsTest(row.HourOfDay,row.Percentage)) for index, row in df.iterrows() ]

# print(listOfReading[0].HourOfDay)

class PredictorBlaze():
    def __init__(self,key,value,typeVal):
        self.key = key
        self.value = value
        self.typeVal = typeVal


def get_datatype_df_blaze(p_datatype):
    if p_datatype == 'object':
        return 'n'
    elif 'datetime' in p_datatype.lower():
        return 'd'
    else:
        return 'n'

def parse_df_objArr(p_df):

    arrayOfPredictors = []

    for column in p_df:
        arrayOfPredictors.append(
            PredictorBlaze(
                str(column),
                str(p_df[column].values[0]),
                get_datatype_df_blaze(str(p_df[column].dtypes))
            )
        )
    return arrayOfPredictors

import json  

def parse_df_json(p_df):

    listOfPredictors = []

    for column in p_df:
            listOfPredictors.append(
            
                {
                "key":str(column),
                "value":str(p_df[column].values[0]),
                "typeVal":get_datatype_df_blaze(str(p_df[column].dtypes))
                }
            
        )
    return json.dumps({"blazeResponseList":listOfPredictors})

print(parse_df_json(df))

# import json

# Predictorlist = [
#         {
#         "key":"MAXAGRMNTHS1_3",
#         "value":"1",
#         "typeVal":"n"
#         },
#         {
#         "key":"MAXAGRMNTHS1_3",
#         "value":"1",
#         "typeVal":"n"
#         }
#     ]

# data = json.dumps({"blazeResponseList":Predictorlist})

# print(data)