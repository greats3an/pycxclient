'''
# NumericalCaptcha Module

    Used to get captcha image witch will be needed

    for logging in,and etc
'''
from . import session
from PIL import Image,ImageEnhance
from io import BytesIO
def RenewCaptcha(enhance=True):
    '''
        Renews captcha

        Returns a `PIL.Image` object of the captcha code
        
        Which will also set the session's cookies to identifiy with
    '''
    response = session.get(
        'https://passport2.chaoxing.com/num/code'
    )    
    captcha = Image.open(BytesIO(response.content))
    # Enhances the image via increasing contrast
    if enhance:
        captcha = ImageEnhance.Contrast(captcha).enhance(3)
    return captcha
