'''
# ObjectStatus Module

    Used to get a object's `status`
'''
from .. import session
from json import loads
import logging
logger = logging.getLogger('ObjectStatus')
def GetObjectStatus(objectid) -> dict:
    '''
        Returns a `dict` object contating infomations on this object
    '''
    logger.debug('Getting object status of object %s' % objectid)
    response = session.get(
        'https://mooc1-1.chaoxing.com/ananas/status/' + objectid
    ) 
    return loads(response.text)