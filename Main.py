from Application import *
from Predictors import *
import numpy as np
from tabulate import tabulate
from sklearn.preprocessing import MinMaxScaler

if __name__ == "__main__":

    # GET INPUT DATA
    #controller = Controller()
    #builder = BuilderVectorDWH()
    #controller.builder = builder
    #controller.buildVctForTestScoreCard()

    # GET OUTPUT DATA
    #predictors_dwh  = TestScoreCardPredictors(builder.product.Application_df,builder.product.CreditBureau_df,builder.product.Behavioral_df)
    
    #print(dir(builder.product.Application_df))
    #print(builder.product.Application_df['SYSDATE'])

    #predictors_dwh.get_predictors_rez_df()

    # PRINT OUTPUT DATAFRAME

    #print(predictors_dwh.rez_df[predictors_dwh.rez_df['SK_APPLICATION']==203841905])

    #min_max_scaler = MinMaxScaler()
    #predictors_dwh.rez_df[['MAX_DATE_OPEN_CARD']] = min_max_scaler.fit_transform(predictors_dwh.rez_df[['MAX_DATE_OPEN_CARD']])

    #df[['MAX_DATE_OPEN_CARD']]=
    #predictors_dwh.rez_df['MAX_DATE_OPEN_CARD'] = normalize(predictors_dwh.rez_df['MAX_DATE_OPEN_CARD'])

    #print(tabulate(predictors_dwh.rez_df[predictors_dwh.rez_df['SK_APPLICATION']==203841905], headers='keys',tablefmt='psql',disable_numparse=True))

    #predictors_dwh.rez_df['MAX_DATE_OPEN_CARD'] = normalize(predictors_dwh.rez_df['MAX_DATE_OPEN_CARD'])
    #print(1)
    #print(tabulate(predictors_dwh.rez_df, headers='keys',tablefmt='psql',disable_numparse=True))

    #print(tabulate(predictors_dwh.rez_df, headers='keys',tablefmt='psql',disable_numparse=True))

    def load_data_frame(self):
        # GET INPUT DATA
        controller = Controller()
        builder = BuilderVectorDWH()
        controller.builder = builder
        controller.buildVctForTestScoreCard()
        # GET OUTPUT DATA
        predictors_dwh  = TestScoreCardPredictors(builder.product.Application_df,builder.product.CreditBureau_df,builder.product.Behavioral_df)
        predictors_dwh.get_predictors_rez_df()
        return predictors_dwh.rez_df

    def load_data_frame_blaze():

        # GET INPUT DATA
        controller = Controller()
        builder = BuilderVectorBlaze()
        controller.builder = builder
        controller.buildVctForTestScoreCardBlaze()
        # GET OUTPUT DATA
        predictors_dwh  = TestScoreCardPredictors(builder.product.Application_df,builder.product.CreditBureau_df,builder.product.Behavioral_df)
        predictors_dwh.get_predictors_rez_df()
        return predictors_dwh.rez_df

    def load_data_frame_dwh():

        # GET INPUT DATA
        controller = Controller()
        builder = BuilderVectorDWH()
        controller.builder = builder
        controller.buildVctForTestScoreCard()
        # GET OUTPUT DATA
        predictors_dwh  = TestScoreCardPredictors(builder.product.Application_df,builder.product.CreditBureau_df,builder.product.Behavioral_df)
        predictors_dwh.get_predictors_rez_df()
        return predictors_dwh.rez_df[predictors_dwh.rez_df['SK_APPLICATION']==203841905]   


    #print('dwh: ',load_data_frame_dwh())
    #print('blaze :',load_data_frame_blaze())   


    print(tabulate(load_data_frame_dwh(), headers='keys',tablefmt='psql',disable_numparse=True))
    print(tabulate(load_data_frame_blaze(), headers='keys',tablefmt='psql',disable_numparse=True))