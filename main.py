'''
PyCxClient

    Python-based all in one Chaoxing learning helper,put to test

    by mos9527 @ mos9527.tooo.top
'''

settings = {
    'loginmethod': 1,
    'username': '341021200410060012',
    'password': '123745698sz',
    'schoolid': '62459'
}
# Set-up these strings to login semi-automaticly (you still need to pass Captcha)
mimic_settings = {
    'step':20,
    # In percentage * 100,the step of the mimic operation
    'block':256
    # The block size of a video request
}
import json
import logging
import os
import sys

import coloredlogs

from apis import session,behaviorlogging, captchas, general, mooclearning, registration,activities
from utils import userio
from atom import streamedatom
coloredlogs.install(logging.DEBUG)
# Selecting user's `unit`

# logging.getLogger("urllib3").setLevel(logging.WARNING)
# turn up logs levels for urllib3 which is used by requests
logger = logging.getLogger('main')
# local logger

# region Init
'''
    Login sequence
'''

def 账号密码登录(settings):
    '''Perform login by interfacing with user,returns login result'''
    print('【卡密登录】')
    # User should login now
    result = registration.login.NormalLogin(
        settings['username'] if settings['username'] else userio.get('输入您的账号'),
        settings['password'] if settings['password'] else userio.get('输入您的密码'),
    )

    if not 'url' in result.keys():
        logger.fatal('Failed to login:%s' %
                      result['mes'] if 'mes' in result.keys() else '原因未知')
        userio.get('按任意键', end='退出')
        sys.exit()
    # We have logged in,now,list all the courses the user has
    logger.info('User logged in')
    return result


def 单位登录(settings):
    '''Perform login by interfacing with user,returns login result'''
    def GetSchoolID():
        '''Seraches unit's ID then let the user choose'''
        units = registration.serachunits.SearchUnits(
            userio.get('请输入您所在机构的名称进行模糊搜索（如：XX中学）'))
        userio.listout(
            units['froms'], foreach=lambda item: item['name'], title='机构列表')
        unit = units['froms'][int(userio.get('输入您所处机构的【序号】'))]
        return unit['schoolid']

    print('【单位登录】')
    # User should login now
    result = registration.login.UnitLogin(
        settings['schoolid'] if settings['schoolid'] else GetSchoolID(),
        settings['username'] if settings['username'] else userio.get(
            '输入您于该机构中的【学号 / 工号】'),
        settings['password'] if settings['password'] else userio.get('输入您的密码'),
        # Prompt the user to input the captcha code
        # Renewing captcha,which will also give us a new JSESSIONID
        captchas.numericalcaptcha.RenewCaptcha(True)
    )

    if not 'url' in result.keys():
        logger.fatal('Failed to login:%s' %
                      result['mes'] if 'mes' in result.keys() else '原因未知')
        userio.get('按任意键', end='退出')
        sys.exit()
    # We have logged in,now,list all the courses the user has
    logger.info('User logged in')
    return result

'''
    Work before loop
'''
def splash():
    userio.get('''
________        _________      __________________            _____ 
___  __ \____  ___  ____/___  ___  ____/__  /__(_)_____________  /_
__  /_/ /_  / / /  /    __  |/_/  /    __  /__  /_  _ \_  __ \  __/
_  ____/_  /_/ // /___  __>  < / /___  _  / _  / /  __/  / / / /_  
/_/     _\__, / \____/  /_/|_| \____/  /_/  /_/  \___//_/ /_/\__/  
        /____/                                                     
                                           Python 实现的超星学习通多合一客户端                                        
使用说明：                                              by greats3an@gmail.com
    · 输入 q 返回上一级
    · 按下【回车】键登录                                                                               
''',end='')


def init():
    # First,perform login
    methods = [账号密码登录, 单位登录]
    if not 'loginmethod' in list(settings.keys()) or settings['loginmethod'] == -1:
        userio.listout(methods, foreach=lambda x: x.__name__, title='选择登录途径')
        method = methods[int(userio.get('输入登录方法【序号】',end='>>>'))]
        # Then we enter the main loop
    else:
        method = methods[int(settings['loginmethod'])]
    method(settings)
# endregion

# region Nested Life Cycle
'''
    Work during loop

    CLI Interfacing is based on this classic nested

    Loop chain construct,might be a little confusing

    But in development,yields great extensiblity and debuggablity

    Since all call stacks can be easily traced
'''

def L(method):
    '''`L:Looper`,wrapper for looping inside a function,then breaks once an exception occures'''
    def wrapper(*args, **kwargs):
        while True:
            try:
                method(*args, **kwargs)
            except Exception as e:
                logger.error(e)
                break
    return wrapper


