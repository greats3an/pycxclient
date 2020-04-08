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
    infobox = soup.find('dl')
    data = {
        'msg':soup.find('p',{'class':'blankTips'}).text,
        'title':infobox.find('h3').text,
        'teacher':infobox.find('p').text,
        'cover':infobox.find('img').attrs['src'],
        'courseId':soup.find('input',{'name':'courseId'}).attrs['value'],
        'classId':soup.find('input',{'name':'classId'}).attrs['value'],
        'userId':soup.find('input',{'name':'userId'}).attrs['value'],
    }

def JoinByInviteCode(inviteCode,classId,userId) -> dict:
    '''
        Requires user to be logged in beforehand
        Loads the specified course as a single `dict` item
    '''
    logger.debug('Joining invite code %s' % inviteCode)
    response = session.get(
        'http://mooc1-api.chaoxing.com/teachingClassPhoneManage/phone/getCourseJson',
        params={
            'courseId':inviteCode,
            'classId':classId,
            'userId':userId
        }
    )    
    return json.loads(response.text)