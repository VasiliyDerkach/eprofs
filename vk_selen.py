from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.by import By
import time
options = ChromeOptions()
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--enable-profile-shortcut-manager')
options.add_argument('--profile-directory=Profile 1')
options.add_argument('--user-data-dir=C:/1/AppData/Local/Google/Chrome/User Data')
# options.add_argument('profile-directory=C:/1/AppData/Local/Google/Chrome/User Data/Profile 1')
options.add_argument("user-agent=" + 'Chrome')
#driver = Chrome(options=options)
driver = Chrome()

#time.sleep(10)
driver.get("https://vk.com/feed")
# driver1 = Chrome()
# driver1.get("https://vk.com/feed")
#login    /html/body/div[3]/div/div/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[1]/div/form/input[1]
ans = input('После авторизации ВК введите Y ')
#time.sleep(40)

if ans=='Y':
    driver.get("https://vk.com/search/people?group_id=176956684")
    try:

        #lst1 = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[1]/div/div[4]/aside/div/a/div/span[1]')
        #lst1.click()
        subs = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[1]/section[2]/div[2]/div/div/section/div/div[5]/div[1]/div/div/div[1]/div/a')
        print(subs.get_property('href'))
        subs = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[1]/section[2]/div[2]/div/div/section/div/div[5]/div[1]/div/div/div[2]/div[1]/div/div[1]/div/a/div')
        print(subs.text)

        # for i,t in enumerate(subs):
        #     print(i,t.text)

    except Exception as e:
        print(e)
        flag_el = False
    pass
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