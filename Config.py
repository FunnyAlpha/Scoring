
# Auhorization to db (oracle)
class Auhorization:
    def __str__(self):

        v_user_name = 'gp_blaze_uwi'
        v_user_password = 'Fender1580'
        v_db_name = 'db19c'
        v_con_name = v_user_name+'/'+v_user_password+'@'+v_db_name

        return v_con_name

# sql_query from db
# CREDIT BUREAU DATA - f_credit_bureau_tt #source "dm"
class f_credit_bureau_tt_cb:
    def __str__(self):

        v_sql_query = 'select * from gp_blaze_uwi.sm_sco_bureau_tab'

        return v_sql_query

# APPLICATION DATA - f_scoring_vector_tt #source "vct"
class f_scoring_vector_tt_app:
    def __str__(self):

        v_sql_query = '''select --+ parallel(8)
        v.sk_application, v.sk_date_decision, v.sk_contract_type,
        max(case when skp_vector_attribute =   9221  then  num_value  end) as  amtCreditDpd30  ,
        max(case when skp_vector_attribute =   4113  then  dtime_value  end) as dateLastDpd30  ,
        max(case when skp_vector_attribute =   469  then  num_value  end) as  maxDpdTol  ,
        max(case when skp_vector_attribute =   4576  then  num_value  end) as  maxDpdTolNotRD_60m  ,
        max(case when skp_vector_attribute =   190  then  num_value  end) as  maxDpdTol6m  ,
        nvl(max(case when skp_vector_attribute =   430  then  num_value  end), max(case when skp_vector_attribute =   414 /*413*/  then  num_value  end)) as  actualDpdTolerance,
        max(case when skp_vector_attribute =   4112  then  num_value  end) as  amtDpd30Ever,
        max(case when skp_vector_attribute =   33  then  dtime_value  end) as  "SYSDATE",
        max(case when skp_vector_attribute =   492  then  dtime_value  end) as  birth,
        max(case when skp_vector_attribute =   3887  then  char_value  end) as  lasteducation,
        max(case when skp_vector_attribute =   196  then  char_value  end) as  education
        from f_scoring_vector_tt v 
        where v.skp_vector_attribute in (9221, 469, 4804, 4576, 190, 430, 414, 4112,7770,4113,33,492,3887,196 )
        group by v.sk_application, v.sk_date_decision, v.sk_contract_type'''

        return v_sql_query

# CREDIT BUREAU DATA - f_scoring_vector_tt #source "vct"
class f_scoring_vector_tt_cb:
    def __str__(self):

        v_sql_query = '''select
        v.sk_application, v.sk_date_decision, v.sk_contract_type,
        v.num_group_position,
        max(case when skp_vector_attribute =   3121  then  char_value  end) as  cbOverdueLine  ,
        max(case when skp_vector_attribute =   95  then  char_value  end) as  creditCurrency  ,
        max(case when skp_vector_attribute =   108  then  dtime_value  end) as  creditDate  ,
        max(case when skp_vector_attribute =   191  then  num_value  end) as  creditDayOverdue  ,
        max(case when skp_vector_attribute =   61  then  dtime_value  end) as  creditEndDate  ,
        max(case when skp_vector_attribute =   1081  then  num_value  end) as  creditJoint  ,
        max(case when skp_vector_attribute =   504  then  char_value  end) as  creditOwner  ,
        max(case when skp_vector_attribute =   425  then  num_value  end) as  creditSum  ,
        max(case when skp_vector_attribute =   277  then  num_value  end) as  creditSumDebt  ,
        max(case when skp_vector_attribute =   422  then  num_value  end) as  creditSumOverdue  ,
        max(case when skp_vector_attribute =   285  then  num_value  end) as  creditType  ,
        max(case when skp_vector_attribute =   7770  then  char_value  end) as creditTypeUni ,
        max(case when skp_vector_attribute =   335  then  dtime_value  end) as  creditEndDateFact  ,
        max(case when skp_vector_attribute =   152  then  num_value  end) as  creditMaxOverdue  ,
        max(case when skp_vector_attribute =   316  then  num_value  end) as  creditProlong,
        max(case when skp_vector_attribute =   1089  then  char_value  end) as  cbId
        from f_scoring_vector_tt v
        where v.skp_vector_attribute in (3121  ,95  ,108  ,191  ,61  ,1081  ,504  ,425  ,277  ,422  ,285  ,335, 152, 316, 7770,1089)
        group by v.sk_application, v.sk_date_decision, v.sk_contract_type,v.num_group_position'''

        return v_sql_query

# BEHAVIOUR DATA - f_scoring_vector_tt #source "vct"
class f_scoring_vector_tt_beh:
    def __str__(self):

        v_sql_query = '''select --+ parallel(8)
        v.sk_application, v.sk_date_decision, v.sk_contract_type,
        max(case when skp_vector_attribute =   4811  then  char_value  end) as  education
        from f_scoring_vector_tt v 
        where v.skp_vector_attribute in (4811)
        group by v.sk_application, v.sk_date_decision, v.sk_contract_type'''

        return v_sql_query

class blaze_vector_output:

    def __str__(self):

        file_name = 'sample_vector_cb.txt'

        return file_name        

        