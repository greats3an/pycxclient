'''
# KnowledgeArgs Module

    Used to get a `KnowledgeCard`'s args via its url
'''
from . import session
from json import loads
import re,logging
regex = r"(?<=mArg = ){.*(?=;)"
def LoadKnowledgeArgs(knowledgeUrl) -> dict:
    '''
        Returns a `dict` object contating infomations on its args
    '''
    response = session.get(
        knowledgeUrl
    )
    logging.debug('Loading KnowledgeArgs (mArgs) of %s' % knowledgeUrl)
    mArgs = re.findall(regex,response.text)[0]
    mArgs = loads(mArgs)
    return mArgs