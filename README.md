# Memeland Bot

Бот для автоматического выполнения заданий проекта Memeland.

## Подготовка

Перед запуском скрипта нужно выполнить следующие действия:

1. [Создать](https://app.adspower.com/registration) аккаунт adspower и [установить](https://adspower.com/download) приложение (подписку покупать необязательно, у AdsPower есть триал версия, выбираем самую жирную)
2. Войти в установленное приложение с созданным аккаунтом
3. Создать аккаунт на [FirstCaptcha](https://1stcaptcha.com/) и пополнить баланс (нужно для разморозки твиттера после изменения имени)

Для выполнения заданий Memeland требуются твиттер аккаунты с минимум пятью подписчиками и возрастом не меньше одного месяца, учесть при покупке.

Также рекомендуется использовать разные прокси, но скрипт может работать без них.

## Заполнение файлов

Перед запуском нужно положить все необходимые для работы скрипта данные в соответствующие файлы.

### Токены твиттер
Открываем файл **tokens.txt** и вставляем в него токены аккаунтов. Формат: одна строка = один токен

Пример токена: `21845e7293c6d4e812019fda1d89b29e3b6cb164`

### Приватные ключи от кошельков
Открываем файл **private_keys.txt** и вставляем в него приватные ключи кошельков. Формат: одна строка = один ключ.

В Memeland нельзя привязать один кошелёк к двум аккаунтам, поэтому все приватные ключи должны быть уникальными.

Пример ключа: `63faad5387cfce7f1b8e4bf87972b6d8c65ebc055a44bd548b0c748954a4c7b9`

### Прокси
Этот этап можно пропустить и оставить файл пустым, если Вы не собираетесь использовать прокси _(что настоятельно не рекомендуется)_

Прокси загружаются в файл **proxies.txt**. Формат: одна строка = один прокси

Прокси загружаются в следующем виде: `ip:port:user:password`

## Настройка конфига

В файле **config.ini** содержатся настройки скипта:
1. **fcaptcha_key** - API-ключ FirstCaptcha. Можно найти [тут](https://1stcaptcha.com/dashboard/apikey)
2. **proxy_type** - тип используемых прокси. Точно поддерживаются socks5, http, https прокси
3. **threads** - количество одновременно работающих аккаунтов. Зависит от мощности ПК, рекомендуется 2-3 
4. **headless** - режим запуска браузера. `1` - невидимый, `0` - обычный
5. **sleep_between_tasks** - время между выполнением заданий. Например: `5` - фиксированно пять секунд; `5-10` - от пяти до десяти секунд
6. **invite_code** - код пригласившего формата MVP.../Captain.../Potatoz... Если кода нет, его можно не указывать, тогда задание с кодом не будет выполнено.
7. **unfreeze_attempts** - количество попыток разморозки аккаунта твиттер после изменения имени

## Запуск скрипта

После всех подготовок и настроек скрипт можно запускать

1. Установить [Python 3.8](https://www.python.org/downloads/release/python-380/)
2. Открыть терминал, перейти в папку проекта и установить зависимости командой `pip install -r requirements.txt`
3. Запустить файл скрипт командой `python main.py`

[Видео с демонстрацией запуска](https://youtu.be/H7h_fE51mN0)
