# from dateutil import parser
# import re
# import pandas as pd
# #from Parse import *

# v_time =parser.parse('03.10.2012 00:00:00', dayfirst=True)
# #print(v_time.month)

# #print(v_time)

# # data=c|ApprovalCharacteristics[48].variation|1
# # n|ApprovalCharacteristics[49].integerValue|0

# # regex = re.compile(r'(.*?)\|ApprovalCharacteristics\[(\d+)\]\.(.*)\|(.*?)\s*$')

# # for line in data.split('\n'):    

# #     print(re.findall(regex,line)[0])



# # v_dict = parse_vct_str(test_str,df_dict,rx_dict)
# # print(v_dict['APPROVALCHARACTERISTIC'])
# # df = get_df_txt('APPROVALCHARACTERISTIC',v_dict)


# d = {'option1': ['1', '0', '1', '1'], 'option2': ['0', '0', '1', '0'], 'option3': ['1', '1', '0', '0']}
# df = pd.DataFrame(d)
# print(df)

# for index,row in df.iterrows():
#     #print (row['option1'])
#     if index == 1:
#         df1 = {'1':[df.loc[index,'option1']],'2':[df.loc[index,'option2']]}
#         print (row['option1'])

# print(pd.DataFrame(df1))

# from pycallgraph import PyCallGraph
# from pycallgraph.output import GraphvizOutput
# from Main import load_data_frame_blaze_str,test_str

# with PyCallGraph(output=GraphvizOutput()):
#     load_data_frame_blaze_str(test_str)



# from sklearn.externals import joblib

# saved_pipeline = joblib.load(filename='model_top_up.pkl')

import xgboost as xgb
import pandas as pd 
import numpy as np
# plot decision tree
#from numpy import loadtxt
#from xgboost import XGBClassifier
#from xgboost import plot_tree
import matplotlib.pyplot as plt


# data={'avg_dpd0':[2.3006134969325154],
#     'cnt_good_pos':[0],
#     'cnt_uniq_phones':[None],
#     'days_appr_first_not_rev':[5624],
#     'cnt_unsuccessful_weeks_24m':[3],
#     'instalment_count_paid_intime':[83],
#     'avg_dpd0_36m':[5.28333333333333],
#     'cnt_inst_to_pay_not_rd':[0],
#     'product_combination_last':[0.0201207243460765],
#     'cnt_part_ep':[None],
#     'avg_dpd0_12m':[14.2],
#     'flag_paid_off_after_dpd':[3],
#     'cnt_rej_9m':[4],
#     'days_last_full_ep':[4091]}

data={'CURRENT_CARD_UTILIZED_NEW_XGB': [None],
        'CNT_AVG_DAYS_BETWEEN_APPL_24M': [0.0], 
        'SUM_AMT_CREDIT': [74771.0], 
        'CNT_APPLICATIONS': [8.0], 
        'MAX_DPD_6': [-2], 
        'SCO_CASH_XSELL': [0.986612135], 
        'MONTHS_ID_PUBLISH': [213.0], 
        'MAX_LTH_WO_PD_36': [1], 
        'CNT_INST_12M': [0], 
        'AGE': [63.0], 
        'AMT_MAX_ANNUITY': [5722.23], 
        'MONTHS_TILL_FREEDOM': [-26], 
        'CBMAXDPD12': [0.0], 
        'AVG_DAYS_BETWEEN_APPS': [591], 
        'DD_CHANGE_MOBIL': [0.0], 
        'CNT_DAY_LAST_CREDIT': [1099.0], 
        'MAX_AMT_CREDIT_CUR': [None], 
        'AMT_PAYMENTS_TOTAL': [71676], 
        'CNT_MAX_MONTHS_TILL_PLANCLOSED': [-61.612900323], 
        'AMT_LIMIT_CREDIT_CARD': [0.0], 
        'CNT_MAX_DAYS_OVERDUE': [18], 
        'ALL_CASH_POS': [4], 
        'RECEIVABLE_TO_CREDIT_CUR': [None], 
        'ANNUITY_TO_CREDIT_CUR': [None], 
        'CNT_CONTRACT_CASH_ACTIVE': [0.0], 
        'CNT_DPD_0PL_EV_T_AL': [0.022], 
        'CRED_LENGTH':[4062.0]
    }


# data={
#         'CURRENT_CARD_UTILIZED_NEW_XGB': [None],
#         'CNT_AVG_DAYS_BETWEEN_APPL_24M': [None], 
#         'SUM_AMT_CREDIT': [220042], 
#         'CNT_APPLICATIONS': [None], 
#         'MAX_DPD_6': [-1], 
#         'SCO_CASH_XSELL': [None], 
#         'MONTHS_ID_PUBLISH': [218], 
#         'MAX_LTH_WO_PD_36': [2], 
#         'CNT_INST_12M': [None], 
#         'AGE': [68], 
#         'AMT_MAX_ANNUITY': [None], 
#         'MONTHS_TILL_FREEDOM': [-26], 
#         'CBMAXDPD12': [0], 
#         'AVG_DAYS_BETWEEN_APPS': [None], 
#         'DD_CHANGE_MOBIL': [0], 
#         'CNT_DAY_LAST_CREDIT': [1342], 
#         'MAX_AMT_CREDIT_CUR': [None], 
#         'AMT_PAYMENTS_TOTAL': [None], 
#         'CNT_MAX_MONTHS_TILL_PLANCLOSED': [None], 
#         'AMT_LIMIT_CREDIT_CARD': [None], 
#         'CNT_MAX_DAYS_OVERDUE': [None], 
#         'ALL_CASH_POS': [7], 
#         'RECEIVABLE_TO_CREDIT_CUR': [None], 
#         'ANNUITY_TO_CREDIT_CUR': [None], 
#         'CNT_CONTRACT_CASH_ACTIVE': [0], 
#         'CNT_DPD_0PL_EV_T_AL': [None], 
#         'CRED_LENGTH':[None]
#     }


df= pd.DataFrame(data)


#df = pd.read_csv("scoring_PTB_1.csv",sep=';')
xgtest = xgb.DMatrix(df.values)

#print(df)

bst = xgb.Booster({'nthread': 4})  # init model
bst.load_model('pos_ptb_model_for_blaze')  # load data

pred = bst.predict(xgtest)
#pd.DataFrame(1-pred).to_csv('out.csv',index=False,float_format='%.15f')
#print(pd.DataFrame(pred).to_excel('out.xlsx'))
print(list(map(lambda x: 1-x, pred)))

# pred = bst.predict(xgb.DMatrix(df))
# print(pred)
# print(list(map(lambda x: 1 - x, pred)))
# xgb.plot_tree(bst)
#xgb.plot_importance(bst,max_num_features=27)
#plt.show()

#0.8 0.9930984922684729
#

# print(-0.0389241911-0.0379365273-0.0336518772-0.0269767437)
# print(1/(1+np.exp(0.269767437)))
# print(1/(1+np.exp(0.0379365273)))
# print(1/(1+np.exp(0.0336518772)))
# print(1/(1+np.exp(0.0389241911)))