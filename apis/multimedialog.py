'''
# MultimediaLog Module

    This moudle will mimic the functions defined inside videojs-ext.js

    which will POST logs about your media watching behavior
'''
from . import session
from hashlib import md5
_salt = "d_yHJ!$pdA~5"
_format = "[{0}][{1}][{2}][{3}][{4}][{5}][{6}][{7}]"

def _GenerateHash(text):
    '''
        Returns MD5 hash of the text encoded
    '''
    HASH = md5(text.encode('utf-8'))
    return HASH.hexdigest()


def _GenerateEnc(clazzId, jobId, objectId, currentTimeSec, totalTimeSec,uid=''):
    '''
        Generates ENC parameter
    '''
    enctext = _format.format(
        clazzId,
        session.cookies.get('_uid') if not uid else uid,
        jobId,
        objectId,
        int(currentTimeSec) * 1000,
        _salt,
        int(totalTimeSec) * 1000,
        '%s_%s' % (currentTimeSec,totalTimeSec)
    )
    return _GenerateHash(enctext)

def MultimediaLog():
    '''
    '''
    pass