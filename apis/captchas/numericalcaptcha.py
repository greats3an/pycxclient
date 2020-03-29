'''
# NumericalCaptcha Module

    Used to get captcha image witch will be needed

    for logging in,and etc
'''
from .. import session
from utils import userio
from typing import Union
import os,logging
def RenewCaptcha(prompt=False) -> Union[bytearray,str]:
    '''
        Renews captcha

        Which will also set the session's cookies to identifiy with

        if `not prompt`:Returns a `bytearray` object of the captcha image
        
        if `prompt`:Returns the user inputed captcha code        
    '''
    logging.debug('Renewing captcha')    
    response = session.get(
        'https://passport2.chaoxing.com/num/code'
    )    
    # Prompts user to input the captcha
    captcha = response.content
    if prompt:
        logging.debug('Prompting user to input captcha')
        userio.get('即将输入验证码，请记下您所看到的四位有效数字；按下回车查看验证码:',end='[确认]')
        # Deletes the old file
        if os.path.exists('captcha.jpg'):os.remove('captcha.jpg')
        open('captcha.jpg','wb').write(captcha)
        if 'termux' in str(os.environ):
            # Special compatibility fix for Termux,the android terminal emulator:
            # View image via termux-open,which will open the image 
            os.system('termux-open captcha.jpg')
        else:
            # For other terminals,which in most cases can directly view such image
            # Using their own image viewer
            os.startfile('captcha.jpg')
        captcha = userio.get('输入您所看到的验证码')
        # Deletes the file afterwards
        os.remove('captcha.jpg')
    return captcha

