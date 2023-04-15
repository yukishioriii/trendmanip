from selenium import webdriver
from selenium.webdriver.common.by import By

import time


def get_all_account():
    with open("accounts.txt", "r") as f:
        return [[j.strip() for j in i.split(",")] for i in f.read().splitlines()]


for account in get_all_account():
    driver = webdriver.Chrome()
    try:
        a, b, email = account
        driver.get('https://www.reddit.com/login')

        # enter your login credentials
        username = driver.find_element(By.NAME, 'username')
        username.send_keys(a)
        password = driver.find_element(By.NAME, 'password')
        password.send_keys(b)

        # submit the login form
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        submit_button.click()

        # wait for the login process to complete
        time.sleep(5)

        # retrieve the session cookie
        session_cookie = driver.get_cookie('reddit_session')

        with open("cookies.txt", "a") as f:
            f.write(f"\n{session_cookie['value']}")
    except Exception as e:
        a, b, email = account
        print(f"ERROR with account: {a}, {e}")
    finally:
        driver.quit()
