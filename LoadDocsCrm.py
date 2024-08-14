import re
import uuid
import os
import ftplib
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
            'path_after_read=': None}
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
        i = 0
        lst_scan = os.listdir(path_config['path_scan='])
    # uuidtest = 'c6f66f3c-eb06-ecda-8d22-66bb47328469'
    # print(len(uuidtest))
    # print(is_valid_uuid(uuidtest))
    # print(lst_scan)
    # for f in lst_scan:
    #     print(f,f[-4:])
    # result = re.search('(?<=Path=).*?(?=\n)', 'Path=D:/yand/\n')
    # print(result.group(0) if result else "Текст между маркерами не найден.")