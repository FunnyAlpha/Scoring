import pandas as pd

class Predictors:
    #construct object with null df
    #def __init__(self)->None:
    #    self.Predictors_df = None

    def is_card(self,credit_type):
        return 1 if credit_type in {4,14,24}  else 0
    
    
    def max_date_open_card(self,p_sk_application,df):
        return
        df.loc[
        (df['SK_APPLICATION'] == p_sk_application) &
        (df['NFLAG_CREDIT_JOINT'] == 1) &
        (df['FLAG_CREDIT_OWNER'] == '0') &
        is_card(df['CREDIT_TYPE']) == 1
        ,'DTIME_CREDIT'
        ].max() 


class TestScoreCardPredictors(Predictors):

    def __init__(self)->None:
        self.Predictors_df = None

    def get_predictors_rez_df(self,p_sk_application,df)->None:

        print(p_sk_application)
        print(df)

        v_max_date_open_card = Predictors.max_date_open_card(self,p_sk_application,df)

        print(v_max_date_open_card)

        d = {
        'sk_application':[p_sk_application],
        'max_date_open_card':[v_max_date_open_card]
        }

        #print(d)

        df = pd.DataFrame(data=d)

        #print(df)

        self.Predictors_df = df