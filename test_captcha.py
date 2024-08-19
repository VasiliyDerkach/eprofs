import io

from selenium.webdriver.common.by import By
import twocaptcha
from selenium import webdriver
import time
from PIL import Image

driver = webdriver.Chrome()
url = "https://chkalovsky--svd.sudrf.ru/modules.php?name=sud_delo&srv_num=1&name_op=sf&delo_id=1540005"
driver.get(url)

imgResults = driver.find_elements(By.XPATH,'//*[@id="calform"]/table[1]/tbody/tr[2]/td/table/tbody/tr[4]/td[2]/img')

solver = twocaptcha.TwoCaptcha('a2fd27620a57b390f7f124a98c249a7f')
# print(imgResults[0].get_attribute("src"))
img_captcha = Image.open(io.BytesIO(imgResults[0].screenshot_as_png))

# img_captcha.show()
result = solver.normal(imgResults[0].get_attribute("src"))
#print ("solved: ",result)
button_ctegor = = driver.find_element(By.XPATH,"/html/body/div[6]/div[2]/div[1]/ul/li[3]/input")
button_ctegor.click()
button_work = = driver.find_element(By.XPATH,"/html/body/div[10]/div[3]/div/div[2]/div[2]/div[2]/form/table[2]/tbody/tr[3]/td[2]/input")
button_work.click()
# можно + еще категории
captchafield = driver.find_element(By.XPATH,"/html/body/div[10]/div[3]/div/div[2]/div[2]/div[2]/form/table[1]/tbody/tr[2]/td/table/tbody/tr[4]/td[2]/input[1]")
time.sleep(7)
captchafield.send_keys(result["code"])
# xpath след. страница /html/body/div[10]/div[3]/div/div[2]/div[2]/div[2]/table[3]/tbody/tr/td/a[3]
time.sleep(7)
driver.close()
#url_captcha = 'https://chkalovsky--svd.sudrf.ru/modules.php?name=sud_delo&srv_num=1&name_op=r&delo_id=1540005&case_type=0&new=0&G1_PARTS__NAMESS=&g1_case__CASE_NUMBERSS=&g1_case__JUDICIAL_UIDSS=&captcha=19080&captchaid=icg5g73kaura1onkdgusubfo37&delo_table=g1_case&g1_case__ENTRY_DATE1D=&g1_case__ENTRY_DATE2D=&lawbookarticles%5B%5D=%D1%EF%EE%F0%FB%2C+%E2%EE%E7%ED%E8%EA%E0%FE%F9%E8%E5+%E8%E7+%F2%F0%F3%E4%EE%E2%FB%F5+%EE%F2%ED%EE%F8%E5%ED%E8%E9&lawbookarticles%5B%5D=%D1%EF%EE%F0%FB%2C+%E2%EE%E7%ED%E8%EA%E0%FE%F9%E8%E5+%E8%E7+%EF%E5%ED%F1%E8%EE%ED%ED%FB%F5+%EE%F2%ED%EE%F8%E5%ED%E8%E9&G1_CASE__JUDGE=&g1_case__RESULT_DATE1D=&g1_case__RESULT_DATE2D=&G1_CASE__RESULT=&G1_CASE__BUILDING_ID=&G1_CASE__COURT_STRUCT=&G1_EVENT__EVENT_NAME=&G1_EVENT__EVENT_DATEDD=&G1_PARTS__PARTS_TYPE=&G1_PARTS__INN_STRSS=&G1_PARTS__KPP_STRSS=&G1_PARTS__OGRN_STRSS=&G1_PARTS__OGRNIP_STRSS=&G1_RKN_ACCESS_RESTRICTION__RKN_REASON=&g1_rkn_access_restriction__RKN_RESTRICT_URLSS=&g1_requirement__ACCESSION_DATE1D=&g1_requirement__ACCESSION_DATE2D=&G1_REQUIREMENT__CATEGORY=&g1_requirement__ESSENCESS=&g1_requirement__JOIN_END_DATE1D=&g1_requirement__JOIN_END_DATE2D=&G1_REQUIREMENT__PUBLICATION_ID=&G1_DOCUMENT__PUBL_DATE1D=&G1_DOCUMENT__PUBL_DATE2D=&G1_CASE__VALIDITY_DATE1D=&G1_CASE__VALIDITY_DATE2D=&G1_ORDER_INFO__ORDER_DATE1D=&G1_ORDER_INFO__ORDER_DATE2D=&G1_ORDER_INFO__ORDER_NUMSS=&G1_ORDER_INFO__EXTERNALKEYSS=&G1_ORDER_INFO__STATE_ID=&G1_ORDER_INFO__RECIP_ID=&Submit=%CD%E0%E9%F2%E8'
# кнопка категории дел /html/body/div[10]/div[3]/div/div[2]/div[2]/div[2]/form/table[2]/tbody/tr[3]/td[2]/input
# checkbox трудовые отношения /html/body/div[6]/div[2]/div[1]/ul/li[3]/input
# button = driver.find_element(By.XPATH,"//button[contains(@class, 'l2z7-tVRGe-3sq5kU4uu5 _2xjDiWmBxfqem8nGQMmGci _2HIb5VBFp6Oi5_JoLdEcl6 _2vbG_IBm-DpI5KeEAHJkRy')]")
# button.click()
# time.sleep(10)
#
# messagefield=driver.find_element(By.XPATH,"//p[contains(@class,'_2WOJoV7Dg493S8DW_GobSK')]")
# print (messagefield.text)