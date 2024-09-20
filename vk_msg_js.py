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
            xpth = input(f"Элемент {element_config['description']} не найден. Введите c - чтобы пропустить поиск или введите XPATH ")
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
                print(f"Элемент {element_config['description']} по указанному xpath не найден")
def pars_webelement_byscn(vdriver,element_config,timeout,**kwargs):
    tc = None
    pth = None
    rez = {}
    ByFind = By.XPATH
    if 'class_name' in element_config:
        ByFind = By.CLASS_NAME
    if 'id_element' in element_config:
        ByFind = By.ID
    if 'link' in element_config:
        ByFind = By.LINK_TEXT
    if 'alert_accept' in element_config:
        vdriver.switch_to().alert().accept()
        return 'alert_accept_execute'
    for xpth in element_config['xpaths']:
        try:
            # if element_config['description']=='email_onecode':
            #     print('email_onecode')
            if element_config['wait'] == 'WebDriverWait':
                tc = WebDriverWait(vdriver, timeout).until(EC.presence_of_element_located((ByFind, xpth)))
            if element_config['wait'] == 'VisibleWait':
                tc = WebDriverWait(vdriver, timeout).until(EC.visibility_of_element_located((ByFind, xpth)))
            elif element_config['wait'] == '':
                tc = vdriver.find_element(ByFind,xpth)
            elif element_config['wait']=='Wait_to_be_clickable':
                try:
                    tc = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((ByFind, xpth )))
                except Exception as e:
                    print(e)
                    print(f"Проблема с кликабельностью или наличием элемента в {element_config['description']}")
                    tc = manual_find_xpath_element(vdriver, element_config, timeout, **kwargs)
            if tc:
                pth = xpth
                print('+',element_config['description'],'->',xpth)
                if element_config['action'] == 'set_key':
                    try:
                        tc.send_keys(kwargs[element_config['values'].replace('|', '')])
                        rez['execute']= True
                    except Exception as e:
                        print(e)
                        print(f"Проблема с sen_key в {element_config['description']}")
                        tc = manual_find_xpath_element(vdriver, element_config, timeout, **kwargs)
                    return rez
                    break
                elif element_config['action'] == 'click':
                    try:
                        tc.click()
                        rez['execute'] = True
                    except Exception as e:
                        print(e)
                        print(f"Проблема с click в {element_config['description']}")
                        alt = vdriver.find_element(ByFind, element_config['alert'])
                        if alt:# and alt.is_displayed():
                            print(f"В {element_config['description']} есть alert")
                            print(alt.get_property())
                        ys = input('Введите y чтобы поискать вручную ')
                        if ys=='y':
                            tc = manual_find_xpath_element(vdriver, element_config, timeout, **kwargs)
                    return rez
                    break

                elif element_config['action'] == 'mouse_move':
                    act_mouse = ActionChains(vdriver)
                    act_mouse.move_to_element(tc).perform()
                    print(tc.text)
                    rez['execute'] = True
                    return rez
                    break
                elif element_config['action'] == 'return':
                    if tc.is_displayed():
                        print(element_config['values'], tc.text)
                        rez['execute'] = True
                        rez['is_blocked'] = element_config['values']
                        rez['mark'] = tc.text
                        return rez
                    else:
                        rez['execute'] = True
                        rez['is_blocked'] = 'blocked_unvisible'
                        return rez
                    break
                elif element_config['action'] == 'set_key_iter':
                    # ans = input('Введите разовый ключ ВК ')
                    ans = kwargs['onecode']
                    itr_xpath = element_config['xpath_iter']
                    for l, a in enumerate(ans):
                        ph = itr_xpath.replace('|number|', str(l + 1))
                        # ph = f'/html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[2]/div/div[|number|]/div/div/input'
                        try:
                            chr = driver.find_element(ByFind, ph)
                            chr.send_keys(a)
                            if chr:
                                print('++', ph, '=', a)
                        except Exception as e:
                            print(e)
                            print(f"Проблема с итеррационным set_key в {element_config['description']}")
                            tc = manual_find_xpath_element(vdriver, element_config, timeout, **kwargs)
                    rez['execute'] = True
                    return rez
                    break
                else:
                    rez['execute'] = True
                    return rez
                    break
            if not tc:
                tc = manual_find_xpath_element(vdriver, element_config, timeout, **kwargs)
            if not tc:
                rez['execute'] = False
                return rez
            # if tc:
            #     return True
            # else:
            #     return False

        except Exception as exs:
            # print(exs)
            print('not find ', element_config['description'], '->', xpth)


def pars_webelements_stage_byscn(vdriver,pars_config,stage,**kwargs):
    timeout = pars_config['minitimeout']
    rez = {}
    rez['execute'] = True
    for stp in pars_config['scenario']:
        if stp['stage']==stage:
            aa = pars_webelement_byscn(vdriver, stp, timeout, **kwargs)
            # if isinstance(aa,bool) and isinstance(rez,bool):
            # rez = rez and aa['execute']
            if aa:
                for k,h in aa.items():
                    if k!='execute':
                        rez[k] = h
                    else:
                        rez[k] = rez[k] and aa['execute']

    return rez


