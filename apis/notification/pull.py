'''
# Pull Module

    Pulls all new notifcations
'''
from .. import session
from json import loads
import logging
logger = logging.getLogger('Pull')
def PullNotifiactions(type=0,lastValue='',getNew=False) -> dict:
    '''
        # 通知
        
        Returns a `dict` object contating infomations on notifications

        ## type:

        0       :       All messages received & sent

        1       :       Messages sent

        ## lastValue:
        
        Specifies last recevied notifcation,only works when `getNew` is `True`

        ## getNew:

        Retrives all notifications that has `id` greater than `lastValue`
    '''
    response = session.post(
        [
            'http://notice.chaoxing.com/pc/notice/getNoticeList',
            'http://notice.chaoxing.com/pc/notice/getNewNotices'
        ][getNew],
        data={
            'type':type,
            'lastValue':lastValue
        }
    ) 
    return loads(response.text)