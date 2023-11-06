from entities import Twitter, Meme, Proxy
from entities.Error import Error
from helpers import adspower, readers, log, convert_ranges_to_array
from colorama import Fore, init
from configparser import ConfigParser
from random import choice
from time import sleep
from os import system, path, mkdir
from threading import Thread

config = ConfigParser()
config.read('config.ini')

max_threads = int(config['settings']['threads'])
active_threads = 0

code = config['settings']['invite_code']


def worker(twitter_token, private_key, proxy: Proxy = None, invite_code=None):
    global active_threads

    log(twitter_token, 'Начинаем работу')
    try:
        serial_number = adspower.create_profile(proxy)
        if isinstance(serial_number, Error):
            log(twitter_token, serial_number)
            return

        launch_result = adspower.run_profile(serial_number, int(config['settings']['headless']))
        if isinstance(launch_result, Error):
            log(twitter_token, launch_result)
            return

        ws, driver_path = launch_result

        t = Twitter(twitter_token, ws, driver_path)

        r = t.connect()
        if isinstance(r, Error):
            log(twitter_token, r)
            return
        log(twitter_token, 'успешное подключение к браузеру')

        r = t.login_twitter()
        if isinstance(r, Error):
            log(twitter_token, r)
            return
        log(twitter_token, 'успешный вход в твиттер')

        m = Meme(t, private_key)

        r = m.login_meme(proxy)
        if isinstance(r, Error):
            log(twitter_token, r)
            return
        log(twitter_token, 'успешный вход в Memeland')

        tasks = m.get_tasks()
        if isinstance(tasks, Error):
            log(twitter_token, tasks)
            return

        sleep_aray = convert_ranges_to_array(config['settings']['sleep_between_tasks'])

        for task in tasks:
            if 'follow' in task:
                username = task.replace('follow', '')
                r = m.follow_account(username)
                if isinstance(r, Error):
                    log(twitter_token, r)
                else:
                    log(twitter_token, f'Подписались на {username}')
            elif task == 'linkWallet':
                r = m.connect_wallet()
                if isinstance(r, Error):
                    log(twitter_token, r)
                else:
                    log(twitter_token, f'Привязали кошелёк')
            elif task == 'shareMessage':
                r = m.tweet()
                if isinstance(r, Error):
                    log(twitter_token, r)
                else:
                    log(twitter_token, f'Написали твит')
            elif task == 'twitterName':
                r = m.twitter_name()
                if isinstance(r, Error):
                    log(twitter_token, r)
                else:
                    log(twitter_token, f'Изменили имя')
            elif task == 'inviteCode':
                if invite_code:
                    r = m.ref_code(invite_code)
                    if isinstance(r, Error):
                        log(twitter_token, r)
                    else:
                        log(twitter_token, f'Ввели реферальный код')
            elif task == 'coingecko':
                r = m.coingecko()
                if isinstance(r, Error):
                    log(twitter_token, r)
                else:
                    log(twitter_token, f'Выполнили задание с coingecko')
            else:
                log(twitter_token, Error('Meme', f'Неизвестное задание: {task}. Будет добавлено в ближайшем обновлении.'))

            sleep(choice(sleep_aray))
        log(twitter_token, f'Аккаунт готов. {twitter_token}:{private_key}{f":{proxy}" if proxy else ""}\n')
    finally:
        active_threads -= 1
        if 'serial_number' in locals():
            adspower.close_profile(serial_number)
            adspower.delete_profile(serial_number)


def init_exit():
    input('\nНажмите Enter, чтобы выйти...')
    exit()


def clear():
    system('cls')


def main():
    global active_threads

    adspower_status = adspower.check_adspower()
    if isinstance(adspower_status, Error):
        print(adspower_status)
        init_exit()

    tokens = readers.read_tokens()
    if isinstance(tokens, Error):
        print(tokens)
        init_exit()

    private_keys = readers.read_private_keys()
    if isinstance(private_keys, Error):
        print(private_keys)
        init_exit()

    proxies = readers.read_proxies()
    if isinstance(proxies, Error):
        print(proxies)
        proxies = []

    if len(tokens) != len(private_keys) or ((len(private_keys) != len(proxies)) if proxies else False):
        print(Error('Data error', 'Число прокси, токенов и приватных ключей не равно'))
        init_exit()

    while 1:
        clear()
        print(f'Загружено {Fore.CYAN}{len(tokens)}{Fore.RESET} токенов, {Fore.CYAN}{len(private_keys)}{Fore.RESET} приватный ключей, {Fore.CYAN}{len(proxies)}{Fore.RESET} прокси\n')

        print('Выберите действие:\n\n'
              '[1] - Выполнение заданий Memeland\n'
              '[0] - Выход\n')

        user_choice = input('Выбор: ')

        if user_choice == '1':
            clear()
            for i in range(len(tokens)):
                while active_threads >= max_threads:
                    continue

                active_threads += 1
                t = Thread(target=worker, args=(tokens[i], private_keys[i], proxies[i] if proxies else None, code if code else None))
                t.start()

            while active_threads != 0:
                continue

            input('\nРабота с токенами завершена, результат сохранён в папку logs. Нажмите Enter, чтобы продолжить')
        elif user_choice == '0':
            break

    clear()
    init_exit()


if __name__ == '__main__':
    init()
    if not path.exists('logs'):
        mkdir('logs')
    main()
