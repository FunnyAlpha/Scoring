import pandas as pd
import numpy as np
from functools import reduce

class Predictors:
    #construct object with null df
    def __init__(self,predictors_cb_df):
        self.predictors_cb_df = predictors_cb_df
        self.predictors_out_df = None

    def is_card(self,credit_type):
        return 1 if credit_type == 4  else 0
    
    
    def max_date_open_card(self,df):

        #print(df['CREDIT_TYPE'].dtype)
        #print(df['CREDIT_TYPE'].apply(lambda x:1 if x in {4,14,24} else 0))

        v_df=df[
        (df['NFLAG_CREDIT_JOINT'] == 1) &
        (df['FLAG_CREDIT_OWNER'] == '0') &
        (df['CREDIT_TYPE'].apply(lambda x:1 if x in {4,14,24,5} else 0)) == 1
        ].groupby(['SK_APPLICATION']).agg({'DTIME_CREDIT':np.max}).rename(columns={"DTIME_CREDIT": "MAX_DATE_OPEN_CARD"})
    
       # df.rename(columns={"B": "c"})

        return v_df
    
    def min_date_open_card(self,df):

        #print(df['CREDIT_TYPE'].dtype)
        #print(df['CREDIT_TYPE'].apply(lambda x:1 if x in {4,14,24} else 0))

        v_df=df[
        (df['NFLAG_CREDIT_JOINT'] == 1) &
        (df['FLAG_CREDIT_OWNER'] == '0') &
        (df['CREDIT_TYPE'].apply(lambda x:1 if x in {4,14,24} else 0)) == 1
        ].groupby(['SK_APPLICATION']).agg({'DTIME_CREDIT':np.min}).rename(columns={"DTIME_CREDIT": "MIN_DATE_OPEN_CARD"})
  

        return v_df



class TestScoreCardPredictors(Predictors):

    def __init__(self,predictors_cb_df):
        super().__init__(predictors_cb_df)
        
        
    def get_predictors_rez_df(self,df)->None:

        #print(df['SK_APPLICATION'])

        #print(Predictors.max_date_open_card(self,df))
        df_base = df['SK_APPLICATION'].unique() 
        df1 = Predictors.max_date_open_card(self,df)
        df2 = Predictors.min_date_open_card(self,df)

        dfs = [df.set_index(['SK_APPLICATION']) for df in [df_base,df1,df2]]

        #data_frames = [df_base,df1,df2]
        #df_merged = reduce(lambda  left,right: pd.merge(left,right,how='outer',on=['SK_APPLICATION']), data_frames)


        #print(df1)
        self.predictors_out_df = pd.concat(dfs, axis=1).reset_index()
        #self.predictors_out_df = pd.merge(df1,df2,how='outer',on=['SK_APPLICATION'])
        #self.predictors_out_df = pd.merge(df1,df2,how='outer',on=['SK_APPLICATION'])
        #self.predictors_out_df = df1.set_index('SK_APPLICATION').join(df2.set_index('SK_APPLICATION'))