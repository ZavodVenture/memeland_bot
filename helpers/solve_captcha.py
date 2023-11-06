from entities import Error
from configparser import ConfigParser
import requests
from time import sleep

config = ConfigParser()
config.read('config.ini')


def get_task_result(task_id):
    data = {
        'apikey': config['settings']['fcaptcha_key'],
        'taskId': task_id
    }

    while 1:
        r = requests.get(url='https://api.1stcaptcha.com/getresult', params=data).json()
        if r['Code'] != 0:
            return Error('Captcha', 'Не удалось получить решение капчи')
        if r['Status'] in ('PROCESSING', 'PENDING'):
            sleep(1)
            continue

        return r['Data']['Token']


def solve_captcha():
    public_key = '0152B4EB-D2DC-460A-89A1-629838B529C9'
    website_url = 'https://twitter.com/account/access'

    data = {
        'apikey': config['settings']['fcaptcha_key'],
        'sitekey': public_key,
        'siteurl': website_url
    }

    r = requests.get(url='https://api.1stcaptcha.com/funcaptchatokentask', params=data).json()
    if r['Code'] != 0:
        return Error('Captcha', 'Не удалось отправить задание на решение капчи')

    task_id = r['TaskId']

    return get_task_result(task_id)
