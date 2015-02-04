import json
import re
import requests
from kc_connector.config import *
from kc_connector.exceptions import *


def get_play_url(login_id, password):

    # Headers
    headers = {
        'user-agent': REQUESTS_USER_AGENT,
    }

    s = requests.Session()

    # Get DMM_TOKEN and token for AJAX request
    req = s.get(LOGIN_URL, headers=headers, timeout=REQUESTS_TIMEOUT, proxies=REQUESTS_PROXIES)
    m = re.search(r'"DMM_TOKEN", "([\d|\w]+)"', req.text)
    if m is None:
        raise DmmTokenError
    else:
        dmm_token = m.group(1)
    m = re.search(r'"token": "([\d|\w]+)"', req.text)
    if m is None:
        raise TokenError
    else:
        token = m.group(1)

    # AJAX request
    # Get id_token, idKey and pwKey
    headers['DMM_TOKEN'] = dmm_token
    headers['Referer'] = LOGIN_URL
    headers['X-Requested-With'] = 'XMLHttpRequest'
    req = s.post(TOKEN_URL, data={'token': token}, headers=headers, timeout=REQUESTS_TIMEOUT, proxies=REQUESTS_PROXIES)
    try:
        j = json.loads(req.text)
        id_token = j['token']
        idKey = j['login_id']
        pwKey = j['password']
    except:
        raise AjaxRequestError

    # login
    del(headers['DMM_TOKEN'])
    del(headers['X-Requested-With'])
    post_data = {
        'login_id': login_id,
        'password': password,
        'token': id_token,
        idKey: login_id,
        pwKey: password,
        'save_login_id': '0',
        'save_password': '0',
        'path': '',
    }
    req = s.post(POST_URL, data=post_data, headers=headers, timeout=REQUESTS_TIMEOUT, proxies=REQUESTS_PROXIES)
    del(headers['Referer'])
    req = s.get(GAME_URL, headers=headers, timeout=REQUESTS_TIMEOUT, proxies=REQUESTS_PROXIES)
    m = re.search('URL\W+:\W+"(.*)",', req.text)
    if m is None:
        raise LoginError
    else:
        play_url = m.group(1)

    return play_url