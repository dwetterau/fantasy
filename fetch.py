from contextlib import closing

from requests import get, RequestException


def fetch(url: str):
    try:
        with closing(get(url, stream=True)) as resp:
            if resp.status_code == 200:
                return resp.content
    except RequestException as e:
        print("Got error from URL {} {}".format(url, str(e)))
