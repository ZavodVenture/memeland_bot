from datetime import datetime
import re


def log(prefix, message):
    now = datetime.now().strftime('%m-%d %H:%M:%S')

    print(f'[{now}] {prefix} - {message}')

    message = re.sub(r"\x1b\[[0-9;]*m", "", str(message))

    with open(f'logs/{prefix}.txt', 'a', encoding='utf-8') as file:
        file.write(f'[{now}] - {message}\n')
        file.close()
