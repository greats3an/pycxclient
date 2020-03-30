'''
# ClassTasks Module

    Used to get a `KnowledgeCard`'s args which contains the `tasks` info via its url
'''
from .. import session
from json import loads
import re,logging
logger = logging.getLogger('ClassTasks')
regex = r"(?<=mArg = ){.*(?=;)"
def LoadClassInfo(knowledgeUrl) -> dict:
    '''
        Returns a `dict` object contating infomations on its args
    '''
    logger.debug('Loading KnowledgeArgs (mArgs) of %s' % knowledgeUrl)
    response = session.get(
        knowledgeUrl
    )
    mArgs = re.findall(regex,response.text)[0]
    mArgs = loads(mArgs)
    return mArgs