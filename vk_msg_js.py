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
            elif element_config['wait']=='Wait_to_be_clickable':
                try:
                    tc = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpth )))
                except Exception as e:
                    print(e)
                    print(f'Проблема с кликабельностью или наличием элемента в {element_config['description']}')
                    tc = manual_find_xpath_element(vdriver, element_config, timeout, **kwargs)
            if tc:
                pth = xpth

                break
        except Exception as exs:
            print(exs)
    if not tc:
        tc = manual_find_xpath_element(vdriver,element_config,timeout,**kwargs)
    if tc:
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
        elif element_config['action'] == 'print':
            if tc.is_displayed():
                print(element_config['values'], tc.get_property('text_length'), tc.get_property('name'))

        elif element_config['action']=='set_key_iter':
            #ans = input('Введите разовый ключ ВК ')
            ans = kwargs['onecode']
            itr_xpath = element_config['xpath_iter']
            for l, a in enumerate(ans):
                ph = itr_xpath.replace('|number|',str(l+1))
                #ph = f'/html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[2]/div/div[|number|]/div/div/input'
                try:
                    chr = driver.find_element(By.XPATH, ph)
                    chr.send_keys(a)
                except Exception as e:
                    print(e)
                    print(f'Проблема с итеррационным set_key в {element_config['description']}')
                    tc = manual_find_xpath_element(vdriver, element_config, timeout, **kwargs)
        return True
    else:
        return False

def pars_webelements_stage_byscn(vdriver,pars_config,stage,**kwargs):
    timeout = pars_config['minitimeout']
    rez =False
    for stp in pars_config['scenario']:
        if stp['stage']==stage:
            aa = pars_webelement_byscn(vdriver, stp, timeout, **kwargs)
            rez = rez and aa
    return rez


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
    eml = get_in_email_code.get_in_email_code(imap_server, email, in_mail_name, psw_mail, priod_sec, now_timezone)
    flaglogin = pars_webelements_stage_byscn(vdriver, parsing_config, 'login', login=login)
    print(f'Этап login {flaglogin}')
    eml = []
    j = 0
    ocode = None
    while True:
        eml = get_in_email_code.get_in_email_code(imap_server, email, in_mail_name, psw_mail, priod_sec, now_timezone)
        j += 1
        if eml:
            if eml[0]==parsing_config['notify_email']:
                ocode = eml[3]
                break
        if j>count_return:
            break
    if ocode:
        print(ocode)
        aa = pars_webelements_stage_byscn(vdriver, parsing_config, 'after_login', onecode=ocode, password= password)
        flaglogin = flaglogin and aa
        print(f'Этап after_login {aa}')
        aa = pars_webelements_stage_byscn(vdriver, parsing_config, 'after_authentific')
        flaglogin = flaglogin and aa
        print(f'Этап after_authentific {aa}')
        return flaglogin
    else:
        return False
def send_vk_message_xpath(vdriver, parsing_config,user_vk_id,text_message):
    messager_url = parsing_config['messager_url']
    driver.get(messager_url+user_vk_id)
    flaglogin = pars_webelements_stage_byscn(vdriver, parsing_config, 'is_user_block')

if __name__=='__main__':
    with open("vkont_msg.json", "r") as rvkfile:
        site_ifo = json.load(rvkfile)
    print(site_ifo)
    print(site_ifo['scenario'][0]['xpaths'][0])
    driver = Chrome()
    driver.implicitly_wait(10)
    driver.get("https://vk.com/")
    driver.maximize_window()
    e_mail = 'profsadokate@mail.ru'
    #profsadokate1@mail.ru
    # AT5wRMu4jWEk79jTumuH
    g = login_with_emailcode(driver,e_mail, 'Htpbcnfyc!cJghjnbdktybt2', e_mail,'BpKrex5kd9pv82aai5FW', site_ifo)
    #driver.get("https://vk.com/im?sel=258101897")
    if g:
        print('Страница кликабельна')
    g = send_vk_message_xpath(driver, site_ifo,'258101897','text_message')
    p = input('*')
    driver.quit()