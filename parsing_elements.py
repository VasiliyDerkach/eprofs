# установим несколько зависимостей. Если у вас их еще нет, выполните команду pip install selenium 2captcha-python
import io
import re
from selenium.webdriver.common.by import By
import twocaptcha
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
from PIL import Image
twocaptcha_key = 'a2fd27620a57b390f7f124a98c249a7f'
def exe_parsing_scenario(url, vscenario, html_scenario, timeout = 5):
# pip install selenium 2captcha-python
    driver = webdriver.Chrome()
    driver.get(url)
    driver.set_page_load_timeout(timeout)
    if len(html_scenario)>0:
        html_scenario1 = sorted(html_scenario, key=lambda elem: elem['sequence'])
        try:
            for html_elscinario in html_scenario1:
                if 'type' in html_elscinario.keys():
                    if 'id' in html_elscinario.keys() and len(html_elscinario['id']>0):
                        ByParam = By.ID
                        Param = html_elscinario['id']
                    elif 'xpath' in html_elscinario.keys() and len(html_elscinario['xpath'])>0:
                        ByParam = By.XPATH
                        Param = html_elscinario['xpath']
                    #+link и другие варианты поиска элемента
                    else:
                        driver.close()
                        return f'Для элемента {html_elscinario} не его задан параметр поиска в html'
                    vtype = html_elscinario['type']
                    if vtype=='findtext':
                        if 'text' in html_elscinario.keys() and len(html_elscinario['text'] > 0):
                            if html_elscinario['text'] in vscenario.keys() and len(vscenario[html_elscinario['text']])>0:
                                txt = vscenario[html_elscinario['text']]
                                elem = driver.find_element(ByParam,Param)
                                if elem:
                                    elem.send_keys(txt)
                                else:
                                    driver.close()
                                    return f'Для элемента {html_elscinario} типа {vtype} не найден элемент {Param}'

                            else:
                                driver.close()
                                return f'Для элемента {html_elscinario} типа {vtype} не задан параметр: text или его значение'

                        else:
                            driver.close()
                            return f'Для элемента {html_elscinario} типа {vtype} не задан параметр: текст для поиска'
                    elif vtype=='captcha_send_keys':
                        if 'xpath_send' in html_elscinario.keys() and len(html_elscinario['xpath_send'] > 0):
                            elem = driver.find_element(ByParam,Param)
                            if elem:
                                imgResults = elem
                                solver = twocaptcha.TwoCaptcha(twocaptcha_key)
                                # print(imgResults[0].get_attribute("src"))
                                img_captcha = Image.open(io.BytesIO(imgResults[0].screenshot_as_png))
                                # img_captcha.show()
                                result = solver.normal(imgResults[0].get_attribute("src"))
                                img_captcha.close()
                                captchafield = driver.find_element(By.XPATH,html_elscinario['xpath_send'])
                                captchafield.send_keys(result["code"])
                            else:
                                driver.close()
                                return f'Для элемента {html_elscinario} типа {vtype} не найден элемент {Param}'

                        else:
                            driver.close()
                            return f'Для элемента {html_elscinario} типа {vtype} не задан параметр xpath_send'
                    elif vtype=='button_click':
                        elem = driver.find_element(ByParam,Param)
                        if elem:
                            elem.click()
                        else:
                            driver.close()
                            return f'Для элемента {html_elscinario} типа {vtype} не найден элемент {Param}'
                    elif vtype=='combobox':
                        if 'text' in html_elscinario.keys() and len(html_elscinario['text']) > 0:
                            if html_elscinario['text'] in vscenario.keys() and len(vscenario[html_elscinario['text']])>0:
                                txt = vscenario[html_elscinario['text']]
                                if isinstance(txt,list):
                                    elem = driver.find_element(ByParam, Param)
                                    if elem:
                                        elem.click()
                                    else:
                                        driver.close()
                                        return f'Для элемента {html_elscinario} типа {vtype} не найден элемент {Param}'
                                    if 'xpath_elem' in html_elscinario.keys() and len(html_elscinario['xpath_elem'])>0 and html_elscinario['xpath_elem'].find('{')>0:
                                        for numbers in txt:
                                            if isinstance(numbers,list) and len(numbers)>0:
                                                xph = html_elscinario['xpath_elem']
                                                for i,num in enumerate(numbers):
                                                    xph = xph.replace('{{elem['+str(i)+']}}',str(num))
                                                el = driver.find_element(By.XPATH,xph)
                                                if el:
                                                    el.click()
                                                else:
                                                    driver.close()
                                                    return f'Для элемента {html_elscinario} типа {vtype} не найден html {html_elscinario['xpath_elem']}'
                                        if 'xpath_send' in html_elscinario.keys() and len(html_elscinario['xpath_send'] > 0):
                                            ec = driver.find_element(By.XPATH, html_elscinario['xpath_send'])
                                            if ec:
                                                ec.click()
                                            else:
                                                driver.close()
                                                return f'Для элемента {html_elscinario} типа {vtype} не найден html {html_elscinario['xpath_send']}'

                                            pass
                                    else:
                                        driver.close()
                                        return f'Для элемента {html_elscinario} типа {vtype} не найдено значение xpath_elem'


                                else:
                                    driver.close()
                                    return f'Для элемента {html_elscinario} типа {vtype} параметр text не является списком'

                            else:
                                driver.close()
                                return f'Для элемента {html_elscinario} типа {vtype} не задан параметр: text или его значение'

                        else:
                            driver.close()
                            return f'Для элемента {html_elscinario} типа {vtype} не задан параметр: текст для поиска'

            imgResults = driver.find_elements(By.XPATH,
                                              f'//*[@id="calform"]/table[1]/tbody/tr[2]/td/table/tbody/tr[4]/td[2]/img')


            # print ("solved: ",result)
            button_ctegor = driver.find_element(By.XPATH,
                                                "/html/body/div[10]/div[3]/div/div[2]/div[2]/div[2]/form/table[2]/tbody/tr[3]/td[2]/input")
            button_ctegor.click()
            button_work = driver.find_element(By.XPATH, "/html/body/div[6]/div[2]/div[1]/ul/li[3]/input")
            #/ html / body / div[6] / div[2] / div / ul / li[4] / input
            button_work.click()
            lnk_ctg_close = driver.find_element(By.XPATH, "/html/body/div[6]/div[1]/a")
            lnk_ctg_close.click()
            time.sleep(7)
            # можно + еще категории
            time.sleep(7)
            captchafield.send_keys(result["code"])
            btn_find = driver.find_element(By.XPATH, "/html/body/div[10]/div[3]/div/div[2]/div[2]/div[2]/form/div[5]/input[1]")
            # кнопка найти дела
            btn_find.click()
            time.sleep(7)
            btn_next = driver.find_element(By.XPATH,
                                           "/html/body/div[10]/div[3]/div/div[2]/div[2]/div[2]/table[3]/tbody/tr/td/a[3]")
            btn_next.click()
            # xpath след. страница /html/body/div[10]/div[3]/div/div[2]/div[2]/div[2]/table[3]/tbody/tr/td/a[3]
            time.sleep(7)

            driver.quit()
        except TimeoutException as e:
            return "Page load Timeout Occurred. Quitting !!!"
            driver.quit()

