from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

#time.sleep(10)
driver.get("https://vk.com/search/people?group_id=176956684")
try:
    login_inp = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[1]/div/form/input[1]')
    login_inp.send_keys(login)
    login_ent = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[1]/div/form/button/span/span')
    login_ent.click()
except:
    pass
#/html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[3]/button[2]/span/span/span

# login_oth = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div/div/div[2]/div[3]/svg')
# login_oth.click()
# driver1 = Chrome()
# driver1.get("https://vk.com/feed")
#login
# 1code /html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[2]/div/input
# другой способ подтверждения
# ans = input('После ввода разового ключа ВК введите y ')
try:
    login_psw = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[1]/div[3]/div/div/input')
    login_psw.send_keys(psw)
    login_psw1 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[2]/button/span')
    login_psw1.click()
except:
    pass
# time.sleep(15)
# if ans=='y':
    # driver.get("https://vk.com/search/people?group_id=176956684")
    # ans = input('После загрузки страницы нажмите y')
    # driver.get("https://web.vk.me/")
    # ph = '/html/body/div[2]/div/div/div[2]/div[2]/div/div[2]/div[2]'
    # subs = driver.find_element(By.XPATH, ph)
    # subs.click()
    # ph1 = '/html/body/div[1]/div/div/div/div/div[1]/div/div/div/div/div/form/div[4]/button/span/span/span/span'
    # subs = driver.find_element(By.XPATH, ph1)
    # subs.click()
    #+ кнопки продолжить + выбор первого профиля
    # if ans == 'y':
        # ph = '/html/body/div[2]/div[1]/div[1]/div[1]/div[1]/section/div[1]/div/div[2]/div/div/div[1]/input'
        # subs = driver.find_element(By.ID, 'search-:vkme_reforged-rootr6:')
        # subs.send_keys('id876652489')
        # ph1 = '/html/body/div[2]/div[1]/div[1]/div[1]/div[1]/section/div[2]/div[2]/div[1]/div/div/div/div[2]/button/header/div'
        # subs = driver.find_element(By.XPATH, ph1)
        # subs.click()
        # ph2 = '/html/body/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/div/div[1]/div[3]/div[2]/div/div/div[2]/div/div'
        #
        #
        # ans = input('После загрузки страницы нажмите y')
        # if ans == 'y':
        #     subs = driver.find_element(By.NAME, 'Напишите сообщение...')
        #     subs.send_keys('id876652489+++' + '\n')
        #     pass

    ##driver.get("https://vk.com/search/people?group_id=176956684")
ans = input('После загрузки страницы группы нажмите y')
if ans == 'y':
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    # time.sleep(5)
    # for _ in range(2):
    #     driver.find_element(By.TAG_NAME,'html').send_keys(Keys.END)
    # time.sleep(5)
    # ph = '/html/body/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[1]/section[2]/span/div'
         #/html/body/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[1]/section[2]/span/div/div[1]/div[3]/div[1]/a
         #/html/body/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[1]/section[2]/span/div/div[5]/div[3]/div[1]/a
         #/html/body/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[1]/section[2]/span/div/div[151]/div[3]/div[1]/a
    n = 1
    p = 0
    while True:
        try:
            ph = f'/html/body/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[1]/section[2]/span/div/div[{str(n)}]/div[3]/div[1]/a'
            #print(ph)
            subs = driver.find_element(By.XPATH, ph)

            print(n,subs.text)
            #/html/body/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[1]/section[2]/span/div/div[4]/div[1]/a
            #href = /html/body/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[1]/section[2]/span/div/div[1]/div[3]/div[1]/a
            n += 1
            p = 0
        except:
            if p>2:
                break
            else:
                driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.END)
                time.sleep(3)
                p += 1
    print(n)
    # for _ in range(50):
    #     driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.END)
    # j = 0
    # for t in subs:
    #     print(t.text,t.get_property('href'))
    #     j +=1
    # print(j)
    # print('__________________')
    # ph = '/html/body/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[1]/section[2]/span/div'
    # subs = driver.find_elements(By.XPATH, ph)
    # for t in subs:
    #     print(t.text,t.get_property('href'))
    #     print(t.__dir__())
        # scn = 1
        #
        # cnt =0
        # endlst = True
        # while endlst:
        #     row = 1
        #     s ='[' + str(scn) + ']'
        #     st = '' if scn == 1 else s
        #     while True:
        #         try:
        #
        #             srow= str(row)
        #             print(st,srow)
        #             ph = f'/html/body/div[4]/div/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[1]/section[2]/div[2]/div/div/section{st}/div/div[{srow}]/div[1]/div/div/div[1]/div/a'
        #             print(ph)
        #             subs = driver.find_element(By.XPATH, ph)
        #             print(subs.get_property('href'))
        #             ph1 = f'/html/body/div[4]/div/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[1]/section[2]/div[2]/div/div/section{st}/div/div[{srow}]/div[1]/div/div/div[2]/div[1]/div/div[1]/div/a/div'
        #
        #             print(ph1)
        #             cnt += 1
        #             row += 1
        #             subs = driver.find_element(By.XPATH, ph1)
        #             print(subs.text)
        #
        #
        #
        #         except Exception as e:
        #             scn +=1
        #             if row==1:
        #                 endlst = False
        #             #print(e)
        #
        #             break
        #
        #         pass
        # print(cnt)
#driver1.close()
driver.close()
#driver.maximize_window()
#time.sleep(20)

#     # начинается попытка логина в случае редиректа
#     try:
#         WebDriverWait(driver, 10).until(
#             ec.presence_of_element_located((By.CSS_SELECTOR, ".login_header"))
#         )
#         login = driver.find_element_by_id("email")
#         login.send_keys(USERNAME_VK)
#
#         login = driver.find_element_by_id("pass")
#         login.send_keys(PASSWORD_VK)
#         login.send_keys(Keys.RETURN)
#
#         driver.get("https://vk.me/chat")
#     except TimeoutException:
#         pass