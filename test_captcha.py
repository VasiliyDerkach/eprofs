from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha
from selenium import webdriver
import time

driver = webdriver.Chrome()
url = "https://chkalovsky--svd.sudrf.ru/modules.php?name=sud_delo&srv_num=1&name_op=sf&delo_id=1540005"
driver.get(url)
time.sleep(7)
imgResults = driver.find_elements(By.ID,'captcha')
solver = TwoCaptcha('a2fd27620a57b390f7f124a98c249a7f')
result = solver.normal(imgResults[0].get_attribute("src"))
print ("solved: " + str(result))

# captchafield = driver.find_element(By.XPATH,"//input[contains(@class,'_26Pq0m_qFk19UXx1w0U5Kv')]")
# captchafield.send_keys(result["code"])
#
# button = driver.find_element(By.XPATH,"//button[contains(@class, 'l2z7-tVRGe-3sq5kU4uu5 _2xjDiWmBxfqem8nGQMmGci _2HIb5VBFp6Oi5_JoLdEcl6 _2vbG_IBm-DpI5KeEAHJkRy')]")
# button.click()
# time.sleep(10)
#
# messagefield=driver.find_element(By.XPATH,"//p[contains(@class,'_2WOJoV7Dg493S8DW_GobSK')]")
# print (messagefield.text)