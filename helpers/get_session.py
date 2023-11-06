from requests import Session
from random import choice


def get_session(meme_token, proxy=None):
    session = Session()
    session.headers = {
        'user-agent': choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 OPR/95.0.0.0'
        ]),
        'accept-language': 'ru,en;q=0.9,vi;q=0.8,es;q=0.7,cy;q=0.6',
        'origin': 'https://www.memecoin.org',
        'referer': 'https://www.memecoin.org/',
        'authorization': f'Bearer {meme_token}'
    }

    if proxy:
        session.proxies = {
            'http': proxy,
            'https': proxy
        }

    return session
