
from sklearn.base import BaseEstimator, TransformerMixin
from Application import *
from Predictors import *
import numpy as np
from tabulate import tabulate
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import xgboost


class CategoricalImputer(BaseEstimator, TransformerMixin):
    def __init__(self, variables=None):
    #Check if the variables passed are in a list format, if not convert 
    #to list format and assign it to self.variables to be used in later 
    #methods
        if not isinstance(variables,list):
            self.variables = [variables]
        else:
            self.variables = variables
    
    def fit(self, X:pd.DataFrame,y:pd.Series=None):
        #Nothing to do here, just return the dataframe as is
        return self
    
    def transform(self, X:pd.DataFrame):
	      #Fill missing values and return the modified dataframe
        X=X.copy()
        for feature in self.variables:
            X[feature] = X[feature].fillna('0')
        return X

class CategoricalEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, variables=None):
    #Check if the variables passed are in a list format, if not convert 
    #to list format and assign it to self.variables to be used in later 
    #methods
        if not isinstance(variables,list):
            self.variables = [variables]
        else:
            self.variables = variables
    
    def fit(self, X:pd.DataFrame,y:pd.Series=None):
        #Nothing to do here, just return the dataframe as is
        return self
    
    def transform(self, X:pd.DataFrame):
	      #Fill missing values and return the modified dataframe
        X=X.copy()
        for feature in self.variables:
            X[feature] = X[feature].astype(int)
        return X

def load_data_frame():
        # GET INPUT DATA
        controller = Controller()
        builder = BuilderVectorDWH()
        controller.builder = builder
        controller.buildVctForTestScoreCard()
        # GET OUTPUT DATA
        predictors_dwh  = TestScoreCardPredictors(builder.product.Application_df,builder.product.CreditBureau_df,builder.product.Behavioral_df)
        predictors_dwh.get_predictors_rez_df()
        return predictors_dwh.rez_df


#print(df1.iloc[:,0:7])
#print(df1.iloc[:,7:8])

test_pipe = Pipeline(
[
('categoricalImputer',CategoricalImputer(variables=['EDUCATION'])),
('categoricalEncoder',CategoricalEncoder(variables=['EDUCATION'])),
('scaler',MinMaxScaler()),
('model',Lasso(alpha=0.005,random_state = 0))
]
)

'''
def save_pipeline(*, pipeline_to_persist) -> None:
    #Persist the pipeline.

    # Prepare versioned save file name
    save_file_name = 'testprediction_pipeline.pkl'
    save_path = “path_to_save/”
    joblib.dump(pipeline_to_persist, save_path+save_file_name)
'''    
 
np.random.seed(7)
df1 = load_data_frame()
df1 = df1.drop('SK_APPLICATION', 1)
df1['TARGET'] = np.random.randint(0, 2, df1.shape[0])

#print(df1['TARGET'])

min_max_scaler = MinMaxScaler()
df1[['MAX_DATE_OPEN_CARD','MIN_DATE_OPEN_CARD']] = min_max_scaler.fit_transform(df1[['MAX_DATE_OPEN_CARD','MAX_DATE_OPEN_CARD']])
df1['EDUCATION'] = df1['EDUCATION'].fillna('0').replace('XNA','0').astype(int)


X = df1.iloc[:,0:6]
Y = df1.iloc[:,6:7]

seed = 7 
test_size = 0.3
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)

#print(X_train)

model = xgboost.XGBClassifier()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_score = model.predict_proba(X_test)

#print(y_score)

predictions = [round(value) for value in y_pred]

accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

#def run_training():


