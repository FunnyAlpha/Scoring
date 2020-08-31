from Application import Controller,BuilderVectorDWH,BuilderVectorBlaze
from Predictors import Predictors
import numpy as np
from tabulate import tabulate
from sklearn.preprocessing import MinMaxScaler
from Parse import test_str,parse_df_objArr,parse_df_json
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

if __name__ == "__main__":   

    def get_predictors_dwh():

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
        return predictors_dwh.rez_df   


    def get_predictors_blaze(p_input_str):

        # GET INPUT DATA
        controller = Controller()
        builder = BuilderVectorBlaze(p_input_str)
        controller.builder = builder
        controller.buildVctForBlaze()
        # GET OUTPUT DATA
        predictors_blaze_df  = Predictors(builder.product.Application_df,
                                        builder.product.CreditBureau_df,
                                        builder.product.Behavioral_df,
                                        builder.product.predictors_list_df,
                                        builder.product.predictor_cash_df
                                        )
        predictors_blaze_df.get_predictors_blaze_df()
        predictors_blaze = parse_df_objArr(predictors_blaze_df.rez_df)
        return predictors_blaze

    def get_predictors_blaze_json(p_input_str):

        # GET INPUT DATA
        controller = Controller()
        builder = BuilderVectorBlaze(p_input_str)
        controller.builder = builder
        controller.buildVctForBlaze()
        # GET OUTPUT DATA
        predictors_blaze_df  = Predictors(builder.product.Application_df,
                                        builder.product.CreditBureau_df,
                                        builder.product.Behavioral_df,
                                        builder.product.predictors_list_df,
                                        builder.product.predictor_cash_df
                                        )
        predictors_blaze_df.get_predictors_blaze_df()
        predictors_blaze = parse_df_json(predictors_blaze_df.rez_df)
        return predictors_blaze

    def get_vector_str(p_input_str):

        return p_input_str
    # print(tabulate(get_predictors_blaze(test_str), headers='keys',tablefmt='psql',disable_numparse=True))

    print(get_predictors_blaze_json(test_str))


    # predObjArrVar = get_predictors_blaze(test_str)
    # for x in predObjArrVar:

    #     print("key: ",x.key)
    #     print("value: ",x.value)
    #     print("typeVal: ",x.typeVal)
    
    # with PyCallGraph(output=GraphvizOutput()):
    #     df=get_predictors_blaze(test_str)

    