from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from functools import reduce
from typing import Any

import pandas as pd

import cx_Oracle
from Config import (Auhorization, f_credit_bureau_tt_cb,
                    f_scoring_vector_tt_app, f_scoring_vector_tt_beh,
                    f_scoring_vector_tt_cb)
from Parse import _df_dict, get_df_vct_blaze, parse_vct, parse_vct_str, _rx_dict

#################################


class Builder(ABC):

 # Builder interface

    @abstractproperty
    def product(self) -> None:
        pass

    @abstractmethod
    def getCreditBureauData(self) -> None:
        pass

    @abstractmethod
    def getApplicationData(self) -> None:
        pass

    @abstractmethod
    def getBehavioralData(self) -> None:
        pass

    @abstractmethod
    def getPredictorListData(self) -> None:
        pass

    @abstractmethod
    def getPredictorCashData(self) -> None:
        pass
#################################


class BuilderVectorDWH (Builder):

 # Builder class - realization of the concrete builder

    def __init__(self, p_InputData) -> None:
        # Null object of the Application is creating
        self.reset(p_InputData)

    def reset(self, p_InputData) -> None:
        self._product = Application(p_InputData)

    @property
    def product(self) -> Application:
        product = self._product
        # self.reset()
        return product

    def getCreditBureauData(self) -> None:

        self._product.CreditBureau_df = self._product.get_df_dwh(f_scoring_vector_tt_cb())

    def getApplicationData(self) -> None:

        self._product.Application_df = self._product.get_df_dwh(f_scoring_vector_tt_app())

    def getBehavioralData(self) -> None:

        self._product.Behavioral_df = self._product.get_df_dwh(f_scoring_vector_tt_beh())

    def getPredictorListData(self) -> None:

        pass

    def getPredictorCashData(self, source) -> None:

        pass

#################################


class BuilderVectorBlazeFile (Builder):

    def __init__(self, p_InputData) -> None:
        # Null object of the Application is creating
        self.reset(p_InputData)

    def reset(self, p_InputData) -> None:
        
        # TO DO
        self._product = Application(p_InputData)
        self._product.get_df_blaze_file()

    @property
    def product(self) -> Application:
        product = self._product
        # self.reset()
        return product

    def getCreditBureauData(self) -> None:

        self._product.CreditBureau_df = get_df_vct_blaze('CREDITBUREAU', self._product.vector_dict)

    def getApplicationData(self) -> None:

        v_dfs = [get_df_vct_blaze('APPLICATION', self._product.vector_dict), get_df_vct_blaze(
                'PERSONS', self._product.vector_dict)]
        v_df_merged = reduce(lambda left, right: pd.merge(
                left, right, how='outer', on=['SK_APPLICATION']), v_dfs)
        self._product.Application_df = v_df_merged

    def getBehavioralData(self) -> None:

        self._product.Behavioral_df = get_df_vct_blaze('BEHAVIOURDATA', self._product.vector_dict)

    def getPredictorListData(self) -> None:

        pass

    def getPredictorCashData(self) -> None:

        pass

#################################


class BuilderVectorBlaze (Builder):

    def __init__(self, p_InputData) -> None:
        # Null object of the Application is creating
        self.reset(p_InputData)

    def reset(self, p_InputData) -> None:
         # TO DO
        self._product = Application(p_InputData)
        self._product.get_df_blaze()

    @property
    def product(self) -> Application:
        # Should reset the builder, if we want to initiallizwe new object , using decorator
        product = self._product
        # self.reset()
        return product

    def getCreditBureauData(self) -> None:

        self._product.CreditBureau_df = get_df_vct_blaze('CREDITBUREAU', self._product.vector_dict)

    def getApplicationData(self) -> None:

        v_dfs = [get_df_vct_blaze('APPLICATION', self._product.vector_dict), get_df_vct_blaze(
                'PERSONS', self._product.vector_dict)]
        v_df_merged = reduce(lambda left, right: pd.merge(
                left, right, how='outer', on=['SK_APPLICATION']), v_dfs)
        self._product.Application_df = v_df_merged

    def getBehavioralData(self) -> None:

        self._product.Behavioral_df = get_df_vct_blaze('BEHAVIOURDATA', self._product.vector_dict)

    def getPredictorListData(self) -> None:

        self._product.predictors_list_df = get_df_vct_blaze('PREDICTORSLIST', self._product.vector_dict)

    def getPredictorCashData(self) -> None:

        self._product.predictor_cash_df = get_df_vct_blaze('PREDICTORSCASH', self._product.vector_dict)
       # self._product.predictor_cash_df['VALUE'] = (self._product.predictor_cash_df['REALVALUE'])
        # print(self._product.predictor_cash_df)


#################################

class Application():

    # get Product

    def __init__(self, p_InputData) -> None:

        self.CreditBureau_df = None
        self.Application_df = None
        self.Behavioral_df = None
        self.predictors_list_df = None
        self.predictor_cash_df = None
        self.vector_dict = None
        self.InputData = p_InputData

    def get_df_dwh(self, p_sql_query: Any):

        v_sql_query = str(p_sql_query)
        v_con_name = str(Auhorization())

        conn = cx_Oracle.connect(v_con_name)

        df = pd.read_sql_query(v_sql_query, conn)

        conn.close()

        return df

    def get_df_blaze_file(self):

        v_dict = parse_vct(self.InputData)

        self.vector_dict = v_dict

        pass

    def get_df_blaze(self):

        # print(df_dict)
        v_dict = parse_vct_str(self.InputData)

        self.vector_dict = v_dict

        pass


#################################

class Controller:
    '''
    Application configuration for definite scorecard
    '''

    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        self._builder = builder

    def buildVctForTestScoreCard(self) -> None:
        self.builder.getCreditBureauData()
        self.builder.getApplicationData()
        self.builder.getBehavioralData()
    #################################

    def buildVctForTestScoreCardBlaze(self) -> None:
        self.builder.getCreditBureauData()
        self.builder.getApplicationData()
        self.builder.getBehavioralData()
    #################################

    def buildVctForBlaze(self) -> None:
        self.builder.getCreditBureauData()
        self.builder.getApplicationData()
        self.builder.getBehavioralData()
        self.builder.getPredictorListData()
        self.builder.getPredictorCashData()
    #################################
