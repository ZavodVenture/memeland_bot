from entities import Twitter, Proxy
from entities.Error import Error
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from json import loads

from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_account.messages import encode_defunct
from requests import Session

from helpers import get_session
from web3.auto import w3


class Meme:
    session: Session = None

    def __init__(self, twitter: Twitter, private_key):
        self.twitter = twitter
        self.driver = twitter.driver
        self.account: LocalAccount = Account.from_key(private_key)

    def login_meme(self, proxy: Proxy = None):
        try:
            self.driver.get('https://www.memecoin.org/farming')
            WebDriverWait(self.driver, 15).until(ec.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div/div/div/div[3]/div/div[4]/div/div/div/div[1]/div[3]/div[1]/div/div/div'))).click()
            try:
                WebDriverWait(self.driver, 5).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="allow"]'))).click()
            except:
                pass
            finally:
                WebDriverWait(self.driver, 15).until(ec.url_to_be('https://www.memecoin.org/farming'))
                WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div/div/div/div[3]/div/div[4]/div/div/div[1]/div/div[2]/div[1]/div[2]/div[1]/p/span')))

            while not self.get_access_token():
                continue

            token = self.get_access_token()

            self.session = get_session(token, str(proxy) if proxy else None)
            self.driver.refresh()
        except Exception as e:
            return Error('Memeland', 'Не удалось войти в аккаунт', e)

    def get_access_token(self):
        script = "return localStorage['meme-farming-store']"
        result = loads(self.driver.execute_script(script))
        return result['state']['jwt']['accessToken']

    def connect_wallet(self):
        try:
            message = 'This wallet willl be dropped $MEME from your harvested MEMEPOINTS. ' \
                      'If you referred friends, family, lovers or strangers, ' \
                      'ensure this wallet has the NFT you referred.\n\n' \
                      'But also...\n\n' \
                      'Never gonna give you up\n' \
                      'Never gonna let you down\n' \
                      'Never gonna run around and desert you\n' \
                      'Never gonna make you cry\n' \
                      'Never gonna say goodbye\n' \
                      'Never gonna tell a lie and hurt you", "\n\n' \
                      f'Wallet: {self.account.address[:5]}...{self.account.address[-4:]}\n' \
                      f'X account: @{self.twitter.username}'
            signature = w3.eth.account.sign_message(encode_defunct(text=message),
                                                    private_key=self.account.key).signature.hex()

            try:
                r = self.session.post(url='https://memefarm-api.memecoin.org/user/verify/link-wallet',
                                      json={
                                          'address': self.account.address,
                                          'delegate': self.account.address,
                                          'message': message,
                                          'signature': signature
                                      })

            except Exception as e:
                return Error('Memeland', 'Не удалось подтвердить коннект кошелька', e)

            if r.json()['status'] == 'verefication_failed':
                return Error('Memeland', 'Не удалось подтвердить коннект кошелька')
            elif r.json()['status'] == 401 and r.json().get('error') and r.json()['error'] == 'unauthorized':
                return Error('Memeland', 'Аккаунт memeland не авторизован')

        except Exception as e:
            return Error('Memeland', 'Непредвиденная ошибка при коннекте кошелька', e)

    def get_tasks(self):
        try:
            result = self.session.get(url='https://memefarm-api.memecoin.org/user/tasks').json()

            tasks = []
            for task in result['tasks'] + result['timely']:
                if not task['completed']:
                    tasks.append(task['id'])

            return tasks
        except Exception as e:
            return Error('Memeland', 'Непредвиденная ошибка при получении заданий', e)

    def follow_account(self, username):
        try:
            r = self.twitter.follow_account(username)
            if isinstance(r, Error):
                return r

            r = self.session.post(url='https://memefarm-api.memecoin.org/user/verify/twitter-follow',
                                  json={'followId': f'follow{username}'}).json()

            if r['status'] != 'success':
                return Error('Memeland', f'Мемеленд не засчитал подписку на {username}')
        except Exception as e:
            return Error('Memeland', f'Непредвиденная ошибка при выполнении задания подписки на {username}', e)

    def coingecko(self):
        try:
            r = self.session.post(url='https://memefarm-api.memecoin.org/user/verify/claim-task/coingecko',
                                  json={}).json()

            if r['status'] != 'success':
                return Error('Memeland', 'Не удалось выполнить задание с coingecko')
        except Exception as e:
            return Error('Memeland', 'Не удалось выполнить задание с coingecko')

    def tweet(self):
        try:
            text = f"Hi, my name is @{self.twitter.username}, and I’m a $MEME (@Memecoin) farmer at @Memeland.\n\n" \
                   "On my honor, I promise that I will do my best to do my duty to my own bag, and to farm #MEMEPOINTS at all times.\n\n" \
                   "It ain’t much, but it’s honest work. 🧑\u200d🌾"
            r = self.twitter.create_twit(text)
            if isinstance(r, Error):
                return r

            r = self.session.post(url='https://memefarm-api.memecoin.org/user/verify/share-message').json()

            if r['status'] != 'success':
                return Error('Memeland', 'Не удалось подтвердить выполнения задания с твитом')
        except Exception as e:
            return Error('Memeland', 'Нерпедвиденная ошибка при выполнении задания с твитом', e)

    def twitter_name(self):
        try:
            r = self.twitter.add_to_name(' ❤️ Memecoin')
            if isinstance(r, Error):
                return r

            r = self.session.post(url='https://memefarm-api.memecoin.org/user/verify/twitter-name').json()

            if r['status'] != 'success':
                return Error('Memeland', 'Не удалось подтвердить изменение имени в твиттере')
        except Exception as e:
            return Error('Memeland', 'Непредвиденная ошибка при выполнении задания с именем', e)

    def ref_code(self, code):
        try:
            r = self.session.post(url='https://memefarm-api.memecoin.org/user/verify/invite-code',
                                  json={'code': code}).json()
            if r['status'] != 'success':
                return Error('Memeland', 'Не удалось выполнить задание с реферальным кодом')
        except Exception as e:
            return Error('Memeland', 'Непредвиденная ошибка при выполнении задания с реферальным кодом')