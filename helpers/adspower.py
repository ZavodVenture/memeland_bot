import requests
from time import sleep
from entities import Proxy
from entities.Error import Error
from threading import Lock

API_URl = 'http://localhost:50325/'

lock = Lock()


def check_adspower():
    try:
        lock.acquire()
        requests.get(API_URl + 'status').json()
        sleep(2)
        lock.release()
    except Exception as e:
        lock.release()
        return Error('Connection error', 'API недоступен. Проверьте, запущен ли AdsPower', e)
    else:
        return True


def get_group_id(group_name):
    args = {
        'group_name': group_name
    }

    try:
        lock.acquire()
        r = requests.get(API_URl + 'api/v1/group/list', params=args).json()
        sleep(2)
        lock.release()
    except Exception as e:
        lock.release()
        return Error('Getting group error', 'Не удалось узнать, существует ли группа', e)
    else:
        if r['code'] != 0:
            return Error('Getting group error', r['msg'])
        else:
            if r['data']['list']:
                return r['data']['list'][0]['group_id']
            else:
                return None


def create_group(name):
    try:
        lock.acquire()
        r = requests.post(API_URl + 'api/v1/group/create', json={'group_name': name}).json()
        sleep(2)
        lock.release()
    except Exception as e:
        lock.release()
        return Error('Group creation error', 'Возникла ошибка при отправке запроса AdsPower', e)
    else:
        if r['code'] != 0:
            return Error('Group creation error', r["msg"])
        else:
            return r['data']['group_id']


def create_profile(proxy: Proxy = None, group_id='0'):
    if proxy:
        account_data = {
            'group_id': group_id,
            'user_proxy_config': {
                'proxy_soft': 'other',
                'proxy_type': 'socks5',
                'proxy_host': proxy.ip,
                'proxy_port': proxy.port,
                'proxy_user': proxy.login,
                'proxy_password': proxy.password
            }
        }
    else:
        account_data = {
            'group_id': group_id,
            'user_proxy_config': {
                'proxy_soft': 'no_proxy'
            }
        }

    try:
        lock.acquire()
        r = requests.post(API_URl + 'api/v1/user/create', json=account_data).json()
        sleep(2)
        lock.release()
    except Exception as e:
        lock.release()
        return Error('Connection error', 'Возникла ошибка при отправке запроса AdsPower', e)
    else:
        if r['code'] != 0:
            return Error('Profile creation error', r['msg'])
        else:
            return r['data']['serial_number']


def run_profile(serial_number, headless=False):
    args = {
        'serial_number': serial_number,
        'ip_tab': 0
    }

    if headless:
        args['launch_args'] = "[\"--headless=new\"]"

    try:
        lock.acquire()
        r = requests.get(API_URl + 'api/v1/browser/start', params=args).json()
        sleep(2)
        lock.release()
    except Exception as e:
        lock.release()
        return Error('Connection error', 'Возникла ошибка при отправке запроса AdsPower', e)
    else:
        if r['code'] != 0:
            return Error('Profile launching error', r['msg'])
        else:
            ws = r["data"]["ws"]["selenium"]
            driver_path = r["data"]["webdriver"]
            return ws, driver_path


def close_profile(serial_number):
    args = {
        'serial_number': serial_number
    }

    try:
        lock.acquire()
        requests.get(API_URl + 'api/v1/browser/stop', params=args)
        sleep(2)
        lock.release()
    except:
        lock.release()


def delete_profile(serial_number):
    args = {
        'serial_number': serial_number
    }

    try:
        lock.acquire()
        r = requests.get(API_URl + '/api/v1/user/list', params=args).json()
        sleep(2)
        lock.release()
    except Exception as e:
        lock.release()
        return Error('Deleting error', f'Не удалось найти профиль adspower {serial_number}', e)

    try:
        lock.acquire()
        user_id = r['data']['list'][0]['user_id']
        requests.post(API_URl + '/api/v1/user/delete', json={'user_ids': [user_id]})
        sleep(2)
        lock.release()
    except:
        lock.release()
