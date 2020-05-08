from Application import *

if __name__ == "__main__":

    vector_dwh = BuilderVectorDWH()
    vector_dwh.getCreditBureauData()

    print (vector_dwh.product.CreditBureau_df)