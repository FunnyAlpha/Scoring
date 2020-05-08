
# Auhorization to db (oracle)
class Auhorization:
    def __str__(self):

        v_user_name = 'gp_blaze_uwi'
        v_user_password = 'Fender1580'
        v_db_name = 'db19c'
        v_con_name = v_user_name+'/'+v_user_password+'@'+v_db_name

        return v_con_name

# sql_query from db
class Credit_bureau_data_mart:
    def __str__(self):

        v_sql_query = 'select * from gp_blaze_uwi.sm_sco_bureau_tab'

        return v_sql_query