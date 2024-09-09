from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

options = ChromeOptions()
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--enable-profile-shortcut-manager')
options.add_argument('--profile-directory=Profile 1')
options.add_argument('--user-data-dir=C:/1/AppData/Local/Google/Chrome/User Data')
# options.add_argument('profile-directory=C:/1/AppData/Local/Google/Chrome/User Data/Profile 1')
options.add_argument("user-agent=" + 'Chrome')
cod_email = 'admin@notify.vk.com'
cod_email_name = 'Tradeunion'
cod_email_str0 = 'на том устройстве, где авторизуетесь.'
cod_email_str1 = 'Если вы не запрашивали код, '
cod_email_subject ='Код для авторизации ВКонтакте'
cod_email_servicename = 'PyMail'
login = 'profsadokate@mail.ru'
psw = 'Htpbcnfyc!cJghjnbdktybt2'
psw_mail = 'BpKrex5kd9pv82aai5FW'

timeout = 15
mtimeout = 7
# login = 'v_derkach@inbox.ru'
# psw = 'Betelgeize#70betelgeize'
#driver = Chrome(options=options)
driver = Chrome()
driver.implicitly_wait(10)
#time.sleep(10)
driver.get("https://vk.com/im?sel=876652489")
ph = '/html/body/div[3]/div/div/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[1]/div/form/input[1]'
tc = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,ph)))
# пробовать tc без повторного find_element
driver.maximize_window()
try:
    login_inp = driver.find_element(By.XPATH,ph)
    login_inp.send_keys(login)
    login_ent = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[1]/div/form/button/span/span')
    login_ent.click()
except:
    pass
ph = []
ph.append('/html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[3]/button[2]/span')
ph.append('/html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[3]/button/span')
     #/html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[3]/button[2]/span/span
for phh in ph:
    tc = WebDriverWait(driver, mtimeout).until(EC.presence_of_element_located((By.XPATH,phh)))
    if tc:
        ph1 = phh
        break
ins = driver.find_element(By.XPATH,ph1)
ins.click()
ph = []
ph.append('/html/body/div[1]/div/div/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div/div/div[2]/div[2]')
ph.append('/html/body/div[1]/div/div/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div/div/div[4]/div[2]')
for phh in ph:
    tc = WebDriverWait(driver, mtimeout).until(EC.presence_of_element_located((By.XPATH,phh)))
    if tc:
        ph1 = phh
        break
ins = driver.find_element(By.XPATH,ph1)
ins.click()
ph = []
ph.append( '/html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[2]/div/div[1]/div/div/input')
ph.append( '/html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[2]/div/div[4]/div/div/input')
for phh in ph:
    tc = WebDriverWait(driver, mtimeout).until(EC.presence_of_element_located((By.XPATH,phh)))
    if tc:
        ph1 = phh
        break
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

# u = input('Проверка ')
phbl = []
phbl.append('/html/body/div[4]/div/div/div[2]/div[2]/div[3]/div/div/div/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/a[10]')
phbl.append('/html/body/div[4]/div/div/div[2]/div[2]/div[3]/div/div/div/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div')
phbl.append('/html/body/div[4]/div/div/div[2]/div[2]/div[3]/div/div/div[1]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/a[9]')
phbl.append('/html/body/div[4]/div/div/div[2]/div[2]/div[3]/div/div/div/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[2]')

for phh in phbl:
    tc = WebDriverWait(driver, mtimeout).until(EC.presence_of_element_located((By.XPATH,phh)))
    if tc:
        phbl1 = phh
        print(phbl1)
        break
act_mouse = ActionChains(driver)
exs = driver.find_element(By.XPATH,phbl1)
act_mouse.move_to_element(exs).perform()

print('1',exs,exs.text)
p = input('Пауза для просмотра. Введите потом любой символ ')
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
