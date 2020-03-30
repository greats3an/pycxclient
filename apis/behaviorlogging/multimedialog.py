'''
# MultimediaLog Module

    This moudle will mimic the functions defined inside videojs-ext.js

    which will log about your media watching behavior
    
    Once the view druation has increased,it CANNOT be decreased again
'''
from .. import session
from hashlib import md5
import logging
_salt = "d_yHJ!$pdA~5"
_format = "[{0}][{1}][{2}][{3}][{4}][{5}][{6}][{7}]"
logger = logging.getLogger('MultimediaLog')
def _GenerateHash(text) -> str:
    '''
        Returns MD5 hash of the text encoded
    '''
    HASH = md5(text.encode('utf-8'))
    return HASH.hexdigest()


def _GenerateEnc(clazzId, jobid, objectId, currentTimeSec, totalTimeSec,uid='') -> str:
    '''
        Generates ENC parameter
    '''
    enctext = _format.format(
        clazzId,
        uid,
        jobid,
        objectId,
        int(currentTimeSec) * 1000,
        _salt,
        int(totalTimeSec) * 1000,
        '0_%s' % totalTimeSec
    )
    return _GenerateHash(enctext)

def MultimediaLog(reportUrl,playtime,duration,dtoken,clazzId,objectId,otherInfo,jobid,isdrag=0,view='pc',dtype='Video') -> str:
    '''
        Log about your video watching duration
    '''
    logger.debug('Logging MultimediaLog with played time of %s (drag=%s)' % (playtime,isdrag))
    enc = _GenerateEnc(clazzId,jobid,objectId,playtime,duration,session.cookies.get('_uid'))
    response = session.get(
        reportUrl + '/' + dtoken,
        params={
            'clazzId':clazzId,
            'playingTime':playtime,
            'duration':duration,
            'clipTime':'0_%s' % duration,
            'objectId':objectId,
            'otherInfo':otherInfo,
            'jobid':jobid,
            'userid':session.cookies.get('_uid'),
            'isdrag':isdrag,
            'view':view,
            'enc':enc,
            'dtype':dtype
        }
    )
    return response.text