from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def get_all_cookies():
    with open("cookies.txt", "r") as f:
        return f.read().splitlines()


def reddit_action(driver):
    driver.get('https://www.reddit.com/r/MonsterHunter/comments/12hqpzh/is_there_a_way_to_play_mho_or_frontier_these_days/')
    time.sleep(5)
    down_vote_button = driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[3]/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[2]/div[3]/div[1]/button[2]")
    down_vote_button.click()
    time.sleep(2)


for cookie in get_all_cookies():
    # set up the webdriver
    try:
        driver = webdriver.Chrome()

        # navigate to Reddit's homepage
        driver.get('https://www.reddit.com')

        # add the session cookie to the webdriver instance

        session_cookie = {
            'name': 'reddit_session',
            'value': cookie
        }
        driver.add_cookie(session_cookie)

        # refresh the page to log in using the session cookie
        reddit_action(driver)
        # close the webdriver
    except Exception as e:
        print(f"ERROR: {cookie}, {e}")
    finally:
        driver.quit()
