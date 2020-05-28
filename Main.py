from Application import *
from Predictors import *
import numpy as np
from tabulate import tabulate

if __name__ == "__main__":

    # GET INPUT DATA
    controller = Controller()
    builder = BuilderVectorDWH()
    controller.builder = builder
    controller.buildVctForTestScoreCard()

    # GET OUTPUT DATA
    predictors_dwh  = TestScoreCardPredictors(builder.product.Application_df,builder.product.CreditBureau_df,builder.product.Behavioral_df)
    
    #print(dir(builder.product.Application_df))
    #print(builder.product.Application_df['SYSDATE'])

    predictors_dwh.get_predictors_rez_df()

    # PRINT OUTPUT DATAFRAME

    #print(predictors_dwh.rez_df[predictors_dwh.rez_df['SK_APPLICATION']==203841905])

    print(tabulate(predictors_dwh.rez_df[predictors_dwh.rez_df['SK_APPLICATION']==203841905], headers='keys',tablefmt='psql',disable_numparse=True))

    #print(tabulate(predictors_dwh.rez_df, headers='keys',tablefmt='psql',disable_numparse=True))