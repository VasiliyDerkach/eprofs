from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def parsing_table_xpath(web_driver,url, html_tab_scenario, timeout = 5):
# pip install selenium 2captcha-python
    recr = {}
    if web_driver and isinstance(web_driver,Chrome):
        driver = web_driver
    else:
        driver = Chrome()
        #print(isinstance(driver,webdriver.Chrome))
    driver.get(url)
    driver.set_page_load_timeout(timeout)
    if len(html_tab_scenario)>0:

        end_flag = False
        conts = html_tab_scenario
        for cn, tx in conts.items():
            flag_el = True
            recr[cn] = []
            if cn != 'None':  # если нет указания на кликабельные элементы, которые надо предварительно активировать
                try:
                    lst1 = driver.find_element(By.XPATH, cn)
                    lst1.click()
                except:
                    flag_el = False

            if flag_el:
                i = 0
                mainlnk = conts[cn]['MainLink']
                nend_tabl = True
                while nend_tabl:
                    rw = {}
                    mainlnk_i = mainlnk.replace('{index}',str(i))
                    for fld in conts[cn]['Fields']:
                        try:
                            el = driver.find_element(By.XPATH,mainlnk_i+fld[1])
                        except:
                            nend_tabl = False
                            break
                        if el:
                            txt = el.text
                            if fld[2]=='link':
                                txt = el.get_attribute('href')
                            elif fld[2]=='e-mail':
                                txt = txt.replace(' ','')
                                txt = txt.replace('mailto:','')
                            elif fld[2].find('phone')>0:
                                txt = txt.replace(' ','')
                                txt = txt.replace('Телефон:','')
                                txt = txt.replace('(','')
                                txt = txt.replace(')','')
                                if fld[2]=='phone7':
                                    txt += '7'
                            rw[fld[0]] = txt
                    recr[cn].append(rw)
                i += 1


    if len(recr)<=0:
        recr = None
    return driver,recr


if __name__ == '__main__':
    url = 'http://oblsud.svd.sudrf.ru/modules.php?name=sud'
    conts = {'/html/body/div[10]/div[3]/div/div[2]/div[2]/a[1]':{'MainLink':'/html/body/div[10]/div[3]/div/div[2]/table/tbody/tr[6]/td[2]/table/tbody/tr[{index}]/td[2]',
                     'Fields':[('name','/a','str'),('email','/table/tbody/tr/td/ul/li[3]','e-mail'),
                               ('legal_street','/table/tbody/tr/td/ul/li[1]','str'),('phone_office','/table/tbody/tr/td/ul/li[2]','phone7'),
                               ('website','/table/tbody/tr/td/ul/li[4]','link')]}
             }
    # ключ conts имя html закладки на сайте на которую надо переходить перед считыванием таблицы, если он None
    # значит страница сайта без закладок
    dr, tb = parsing_table_xpath(None,url, conts, timeout = 25)
    dr.quit()
    print(tb)