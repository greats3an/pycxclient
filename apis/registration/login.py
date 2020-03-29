'''
# Login Module

    Logging you in with the username,password,captcha code and unit code given
'''
from .. import session
from base64 import b64encode
from json import loads
import logging

def NormalLogin(username, password) -> dict:
    '''
        This method DOES NOT require capthca verification

        Returns a `dict` object containing a url which you should be shortly redirected to

        Which will also set a bunch of cookies
    '''
    data = {
        'fid': -1,
        'uname': username,
        'password': b64encode(password.encode()).decode(),
        # The password is base-64 encoded
        't': 'true'
    }
    response = session.post(
        'https://passport2.chaoxing.com/fanyalogin',
        data=data
    )
    logging.debug('Logging in with form-data %s' % data)
    return loads(response.text)


def UnitLogin(unit_code,username, password, captcha_code) -> dict:
    '''
        ⚠️Requires one kind of `capcha` has already been defeated before use

        Returns a `dict` object containing a url which you should be shortly redirected to

        Which will also set a bunch of cookies
    '''
    data = {
        'fid': unit_code,
        'uname': username,
        'numcode': captcha_code,
        'password': b64encode(password.encode()).decode(),
        # The password is base-64 encoded
        't': 'true'
    }
    response = session.post(
        'https://passport2.chaoxing.com/unitlogin',
        data=data
    )
    logging.debug('Logging in with form-data %s' % data)
    return loads(response.text)
