"""
new account and manage them
"""

from selenium.webdriver.common.by import By
import time
from selenium import webdriver
import string
from random import randint, choice
import requests
import json
url = "https://old.reddit.com/register"

with open("cred.json", "r") as f:
    a = json.loads(f.read())
    API_KEY = a["API_KEY"]


def generate_user():
    with open("names.txt", "r") as f:
        names = f.read().splitlines()
        username = f"{choice(names)}_{choice(names)}_{randint(1, 10000)}"[:20]
        password = ''.join(choice(string.ascii_letters+string.digits)
                           for i in range(randint(10, 20)))
        return username, password


def get_email():
    email_driver = webdriver.Chrome()
    email_driver.get('https://getnada.com')
    email_text = email_driver.find_element(
        By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div[1]/div/div/p/span[1]/a/button').text.strip()

    return email_text, email_driver


def captcha_create_task():
    url = "https://api.capsolver.com/createTask"
    body = {
        "clientKey": API_KEY,
        "task": {
            "type": "ReCaptchaV2TaskProxyLess",
            "websiteURL": "https://old.reddit.com/register",
            "websiteKey": "6LeTnxkTAAAAAN9QEuDZRpn90WwKk_R1TRW_g-JC"
        }
    }
    res = requests.post(url, json=body)
    print(res.json())
    # assert res.json()["errorId"] == 0, Exception("ERROR: couldn't create task")
    return res.json()["taskId"]


def captcha_get_res(task_id):
    url = "https://api.capsolver.com/getTaskResult"
    body = {
        "clientKey": API_KEY,
        "taskId": task_id
    }
    res = requests.post(url, json=body)
    res_body = res.json()
    print(res_body)
    if res_body["status"] == "ready":
        solution = res_body["solution"]["gRecaptchaResponse"]
        return solution
    if (res_body["errorId"] == 1 or res_body["status"] != "ready"):
        print("cucked, waiting again")
        time.sleep(10)
        res = requests.post(url, json=body)
        res_body = res.json()
        print(res_body)
        solution = res_body["solution"]["gRecaptchaResponse"]
        return solution


def fill_user_metadata(driver, username, password):
    print("fill_user_metadata")
    driver.find_element(By.ID, 'user_reg').click()
    driver.find_element(By.ID, 'user_reg').send_keys(username)

    driver.find_element(By.ID, 'passwd_reg').click()
    driver.find_element(By.ID, 'passwd_reg').send_keys(password)

    driver.find_element(By.ID, 'passwd2_reg').send_keys(password)
    driver.find_element(By.ID, 'passwd2_reg').click()


def solving_captcha(driver):
    print('Solving captcha...')
    task_id = captcha_create_task()
    time.sleep(30)
    print("awaken ayaya")
    token = captcha_get_res(task_id)
    # print('Answer token recieved: ' + token)
    captchaInput = driver.find_element(By.ID, 'g-recaptcha-response')
    driver.execute_script(
        "arguments[0].setAttribute('style','visibility:visible;');", captchaInput)
    captchaInput.send_keys(token)
    # print('Submitting token')
    driver.find_element(
        By.XPATH, '/html/body/div[3]/div/div/div[1]/form/div[8]/button').click()


def checking_email(email_driver):
    print('Checking email...')
    retry = 0
    while retry < 3:
        try:
            retry += 1
            time.sleep(30)
            email_driver.find_element(
                By.XPATH,
                '/html/body/div[1]/div/div/div/div[2]/div/div[1]/div/div/div[1]/div[2]/table/tbody/tr/td[1]/a').click()
            frame = email_driver.find_element(By.ID, 'the_message_iframe')
            email_driver.switch_to.frame(frame)
            email_driver.find_element(
                By.XPATH, '/html/body/center/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/a').click()

            next_handle = [handle for handle in email_driver.window_handles
                           if handle != email_driver.current_window_handle][0]
            email_driver.switch_to.window(next_handle)
            email_driver.find_element(
                By.XPATH, "/html/body/div[3]/div[1]/form/button").click()
            return email_driver
        except Exception as e:
            print(e)


def create_account():
    try:
        driver = webdriver.Chrome()

        username, password = generate_user()
        print('Creating account with username: ' +
              username + ' and password: ' + password + '...')

        driver.delete_all_cookies()

        driver.get("https://old.reddit.com/register")

        fill_user_metadata(driver, username, password)

        retry = 0
        email = ""
        while retry < 3:
            print(f"attempt {retry} :", end="")
            email, email_driver = get_email()
            print(f"res = {email}")
            if "@" in email:
                break

        if not email or email == " ":
            raise Exception("ERROR: can't get email ")

        print('Entering email...')
        driver.find_element(By.ID, 'email_reg').click()
        driver.find_element(By.ID, 'email_reg').send_keys(email)

        solving_captcha(driver)
        time.sleep(30)
        checking_email(email_driver)

        with open("cookies.txt", "a") as f:
            f.write(f"\n{username}, {password}, {email}")
        print("SUCCESS")

    except Exception as e:
        print(f'Error {e}. wac...')
        # time.sleep(120)
        create_account()
    finally:
        if driver:
            driver.close()
        if email_driver:
            email_driver.close()


for i in range(20):
    create_account()
