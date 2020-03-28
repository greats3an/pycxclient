'''
# NumericalCaptcha Module

    Used to get captcha image witch will be needed

    for logging in,and etc
'''
from . import session
from utils import userio
from PIL import Image,ImageEnhance
from io import BytesIO
from typing import Union
import os,logging
def RenewCaptcha(prompt=False,enhance=True) -> Union[type(Image),str]:
    '''
        Renews captcha

        Which will also set the session's cookies to identifiy with

        if `not prompt`:Returns a `PIL.Image` object of the captcha code
        
        if `prompt`:Returns the user inputed captcha code        
    '''
    response = session.get(
        'https://passport2.chaoxing.com/num/code'
    )    
    logging.debug('Renewing captcha')
    captcha = Image.open(BytesIO(response.content))
    # Enhances the image via increasing contrast
    if enhance:
        captcha = ImageEnhance.Contrast(captcha).enhance(3)
    # Prompts user to input the captcha
    if prompt:
        logging.debug('Prompting user to input captcha')
        userio.get('即将输入验证码，请记下您所看到的四位有效数字；按下回车查看验证码:',end='[确认]')
        # Deletes the old file
        if os.path.exists('captcha.jpg'):os.remove('captcha.jpg')
        captcha.save('captcha.jpg')
        if 'termux' in ''.join(os.environ):
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

