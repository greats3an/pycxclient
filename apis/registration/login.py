'''
# Login Module

    Logging you in with the username,password,captcha code and unit code given
'''
from .. import session
from base64 import b64encode
from json import loads
import logging
logger = logging.getLogger('Login')
def NormalLogin(username, password) -> dict:
    '''
        # 卡密登录
        
        Does not require any captcha to be solved

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
    logger.debug('Logging in with form-data %s' % data)    
    response = session.post(
        'https://passport2.chaoxing.com/fanyalogin',
        data=data
    )
    return loads(response.text)


def UnitLogin(unit_code,username, password, captcha_code) -> dict:
    '''
        # 单位登录

        Requires `captchas.logincaptcha` to be solved first to get us `captcha_code`

        Returns a `dict` object containing a url which you should be shortly redirected to

        ## unit_code

        Fecthable via `registration.serachunits`
    '''
    data = {
        'fid': unit_code,
        'uname': username,
        'numcode': captcha_code,
        'password': b64encode(password.encode()).decode(),
        # The password is base-64 encoded
        't': 'true'
    }
    logger.debug('Unit Logging in with form-data %s' % data)   
    response = session.post(
        'https://passport2.chaoxing.com/unitlogin',
        data=data
    )

    return loads(response.text)
