'''
# Rating Module

    Rate a rating activity

    (appType:23)
'''
from .. import session
from bs4 import BeautifulSoup
from utils.myutils import urlparams,js2dict
import logging,json
logger = logging.getLogger('Rating')

def RateDetail(rate_url) -> dict:
    '''
        Parses HTML info a dict object containing rate info
    '''
    logger.debug('Loading Rate info')
    response = session.get(
        rate_url
    )
    
    soup = BeautifulSoup(response.text,'lxml')
    script = soup.find_all('script')[-1].text
    variables = js2dict.js2dict(script)
    rate_infoDOM = soup.find('div',{'class':'Mct2'})
    
    rate_info = {
        'title':json.loads('%s'%variables['title'][0].replace("'",'"')),
        'deploy_info': rate_infoDOM.find('div',{'class':'Mcp1'}).find('p',{'class':'fl'}).text.replace('\n','\t').strip()
    }
    rate_imgs = [
        img.attrs['href'] for img in soup.find_all('a',{'class':'fancybox'})
    ]
    rate_survey_dom = soup.find('div',{'class':'main1100'})
    rate_survey = [
        {
            'sender':survey_dom.find('h3',{'class':'ypTit'}).find('span').text,
            'score':survey_dom.find('h3',{'class':'ypTit'}).find('b').text,
            'message':survey_dom.find('div',{'class':'YpPcon'}).text
        } for survey_dom in rate_survey_dom.find_all('div',{'class':'pad25'})
    ] if rate_survey_dom else []
    return {
        'rate_info':rate_info,
        'rate_imgs':rate_imgs,
        'rate_survey':rate_survey
    }

def Rate(rate_url,content,score) -> dict:
    '''
        Perform rating
    '''
    logger.debug('Rating %s ' % rate_url)
    params = urlparams.GetParams(rate_url)
    response = session.post(
        'https://mobilelearn.chaoxing.com/widget/score/pc/stuSaveScore',
        data={
            **params,
            'content':content,
            'score':score,
            'puid':session.cookies.get('_uid')
        }
    ) 
    return json.loads(response.text)