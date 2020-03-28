'''
# ObjectStatus Module

    Used to get a object's `status`
'''
from . import session
from json import loads
def GetObjectStatus(objectid):
    '''
        Returns a `dict` object contating infomations on this object
    '''
    response = session.get(
        'https://mooc1-1.chaoxing.com/ananas/status/' + objectid
    )
    return loads(response.text)