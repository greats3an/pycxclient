'''
# ClassTasks Module

    Used to get a `KnowledgeCard`'s args which contains the `tasks` info via its url
'''
from .. import session
from json import loads
from utils.myutils import js2dict
import logging
logger = logging.getLogger('ClassTasks')

def LoadClassInfo(knowledgeUrl) -> dict:
    '''
        Returns a `dict` object contating infomations on its args
    '''
    logger.debug('Loading KnowledgeArgs (mArg) of %s' % knowledgeUrl)
    response = session.get(
        knowledgeUrl
    )
    mArg = js2dict.js2dict(response.text)
    mArg = mArg['mArg'][-1]
    return loads(mArg)