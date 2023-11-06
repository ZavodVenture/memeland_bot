from entities.Error import Error
from entities import Proxy
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')


def read_tokens():
    try:
        with open('tokens.txt') as file:
            tokens = file.read().split('\n')
            if not tokens[-1]:
                tokens = tokens[:-1]

        return tokens
    except Exception as e:
        return Error('Tokens', 'Не удалось прочитать файл с токенами', e)


def read_private_keys():
    try:
        with open('private_keys.txt') as file:
            private_keys = file.read().split('\n')
            if not private_keys[-1]:
                private_keys = private_keys[:-1]

        return private_keys
    except Exception as e:
        return Error('Private keys', 'Не удалось прочитать файл с приватными ключами', e)


def read_proxies():
    try:
        with open('proxy.txt') as file:
            proxies = file.read().split('\n')
            if not proxies[-1]:
                proxies = proxies[:-1]

            for i in range(len(proxies)):
                proxies[i] = Proxy(config['settings']['proxy_type'], *proxies[i].split(':'))

        return proxies
    except Exception as e:
        return Error('Proxy', 'Не удалось прочитать файл с прокси', e)
