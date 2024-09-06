from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
options = ChromeOptions()
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--enable-profile-shortcut-manager')
options.add_argument('--profile-directory=Profile 1')
options.add_argument('--user-data-dir=C:/1/AppData/Local/Google/Chrome/User Data')
# options.add_argument('profile-directory=C:/1/AppData/Local/Google/Chrome/User Data/Profile 1')
options.add_argument("user-agent=" + 'Chrome')
# login = 'profsadokate@mail.ru'
# psw = 'Htpbcnfyc!cJghjnbdktybt2'
login = 'v_derkach@inbox.ru'
psw = 'Betelgeize#70betelgeize'
#driver = Chrome(options=options)
driver = Chrome()
timeout = 15
#time.sleep(10)
driver.get("https://vk.com/search/people?group_id=176956684")

# time.sleep(15)
#ans = input('После загрузки страницы группы нажмите y')
n = 1
p = 0
ph1 = f'/html/body/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[1]/section[2]/span/div/div[1]/div[3]/div[1]/a'
tc = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH,ph1 ))
            )

while True:
    try:
        ph = f'/html/body/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[1]/section[2]/span/div/div[{str(n)}]/div[3]/div[1]/a'
        #print(ph)
        if ph1==ph and tc:
            subs = tc
        else:
            subs = driver.find_element(By.XPATH, ph)
        tc = None
        ph1 = ''
        print(n,subs.text)
        ph = f'/html/body/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[1]/section[2]/span/div/div[{str(n)}]/div[1]/a'
        subs = driver.find_element(By.XPATH, ph)
        print(subs.get_property('href'))
        n += 1
        p = 0
    except:

        driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.END)
        #time.sleep(3)
        ph1 = f'/html/body/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[1]/section[2]/span/div/div[{str(n+1)}]/div[3]/div[1]/a'
        try:
            ec1 = EC.presence_of_element_located((By.XPATH,ph1 ))

        except:
            break
        tc = WebDriverWait(driver, timeout).until(ec1)
        if tc:
            p += 1
        else:
            break
print(n)
driver.close()
