from contextlib import closing
from typing import Dict

from fake_useragent import UserAgent
from requests import get, RequestException


def fetch(url: str):
    try:
        with closing(get(url, headers=random_headers(), stream=True)) as resp:
            if resp.status_code == 200:
                return resp.content
            else:
                print("Got non-200 status code {}".format(resp.status_code))
    except RequestException as e:
        print("Got error from URL {} {}".format(url, str(e)))


def random_headers() -> Dict[str, str]:
    return {
        'User-Agent': UserAgent().random,
    }
