options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=" + PROFILE)
options.add_argument("user-agent=" + USER_AGENT)

# driver = webdriver.Chrome('chromedriver', chrome_options=options)
# driver.get("https://vk.me/chat")
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