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
        sq = f"select id from accounts where deleted=0 and website like '%{wb}%' order by date_modified desc"
        # if crt['website']=='http://oktiabrsky.svd.sudrf.ru':
        #     print(sq)
        cur.execute(sq)
        lst = cur.fetchall()
        id_reg = db_eprof.get_city_id_in_db(cur, 'regions', crt['legal_street'][1], '1')
        id_reg = id_reg[0]
        id_cit = db_eprof.get_city_id_in_db(cur, 'cities', crt['legal_street'][2], id_reg[:2])
        id_munic = id_cit[1]
        id_cit = id_cit[0]
        llst = len(lst)
        s = None
        if not llst>0:
            uu_id = uuid.uuid4().urn.replace('urn:uuid:', '')
            dnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            sqli = f'insert into accounts (id,date_entered,date_modified,name,legal_entity_name,account_as_parent_child_id,type,phone_office,'
            sqli = sqli + f"industry,assigned_team_id,legal_country,actual_country,legal_region,actual_region,legal_municipal,"
            sqli = sqli + f"actual_municipal,legal_city,actual_city,legal_street,actual_street,legal_house,actual_house,"
            sqli = sqli + f"legal_postalcode,actual_postalcode,website) values('{uu_id}','{dnow}','{dnow}','{crt['name']}','{crt['name']}',"
            sqli = sqli + f"'{id_up}','court','{crt['phone_office']}','court1','{id_tm}','1','1','{id_reg}','{id_reg}','{id_munic}','{id_munic}',"
            sqli = sqli + f"'{id_cit}','{id_cit}','{crt['legal_street'][3]}','{crt['legal_street'][3]}','{crt['legal_street'][4]}','{crt['legal_street'][4]}',"
            sqli = sqli + f"'{crt['legal_street'][0]}','{crt['legal_street'][0]}','{wb}')"
            s = f"call SetEmailContact('{uu_id}','{crt['email']}','1')"
            # print(sqli)
            # print(s)
        else:
            print(f'Найден {crt}')
            # s1 = f"select name, legal_entity_name,phone_office,assigned_team_id,legal_country_id,actual_country_id,legal_region_id,"
            # s1 = s1 + f"actual_region_id,legal_municipal_id,actual_municipal_id,legal_city_id,actual_city_id,legal_street,actual_street,"
            # s1 = s1 + f"legal_house,actual_house,legal_postalcode,actual_postalcode from accounts where id='{lst[0]['id']}'"
            # s1 = f"select * from accounts where id='{lst[0]['id']}'"
            # cur.execute(s1)
            # lst_f = cur.fetchall()
            sqli = f"update accounts set date_modified='{dnow}',name=if(name is null or name='','{crt['name']}',name),legal_entity_name='{crt['name']}'"
            sqli = sqli + f",account_as_parent_child_id='{id_up}',type='court',phone_office='{crt['phone_office']}',industry='court1'"
            sqli = sqli + f",assigned_team_id='{id_tm}',legal_country='1',actual_country='1',legal_region='{id_reg}',actual_region='{id_reg}'"
            sqli= sqli + f",legal_municipal='{id_munic}',actual_municipal='{id_munic}',legal_city='{id_cit}',actual_city='{id_cit}'"
            sqli = sqli + f",legal_street='{crt['legal_street'][3]}',actual_street='{crt['legal_street'][3]}'"
            sqli = sqli + f",legal_house='{crt['legal_street'][4]}',actual_house='{crt['legal_street'][4]}',legal_postalcode='{crt['legal_street'][0]}',actual_postalcode='{crt['legal_street'][0]}',website='{wb}' "
            sqli= sqli+ f"where id='{lst[0]['id']}'"
            # for k,v in lst_f[0].items():
            #     print(k,v)
        try:
            cur.execute(sqli)
            cnx.commit()
            if s:
                try:
                    cur.execute(s)
                    cnx.commit()
                    print(f'Выполнено  email для {crt['name']}')
                except Exception as e:
                    cnx.rollback()
                    print(f'Ошибка email {e} для {crt['name']}')


            print(f'Выполнено {'insert' if s else 'update'} для {crt['name']}')
        except Exception as e:
            cnx.rollback()
            print(f'Ошибка  {e} в {'insert' if s else 'update'} для {crt['name']}')
            print(sqli)


    cur.close()
    cnx.close()