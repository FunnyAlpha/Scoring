import pandas as pd
import numpy as np
from functools import reduce
from tabulate import tabulate
#from Config import predictors_fun

class Predictors():
    #construct object
    def __init__(self,app_df,cb_df,beh_df,predictors_list_df,predictor_cash_df):
        self.app_df = app_df
        self.cb_df = cb_df
        self.beh_df = beh_df 
        self.rez_df = None
        self.predictors_list_df = predictors_list_df
        self.predictors_cash_df = predictor_cash_df

        self.predictors_fun={
        'MAX_DATE_OPEN_CARD':self.max_date_open_card(),
        'MIN_DATE_OPEN_CARD':self.min_date_open_card(),
        'CNT_CLOSED_CASH_POS':self.cnt_closed_cash_pos(),
        'AGE_YEARS_REAL':self.age_years_real(),
        'EDUCATION':self.education(),
        'ALL_CASH_POS':self.all_cash_pos()
        }

    def add_unknown_columns(self,df,features_list):
        
        for el in features_list:
            if el not in df:
                df[el] = np.nan
        pass

    def is_card(self,credit_type):
        return 1 if credit_type == 4  else 0

    def age_years_real(self):

        v_df = self.app_df[['SK_APPLICATION']].assign(AGE_YEARS_REAL=(self.app_df['SYSDATE'] - self.app_df['BIRTH'])/np.timedelta64(1,'Y'))

        return v_df

    def education(self):

        self.add_unknown_columns(self.app_df,['EDUCATION'])
        self.add_unknown_columns(self.beh_df,['EDUCATION'])

        df = reduce(
        lambda  left,right: pd.merge(left,right,how='outer',on=['SK_APPLICATION']),
        [self.app_df,self.beh_df.rename(columns={"EDUCATION": "BEHEDUCATION"})]
        )
        v_df= self.app_df[['SK_APPLICATION']].assign(EDUCATION=(df['EDUCATION'].fillna(df['BEHEDUCATION'])))

        #print(v_df)

        return v_df
    
    def max_date_open_card(self):

        #print(df['CREDIT_TYPE'].dtype)
        #print(df['CREDIT_TYPE'].apply(lambda x:1 if x in {4,14,24} else 0))

        v_df=self.cb_df[
        (self.cb_df['CREDITJOINT'] == 1) &
        (self.cb_df['CREDITOWNER'] == '0') &
        (self.cb_df['CREDITTYPE'].apply(lambda x:1 if x in {4,14,24} else 0)) == 1
        ].groupby(['SK_APPLICATION']).agg({'CREDITDATE':np.max}).rename(columns={"CREDITDATE": "MAX_DATE_OPEN_CARD"})
    
       # df.rename(columns={"B": "c"})

        return v_df
    
    def min_date_open_card(self):

        #print(df['CREDIT_TYPE'].dtype)
        #print(df['CREDIT_TYPE'].apply(lambda x:1 if x in {4,14,24} else 0))

        v_df = self.cb_df[
        (self.cb_df['CREDITJOINT'] == 1) &
        (self.cb_df['CREDITOWNER'] == '0') &
        (self.cb_df['CREDITTYPE'].apply(lambda x:1 if x in {4,14,24} else 0)) == 1
        ].groupby(['SK_APPLICATION']).agg({'CREDITDATE':np.min}).rename(columns={"CREDITDATE": "MIN_DATE_OPEN_CARD"})
  

        return v_df

    def all_cash_pos(self):

        v_df = self.cb_df[
        (self.cb_df['CREDITJOINT'] == 1) &
        (self.cb_df['CREDITOWNER'] == '0') &
        (self.cb_df['CREDITTYPE'].apply(lambda x:1 if x in {5,8,13} else 0)) == 1
        ].groupby(['SK_APPLICATION']).agg({'SK_APPLICATION':np.count_nonzero}).rename(columns={"SK_APPLICATION": "ALL_CASH_POS"})

        return v_df

    def cnt_closed_cash_pos(self):

        #print(df_test)

        v_df = self.cb_df[
        (self.cb_df['CREDITJOINT'] == 1) &
        (self.cb_df['CREDITOWNER'] == '0') &
        (self.cb_df['CREDITTYPE'].apply(lambda x:1 if x in {4,14,24} else 0)) == 1
        #(df['SK_DATE_DECISION']==df['SK_DATE_DECISION'])
        ].groupby(['SK_APPLICATION']).agg({'SK_APPLICATION':np.count_nonzero}).rename(columns={"SK_APPLICATION": "CNT_CLOSED_CASH_POS"})

        return v_df


    def get_predictors_dwh_df(self)->None:

        df_base = pd.DataFrame({"SK_APPLICATION":self.app_df['SK_APPLICATION'].unique()})

        dfs = [
        df_base,
        self.cnt_closed_cash_pos(),                 # cnt_closed_cash_pos
        self.max_date_open_card(),                  # max_date_open_card
        self.min_date_open_card(),                  # min_date_open_card
        self.all_cash_pos(),                        # all_cash_pos
        self.age_years_real(),                      # age_years_real
        self.education(),                           # education
        ]

        df_merged = reduce(lambda  left,right: pd.merge(left,right,how='outer',on=['SK_APPLICATION']), dfs)

        self.rez_df = df_merged

    def get_predictors_blaze_df(self)->None:

        df_base = pd.DataFrame({"SK_APPLICATION":self.app_df['SK_APPLICATION'].unique()})

        dfs=[df_base]
        #print(dfs)

        for index,row in self.predictors_list_df.iterrows():
            #print(row['NAME'])
            v_dfs=self.get_predictor_value(row['NAME'])

            #print(v_dfs)

            dfs.append(v_dfs)
    
        df_merged = reduce(lambda  left,right: pd.merge(left,right,how='outer',on=['SK_APPLICATION']), dfs)

        self.rez_df = df_merged



    def get_predictor_value(self,p_name):
        #print(tabulate(self.predictors_cash_df, headers='keys',tablefmt='psql',disable_numparse=True))
        #print(self.predictors_cash_df)
        for index,row in self.predictors_cash_df.iterrows():
            #print(row['NAME'])
            #print(p_name)
            if row['NAME'] == p_name and row['CLASS'] == 'scoreCardPredictor':
                #print(self.predictors_cash_df)
                #print('HERE')
                #v_value = row['VALUE']
                v_df = pd.DataFrame({
                    'SK_APPLICATION':[self.predictors_cash_df.loc[index,'SK_APPLICATION']],
                    row['NAME']:[self.predictors_cash_df.loc[index,'VALUE']]
                })
                return v_df
            else:
                #print(row['NAME'])
                v_df = self.predictors_fun.get(p_name)
        return v_df
                
            



        
