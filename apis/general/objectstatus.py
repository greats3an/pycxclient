'''
# ObjectStatus Module

    Used to get a object's `status`
'''
from .. import session
from json import loads
import logging
def GetObjectStatus(objectid) -> dict:
    '''
        Returns a `dict` object contating infomations on this object
    '''
    response = session.get(
        'https://mooc1-1.chaoxing.com/ananas/status/' + objectid
    )
    logging.debug('Getting object status of object %s' % objectid)
    return loads(response.text)