import parsing_table_xpath
import db_eprof
import datetime
import re
import uuid
import os
import shutil
import ftplib
import pymysql
import uuid

if __name__=='__main__':
    url = 'http://oblsud.svd.sudrf.ru/modules.php?name=sud'
    xp = '/html/body/div[10]/div[3]/div/div[2]/div[2]/a[1]'
    conts = {xp:{'MainLink':'/html/body/div[10]/div[3]/div/div[2]/table/tbody/tr[6]/td[2]/table/tbody/tr[{index}]/td[2]',
                     'Fields':[('name','/a','str'),('email','/table/tbody/tr/td/ul/li[3]','e-mail'),
                               ('legal_street','/table/tbody/tr/td/ul/li[1]','adress'),
                               ('phone_office','/table/tbody/tr/td/ul/li[2]','phone7'),
                               ('website','/table/tbody/tr/td/ul/li[4]','link')]}
             }
    id_up ='69241fc6-28ad-fb9f-9a07-51ea53b16d27'
    id_tm = '6dbad3e5-04d7-d9d7-0a2f-52e73c92b7b3'
    # ключ conts имя html закладки на сайте на которую надо переходить перед считыванием таблицы, если он None
    # значит страница сайта без закладок
    dr, tb = parsing_table_xpath.parsing_table_xpath(None,url, conts, start_row=1,timeout = 25)
    dr.quit()
    path_config = db_eprof.getnull_db_path_config()
    cnf_dict = db_eprof.load_cnf_file('load_crm-config.cnf', path_config)
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
    ctabl = tb[xp]
    for crt in ctabl:
        wb = crt['website'].replace('http://', '')
        wb = wb.replace('https://', '')
        #sq = f"select id from accounts where deleted=0 and website='{wb}' and account_as_parent_child_id='{id_up}' order by date_modified desc"
        sq = f"select id from accounts where deleted=0 and website='{wb}' order by date_modified desc"
        #print(sq)
        cur.execute(sq)
        lst = cur.fetchall()
        id_reg = db_eprof.get_city_id_in_db(cur, 'regions', crt['legal_street'][1], '1')
        id_reg = id_reg[0]
        id_cit = db_eprof.get_city_id_in_db(cur, 'cities', crt['legal_street'][2], id_reg[:2])
        id_munic = id_cit[1]
        id_cit = id_cit[0]
        llst = len(lst)
        if not llst>0:
            uu_id = uuid.uuid4().urn.replace('urn:uuid:', '')
            dnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            sqli = f'insert into accounts (id,date_entered,date_modified,name,legal_entity_name,account_as_parent_child_id,type,phone_office,'
            sqli = sqli + f"industry,assigned_team_id,legal_country_id,actual_country_id,legal_region_id,actual_region_id,legal_municipal_id,"
            sqli = sqli + f"actual_municipal_id,legal_city_id,actual_city_id,legal_street,actual_street,legal_house,actual_house,"
            sqli = sqli + f"legal_postalcode,actual_postalcode,website) values('{uu_id}','{dnow}','{dnow}','{crt['name']}','{crt['name']}',"
            sqli = sqli + f"'{id_up}','court','{crt['phone_office']}','court1','{id_tm}','1','1','{id_reg}','{id_reg}','{id_munic}','{id_munic}',"
            sqli = sqli + f"'{id_cit}',{id_cit}','{crt['legal_street'][3]}','{crt['legal_street'][3]}','{crt['legal_street'][4]}','{crt['legal_street'][4]}',"
            sqli = sqli + f"'{crt['legal_street'][0]}','{crt['legal_street'][0]}','{wb}'"
            s = f"call SetEmailContact('{uu_id}','{crt['email']}','1')"
            # print(sqli)
            # print(s)
        else:
            print(f'Найден {crt}')
            s1 = f"select name, legal_entity_name,phone_officeassigned_team_id,legal_country_id,actual_country_id,legal_region_id,"
            s1 = s1 + f"actual_region_id,legal_municipal_id,actual_municipal_id,legal_city_id,actual_city_id,legal_street,actual_street,"
            s1 = s1 + f"legal_house,actual_house,legal_postalcode,actual_postalcode from accounts where id='{lst[0]['id']}'"
            cur.execute(sq)
            lst_f = cur.fetchall()
            for k,v in lst_f[0]:
                print(k,v)
    cur.close()
    cnx.close()