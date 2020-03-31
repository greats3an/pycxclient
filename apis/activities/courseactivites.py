'''
# CourseActivites Module

    Used to register 'progress' of a document
    
    which,once set,CANNOT be altered again
'''
from .. import session
from utils.myutils import urlparams
from bs4 import BeautifulSoup
import logging
import re
logger = logging.getLogger('CourseActivites')
regex = r"(?<=\().*(?=\))"

def _url_appendices(activeId, appType,puid,courseId,classId,fid): 
    '''URL appendices defined in util2.js'''
    return {
        '11': "/widget/pick/pc/startPick?activeId="+activeId+"&classId="+classId+"&fid="+fid+"&courseId="+courseId,
        '2': "/widget/sign/pcStuSignController/preSign?activeId="+activeId+"&classId="+classId+"&fid="+fid+"&courseId="+courseId,
        '4': "/widget/pcAnswer/teaAnswer?activeId="+activeId+"&classId="+classId+"&fid="+fid+"&courseId="+courseId,
        '14': "/widget/pcvote/goStudentVotePage?activeId="+activeId+"&classId="+classId+"&fid="+fid+"&courseId="+courseId+"&quessequence=1",
        '42': "/widget/pcvote/goStudentVotePage?activeId="+activeId+"&classId="+classId+"&fid="+fid+"&courseId="+courseId+"&quessequence=1",
        '23': "/widget/score/pc/queryScore?activeId="+activeId+"&classId="+classId+"&fid="+fid+"&courseId="+courseId
    }[appType]

def GetCourseActivites(course_url) -> dict:
    '''
        Returns a `dict` object contating infomations of the operation
    '''
    logger.debug('Getting all activites of %s' % course_url)
    params = urlparams.GetParams(course_url)
    response = session.get(
        'https://mobilelearn.chaoxing.com/widget/pcpick/stu/index',
        params={
            'courseId': params['courseId'],
            'jclassId': params['clazzid'],
        }
    )
    soup = BeautifulSoup(response.text, 'lxml')
    # Loads HTML via bs4
    # Load variables
    puid = soup.find('input', {'id': 'puid'}).attrs['value']
    courseId = soup.find('input', {'id': 'courseId'}).attrs['value']
    classId = soup.find('input', {'id': 'classId'}).attrs['value']
    fid = soup.find('input', {'id': 'fid'}).attrs['value']

    def load_activites(parent_dom,end=False):
        # All activites are belong to class 'Mct'
        activites = []
        for activity_dom in parent_dom.find_all('div', {'class': 'Mct'}):
            onclick = activity_dom.attrs['onclick']

            activeId, appType, event = re.findall(regex, onclick)[0].split(',')
            activity_url = 'https://mobilelearn.chaoxing.com' + _url_appendices(activeId,appType,puid,courseId,classId,fid)

            activites.append({
                'url': activity_url,
                'activity_id':activeId,
                'activity_type':appType,
                'activity_type_str': activity_dom.find('dl').find('a').find('dd').text,
                'activity_description': activity_dom.find('div').find('a').text,
                'activity_alert': activity_dom.find('p').find('span').text,
                'activity_ended':end
            })
        return activites

    return load_activites(soup.find('div',{'id':'startList'})) + load_activites(soup.find('div',{'id':'endList'}),True)
