import datetime
import re
import uuid
import os
import shutil
import ftplib
import pymysql
import LoadDocsCrm

if __name__=='__main__':
    path_config = {'path_scan=': None,

            'path_error_uuid=': None,
            'path_error_finddoc=': None,
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
            'path_after_end=': None,
            'exe_doc_status=': None,
            'rtf_str_end=': None,
            'rtf_str_start_num=': None,
            'rtf_str_start_date=': None,
            'rtf_str_start_sum=': None,
            'rtf_nstr_num=': None,
            'rtf_nstr_date=': None,
            'rtf_nstr_sum=': None,
            'path_after_find=': None
    }
    cnf_dict = LoadDocsCrm.load_cnf_file('load_plat_config.cnf',path_config)
    allfind = cnf_dict['allfind']
    cfile = cnf_dict['file']
    path_config = cnf_dict['config']

    if not cfile:
        print('Не найден файл cnf')
    elif allfind:
        i,j,g,nid = 0,0,0,0
        exestatus = path_config['exe_doc_status=']

        try:
            cnx = pymysql.connect(user=path_config['sql_login='], password=path_config['sql_password='],
                                      host=path_config['sql_server='],port=3306,  #path_config['sql_port='],
                                      database=path_config['sql_basename='],cursorclass=pymysql.cursors.DictCursor)

            cur = cnx.cursor()
        except Exception as Exsql:
            print(Exsql)

        #ftpfile = ftplib.FTP()
        #ftpfile = ftplib.FTP_TLS()
        #print('FTP запущен')
        #ftpfile.prot_p()
        # on_ftp = False
        # try:
        #     ftpfile.connect(path_config['ftp_server='],22,6)
        #     print('FTP соединение успешно')
        #     ftpfile.login(user=path_config['ftp_login='],passwd=path_config['ftp_password='])
        #     print('FTP аутификация пройдена')
        #
        #     ftpfile.cwd(path_config['ftp_dir='])
        #     print('FTP переход в папку')
        #     on_ftp = True
        # except Exception as excftp:
        #     on_ftp = False
        #     print('FTP нет соединения ',excftp)
            #ftpfile.quit()


        lst_scan = os.listdir(path_config['path_scan='])
        for gfile in lst_scan:
            exx = gfile[-4:]
            old_fname = gfile
            if exx in ('.rtf','.pdf') and gfile[0:2]!='==':
                # для pdf учеть другие теги данных платежким и перенести теги для каждого типа файла в config
                i += 1
                txtfile_name = gfile
                txtfile_name_path = path_config['path_scan='] + txtfile_name
                if exx=='.rtf':
                    nstr_date = int(path_config['rtf_nstr_date='])
                    str_start_dat = path_config['rtf_str_start_date=']
                    nstr_sum = int(path_config['rtf_nstr_sum='])
                    str_start_sum = path_config['rtf_str_start_sum=']
                    nstr_num = int(path_config['rtf_nstr_num='])
                    str_start_num = path_config['rtf_str_start_num=']
                elif exx=='.pdf':
                    pass
                try:
                    file_r = open(txtfile_name_path,mode='r')
                except Exception as exftxt:
                    print(f'При открытии файла {txtfile_name_path} произошла ошибка {exftxt}')
                    file_r = None
                if file_r:
                    j += 1
                    str_end = path_config['rtf_str_end=']
                    if exx in ('.pdf', '.rtf'):
                        exx0 = exx.replace('.', '')
                        exx1 = 'doc/rtf' if exx == '.rtf' else 'image/pdf' if exx == '.pdf' else exx
                        # doc/rtf посмотреть как в crm
                    else:
                        exx0, exx1 = '', ''

                    txt_id = file_r.read()
                    file_r.close()
                    #print(txt_id)
                    txt_id = txt_id.replace('[', 'id_doc=')
                    txt_id = txt_id.replace(']', '=id_doc')
                    doc_id = re.search('(?<=id_doc=).*?(?==id_doc)', txt_id)
                    if doc_id:
                        doc_id = doc_id.group(0)
                        if len(doc_id) == 36:
                            print('doc_id=', doc_id)
                            if LoadDocsCrm.is_valid_uuid(doc_id):
                                print(f'Валидный {doc_id}')
                                cur.execute(f"select id,stage,date_sign from documents where id='{doc_id}' limit 1")
                                id_lst = cur.fetchall()
                                id_rez=id_lst[0]['id']
                                if len(id_rez)>0 and id_rez.upper()==doc_id.upper():
                                    uu_id = uuid.uuid4().urn.replace('urn:uuid:','').upper()
                                    try:
                                        os.rename(path_config['path_scan=']+gfile,path_config['path_scan=']+uu_id)
                                    except Exception as ex:
                                        print(f'При переименовании файла {gfile} возникла ошибка {ex}' )
                                    dnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    sql_ins = f"insert into document_revisions(id, date_entered,  document_id, filename, file_ext, file_mime_type, stage) values('{uu_id}','{dnow}','{doc_id}','{old_fname}','{exx0}','{exx1}','scan in pyth')"
                                    try:
                                        cur.execute(sql_ins)
                                        cnx.commit()
                                    except:
                                        cnx.rollback()
                                    try:
                                        shutil.move(path_config['path_scan='] + uu_id,
                                                path_config['path_after_find='] + uu_id)
                                    except Exception as ex:
                                        print(f'При переносе файла {gfile} возникла ошибка {ex}' )
                                    txt = txt_id.split('\n')
                                    #print(txt[17])
                                    txt17 = txt[nstr_date].replace('\\','~')
                                    pdata = re.search(f'(?<={str_start_dat}).*?(?={str_end})', txt17)
                                    if pdata:
                                        pdata = pdata.group(0)
                                    print(pdata)
                                    pdata.replace(' ','')
                                    pdata = pdata[-10:]
                                    date1 = pdata[-4:]+'-'+pdata[3:5]+'-'+pdata[0:2]
                                    txt19 = txt[nstr_num].replace('\\','~')
                                    #print(txt19)
                                    pnum = re.search(f'(?<={str_start_num}).*?(?={str_end})', txt19)
                                    if pnum:
                                        pnum = pnum.group(0)
                                    print(pnum)
                                    txt119 = txt[nstr_sum].replace('\\','~')
                                    #print(txt19)
                                    psum = re.search(f'(?<={str_start_sum}).*?(?=={str_end})', txt119)
                                    if psum:
                                        psum = psum.group(0)
                                    print(psum)
                                    sql_upd = f"update documents set document_number='{pnum}',date_sign='{date1}', stage='{exestatus}', attachment_number='{psum}' where deleted =0 and (document_as_business_id= '{id_rez}' or id='{id_rez}')"
                                    try:
                                        cur.execute(sql_upd)
                                        cnx.commit()
                                    except:
                                        cnx.rollback()
                                    os.startfile(path_config['ftp_bat='])
                                    print(f'Запущен файл {path_config['ftp_bat=']}')
                                    #shutil.move(path_config['path_after_find=']+uu_id,path_config['path_after_end=']+uu_id)

                                #print(txt[19])
                                #print(txt[119])

                    else:
                        shutil.move(txtfile_name_path,path_config['path_error_uuid=']+txtfile_name)


                else:
                    print(f'Файл {gfile} не найден')
                    os.rename(path_config['path_scan='] + gfile,path_config['path_scan='] + '==' + gfile)
        print(f'В папке {path_config['path_scan=']} найдено {i} файла.\n')
        if i>j:
              print(f'Из них для {i-j} не найдена директория')
        if j>g:
            print(f'Для {j-g} файлов не распознан id документа')
        if nid>0:
            print(f'Для {nid} файлов не найден в БД документ с нужным id или такой документ был удален из БД')
        # if on_ftp:
        #     ftpfile.quit()
        cur.close()
        cnx.close()
    # h = 'tytyty.jpg'
    # print(h[0:-4])
    # uuidtest = 'c6f66f3c-eb06-ecda-8d22-66bb47328469--'
    # print(uuidtest[36:38],'___',uuidtest[38:len(uuidtest)])
    # print(len(uuidtest))
    # print(is_valid_uuid(uuidtest))
    # print(lst_scan)
    # for f in lst_scan:
    #     print(f,f[-4:])
    # result = re.search('(?<=Path=).*?(?=\n)', 'Path=D:/yand/\n')
    # print(result.group(0) if result else "Текст между маркерами не найден.")
