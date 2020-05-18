
from enum import Enum, auto
import cx_Oracle
import pandas as pd
from Config import *

#conn = cx_Oracle.connect('gp_blaze_uwi/Fender1580@db19c')
v_sql_query = str(f_scoring_vector_tt_beh())
v_con_name = str(Auhorization())

conn = cx_Oracle.connect(v_con_name)

#mycursor = myconnection.cursor()

#mycursor.execute('select * from MSolovev.Python_Test')

#result = mycursor.fetchall()

#print(v_con_name)
#print(v_sql_query)

df1 = pd.read_sql_query(v_sql_query,conn)
#df2 = pd.read_sql_query(v_sql_query,conn)

#for  (sk_application) in result:
#       print (sk_application)


conn.close()

#SUM_AMT_CREDIT_SUM=0

print('df1')
print(df1)

#for index, row in df.iterrows(): 
   # print(row['DATE_EFFECTIVE'], row['AMT_ANNUITY'])
   # if row['CREDIT_ACTIVE'] == 1 and row['CREDIT_TYPE_UNI']==5:
   #     SUM_AMT_CREDIT_SUM += row['AMT_CREDIT_SUM_DEBT']

#print(SUM_AMT_CREDIT_SUM)

'''
class Bureau(Enum):
    SK_APPLICATION = auto()
    SK_DATE_DECISION = auto()
    SK_CONTRACT_TYPE = auto()


print(SK_CONTRACT_TYPE) # SK_CONTRACT_TYPE
'''

'''
from enum import Enum, auto
import cx_Oracle

myconnection = cx_Oracle.connect('MSolovev/Fender1580@db19c')


mycursor = myconnection.cursor()

mycursor.execute('select sk_application from MSolovev.Sm_Tmp_Bureau_Raw_Test_Table')

result = mycursor.fetchall()


for  (sk_application) in result:
        print (sk_application)


myconnection.close()
'''