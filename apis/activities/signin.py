'''
# Singin Module

    Sing-ins the user with url given

    (appType:2)
'''
from .. import session
from bs4 import BeautifulSoup
from utils.myutils import urlparams
import logging
logger = logging.getLogger('Singin')
def NormalSingin(singin_url) -> str:
    '''
        # 签到、手势签到

        Returns a string suggesting whether the signin has succeeded or not

        ...this only works on these two singins
    '''
    logger.debug('Signin in with URL %s' % singin_url)
    
    response = session.get(
        'https://mobilelearn.chaoxing.com/widget/sign/pcStuSignController/signIn',
        params=urlparams.GetParams(singin_url)
    ) 
    soup = BeautifulSoup(response.text,'lxml')
    result = soup.find('div',{'class':'qd_Success'}).text.strip()
    return result