def login_with_emailcode(vdriver,login, password, email,email_key, parsing_config,in_mail_name):

    cod_email_name = parsing_config['cod_email_name']
    cod_email_str0 = parsing_config['cod_email_str0']
    cod_email_str1 = parsing_config['cod_email_str1']
    cod_email_subject = parsing_config['cod_email_subject']
    cod_email_servicename = parsing_config['cod_email_servicename']
    now_timezone = parsing_config['now_timezone']
    imap_server = parsing_config['imap_server']
    # in_mail_name = parsing_config['cod_email_name']
    priod_sec = parsing_config['priod_sec_for_email']
    count_return = parsing_config['count_return_email']
    psw_mail = email_key
    timeout = parsing_config['timeout']
    mtimeout = parsing_config['minitimeout']
    eml = get_in_email_code.get_in_email_code(imap_server, email, in_mail_name, psw_mail, priod_sec, now_timezone)
    flaglogin = pars_webelements_stage_byscn(vdriver, parsing_config, 'login', login=login)
    print(f"Этап login {flaglogin['execute']}")
    flagdef = flaglogin['execute']
    eml = []
    j = 0
    ocode = None
    while True:
        eml = get_in_email_code.get_in_email_code(imap_server, email, in_mail_name, psw_mail, priod_sec, now_timezone)
        print(eml)
        j += 1
        if eml:
            if parsing_config['notify_email'] in eml[0]:
                ocode = eml[3]
                break
        if j>count_return:
            break
    if ocode:
        print(ocode)
        aa = pars_webelements_stage_byscn(vdriver, parsing_config, 'after_login', onecode=ocode, password= password)
        flagdef = flagdef and aa['execute']
        print(f"Этап after_login {aa['execute']}")
        aa = pars_webelements_stage_byscn(vdriver, parsing_config, 'after_authentific')

        flagdef = flagdef and aa['execute']
        print(f"Этап after_authentific {aa['execute']}")

        return flagdef
    else:
        return False
def send_vk_message_xpath(vdriver, parsing_config,user_vk_id,text_message):
    messager_url = parsing_config['messager_url']
    alert_my_blacklist = parsing_config['alert_my_blacklist']
    alert_out_blacklist = parsing_config['alert_out_blacklist']
     # которые могут присылать ему сообщения
    driver.get(messager_url+user_vk_id)
    blc = pars_webelements_stage_byscn(vdriver, parsing_config, 'is_user_block')
    print('is_user_block',blc)
    if blc['execute']:
        if ('is_blocked' in blc and blc['is_blocked']=='this user is block'
            and 'mark' in blc ):
            if alert_my_blacklist in blc['mark']:
                print('Запуск is_user_unblock')
            # строки перенести в настройки, сделать blc словарем
                r = pars_webelements_stage_byscn(vdriver, parsing_config, 'is_user_unblock')
            if alert_out_blacklist in blc['mark']:
                return 'us_is_ban'
        r1 = pars_webelements_stage_byscn(vdriver, parsing_config, 'send_vk_message',message=text_message+'\n')
        print('r1=',r1)
        r2 = pars_webelements_stage_byscn(vdriver, parsing_config, 'after_vk_message')
        print('r2=', r2)

if __name__=='__main__':
    with open("vkont_msg.json", "r",encoding='utf-8') as rvkfile:
        site_ifo = json.load(rvkfile)
    print(site_ifo)
    print(site_ifo['scenario'][0]['xpaths'][0])
    driver = Chrome()
    driver.implicitly_wait(10)
    driver.get("https://vk.com/")
    driver.maximize_window()
    e_mail = 'profsadokate@mail.ru'



    # g = login_with_emailcode(driver, e_mail, 'Htpbcnfyc!cJghjnbdktybt2', e_mail, 'BpKrex5kd9pv82aai5FW', site_ifo,'Tradeunion')
    # g = login_with_emailcode(driver, 'profsadokate2@mail.ru', '0Htpbcnfyc!cJghjnbdktybt2', 'profsadokate2@mail.ru',
    #                          'b0eMHbPTGsUfYxFPjCYh', site_ifo,'Tradeunionc')
    g = login_with_emailcode(driver, 'profsadokate3@mail.ru', '0Htpbcnfyc!cJghjnbdktybt28', 'profsadokate3@mail.ru',
                         'jvWWN1FsSm9xvekWCVAg', site_ifo,'Tradeuniond')
    # g = login_with_emailcode(driver, 'profsadokate4@mail.ru', '0Htpbcnfyc!cJghjnbdktybt28', 'profsadokate4@mail.ru',
    #                          'imX4VAJUR2k5Cngp4hqf', site_ifo,'Tradeunion')

    # l = input('*')
    #driver.get("https://vk.com/im?sel=258101897")
    if g:
        print('Страница кликабельна')
    g = send_vk_message_xpath(driver, site_ifo,'258101897','text_message222')
    p = input('*')
    driver.quit()

    # profsadokate2@mail.ru
    # b0eMHbPTGsUfYxFPjCYh
    # vk 0Htpbcnfyc!cJghjnbdktybt2

    #profsadokate3@mail.ru
    #jvWWN1FsSm9xvekWCVAg
    #vk 0Htpbcnfyc!cJghjnbdktybt28

    #profsadokate4@mail.ru
    #imX4VAJUR2k5Cngp4hqf
    #vk 0Htpbcnfyc!cJghjnbdktybt28

    # разблокировка пользов //ui_actions_menu_item im-action im-action_unblacklist _im_action