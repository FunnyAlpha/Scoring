from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
from typing import Any
import cx_Oracle
import pandas as pd
from Config import *
from Parse import *
from functools import reduce

#################################

class Builder(ABC):

 #Builder interface
 
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
#################################

class BuilderVectorDWH (Builder):
 
 #Builder class - realization of the concrete builder

 def __init__(self) -> None:
     #Null object of the Application is creating
     self.reset()
 
 def reset(self) -> None:
     self._product = Application()
 
 @property
 def product(self) -> Application:
     #Should reset the builder, if we want to initiallizwe new object , using decorator
     product = self._product
     #self.reset()
     return product
 
 def getCreditBureauData(self,source) -> None:

     if source == 'vct':
         self._product.CreditBureau_df = self._product.get_df_dwh(f_scoring_vector_tt_cb())
     elif source == 'dm':
         self._product.CreditBureau_df = self._product.get_df_dwh(f_credit_bureau_tt_cb())
     else:
         self._product.CreditBureau_df = self._product.get_df_dwh(f_credit_bureau_tt_cb())

 def getApplicationData(self,source) -> None:

     if source == 'vct':
         self._product.Application_df = self._product.get_df_dwh(f_scoring_vector_tt_app())
     elif source == 'dm':
         self._product.Application_df = self._product.get_df_dwh(f_scoring_vector_tt_app())
     else:
         self._product.Application_df = self._product.get_df_dwh(f_scoring_vector_tt_app())

 def getBehavioralData(self,source) -> None:

     if source == 'vct':
         self._product.Behavioral_df = self._product.get_df_dwh(f_scoring_vector_tt_beh())
     elif source == 'dm':
         self._product.Behavioral_df = self._product.get_df_dwh(f_scoring_vector_tt_beh())
     else:
         self._product.Behavioral_df = self._product.get_df_dwh(f_scoring_vector_tt_beh())
#################################


class BuilderVectorBlaze (Builder):

    def __init__(self) -> None:
        #Null object of the Application is creating
        self.reset()
 
    def reset(self) -> None:
        self._product = Application()
        self._product.get_df_blaze('sample_vector_cb.txt')
 
    @property
    def product(self) -> Application:
        #Should reset the builder, if we want to initiallizwe new object , using decorator
        product = self._product
        #self.reset()
        return product
 
    def getCreditBureauData(self,source) -> None:

        if source == 'txt':
            self._product.CreditBureau_df = get_df_txt('CREDITBUREAU',self._product.Vector_dict)
        else:
            self._product.CreditBureau_df = get_df_txt('CREDITBUREAU',self._product.Vector_dict)

    def getApplicationData(self,source) -> None:
        
        if source == 'txt':
            v_dfs=[get_df_txt('APPLICATION',self._product.Vector_dict),get_df_txt('PERSONS',self._product.Vector_dict)]
            v_df_merged = reduce(lambda  left,right: pd.merge(left,right,how='outer',on=['SK_APPLICATION']), v_dfs)
            self._product.Application_df = v_df_merged
        else:
            self._product.Application_df = get_df_txt('APPLICATION',self._product.Vector_dict)

    def getBehavioralData(self,source) -> None:

        if source == 'txt':
            self._product.Behavioral_df = get_df_txt('BEHAVIOURDATA',self._product.Vector_dict)
        else:
            self._product.Behavioral_df = get_df_txt('BEHAVIOURDATA',self._product.Vector_dict)

            self._product.Behavioral_df = None

#################################


class Application():
 
 #get Product
 
 def __init__(self) -> None:

     self.CreditBureau_df = None
     self.Application_df = None
     self.Behavioral_df = None
     self.Vector_dict = None
 
 def get_df_dwh(self, p_sql_query: Any):
     
     v_sql_query = str(p_sql_query)
     v_con_name = str(Auhorization())

     conn = cx_Oracle.connect(v_con_name)

    #print(v_con_name)
    #print(v_sql_query)

     df = pd.read_sql_query(v_sql_query,conn)

     conn.close()

     return df

 def get_df_blaze(self,p_type):
     
     v_dict = parse_vct(p_type,df_dict,rx_dict)
     
     self.Vector_dict = v_dict

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
     self.builder.getCreditBureauData('vct')
     self.builder.getApplicationData('vct')
     self.builder.getBehavioralData('vct')
 #################################
 
 def buildVctForTestScoreCardBlaze(self) -> None:
     self.builder.getCreditBureauData('txt')
     self.builder.getApplicationData('txt')
     self.builder.getBehavioralData('txt')
 #################################