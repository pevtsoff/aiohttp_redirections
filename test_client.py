import requests

from server import char_qty

max_redirects = 50
class TooBigBody(Exception): pass


def test_managed_redirection():
    """
        Managed redirection will finish with successfull response
    """
    start_url = 'http://localhost:9005/first_endpoint'
    final_url = get_final_url(start_url)
    assert final_url == 'http://localhost:9005/second_endpoint'

    if final_url:
        resp = requests.get(url=final_url, stream=True)

        if int(resp.headers.get('Content-Length', '0')) < char_qty + 1:
            print_huge_body(resp)
        else:
            raise TooBigBody(f'The body exceeds the limit of 10000')


def test_cyclic_redirection():
    """
        handling cyclic redirections
    """
    start_url = 'http://localhost:9005/first_cyclic_endpoint'
    final_url = get_final_url(start_url)
    assert final_url is None


def get_final_url(url):
    sess = requests.Session()
    sess.max_redirects = max_redirects
    try:
        resp = sess.head(url, allow_redirects=True)
        print("redirect url list:")
        for resp in resp.history:
            print(f'{resp.status_code=}, {resp.url=}')
        return resp.url

    except requests.exceptions.TooManyRedirects as e:
        print(e)
        return None


def print_huge_body(resp):
    for line in resp.iter_lines():
        print(line)