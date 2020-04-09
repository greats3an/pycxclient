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
        # 课时任务点
        
        Returns a `dict` object contating infomations on its args

        ## knowledgeUrl

        The url to the "Knowledge Card",which you can get throgh `mooclearning.courseclasses`
    '''
    logger.debug('Loading KnowledgeArgs (mArg) of %s' % knowledgeUrl)
    response = session.get(
        knowledgeUrl
    )
    args = js2dict.js2dict(response.text)
    mArg = [arg for arg in args['mArg'] if len(arg) > 8][0]
    return loads(mArg)