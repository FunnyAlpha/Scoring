from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
from typing import Any
import cx_Oracle
import pandas as pd
from Config import Auhorization,Credit_bureau_data_mart
 
#################################

class Builder(ABC):

 #Builder interface
 
 @abstractproperty
 def product(self) -> None:
     pass
 @abstractmethod
 def getCreditBureauData(self) -> None:
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
     self.reset()
     return product
 
 def getCreditBureauData(self) -> None:
    self._product.get_dwh(Credit_bureau_data_mart())
 
#################################

class Application():
 
 #get Product
 
 def __init__(self) -> None:
     self.CreditBureau_df = None
 
 def get_dwh(self, p_sql_query: Any) -> None:

    v_sql_query = str(p_sql_query)
    v_con_name = str(Auhorization())

    conn = cx_Oracle.connect(v_con_name)

    #print(v_con_name)
    #print(v_sql_query)

    df = pd.read_sql_query(v_sql_query,conn)

    conn.close()

    self.CreditBureau_df = df   
#################################
'''
class Controller:
 """
 Application configuration for definite scorecard
 """
 def __init__(self) -> None:
     self._builder = None
@property
 def builder(self) -> Builder:
     return self._builder
@builder.setter
 def builder(self, builder: Builder) -> None:
 """
 """
 self._builder = builder
 """

 """
 def buildAppforBureauScoreCard(self) -> None:
    self.builder.getCreditBureauData()
 #################################
 '''