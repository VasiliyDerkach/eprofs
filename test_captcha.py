from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha
from selenium import webdriver
import time

driver = webdriver.Chrome()
url = "https://2captcha.com/demo/normal"
driver.get(url)

imgResults = driver.find_elements(By.XPATH,"//img[contains(@class,'_2hXzbgz7SSP0DXCyvKWcha')]")
solver = TwoCaptcha(Your_2Captcha_API_key)
result = solver.normal(imgResults[0].get_attribute("src"))
print ("solved: " + str(result))

captchafield = driver.find_element(By.XPATH,"//input[contains(@class,'_26Pq0m_qFk19UXx1w0U5Kv')]")
captchafield.send_keys(result["code"])

button = driver.find_element(By.XPATH,"//button[contains(@class, 'l2z7-tVRGe-3sq5kU4uu5 _2xjDiWmBxfqem8nGQMmGci _2HIb5VBFp6Oi5_JoLdEcl6 _2vbG_IBm-DpI5KeEAHJkRy')]")
button.click()
time.sleep(10)

messagefield=driver.find_element(By.XPATH,"//p[contains(@class,'_2WOJoV7Dg493S8DW_GobSK')]")
print (messagefield.text)