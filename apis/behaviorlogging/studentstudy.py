'''
# StudentStudy Module

    Used to register that you have visted the task itself
    
    which,once set,CANNOT be altered again
'''
from .. import session
from utils.myutils import urlparams
from json import loads
import logging
logger = logging.getLogger('StudentStudy')
def SetStudentStudy(studyUrl) -> dict:
    '''
        Sets your study log to valid
    '''
    UrlParams = urlparams.GetParams(studyUrl)
    data = {
        'courseId':UrlParams['courseId'],            
        'clazzid':UrlParams['clazzid'],
        'chapterId':UrlParams['chapterId'],
        'cpi':0,
        'verificationcode':'',
        # Reserved,for future uses            
    }
    logger.debug('Setting StudentStudy-point with form-data %s' % data)
    response = session.post(
        'https://mooc1-1.chaoxing.com/mycourse/studentstudyAjax',
        data = data,
        headers={
            'Referer':studyUrl
        }
    )
    return response.text if len(response.text) < 16 else '成功'