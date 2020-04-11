'''
# InviteCode Module

    Parses invite code to actual course IDs with / without joining it
'''
from .. import session
from bs4 import BeautifulSoup
import logging,json
logger = logging.getLogger('InviteCode')
def ParseInviteCode(inviteCode) -> dict:
    '''
        # 输入邀请码

        Requires user to be logged in beforehand

        Loads the specified course as a single `dict` item containing

        `courseId`,`classId`,`userId` necessary for joining a class

        and it's other info
    '''
    logger.debug('Parsing invite code %s' % inviteCode)
    response = session.get(
        'http://mooc1-api.chaoxing.com/teachingClassPhoneManage/phone/toParticipateCls',
        params={
            'inviteCode':inviteCode
        }
    )    
    soup = BeautifulSoup(response.text, 'lxml')
    infobox,blankTips = soup.find('dl'),soup.find('p',{'class':'blankTips'})
    data = {
        'msg':blankTips.text if blankTips else '',
        'title':infobox.find('h3').text if not blankTips else '',
        'teacher':infobox.find('p').text if not blankTips else '',
        'cover':infobox.find('img') if not blankTips else None,
        'courseId':soup.find('input',{'name':'courseId'}) if not blankTips else None,
        'classId':soup.find('input',{'name':'classId'}) if not blankTips else None,
        'userId':soup.find('input',{'name':'userId'}) if not blankTips else None,
    }    
    data['cover'] = data['cover'].attrs['src'] if data['cover'] else ''
    data['courseId'] = data['courseId'].attrs['value'] if data['courseId'] else '0'
    data['classId'] = data['classId'].attrs['value'] if data['classId'] else '0'
    data['userId'] = data['userId'].attrs['value'] if data['userId'] else '0'
    return data

def JoinByInviteCode(courseId,classId) -> dict:
    '''
        # 邀请码加入
        
        Requires user to be logged in beforehand

        Joins the course via `courseId` & `classId`

        which you can get via `ParseInviteCode`
    '''
    logger.debug('Joining invite code %s' % courseId)
    response = session.get(
        'http://mooc1-api.chaoxing.com/teachingClassPhoneManage/phone/getCourseJson',
        params={
            'courseId':courseId,
            'classId':classId,
            'userId':session.cookies.get('_uid')
        }
    )    
    return json.loads(response.text)