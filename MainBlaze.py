from Application import *
from Predictors import *
import numpy as np
from tabulate import tabulate

if __name__ == "__main__":

    # GET INPUT DATA
    controller = Controller()
    builder = BuilderVectorBlaze()
    controller.builder = builder
    controller.buildVctForTestScoreCardBlaze()

    print(builder.product.CreditBureau_df[['CREDITJOINT','CREDITOWNER','CREDITTYPE','CREDITDATE']])

    #df = builder.product.CreditBureau_df
    #df['CREDITJOINT'].astype(str).

    #print(df['CREDITJOINT'].dtype)

    # GET OUTPUT DATA
    predictors_dwh  = TestScoreCardPredictorsBlaze(builder.product.Application_df,builder.product.CreditBureau_df,builder.product.Behavioral_df)
    
    #print(dir(predictors_dwh))

    predictors_dwh.get_predictors_rez_df()

    # PRINT OUTPUT DATAFRAME
    print(tabulate(predictors_dwh.rez_df, headers='keys',tablefmt='psql',disable_numparse=True))