from Application import *
from Predictors import *
import numpy as np
from tabulate import tabulate

if __name__ == "__main__":

    vector_dwh = BuilderVectorDWH()
    vector_dwh.getCreditBureauData()
    df_input = vector_dwh.product.CreditBureau_df

    #print (df_input)

    #print(df_input['SK_APPLICATION'].dtype)
    #print(list(df_input))
    
   # dd = {'sk_application': [203388465], 'max_date_open_card': [None]}
   # dff = pd.DataFrame(data=dd)
   # print(dff)

    print(
    df_input[
    (df_input['NFLAG_CREDIT_JOINT'] == 1) &
    (df_input['FLAG_CREDIT_OWNER'] == '0') &
    (df_input['CREDIT_TYPE'].apply(lambda x:1 if x in {4,14,24} else 0)) == 1
    ].groupby(['SK_APPLICATION']).agg({'DTIME_CREDIT':np.min}).rename(columns={"DTIME_CREDIT": "MIN_DATE_OPEN_CARD"})
    )

    predictors_dwh  = TestScoreCardPredictors(df_input)
    predictors_dwh.get_predictors_rez_df(df_input)

    print(tabulate(predictors_dwh.predictors_out_df, headers='keys',tablefmt='psql',disable_numparse=True))
    #print (predictors_dwh.predictors_out_df)