if __name__=='__main__':
    html_court1 = [
        {'xpath': '//*[@id="calform"]/table[1]/tbody/tr[2]/td/table/tbody/tr[4]/td[2]/img',
         'type': 'captcha_send_keys',
         'xpath_send': "/html/body/div[10]/div[3]/div/div[2]/div[2]/div[2]/form/div[5]/input[1]",
         'sequence': 2},
        {'type': 'combobox',
         'xpath': "/html/body/div[10]/div[3]/div/div[2]/div[2]/div[2]/form/table[2]/tbody/tr[3]/td[2]/input",
         'xpath_elem': f"/html/body/div[6]/div[2]/div[1]/ul/li[{{elem[0]}}]/input",
         'xpath_send': "/html/body/div[6]/div[1]/a",
         'text': 'categoryes',
         'sequence': 0},
        {'type': 'findtext',
         'xpath': '/html/body/div[10]/div[3]/div/div[2]/div[2]/div[2]/form/table[1]/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/input',
         'sequence': 1,
         'text': 'last_name'},
        {'type': 'button_click',
         'xpath':"/html/body/div[10]/div[3]/div/div[2]/div[2]/div[2]/form/div[5]/input[1]",
         'sequence': 3}
    ]
    scenario = { 'last_name': 'Иванов', 'categoryes': [[3],[4]]}
    url1 = "https://chkalovsky--svd.sudrf.ru/modules.php?name=sud_delo&srv_num=1&name_op=sf&delo_id=1540005"
    print(exe_parsing_scenario(url1, scenario, html_court1, timeout = 25))