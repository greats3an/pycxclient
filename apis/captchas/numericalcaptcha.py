'''
# NumericalCaptcha Module

    Used to get captcha image witch will be needed

    for logging in,and etc
'''
from .. import session
from utils.myutils import userio
from utils.showfile import showfile
from typing import Union
import os,logging
logger = logging.getLogger('NumericalCaptcha')
def RenewCaptcha(prompt=False) -> Union[bytearray,str]:
    '''
        Renews captcha

        Which will also set the session's cookies to identifiy with

        if `not prompt`:Returns a `bytearray` object of the captcha image
        
        if `prompt`:Returns the user inputed captcha code        
    '''
    logger.debug('Renewing captcha')    
    response = session.get(
        'https://passport2.chaoxing.com/num/code'
    )    
    # Prompts user to input the captcha
    captcha = response.content
    if prompt:
        logger.debug('Prompting user to input captcha')
        userio.get('即将输入验证码，请记下您所看到的四位有效数字；按下回车查看验证码:',end='[确认]')
        # Deletes the old file
        showfile.ShowBytes(captcha,ext='jpg',lifetime=10)
        captcha = userio.get('输入验证码')
    return captcha

