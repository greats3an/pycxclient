'''
# Rating Module

    Rate a rating activity

    (appType=23)
'''
from .. import session
from bs4 import BeautifulSoup
from utils import urlparams,js2dict
import logging,json
logger = logging.getLogger('Rating')

def RateDetail(rate_url) -> str:
    '''
        Parses HTML info a dict object containing rate info
    '''
    logger.debug('Loading Rate info')
    response = session.get(
        rate_url
    )
    soup = BeautifulSoup(rate_url.text,'lxml')

    rate_infoDOM = soup.find('div',{'class':'Mct2'})
    rate_info = {
        'title':rate_infoDOM.find('a',{'id':'title'}),
        'deploy_info': rate_infoDOM.find('div',{'class':'Mcp1'}).find('p',{'class':'fl'}).text        
    }
    rate_imgs = [
        img.attrs['href'] for img in soup.find_all('a',{'class':'fancybox'})
    ]
    return {
        'rate_info':rate_info,
        'rate_imgs':rate_imgs
    }

def PickInfo(pick_url) -> bool:
    '''
        For 选人
    '''
    logger.debug('Loading Pick info with URL %s' % pick_url)
    
    response = session.get(
        pick_url
    ) 
    result = js2dict.js2dict(response.text)['userChoose'][5:-1]
    result = json.loads(result.replace("'",'"'))
    return result