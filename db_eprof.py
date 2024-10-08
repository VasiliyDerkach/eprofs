import datetime
import re
import uuid
import os
import shutil
import ftplib
import pymysql
temp_tabl = {}
def is_valid_uuid(uuid_to_test, version=None):
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version).urn
    except ValueError:
        return False
    flag = uuid_obj.upper().find(uuid_to_test.upper())>0
    #print(uuid_obj,uuid_to_test)
    return flag
def load_cnf_file(filename,cnf_list):
    with open(filename, mode='r') as cfile:
        txt = cfile.read()
        allfind = False
        for y,p in cnf_list.items():
            po = re.search('(?<='+y+').*?(?=\n)', txt)
            pp = po.group(0)
            if not po:
                allfind = False
                print(f'Не определен путь к {y}')
            else:
                allfind = True
                cnf_list[y] = pp
                print(y,pp)
                if not os.path.exists(pp) and y.find('path_')==0:
                    allfind = False
                    print(f'Папки {pp} не существует или к ней нет доступа')
                else:
                    print(f'Параметр {y} обнаружен {pp}')
    return {'file': cfile,'allfind': allfind,'config':cnf_list}
def get_city_id_in_db(cursor,tablename,cityname,id_reg):
    if tablename in temp_tabl:
        if cityname in temp_tabl[tablename]:
            return temp_tabl[tablename][cityname]['id'],temp_tabl[tablename][cityname]['parent_id'],1
    if cursor and id_reg and len(id_reg)>0:
        citynm = cityname.split(' ')
        if tablename=='cities':
            cname = cityname[len(citynm[0]):len(cityname)]+' '+citynm[0][0]
        elif tablename in ('regions','municipals'):
            cname = cityname.replace('.','')
        cname = cname.strip()
        sq = f"select id,parent_id from {tablename} where locate('{id_reg}',parent_id)=1 and locate(upper('{cname}'),upper(name))=1"
        cursor.execute(sq)
        lst = cursor.fetchall()
        llst = len(lst)
        if not llst>0:
            #citynm.sort(key= lambda cit:(len(cit),cit))
            for i,ncit in enumerate(citynm):
                sq = f"select id,parent_id from {tablename} where locate('{id_reg}',parent_id)=1 and locate(upper('{ncit}'),upper(name))=1"
                cursor.execute(sq)
                lst = cursor.fetchall()
                llst = len(lst)
                if llst==1:
                    break

        if llst > 0:
            if llst == 1:
                rez = {'id': lst[0]['id'], 'parent_id': lst[0]['parent_id']}
                temp_tabl[tablename] = {cityname: rez}
            return lst[0]['id'], lst[0]['parent_id'], llst
        else:
            return None,None,None
def getnull_db_path_config():
     return  {'path_scan=': None,
                   'path_read_scan=': None,
                   'path_error_uuid=': None,
                   'path_error_finddoc=': None,
                   'path_after_read=': None,
                   'ftp_server=': None,
                   'ftp_login=': None,
                   'ftp_password=': None,
                   'ftp_dir=': None,
                   'sql_server=': None,
                   'sql_login=': None,
                   'sql_password=': None,
                   'sql_basename=': None,
                   'sql_port=': None,
                   'ftp_bat=': None,
                   'path_after_end=': None}

if __name__=='__main__':
    path_config = getnull_db_path_config()
    cnf_dict = load_cnf_file('load_crm-config.cnf', path_config)
    allfind = cnf_dict['allfind']
    cfile = cnf_dict['file']
    path_config = cnf_dict['config']
    cur = None
    try:
        cnx = pymysql.connect(user=path_config['sql_login='], password=path_config['sql_password='],
                              host=path_config['sql_server='], port=3306,  # path_config['sql_port='],
                              database=path_config['sql_basename='], cursorclass=pymysql.cursors.DictCursor)

        cur = cnx.cursor()
    except Exception as Exsql:
        print(Exsql)
    # if cur:
    #     print(get_city_id_in_db(cur,'cities','город Екатеринбург','66'))
    #     print(temp_tabl)
