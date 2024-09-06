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
# login = 'profsadokate@mail.ru'
# psw = 'Htpbcnfyc!cJghjnbdktybt2'
timeout = 15
login = 'v_derkach@inbox.ru'
psw = 'Betelgeize#70betelgeize'
#driver = Chrome(options=options)
driver = Chrome()

#time.sleep(10)
driver.get("https://vk.com/im?sel=876652489")
ph = '/html/body/div[3]/div/div/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[1]/div/form/input[1]'
tc = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,ph)))
driver.maximize_window()
try:
    login_inp = driver.find_element(By.XPATH,ph)
    login_inp.send_keys(login)
    login_ent = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[1]/div/form/button/span/span')
    login_ent.click()
except:
    pass
#ph = '/html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[3]/button[2]/span'
ph = '/html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[3]/button/span'

tc = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,ph)))
ins = driver.find_element(By.XPATH,ph)
ins.click()
#ph = '/html/body/div[1]/div/div/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div/div/div[2]/div[2]'
ph = '/html/body/div[1]/div/div/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div/div/div[4]/div[2]'
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
ph = '/html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[1]/div[3]/div/div/input'
tc = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,ph)))
try:
    login_psw = driver.find_element(By.XPATH,ph)
    login_psw.send_keys(psw)
    login_psw1 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[2]/button/span')
    login_psw1.click()
except:
    pass
#/html/body/div[4]/div/div/div[2]/div[2]/div[3]/div/div/div/div[3]/div[2]/div[1]/div/div[2]/div[3]/div/span[1]/span/a
     #/html/body/div[4]/div/div/div[2]/div[2]/div[3]/div/div/div[1]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div
# ph = '/html/body/div[4]/div/div/div[2]/div[2]/div[3]/div/div/div[1]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[2]'
#      #/html/body/div[4]/div/div/div[2]/div[2]/div[3]/div/div/div[1]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[2]
# tc = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,ph)))
# exs = driver.find_element(By.XPATH,ph)
# exs.click()
# time.sleep(5)
# u = input('Проверка ')

#phbl = '/html/body/div[4]/div/div/div[2]/div[2]/div[3]/div/div/div/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/a[10]'
phbl = '/html/body/div[4]/div/div/div[2]/div[2]/div[3]/div/div/div[1]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/a[9]'
tc = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,phbl)))
exs = driver.find_element(By.XPATH,phbl)
print('1',exs,exs.text)
if exs.text==' Разблокировать':
    exs.click()
#/html/body/div[4]/div/div/div[2]/div[2]/div[3]/div/div/div/div[3]/div[2]/div[4]/div[4]/div[1]/span
#Вы не можете отправить сообщение этому пользователю
tc = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID,'im_editable876652489' )))
if tc:
    msg = driver.find_element(By.ID,'im_editable876652489')
    msg.send_keys('Hhello!! +1')
    time.sleep(5)
    msg.send_keys(Keys.RETURN)
    time.sleep(5)
    tc = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, phbl)))
    exs = driver.find_element(By.XPATH, phbl)
    print(exs.text)
    if exs.text == ' Заблокировать':
        exs.click()
        ph = '/html/body/div[12]/div/div[2]/div/div[3]/div[1]/div[1]/button[2]'
        tc = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, ph)))
        exs = driver.find_element(By.XPATH, ph)
        exs.click()

    #msg = driver.find_element(By.ID,'send_24__Mask')
    #msg.click()
driver.close()
