import datetime
import re
import uuid
import os
import shutil
import ftplib
import pymysql
def is_valid_uuid(uuid_to_test, version=None):
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version).urn
    except ValueError:
        return False
    flag = uuid_obj.upper().find(uuid_to_test.upper())>0
    #print(uuid_obj,uuid_to_test)
    return flag
if __name__=='__main__':
    try:
        cnx = pymysql.connect(user=path_config['sql_login='], password=path_config['sql_password='],
                              host=path_config['sql_server='], port=3306,  # path_config['sql_port='],
                              database=path_config['sql_basename='], cursorclass=pymysql.cursors.DictCursor)

        cur = cnx.cursor()
    except Exception as Exsql:
        print(Exsql)
    if cur:
        pass