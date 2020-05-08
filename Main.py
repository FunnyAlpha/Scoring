from Application import *
from Predictors import *

if __name__ == "__main__":

    vector_dwh = BuilderVectorDWH()
    vector_dwh.getCreditBureauData()
    df_input = vector_dwh.product.CreditBureau_df

    #print (vector_dwh.product.CreditBureau_df)

    #print(df_input['SK_APPLICATION'].dtype)
    #print(list(df_input))

    '''
    print(     df_input.loc[
        (df_input['SK_APPLICATION'] == 203388465) &
        (df_input['NFLAG_CREDIT_JOINT'] == 1) &
        (df_input['FLAG_CREDIT_OWNER'] == '0')
        #is_card(df['CREDIT_TYPE']) == 1
        ,'DTIME_CREDIT'
        ].max() 
    )
    '''
    
   # dd = {'sk_application': [203388465], 'max_date_open_card': [None]}
   # dff = pd.DataFrame(data=dd)
   # print(dff)

    predictors_dwh  = TestScoreCardPredictors()
    predictors_dwh.get_predictors_rez_df(203388465,df_input)
    print (predictors_dwh.Predictors_df)