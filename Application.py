from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
from typing import Any
 
class Builder(ABC):
 """
 Builder interface
 """
 @abstractproperty
 def product(self) -> None:
 pass
 @abstractmethod
 def getAggregatorParamData(self) -> None:
 pass
 @abstractmethod
 def getBehaviourData(self) -> None:
 pass
 @abstractmethod
 def getCreditBureauData(self) -> None:
 pass
 
class BuilderVectorDWH (Builder):
 """
 Builder class - realization of the concrete builder
 """
 def __init__(self) -> None:
 """
 Null object of the Application is creating
 """
 self.reset()
 def reset(self) -> None:
 self._product = Applicatiton()
 
 @property
 def product(self) -> Application:
 """
 Should reset the builder, if we want to initiallizwe new object , using decorator 
 """
 product = self._product
 self.reset()
 return product
 
 def getCreditBureauData(self) -> None:
 self._product.get("CreditBurea")
 def getBehaviourData(self) -> None:
 self._product.get("AgregatorResult")
 def getAggregatorParamData(self) -> None:
 self._product.get("BehaviorData")
 
class Application():
 """
 get Product
 """
 def __init__(self) -> None:
 
 'TO DO DYNAMIC INITIALIZATION HERE'
 
 def get(self, part: Any) -> None:
 
 'TO DO DWH REQUEST HERE'
 
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
 def buildAppforXGBScoreCard(self) -> None:
 self.builder.getCreditBureauData()
 self.builder.getBehaviourData()
 self.builder.getAggregatorParamData()
 
 