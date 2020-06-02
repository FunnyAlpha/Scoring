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

 def __init__(self,p_InputData) -> None:
     #Null object of the Application is creating
     self.reset(p_InputData)
 
 def reset(self,p_InputData) -> None:
     self._product = Application(p_InputData)
 
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

    def __init__(self,p_InputData) -> None:
        #Null object of the Application is creating
        self.reset(p_InputData)
 
    def reset(self,p_InputData) -> None:

        self._product = Application(p_InputData)
        # TO DO - p_input_data
        #print(self._product.InputData)
        self._product.get_df_blaze()
 
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


class BuilderVectorBlazeStr (Builder):

    def __init__(self,p_InputData) -> None:
        #Null object of the Application is creating
        self.reset(p_InputData)
 
    def reset(self,p_InputData) -> None:

        self._product = Application(p_InputData)
        # TO DO - p_input_data
        self._product.get_df_blaze_str()

        #print(self._product.Vector_dict['DOCUMENTS'])
 
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
 
 def __init__(self,p_InputData) -> None:

     self.CreditBureau_df = None
     self.Application_df = None
     self.Behavioral_df = None
     self.Vector_dict = None
     self.InputData = p_InputData
 
 def get_df_dwh(self, p_sql_query: Any):
     
     v_sql_query = str(p_sql_query)
     v_con_name = str(Auhorization())

     conn = cx_Oracle.connect(v_con_name)

    #print(v_con_name)
    #print(v_sql_query)

     df = pd.read_sql_query(v_sql_query,conn)

     conn.close()

     return df

 def get_df_blaze(self):
     
     #print(df_dict)
     #print(rx_dict)s
     reset_config_vars()
     v_dict = parse_vct(self.InputData,df_dict,rx_dict)
     
     self.Vector_dict = v_dict

     pass

 def get_df_blaze_str(self):
     
     #print(df_dict)
     #print(rx_dict)
     #reset_config_vars()
     
     df_dict  = {
    'CREDITBUREAU':[],
    'BEHAVIOURDATA':[],
    'APPLICATION':[],
    'PREVAPPLICATION':[],
    'DOCUMENTS':[],
    'PERSONS':[],
    'SK_APPLICATION':[]
    }
    
     #print(df_dict)
     v_dict = parse_vct_str(self.InputData,df_dict,rx_dict)
     
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