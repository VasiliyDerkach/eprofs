import json
import get_in_email_code
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

def manual_find_xpath_element(vdriver,element_config,timeout,**kwargs):
    tc = None
    pth = None
    #for xpth in element_config['xpaths']:
    flagnonstop = True
    while flagnonstop:
        flagx = True
        while flagx:
            xpth = input(f'Элемент {element_config['description']} не найден. Введите c - чтобы пропустить поиск или введите XPATH ')
            if xpth=='c':
                flagx =False
            else:
                try:
                    # if element_config['wait'] == 'WebDriverWait':
                    #     tc = WebDriverWait(vdriver, timeout).until(EC.presence_of_element_located((By.XPATH, xpth)))
                    # elif element_config['wait'] == '':
                    #     tc = vdriver.find_element(By.XPATH,xpth)
                    tc = vdriver.find_element(By.XPATH, xpth)
                    if tc:
                        pth = xpth
                        break
                except Exception as exs:
                    print(exs)

            if tc:
                if element_config['action']=='set_key':
                    tc.send_keys(kwargs[element_config['values'].replace('|','')])
                elif element_config['action'] == 'click':
                    tc.click()
                elif element_config['action'] == 'mouse_move':
                    act_mouse = ActionChains(vdriver)
                    act_mouse.move_to_element(tc).perform()
                asw = input('Если результат достигнут скопируйте xpath и cнажмите  c')
                if asw=='c':
                    flagnonstop = False

            else:
                print(f'Элемент {element_config['description']} по указанному xpath не найден')
def pars_webelement_byscn(vdriver,element_config,timeout,**kwargs):
    tc = None
    pth = None
    for xpth in element_config['xpaths']:
        try:
            if element_config['wait'] == 'WebDriverWait':
                tc = WebDriverWait(vdriver, timeout).until(EC.presence_of_element_located((By.XPATH, xpth)))
            elif element_config['wait'] == '':
                tc = vdriver.find_element(By.XPATH,xpth)
            if tc:
                pth = xpth
                break
        except Exception as exs:
            print(exs)
    if not tc:
        tc = manual_find_xpath_element(vdriver,element_config,timeout,**kwargs)
    elif tc:
        if element_config['action']=='set_key':
            try:
                tc.send_keys(kwargs[element_config['values'].replace('|','')])
            except Exception as e:
                print(e)
                print(f'Проблема с sen_key в {element_config['description']}')
                tc = manual_find_xpath_element(vdriver,element_config,timeout,**kwargs)
        elif element_config['action'] == 'click':
            try:
                tc.click()
            except Exception as e:
                print(e)
                print(f'Проблема с click в {element_config['description']}')
                tc = manual_find_xpath_element(vdriver,element_config,timeout,**kwargs)
        elif element_config['action'] == 'mouse_move':
            act_mouse = ActionChains(vdriver)
            act_mouse.move_to_element(tc).perform()
def pars_webelements_stage_byscn(vdriver,pars_config,stage,**kwargs):
    timeout = pars_config['minitimeout']

    for stp in pars_config['scenario']:
        if stp['stage']==stage:
            pars_webelement_byscn(vdriver, stp, timeout, **kwargs)


def login_with_emailcode(vdriver,login, password, email,email_key, parsing_config):

    cod_email_name = parsing_config['cod_email_name']
    cod_email_str0 = parsing_config['cod_email_str0']
    cod_email_str1 = parsing_config['cod_email_str1']
    cod_email_subject = parsing_config['cod_email_subject']
    cod_email_servicename = parsing_config['cod_email_servicename']
    now_timezone = parsing_config['now_timezone']
    imap_server = parsing_config['imap_server']
    in_mail_name = parsing_config['cod_email_name']
    priod_sec = parsing_config['priod_sec_for_email']
    count_return = parsing_config['count_return_email']
    psw_mail = email_key
    timeout = parsing_config['timeout']
    mtimeout = parsing_config['minitimeout']
    pars_webelements_stage_byscn(vdriver, parsing_config, 'login', login=login)
    eml = []
    j = 0
    while True:
        eml = get_in_email_code(imap_server, email, in_mail_name, psw_mail, priod_sec, now_timezone)
        j += 1
        if eml:
            ocode = eml[3]
            break
        if j>count_return:
            break
    if ocode:
        print(ocode)
if __name__=='__main__':
    with open("vkont_msg.json", "r") as rvkfile:
        site_ifo = json.load(rvkfile)
    print(site_ifo)
    print(site_ifo['scenario'][0]['xpaths'][0])
    driver = Chrome()
    driver.implicitly_wait(10)
    driver.get("https://vk.com/im?sel=876652489")
    driver.maximize_window()
    e_mail = 'profsadokate@mail.ru'
    login_with_emailcode(driver,e_mail, 'Htpbcnfyc!cJghjnbdktybt2', e_mail,'BpKrex5kd9pv82aai5FW', site_ifo)
    p = input('*')
    driver.quit()