def A(actions):
    '''`A:Action`,prompts user to select a action of choice'''
    userio.listout(actions, foreach=lambda x: x.__name__, title='可用操作')
    action = actions[int(userio.get('输入操作【序号】'))]
    return action


def 课堂列表():
    def _select():
        '''User will pick one courses from the list,this funtions returns the one selected'''
        courses = mooclearning.studentcourses.LoadCourses()
        userio.listout(
            courses, foreach=lambda item: item["title"] + ' (' + item["description"][0] + ')', title='课堂列表')
        course = courses[int(userio.get('输入课堂【序号】'))]
        # Now the user should choose one of those courses
        return course    
    course = _select()

    def 课程列表(course):
        def _select(course):
            '''Then,user picks one task from the course,this function returns it'''
            logger.debug('Loading course %s' % course['title'])
            classes = mooclearning.courseclasses.LoadClasses(course['url'])
            # User can now select one of the classes to start 'learning'
            userio.listout(classes.keys(), title='课程列表')
            class_ = classes[list(classes.keys())[int(userio.get('输入课程【序号】'))]]
            # Returns the class selected
            return class_        
        class_ = _select(course)

        def 任务列表(class_):
            def _select(class_):
                '''We can finally do things on this praticlar task'''
                userio.listout(class_, foreach=lambda x: x['chapter'] + ' ' + x['title'], title='任务列表')
                task = class_[int(userio.get('输入任务【序号】'))]
                # Now we load the info of such sub task
                logger.debug('Loading task %s' % task['title'])
                task = mooclearning.classtasks.LoadClassInfo(task['knowledge_url'])
                # returns the task selected
                return task            
            task = _select(class_)

            def 任务点列表(task):
                def _select(task):
                    '''User will now select a task point of choice'''
                    userio.listout(task['attachments'],
                                foreach=lambda x: x['property']['name'], title='任务点')
                    attachment = task['attachments'][int(userio.get('输入任务点【序号】'))]
                    status = {
                        **general.objectstatus.GetObjectStatus(attachment['property']['objectid']),
                        'isPassed': attachment['isPassed'] if 'isPassed' in attachment.keys() else False
                    }
                    # returns the task's
                    return {'attachment': attachment, 'status': status}                
                taskpoint = _select(task)

                print('\n'.join([
                    f"任务点状态{'_' * 50}",
                    f"  名称：{taskpoint['attachment']['property']['name']}",
                    f"  类型：{taskpoint['attachment']['type']}",
                    f"通过状态：{['未通过 / 未知','已通过'][taskpoint['status']['isPassed']]}"
                ]))

                def _enumerate(task, attachment, status):
                    '''Gets all supported operations for the certain task'''
                    def 获取下载链接():
                        return f"""
                    直链：{status['download']}
                    可续传：{status['http']} (需要额外 Header 'referer':'https://mooc1-1.chaoxing.com/ananas/modules/video/index.html?v=2019-1113-1705')
                    """

                    def 获取封面():
                        return f"""
                    链接：{status['screenshot']}
                    """

                    def 下载为MP3():
                        return f"""
                    链接：{status['mp3']} (需要额外 Header 'referer':'https://mooc1-1.chaoxing.com/ananas/modules/video/index.html?v=2019-1113-1705')
                    """

                    def 设置观看时长(mimic_settings=mimic_settings):
                        step = mimic_settings['step']
                        block = mimic_settings['block']
                        logger.debug('Fecthing HTTP Video ATOM header')
                        headers = {'referer': 'https://mooc1-1.chaoxing.com/ananas/modules/video/index.html?v=2019-1113-1705'}
                        # The header necessary to request the HTTP streamed (206) video source
                        header = streamedatom.GetHTTPVideoHeader(status['http'],session,headers=headers)
                        
                        content_length = int(header['http']['Content-Length'])
                        duration = int(header['atom'].ATOM_DURATION_SEC)

                        print('警告：1.更改操作只能【增加】时长，而不能【消减】时长')
                        print()
                        print('       故该操作不可逆，请慎重使用')
                        print()
                        print(f'      2.该操作将视频分为 {int(100 / step)} 份并同时对API和视频源(分块:{block} B)进行')
                        print()
                        print('        请求，且在大多数情况下表现安全，但**不保证**')
                        print()
                        print('        不会导致后台数据的异常，所产生的后果将由阁下')
                        print()
                        print('        自行承担')
                        print()
                        print('  注：需要刷新视频页面查看结果')
                        print()
                        print('视频总时长（秒）：', duration)

                        set_duration = int(userio.get('欲调节到的观看时长'))
                        percentage = set_duration / duration



                        print('观看时长、总时长比：%s ' % percentage)

                        def postLog(played_duration):
                            '''Posts a MultimediaLog'''
                            return behaviorlogging.multimedialog.MultimediaLog(
                                task['defaults']['reportUrl'],
                                int(played_duration),
                                duration,
                                status['dtoken'],
                                task['defaults']['clazzId'],
                                attachment['property']['objectid'],
                                attachment['otherInfo'],
                                attachment['property']['jobid'] if 'jobid' in attachment['property'].keys(
                                ) else attachment['property']['_jobid'],
                                isdrag=0 if played_duration < int(duration) * 0.5 else 4
                                # Minium playback 'pass' ratio
                            )

                        for seek in range(0,100 + step,step):
                            # Mimic a normal watch routine
                            seek_precentage = seek / 100
                            # Precentage of the loop
                            seek_head = int(content_length * percentage * seek_precentage)
                            # Byte start posistion of the request           
                            played_duration = int(duration * percentage * seek_precentage)
                            # Time start posistion of the log
                            logger.debug('Stepping watch routine head: %s / %s (%s / 100)' % (seek_head,content_length,seek))
                            # Loads the streaming video sources by chunks
                            r = streamedatom.PartialGet(status['http'],session,seek_head,block,headers=headers)
                            logger.debug('Server returned code %s' % r.status_code)
                            # Sends the request
                            result = postLog(played_duration)
                            # Does the logger
                        return f'''
                    返回值：{result}
                    结果：{'播放已结束' if 'true' in result else '播放未结束' if 'false' in result else '修改失败'}
                    '''

                    def 设置考核点():
                        print('警告： 该操作不可逆，请慎重使用')
                        userio.get('按下回车键', end='[确定]')
                        result = behaviorlogging.documentpoint.SetDocumentPoint(
                            attachment['property']['jobid'] if 'jobid' in attachment['property'].keys(
                            ) else attachment['property']['_jobid'],
                            task['defaults']['knowledgeid'],
                            task['defaults']['courseid'],
                            task['defaults']['clazzId'],
                            attachment['jtoken']
                        )
                        return f'''
                    信息：{result["msg"]}
                    结果：{'设置成功' if result['status'] else '设置失败（该项目可能不属于考核点）' }
                    '''
                    operations = {
                        '*': [获取下载链接],
                        'video': [获取封面, 下载为MP3, 设置观看时长],
                        'document': [设置考核点]
                    }
                    return operations['*'] + operations[attachment['type']] if attachment['type'] in operations.keys() else []

                AS = _enumerate(task, taskpoint['attachment'], taskpoint['status'])
                print(A(AS)())

            AS = [任务点列表]
            A(AS)(task)

        AS = [任务列表]
        L(A(AS))(class_)

    def 活动列表(course):
        def _select(activitylist):
            '''User will now choose one of the activites'''
            userio.listout(activitylist,foreach=lambda x:'[%s] [%s] %s %s' %(['进行中','已结束'][x['activity_ended']],x['activity_type_str'],x['activity_description'],x['activity_alert']),title='活动列表')
            return activitylist[int(userio.get('输入序号'))]

        activitylist = activities.courseactivites.GetCourseActivites(course['url'])
        activity = _select(activitylist)
        
        def 签到():
            try:
                userio.get('输入 q 取消，否则按回车键继续')
                result = activities.signin.NormalSingin(activity['url'])
                return '结果：\n    ' + result
            except Exception:
                return ''

        
        def 查看选人情况():
            result = activities.pick.PickInfo(activity['url'])
            userio.listout(
                result,
                foreach=lambda x:f"{x['name']} {('（我）' if str(x['uid']) == str(session.cookies.get('_uid')) else '......')} {x['updatetimeStr']}",
                title='被选到的人')
            userio.get('按回车键')
            return ''

        def _enumerate(activity_type):
            operations = {
                '*':[],
                '2':[签到],
                '11':[查看选人情况]
            }
            
            return operations['*'] + operations[str(activity_type)] if str(activity_type) in operations.keys() else []
        
        print(A(_enumerate(activity['activity_type']))())

    AS = [课程列表,活动列表]
    L(A(AS))(course)


def entryPoint():
    '''Entry point to the looper'''
    AS = [课堂列表]
    # AS:ActionS to be emurated
    L(A(AS))()

# endregion

if __name__ == "__main__":
    # Enters entery point once startup
    splash()
    init()
    L(entryPoint)()