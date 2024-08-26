#установим несколько зависимостей. Если у вас их еще нет, выполните команду pip install selenium 2captcha-python
import io

from selenium.webdriver.common.by import By
import twocaptcha
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
from PIL import Image
#pip install selenium 2captcha-python
driver = webdriver.Chrome()
url = "https://chkalovsky--svd.sudrf.ru/modules.php?name=sud_delo&srv_num=1&name_op=sf&delo_id=1540005"
driver.get(url)
driver.set_page_load_timeout(20)
try:
    imgResults = driver.find_elements(By.XPATH,f'//*[@id="calform"]/table[1]/tbody/tr[2]/td/table/tbody/tr[4]/td[2]/img')

    solver = twocaptcha.TwoCaptcha('a2fd27620a57b390f7f124a98c249a7f')
    # print(imgResults[0].get_attribute("src"))
    img_captcha = Image.open(io.BytesIO(imgResults[0].screenshot_as_png))

    # img_captcha.show()
    result = solver.normal(imgResults[0].get_attribute("src"))
    #print ("solved: ",result)
    button_ctegor = driver.find_element(By.XPATH,"/html/body/div[10]/div[3]/div/div[2]/div[2]/div[2]/form/table[2]/tbody/tr[3]/td[2]/input")
    button_ctegor.click()
    button_work = driver.find_element(By.XPATH,"/html/body/div[6]/div[2]/div[1]/ul/li[3]/input")
    button_work.click()
    lnk_ctg_close = driver.find_element(By.XPATH,"/html/body/div[6]/div[1]/a")
    lnk_ctg_close.click()
    time.sleep(7) 
    # можно + еще категории
    captchafield = driver.find_element(By.XPATH,"/html/body/div[10]/div[3]/div/div[2]/div[2]/div[2]/form/table[1]/tbody/tr[2]/td/table/tbody/tr[4]/td[2]/input[1]")
    time.sleep(7)
    captchafield.send_keys(result["code"])
    btn_find = driver.find_element(By.XPATH,"/html/body/div[10]/div[3]/div/div[2]/div[2]/div[2]/form/div[5]/input[1]")
    #кнопка найти дела
    btn_find.click()
    time.sleep(7)
    btn_next = driver.find_element(By.XPATH,"/html/body/div[10]/div[3]/div/div[2]/div[2]/div[2]/table[3]/tbody/tr/td/a[3]")
    btn_next.click()
    # xpath след. страница /html/body/div[10]/div[3]/div/div[2]/div[2]/div[2]/table[3]/tbody/tr/td/a[3]
    time.sleep(7)
    
    driver.quit()
except TimeoutException as e:
    print("Page load Timeout Occurred. Quitting !!!")
    driver.quit()
#url_captcha = 'https://chkalovsky--svd.sudrf.ru/modules.php?name=sud_delo&srv_num=1&name_op=r&delo_id=1540005&case_type=0&new=0&G1_PARTS__NAMESS=&g1_case__CASE_NUMBERSS=&g1_case__JUDICIAL_UIDSS=&captcha=19080&captchaid=icg5g73kaura1onkdgusubfo37&delo_table=g1_case&g1_case__ENTRY_DATE1D=&g1_case__ENTRY_DATE2D=&lawbookarticles%5B%5D=%D1%EF%EE%F0%FB%2C+%E2%EE%E7%ED%E8%EA%E0%FE%F9%E8%E5+%E8%E7+%F2%F0%F3%E4%EE%E2%FB%F5+%EE%F2%ED%EE%F8%E5%ED%E8%E9&lawbookarticles%5B%5D=%D1%EF%EE%F0%FB%2C+%E2%EE%E7%ED%E8%EA%E0%FE%F9%E8%E5+%E8%E7+%EF%E5%ED%F1%E8%EE%ED%ED%FB%F5+%EE%F2%ED%EE%F8%E5%ED%E8%E9&G1_CASE__JUDGE=&g1_case__RESULT_DATE1D=&g1_case__RESULT_DATE2D=&G1_CASE__RESULT=&G1_CASE__BUILDING_ID=&G1_CASE__COURT_STRUCT=&G1_EVENT__EVENT_NAME=&G1_EVENT__EVENT_DATEDD=&G1_PARTS__PARTS_TYPE=&G1_PARTS__INN_STRSS=&G1_PARTS__KPP_STRSS=&G1_PARTS__OGRN_STRSS=&G1_PARTS__OGRNIP_STRSS=&G1_RKN_ACCESS_RESTRICTION__RKN_REASON=&g1_rkn_access_restriction__RKN_RESTRICT_URLSS=&g1_requirement__ACCESSION_DATE1D=&g1_requirement__ACCESSION_DATE2D=&G1_REQUIREMENT__CATEGORY=&g1_requirement__ESSENCESS=&g1_requirement__JOIN_END_DATE1D=&g1_requirement__JOIN_END_DATE2D=&G1_REQUIREMENT__PUBLICATION_ID=&G1_DOCUMENT__PUBL_DATE1D=&G1_DOCUMENT__PUBL_DATE2D=&G1_CASE__VALIDITY_DATE1D=&G1_CASE__VALIDITY_DATE2D=&G1_ORDER_INFO__ORDER_DATE1D=&G1_ORDER_INFO__ORDER_DATE2D=&G1_ORDER_INFO__ORDER_NUMSS=&G1_ORDER_INFO__EXTERNALKEYSS=&G1_ORDER_INFO__STATE_ID=&G1_ORDER_INFO__RECIP_ID=&Submit=%CD%E0%E9%F2%E8'
# кнопка категории дел /html/body/div[10]/div[3]/div/div[2]/div[2]/div[2]/form/table[2]/tbody/tr[3]/td[2]/input
# закрыть форму выбора категорий /html/body/div[6]/div[1]/a
# checkbox трудовые отношения /html/body/div[6]/div[2]/div[1]/ul/li[3]/input
# button = driver.find_element(By.XPATH,"//button[contains(@class, 'l2z7-tVRGe-3sq5kU4uu5 _2xjDiWmBxfqem8nGQMmGci _2HIb5VBFp6Oi5_JoLdEcl6 _2vbG_IBm-DpI5KeEAHJkRy')]")
# button.click()
# time.sleep(10)
#
# messagefield=driver.find_element(By.XPATH,"//p[contains(@class,'_2WOJoV7Dg493S8DW_GobSK')]")
# print (messagefield.text)

#input name="Submit" type="submit" class="booton" value="Найти" onclick="checkForm(event);">
##calform > div:nth-child(14) > input:nth-child(1)
#<input name="Submit" type="submit" class="booton" value="Найти" onclick="checkForm(event);">
#<input name="captcha" autocomplete="off" id="captcha" type="text" class="Lookup" style="vertical-align:top;height:25px;font-size:17px;" size="10">
#<img src="data: image/png;base64, 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" style="border: 1px solid #4a739d;">