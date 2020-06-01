import pandas as pd
import numpy as np
from functools import reduce

class Predictors:
    #construct object with null df
    def __init__(self):
        pass

    def add_unknown_columns(self,df,features_list):
        
        for el in features_list:
            if el not in df:
                df[el] = np.nan
        pass

    def is_card(self,credit_type):
        return 1 if credit_type == 4  else 0

    def age_years_real(self,p_app_df):

        v_df= p_app_df[['SK_APPLICATION']].assign(AGE_YEARS_REAL=(p_app_df['SYSDATE'] - p_app_df['BIRTH'])/np.timedelta64(1,'Y'))

        return v_df

    def education(self,p_app_df,p_beh_df):

        self.add_unknown_columns(p_app_df,['EDUCATION'])
        self.add_unknown_columns(p_beh_df,['EDUCATION'])

        df = reduce(
        lambda  left,right: pd.merge(left,right,how='outer',on=['SK_APPLICATION']),
        [p_app_df,p_beh_df.rename(columns={"EDUCATION": "BEHEDUCATION"})]
        )
        v_df= p_app_df[['SK_APPLICATION']].assign(EDUCATION=(df['EDUCATION'].fillna(df['BEHEDUCATION'])))

        #print(v_df)

        return v_df
    
    def max_date_open_card(self,df):

        #print(df['CREDIT_TYPE'].dtype)
        #print(df['CREDIT_TYPE'].apply(lambda x:1 if x in {4,14,24} else 0))

        v_df=df[
        (df['CREDITJOINT'] == 1) &
        (df['CREDITOWNER'] == '0') &
        (df['CREDITTYPE'].apply(lambda x:1 if x in {4,14,24} else 0)) == 1
        ].groupby(['SK_APPLICATION']).agg({'CREDITDATE':np.max}).rename(columns={"CREDITDATE": "MAX_DATE_OPEN_CARD"})
    
       # df.rename(columns={"B": "c"})

        return v_df
    
    def min_date_open_card(self,df):

        #print(df['CREDIT_TYPE'].dtype)
        #print(df['CREDIT_TYPE'].apply(lambda x:1 if x in {4,14,24} else 0))

        v_df = df[
        (df['CREDITJOINT'] == 1) &
        (df['CREDITOWNER'] == '0') &
        (df['CREDITTYPE'].apply(lambda x:1 if x in {4,14,24} else 0)) == 1
        ].groupby(['SK_APPLICATION']).agg({'CREDITDATE':np.min}).rename(columns={"CREDITDATE": "MIN_DATE_OPEN_CARD"})
  

        return v_df

    def all_cash_pos(self,df):

        v_df = df[
        (df['CREDITJOINT'] == 1) &
        (df['CREDITOWNER'] == '0') &
        (df['CREDITTYPE'].apply(lambda x:1 if x in {5,8,13} else 0)) == 1
        ].groupby(['SK_APPLICATION']).agg({'SK_APPLICATION':np.count_nonzero}).rename(columns={"SK_APPLICATION": "ALL_CASH_POS"})

        return v_df

    def cnt_closed_cash_pos(self,df_test,df):

        #print(df_test)

        dfs = [df,df_test]
        df = reduce(lambda  left,right: pd.merge(left,right,how='outer',on=['SK_APPLICATION']), dfs)

        v_df = df[
        (df['CREDITJOINT'] == 1) &
        (df['CREDITOWNER'] == '0') &
        (df['CREDITTYPE'].apply(lambda x:1 if x in {4,14,24} else 0)) == 1
        #(df['SK_DATE_DECISION']==df['SK_DATE_DECISION'])
        ].groupby(['SK_APPLICATION']).agg({'SK_APPLICATION':np.count_nonzero}).rename(columns={"SK_APPLICATION": "CNT_CLOSED_CASH_POS"})

        return v_df

class TestScoreCardPredictorsBlaze(Predictors):

    def __init__(self,app_df,cb_df,beh_df):
        self.app_df = app_df
        self.cb_df = cb_df
        self.beh_df = beh_df 
        self.rez_df = None
        
    def get_predictors_rez_df(self)->None:

        df_base = pd.DataFrame({"SK_APPLICATION":self.cb_df['SK_APPLICATION'].unique()})

        dfs = [
        df_base,
        Predictors.max_date_open_card(self,self.cb_df),                  # max_date_open_card
        Predictors.min_date_open_card(self,self.cb_df),                  # min_date_open_card
        Predictors.all_cash_pos(self,self.cb_df),                        # all_cash_pos
        ]

        df_merged = reduce(lambda  left,right: pd.merge(left,right,how='outer',on=['SK_APPLICATION']), dfs)

        self.rez_df = df_merged



class TestScoreCardPredictors(Predictors):

    def __init__(self,app_df,cb_df,beh_df):
        self.app_df = app_df
        self.cb_df = cb_df
        self.beh_df = beh_df 
        self.rez_df = None
        
    def get_predictors_rez_df(self)->None:

        df_base = pd.DataFrame({"SK_APPLICATION":self.app_df['SK_APPLICATION'].unique()})

        dfs = [
        df_base,
        Predictors.max_date_open_card(self,self.cb_df),                  # max_date_open_card
        Predictors.min_date_open_card(self,self.cb_df),                  # min_date_open_card
        Predictors.all_cash_pos(self,self.cb_df),                        # all_cash_pos
        Predictors.cnt_closed_cash_pos(self,self.app_df,self.cb_df),     # cnt_closed_cash_pos
        Predictors.age_years_real(self,self.app_df),                     # age_years_real
        Predictors.education(self,self.app_df,self.beh_df),              # education
        ]

        df_merged = reduce(lambda  left,right: pd.merge(left,right,how='outer',on=['SK_APPLICATION']), dfs)

        self.rez_df = df_merged