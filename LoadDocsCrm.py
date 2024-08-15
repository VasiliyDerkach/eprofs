import re
import uuid
import os
import shutil
import ftplib
import pymysql
# path_scan=D:/SUI-Doc/sui-after-read/
# path_read_scan=D:/SUI-Doc/sui-txt/
# path_error_uuid=D:/SUI-Doc/err-uuid/
# path_error_finddoc=D:/SUI-Doc/err-fnddoc/
# path_after_read=
def is_valid_uuid(uuid_to_test, version=None):
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version).urn
    except ValueError:
        return False
    flag = uuid_obj.upper().find(uuid_to_test.upper())>0
    #print(uuid_obj,uuid_to_test)
    return flag
if __name__=='__main__':
    path_config = {'path_scan=': None,
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
            'sql_port=': None
    }
    with open('load_crm-config.cnf', mode='r') as cfile:
        txt = cfile.read()
        allfind = False
        for y,p in path_config.items():
            po = re.search('(?<='+y+').*?(?=\n)', txt)
            pp = po.group(0)
            if not po:
                allfind = False
                print(f'Не определен путь к {y}')
            else:
                allfind = True
                path_config[y] = pp
                print(y,pp)
                if not os.path.exists(pp) and y.find('path_')==0:
                    allfind = False
                    print(f'Папки {pp} не существует или к ней нет доступа')
                else:
                    print(f'Параметр {y} обнаружен {pp}')

    if not cfile:
        print('Не найден файл load_crm-config.cnf')
    elif allfind:
        i,j,g,nid = 0,0,0,0
        try:
            cnx = pymysql.connect(user=path_config['sql_login='], password=path_config['sql_password='],
                                      host=path_config['sql_server='],port=3306,  #path_config['sql_port='],
                                      database=path_config['sql_basename='],cursorclass=pymysql.cursors.DictCursor)

            cur = cnx.cursor()
        except Exception as Exsql:
            print(Exsql)

        ftpfile = ftplib.FTP()
        #ftpfile = ftplib.FTP_TLS()
        print('FTP запущен')
        #ftpfile.prot_p()
        on_ftp = False
        try:
            ftpfile.connect(path_config['ftp_server='],22,6)
            print('FTP соединение успешно')
            ftpfile.login(user=path_config['ftp_login='],passwd=path_config['ftp_password='])
            print('FTP аутификация пройдена')

            ftpfile.cwd(path_config['ftp_dir='])
            print('FTP переход в папку')
            on_ftp = True
        except Exception as excftp:
            on_ftp = False
            print('FTP нет соединения ',excftp)
            #ftpfile.quit()


        lst_scan = os.listdir(path_config['path_scan='])
        for gfile in lst_scan:
            exx = gfile[-4:]
            if exx in ('.jpg','.pdf','.png') and gfile[0:1]!='==':
                i += 1
                file_r = open(path_config['path_read_scan='] + gfile[0:-4]+'.txt',mode='r')
                if file_r:
                    j += 1
                    txt_id = file_r.read()
                    txt_id = txt_id.split('\n')
                    l = 0
                    for str in txt_id:
                        if len(str)>=36:
                            doc_id = str[0:36]
                            if is_valid_uuid(doc_id):
                                if len(str)>l:
                                    l = len(str)
                                    doc_id1= doc_id
                                    str1 = str
                    if l>0:
                        g += 1
                        pg= ''
                        if str1[36:38]=='--':
                            pg = str1[38:len(str1)]
                        cur.execute(f"select id from documents where id='{doc_id1}' limit 1")
                        id_lst = cur.fetchall()
                        id_rez=id_lst[0]['id']
                        if len(id_rez)>0 and id_rez.upper()==doc_id1.upper():
                            uu_id = uuid.uuid4()
                            old_fname = gfile
                            if exx in ('.jpg', '.pdf', '.png'):
                                exx0 = exx.replace('.','')
                                exx1 = 'image/jpeg' if exx=='.jpg' else 'image/pdf' if exx == '.pdf' else 'image/png' if exx == '.png' else exx
                            else:
                                exx0, exx1 = '',''
                            pg1 = f'стр.{pg}'
                            os.rename(path_config['path_scan=']+gfile,path_config['path_scan=']+uu_id)
                            sql_ins = f'insert into document_revisions(id, date_entered, change_log, document_id, '
                            sql_ins += f'filename, file_ext, file_mime_type, stage)) values('
                            sql_ins += f"{uu_id},now(),{pg1 if pg!='' else ''},{doc_id1},{old_fname},{exx0},{exx1},'scan in pyth'"
                            cur.execute(sql_ins)
                            if on_ftp:
                                with open(path_config['path_scan=']+uu_id,'rb') as gfile_n:
                                    ftpfile.storbinary('STOR ' +uu_id,gfile_n)

                        else:
                            nid += 1
                            shutil.move(path_config['path_scan=']+gfile,path_config['path_error_finddoc=']+gfile)
                            shutil.move(path_config['path_read_scan=']+file_r,path_config['path_error_finddoc=']+file_r)
                    else:
                        shutil.move(path_config['path_scan=']+gfile,path_config['path_error_uuid=']+gfile)
                        shutil.move(path_config['path_read_scan=']+file_r,path_config['path_error_uuid=']+file_r)
                    file_r.close()

                else:
                    print(f'Для файла {gfile} не найден файл распозонования')
                    os.rename(path_config['path_scan='] + gfile,path_config['path_scan='] + '==' + gfile)
        print(f'В папке {path_config['path_scan=']} найдено {i} графических файла.\n')
        if i>j:
              print(f'Из них для {i-j} не найдено файлов распознования')
        if j>g:
            print(f'Для {j-g} файлов не распознан id документа')
        if g>nid:
            print(f'Для {g-nid} файлов не найден в БД документ с нужным id или такой документ был удален из БД')
        if on_ftp:
            ftpfile.quit()
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
