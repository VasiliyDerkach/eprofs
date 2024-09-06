from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
options = ChromeOptions()
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--enable-profile-shortcut-manager')
options.add_argument('--profile-directory=Profile 1')
options.add_argument('--user-data-dir=C:/1/AppData/Local/Google/Chrome/User Data')
# options.add_argument('profile-directory=C:/1/AppData/Local/Google/Chrome/User Data/Profile 1')
options.add_argument("user-agent=" + 'Chrome')
login = 'profsadokate@mail.ru'
psw = 'Htpbcnfyc!cJghjnbdktybt2'
timeout = 15
# login = 'v_derkach@inbox.ru'
# psw = 'Betelgeize#70betelgeize'
#driver = Chrome(options=options)
driver = Chrome()

#time.sleep(10)
driver.get("https://vk.com/im?sel=258101897")
ph = '/html/body/div[3]/div/div/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[1]/div/form/input[1]'
tc = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,ph)))
try:
    login_inp = driver.find_element(By.XPATH,ph)
    login_inp.send_keys(login)
    login_ent = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[1]/div/form/button/span/span')
    login_ent.click()
except:
    pass
ph = '/html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[3]/button[2]/span'
tc = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,ph)))
ins = driver.find_element(By.XPATH,ph)
ins.click()
ph = '/html/body/div[1]/div/div/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div/div/div[2]/div[2]'
tc = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,ph)))
ins = driver.find_element(By.XPATH,ph)
ins.click()
ph = '/html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[2]/div/div[1]/div/div/input'
tc = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,ph)))
#/html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[2]/div/div[4]/div/div/input
ans = input('Введите разовый ключ ВК ')
for l,a in enumerate(ans):
    ph = f'/html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[2]/div/div[{l+1}]/div/div/input'
    chr = driver.find_element(By.XPATH,ph)
    chr.send_keys(a)
try:
    login_psw = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[1]/div[3]/div/div/input')
    login_psw.send_keys(psw)
    login_psw1 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[2]/button/span')
    login_psw1.click()
except:
    pass
#/html/body/div[4]/div/div/div[2]/div[2]/div[3]/div/div/div/div[3]/div[2]/div[1]/div/div[2]/div[3]/div/span[1]/span/a
tc = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID,'im_editable258101897' )))
if tc:
    msg = driver.find_element(By.ID,'im_editable258101897')
    msg.send_keys('Hhello!! +1')
    time.sleep(5)
    msg.send_keys(Keys.RETURN)
    time.sleep(5)
    #msg = driver.find_element(By.ID,'send_24__Mask')
    #msg.click()
driver.close()
