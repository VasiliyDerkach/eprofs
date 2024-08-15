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
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test
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
            p = po.group(0)
            if not po:
                allfind = False
                print(f'Не определен путь к {y}')
            else:
                allfind = True
                print(y,p)
                if not os.path.exists(p) and y.find('path_')==0:
                    allfind = False
                    print(f'Папки {p} не существует или к ней нет доступа')
                else:
                    print(f'Параметр {y} обнаружен {p}')

    if not cfile:
        print('Не найден файл load_crm-config.cnf')
    elif allfind:
        i,j,g,nid = 0,0,0,0
        cnx = pymysql.connect(user=path_config['sql_login='], password=path_config['sql_password='],
                                      host=path_config['sql_server='],port=3306,  #path_config['sql_port='],
                                      database=path_config['sql_basename='],cursorclass=pymysql.cursors.DictCursor)
        if not cnx:
            print('Ошибка соединения с сервером sql')
        else:
            cur = cnx.cursor()
        ftpfile = ftplib.FTP(path_config['ftp_server='])
        ftpfile.login(user=path_config['ftp_login='],passwd=path_config['ftp_password='])
        ftpfile.cwd(path_config['ftp_dir='])
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
                        if str1[36,38]=='--':
                            pg = str1[38:len(str1)]
                        cur.execute(f"select id from documents where id='{doc_id1}' limit 1")
                        id_lst = cur.fetchall()
                        id_rez=id_lst[0]
                        if len(id_rez)>0 and id_rez==doc_id1:
                            uu_id = uuid.uuid4()
                            old_fname = gfile
                            if exx in ('.jpg', '.pdf', '.png'):
                                exx0 = exx.replace('.','')
                                exx1 = 'image/jpeg' if exx=='.jpg'
                                exx1 = 'image/pdf' if exx == '.pdf'
                                exx1 = 'image/png' if exx == '.png'
                            else:
                                exx0, exx1 = '',''
                            pg1 = f'стр.{pg}'
                            os.rename(path_config['path_scan=']+gfile,path_config['path_scan=']+uu_id)
                            sql_ins = f'insert into document_revisions(id, date_entered, change_log, document_id, '
                            sql_ins += f'filename, file_ext, file_mime_type, stage)) values('
                            sql_ins += f"{uu_id},now(),{pg1 if pg!='' },{doc_id1},{old_fname},{exx0},{exx1},'scan in pyth'"
                        else:
                            nid += 1
                            shutil.move(path_config['path_scan=']+gfile,path_config['path_error_finddoc=']+gfile)
                            shutil.move(path_config['path_read_scan=']+file_r,path_config['path_error_finddoc=']+file_r)
                    else:
                        shutil.move(path_config['path_scan=']+gfile,path_config['path_error_uuid=']+gfile)
                        shutil.move(path_config['path_read_scan=']+file_r,path_config['path_error_uuid=']+file_r)


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
