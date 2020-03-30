'''
# DocumentPoint Module

    Used to register 'progress' of a document
    
    which,once set,CANNOT be altered again
'''
from .. import session
from json import loads
import logging
logger = logging.getLogger('DocumentPoint')
def SetDocumentPoint(jobid,knowledgeid,courseid,clazzid,jtoken) -> dict:
    '''
        Returns a `dict` object contating infomations of the operation
    '''
    logger.debug('Setting document-point for course %s' % courseid)
    response = session.get(
        'https://mooc1-1.chaoxing.com/ananas/job/document',
        params = {
            'jobid':jobid,
            'knowledgeid':knowledgeid,
            'courseid':courseid,
            'clazzid':clazzid,
            'jtoken':jtoken
        }
    )
    return loads(response.text)