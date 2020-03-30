'''
# Pick Module

    Pick function details

    (appType:11)

'''
from .. import session
from utils import urlparams,js2dict
import logging,json
logger = logging.getLogger('Pick')

def PickInfo(pick_url) -> dict:
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