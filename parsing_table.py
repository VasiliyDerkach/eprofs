from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def parsing_table(web_driver,url, html_tab_scenario, critery_end,timeout = 5):
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
        while not end_flag:
            for cn, tx in conts.items():
                flag_el = True
                if cn != 'None':  # если нет указания на кликабельные элементы, которые надо предварительно активировать
                    try:
                        lst1 = driver.find_element(By.ID, cn)
                        lst1.click()
                    except:
                        flag_el = False

                if flag_el:
                    try:
                        tc = WebDriverWait(driver, timeout).until(
                            EC.presence_of_element_located((By.ID, tx[0]))
                        )
                        # предусмотреть чтение заголовков таблиц
                        if tx[0] == tx[1]:
                            htms[0] = tc
                        else:
                            htms = tc.find_elements(By.ID, tx[1])
                            # предусмотреть случаи (реально есть), когда элементов tx[1] несколько на закладке (несколько таблиц)
                        for htm in htms:
                            if tx[3] == 'doc':
                                # print(htm.text)
                                thead = htm.text
                            elif tx[3] == 'table':
                                try:
                                    thead = htm.find_elements(by=By.TAG_NAME, value='th')
                                except:
                                    thead = []
                                rows = htm.find_elements(by=By.TAG_NAME, value='tr')
                                # подсчет количества столбцов
                                tab = []
                                for r in rows:
                                    cols = r.find_elements(by=By.TAG_NAME, value='td')
                                    # refs = r.find_elements(by=By.TAG_NAME,value='ref')
                                    # for f in refs:
                                    #     print(f.text)
                                    cl = []
                                    ln = len(cols)
                                    if isinstance(cols, list) and ln > 0:
                                        j = 0
                                        for c in cols:
                                            cl.append(c.text)

                                            j += 1
                                            if len(tx[2]) > 0 and j in tx[2]:
                                                try:
                                                    # rr = c.get_attribute('href')
                                                    y = c.find_element(by=By.LINK_TEXT, value=c.text)
                                                    if y:
                                                        cl.append(y.get_attribute('href'))
                                                except Exception as ex0:
                                                    pass
                                    if len(cl) > 0:
                                        try:
                                            tab.append(cl)
                                        except Exception as ecl:
                                            print(ecl)
                            thh = []
                            recr[cn] = {}
                            if tx[3] == 'table' and len(thead) > 0:
                                for he in thead:
                                    thh.append(he.text)
                                recr[cn]['head'] = thh
                            elif tx[3] == 'doc':
                                recr[cn]['head'] = thead
                            if len(tab) > 0:
                                recr[cn]['table'] = tab
                    except Exception as exc:
                        print(f'не загрузилось {exc}')
            if critery_end:
                pass
            else:
                end_flag = True
    if len(recr)<=0:
        recr = None
    return driver,recr


if __name__ == '__main__':
    url = 'https://asbestovsky--svd.sudrf.ru/modules.php?name=sud_delo&srv_num=1&name_op=case&case_id=390794311&case_uid=a4534ef3-49d4-46c0-a04b-fc9e2ab5a9b4&delo_id=1540005'
    conts = {'tab1':('cont1','tablcont',[],'table'),'tab2':('cont2','tablcont',[],'table')
        ,'tab3':('cont3','tablcont',[],'table')
     ,'tab4':('cont4','tablcont',[],'table'), 'tab5':('cont5','cont_doc1',[],'doc')
        ,'tab6':('cont6','tablcont',[],'table'), 'tab7':('cont7','cont_doc1',[],'doc')}
    # 6  исп.листы? 7-кассац.опред.
    # conts  = {'tab5':('cont5','cont_doc1',[],'doc')}
    #conts = {'None':('tablcont','tablcont',[1],'table')}
    # ключ conts имя html закладки на сайте на которую надо переходить перед считыванием таблицы, если он None
    # значит страница сайта без закладок
    # первый элемент кортежа - имя html элемента, в который вложена таблица
    # второй элемент кортежа - имя html элемента таблицы (если совпадает с предыдущем, то таблицу сразу можно найти по ее имени)
    # третий элемент кортежа - список столбцов таблицы, которые надо проверить на наличие ссылок
    # если последний элемент пуст [] - то проверять на ссылки не надо. Ссылки добавляются в итоговую таблицу как доп.столбец справа
    # recr = {}

# пример мэйл районных судов
#/html/body/div[10]/div[3]/div/div[2]/table/tbody/tr[6]/td[2]/table/tbody/tr[1]/td[2]/table/tbody/tr/td/ul/li[3]/a
#/html/body/div[10]/div[3]/div/div[2]/table/tbody/tr[6]/td[2]/table/tbody/tr[10]/td[2]/table/tbody/tr/td/ul/li[3]/a