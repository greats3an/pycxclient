'''
# DoucmentPoint Module

    Used to register 'progress' of a document
    
    ⚠️ which,once set,CANNOT be altered again
'''
from .. import session
from json import loads
import logging
def SetDocumentPoint(jobid,knowledgeid,courseid,clazzid,jtoken) -> dict:
    '''
        Returns a `dict` object contating infomations of the operation
    '''
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
    logging.debug('Setting document-point for course %s' % courseid)
    return loads(response.text)