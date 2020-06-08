from Application import *
from Predictors import *
import numpy as np
from tabulate import tabulate
from sklearn.preprocessing import MinMaxScaler
from Parse import test_str

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
    '''
    def load_data_frame(self):
        # GET INPUT DATA
        v_input_data = None
        controller = Controller()
        builder = BuilderVectorDWH(v_input_data)
        controller.builder = builder
        controller.buildVctForTestScoreCard()
        # GET OUTPUT DATA
        predictors_dwh  = TestScoreCardPredictors(builder.product.Application_df,builder.product.CreditBureau_df,builder.product.Behavioral_df)
        predictors_dwh.get_predictors_rez_df()
        return predictors_dwh.rez_df


    def load_data_frame_blaze():

        # GET INPUT DATA
        v_input_data = 'sample_vector_cb.txt'
        controller = Controller()
        builder = BuilderVectorBlaze(v_input_data)
        controller.builder = builder
        controller.buildVctForTestScoreCardBlaze()
        # GET OUTPUT DATA
        predictors_dwh  = Predictors(builder.product.Application_df,
                                    builder.product.CreditBureau_df,
                                    builder.product.Behavioral_df,
                                    builder.product.predictors_list_df,
                                    builder.product.predictor_cash_df,
                                    )
        predictors_dwh.get_predictors_rez_df()
        return predictors_dwh.rez_df
    '''
    def load_data_frame_dwh():

        # GET INPUT DATA
        v_input_data = None
        controller = Controller()
        builder = BuilderVectorDWH(v_input_data)
        controller.builder = builder
        controller.buildVctForTestScoreCard()
        # GET OUTPUT DATA
        predictors_dwh  = Predictors(builder.product.Application_df,
                                    builder.product.CreditBureau_df,
                                    builder.product.Behavioral_df,
                                    builder.product.predictors_list_df,
                                    builder.product.predictor_cash_df
                                    )
        predictors_dwh.get_predictors_dwh_df()
        return predictors_dwh.rez_df[predictors_dwh.rez_df['SK_APPLICATION']==203841905]   


    def load_data_frame_blaze_str(p_input_str):

        # GET INPUT DATA
        #v_input_data = p_input_str
        controller = Controller()
        builder = BuilderVectorBlazeStr(p_input_str)
        controller.builder = builder
        controller.buildVctForBlaze()
        # GET OUTPUT DATA
        #print(builder.product.Behavioral_df)
        predictors_dwh  = Predictors(builder.product.Application_df,
                                    builder.product.CreditBureau_df,
                                    builder.product.Behavioral_df,
                                    builder.product.predictors_list_df,
                                    builder.product.predictor_cash_df
                                    )
        predictors_dwh.get_predictors_blaze_df()
        return predictors_dwh.rez_df

    #print('dwh: ',load_data_frame_dwh())
    #print('blaze :',load_data_frame_blaze())   


    print(tabulate(load_data_frame_dwh(), headers='keys',tablefmt='psql',disable_numparse=True))
    #print(tabulate(load_data_frame_blaze(), headers='keys',tablefmt='psql',disable_numparse=True))
    print(tabulate(load_data_frame_blaze_str(test_str), headers='keys',tablefmt='psql',disable_numparse=True))