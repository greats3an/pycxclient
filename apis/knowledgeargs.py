'''
# KnowledgeArgs Module

    Used to get a `KnowledgeCard`'s args via its url
'''
from . import session
from json import loads
import re
regex = r"(?<=mArg = ){.*(?=;)"
def LoadKnowledgeArgs(cardurl):
    '''
        Returns a `dict` object contating infomations on its args
    '''
    response = session.get(
        cardurl
    )
    mArgs = re.findall(regex,response.text)[0]
    mArgs = loads(mArgs)
    return mArgs