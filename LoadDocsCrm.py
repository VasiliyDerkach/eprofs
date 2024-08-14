import re
import uuid
import os
import shutil
import ftplib
import mysql.connector

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
            'sql_basename=': None
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
                if not os.path.exists(p):
                    allfind = False
                    print(f'Папки {p} не существует или к ней нет доступа')
                else:
                    print(f'Папка {p} обнаружена')

    if not cfile:
        print('Не найден файл load_crm-config.cnf')
    elif allfind:
        i,j,g = 0,0,0
        cnx = mysql.connector.connect(user=path_config['sql_login='], password=path_config['sql_password='],
                                      host=path_config['sql_server='],
                                      database=path_config['sql_basename='])
        if not cnx:
            print('Ошибка соединения с сервером sql')
        lst_scan = os.listdir(path_config['path_scan='])
        for gfile in lst_scan:
            if gfile[-4:] in ('.jpg','.pdf','.png') and gfile[0:1]!='==':
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
                        if str1[36,38]=='--':
                            pg = str1[38:len(str1)]
                        uu_id = uuid.uuid4()
                    else:
                        shutil.move(path_config['path_scan=']+gfile,path_config['path_error_uuid=']+gfile)
                        shutil.move(path_config['path_read_scan=']+file_r,path_config['path_error_uuid=']+file_r)


                else:
                    print(f'Для файла {gfile} не найден файл распозонования')
                    os.rename(path_config['path_scan='] + gfile,path_config['path_scan='] + '==' + gfile)
        print(f'В папке {path_config['path_scan=']} найдено {i} графических файла.\n Из них для {i-j} не найдено файлов распознования')
        print(f'Для {j-g} файлов не распознан id документа')
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
    # set
    # exx = right(newname, 4);
    # insert
    # into
    # document_revisions(id, date_entered, change_log, document_id, filename, file_ext, file_mime_type, stage)
    # values(ids, now(), if (s1 is null or s1='', if (iddocp is null, 'Скан с email', iddocp), concat('стр.',
    #                                                                                                 s1)), iddocp, fname,
    # case
    # exx
    # when
    # '.pdf'
    # then
    # 'pdf'
    # when
    # '.jpg'
    # then
    # 'jpg'
    # end,
    # case
    # exx
    # when
    # '.pdf'
    # then
    # 'image/pdf'
    # when
    # '.jpg'
    # then
    # 'image/jpeg'
    # end, 'scaninmail');
