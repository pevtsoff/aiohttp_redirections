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
    assert final_url == 'http://localhost:9005/final_endpoint'
    _get_big_request(final_url)


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
        print(f'start {url=}')
        resp = sess.head(url, allow_redirects=True)
        print(f'final url={resp.url}')
        print('url redirection history:')

        for re_resp in resp.history:
            print(f'{re_resp.status_code=}, {re_resp.url=}')

        return resp.url

    except requests.exceptions.TooManyRedirects as e:
        print(f'Unabled to get the final url (without redirections). '
              f'Error occured: {e}')
        return None


def _get_big_request(url):
    if url:
        resp = requests.get(url=url, stream=True)

        if int(resp.headers.get('Content-Length', '0')) < char_qty + 1:
            _print_huge_body(resp)
        else:
            raise TooBigBody(f'The body exceeds the limit of {char_qty}')


def _print_huge_body(resp):
    for line in resp.iter_lines():
        print(line)