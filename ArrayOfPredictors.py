class PredictorsTest():
    def __init__(self,key,value,typeVal):
        self.key = key
        self.value = value
        self.typeVal = typeVal

PredictorsTestObj1 = PredictorsTest('CB_MAXAGRMNTHS_1_3','1','n')
PredictorsTestObj2 = PredictorsTest('CB_MAXAGRMNTHS_2_3','2','n')
PredictorsTestObj3 = PredictorsTest('CB_MAXAGRMNTHS_3_3','3','n')
PredictorsTestObj4 = PredictorsTest('SEX','m','c')


arrayOfPredictors = []
arrayOfPredictors.append(PredictorsTestObj1)
arrayOfPredictors.append(PredictorsTestObj2)
arrayOfPredictors.append(PredictorsTestObj3)
arrayOfPredictors.append(PredictorsTestObj4)

def getPredictorArray():
    return arrayOfPredictors
