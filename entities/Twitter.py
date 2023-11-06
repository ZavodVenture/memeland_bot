from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from entities.Error import Error
from time import sleep
from helpers import solve_captcha
from selenium.webdriver import ActionChains
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')


class Twitter:
    driver: webdriver.Chrome = None
    username = None

    def __init__(self, twitter_token, ws, driver_path):
        self.token = twitter_token
        self.ws = ws
        self.driver_path = driver_path

    def connect(self):
        try:
            options = Options()
            options.add_experimental_option("debuggerAddress", self.ws)
            service = Service(executable_path=self.driver_path)
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.maximize_window()
        except Exception as e:
            return Error('Driver connection error', 'Не удалось подключиться к открытому профилю', e)

    def login_twitter(self):
        try:
            self.driver.get('https://twitter.com/')
            self.driver.add_cookie({'name': 'auth_token', 'value': self.token})
            self.driver.refresh()
            try:
                WebDriverWait(self.driver, 5).until(ec.url_to_be('https://twitter.com/home'))
            except:
                return Error('Twitter', f'Не удалось залогиниться в твиттер с токеном {self.token}')

            profile_button = WebDriverWait(self.driver, 15).until(ec.presence_of_element_located((By.XPATH, '//a[@data-testid="AppTabBar_Profile_Link"]')))

            self.username = profile_button.get_attribute('href').split('/')[-1]

            self.driver.get('https://api.twitter.com/oauth/authenticate?oauth_token=fQCw3QAAAAABqrFiAAABi5bqJjA')
            self.driver.add_cookie({'name': 'auth_token', 'value': self.token})
        except Exception as e:
            return Error('Twitter', 'Произошла непредвиденная ошибка при логине в твиттер', e)

    def follow_account(self, username):
        try:
            self.driver.get(f'https://twitter.com/{username}')
            try:
                WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.XPATH, '//div[@data-testid="BottomBar"]//div[@role="button"]'))).click()
            except:
                pass

            try:
                # Кнопка "Yes, view profile" для NSFW аккаунтов
                WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div[2]/div/div[3]'))).click()
            except:
                pass

            element = WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//div[@data-testid="placementTracking"]//div[contains(@data-testid, "follow")]')))
            element_attribute = element.get_attribute('data-testid')
            if '-unfollow' in element_attribute:
                return Error('Twitter', f'Подписка на {username} уже выполнена')
            else:
                element.click()

            sleep(2)
        except Exception as e:
            return Error('Twitter', f'Произошла непредвиденная ошибка при попытке подписаться на {username}', e)

    def unfreeze_account(self):
        try:
            captcha_key = solve_captcha()
            if isinstance(captcha_key, type(Error)):
                return captcha_key

            frame = WebDriverWait(self.driver, 15).until(ec.presence_of_element_located((By.ID, 'arkose_iframe')))
            self.driver.switch_to.frame(frame)
            self.driver.execute_script(f'parent.postMessage(JSON.stringify({{eventId:"challenge-complete",payload:{{sessionToken:"{captcha_key}"}}}}),"*")')
            WebDriverWait(self.driver, 15).until(ec.url_contains('https://twitter.com/home'))
            self.driver.get('https://twitter.com/home')
        except Exception as e:
            return Error('Twitter', 'Не удалось разморозить аккаунт', e)

    def add_to_name(self, thing_to_add):
        try:
            self.driver.get('https://twitter.com/settings/profile')
            sleep(1)
            self.driver.refresh()

            WebDriverWait(self.driver, 15).until(ec.presence_of_element_located((By.XPATH, '//input[@name="displayName"]'))).send_keys(f' {thing_to_add}')
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//div[@data-testid="Profile_Save_Button"]'))).click()
            WebDriverWait(self.driver, 15).until(ec.url_to_be('https://twitter.com/home'))
            self.driver.refresh()
            try:
                WebDriverWait(self.driver, 5).until(ec.url_to_be('https://twitter.com/account/access'))
            except:
                pass
            else:
                for _ in range(int(config['settings']['unfreeze_attempts'])):
                    r = self.unfreeze_account()
                    if not isinstance(r, Error):
                        break
                if isinstance(r, Error):
                    return r
        except Exception as e:
            return Error('Twitter', 'Не удалось изменить имя', e)

    def create_twit(self, text):
        try:
            ac = ActionChains(self.driver)
            self.driver.get('https://twitter.com/intent/tweet')
            sleep(1)
            self.driver.refresh()

            text_element = WebDriverWait(self.driver, 15).until(ec.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetTextarea_0"]')))
            ac.move_to_element(text_element).click(text_element).send_keys(text).perform()

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//div[@data-testid="tweetButton"]'))).click()

            WebDriverWait(self.driver, 15).until(ec.url_to_be('https://twitter.com/home'))
        except Exception as e:
            return Error('Twitter', 'Не удалось сделать твит', e)
