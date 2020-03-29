'''
PyCxClient

    Python-based all in one Chaoxing learning helper,put to test

    by mos9527 @ mos9527.tooo.top
'''

settings = {
    'loginmethod': -1,
    'username': '',
    'password': '',
    'schoolid': ''
}
# Set-up these strings to login semi-automaticly (you still need to pass Captcha)

import json
import logging
import os
import sys

import coloredlogs

from apis import behaviorlogging, captchas, general, mooclearning, registration
from utils import userio

coloredlogs.install(logging.DEBUG)
# Selecting user's `unit`

# region Sub Functions
'''
    Sub functions bulit on `apis` module
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
        logging.fatal('Failed to login:%s' %
                      result['mes'] if 'mes' in result.keys() else '原因未知')
        userio.get('按任意键', end='退出')
        sys.exit()
    # We have logged in,now,list all the courses the user has
    logging.info('User logged in')
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
        logging.fatal('Failed to login:%s' %
                      result['mes'] if 'mes' in result.keys() else '原因未知')
        userio.get('按任意键', end='退出')
        sys.exit()
    # We have logged in,now,list all the courses the user has
    logging.info('User logged in')
    return result


def selectCourse():
    '''User will pick one courses from the list,this funtions returns the one selected'''
    courses = mooclearning.studentcourses.LoadCourses()
    userio.listout(
        courses, foreach=lambda item: item["title"] + ' (' + item["description"][0] + ')', title='课堂列表')
    course = courses[int(userio.get('输入课堂【序号】'))]
    # Now the user should choose one of those courses
    return course


def selectClass(course):
    '''Then,user picks one task from the course,this function returns it'''
    logging.debug('Loading course %s' % course['title'])
    classes = mooclearning.courseclasses.LoadClasses(course['url'])
    # User can now select one of the classes to start 'learning'
    userio.listout(classes.keys(), title='课程列表')
    class_ = classes[list(classes.keys())[int(userio.get('输入课程【序号】'))]]
    # Returns the class selected
    return class_


def selectTask(class_):
    '''We can finally do things on this praticlar task'''
    userio.listout(class_, foreach=lambda x: x['title'], title='子课程列表')
    task = class_[int(userio.get('输入子课程【序号】'))]
    # Now we load the info of such sub task
    logging.debug('Loading task %s' % task['title'])
    task = mooclearning.classtasks.LoadClassInfo(task['knowledge_url'])
    # returns the task selected
    return task


def selectTaskPoint(task):
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


def getTaskSupportedOperations(task, attachment, status):
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

    def 设置观看时长():
        print('警告：更改操作只能【增加】时长，而不能【消减】时长')
        print('      故该操作不可逆，请慎重使用')
        print('视频总时长（秒）：', status['duration'])

        set_duration = userio.get('欲调节到的观看时长')
        result = behaviorlogging.multimedialog.MultimediaLog(
            task['defaults']['reportUrl'],
            set_duration,
            status['duration'],
            status['dtoken'],
            task['defaults']['clazzId'],
            attachment['property']['objectid'],
            attachment['otherInfo'],
            attachment['property']['jobid'] if 'jobid' in attachment['property'].keys(
            ) else attachment['property']['_jobid'],
            isdrag=0 if set_duration != str(status['duration']) else 4
        )
        return f'''
    返回值：{result}
    结果：{'播放已结束' if 'true' in result else '播放未结束' if 'false' in result else '修改失败'}
    '''

    def 设置考核点():
        print('警告： 该操作不可逆，请慎重使用')
        userio.get('按下回车键', end='[确定]')
        result = mooclearning.documentpoint.SetDocumentPoint(
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

# endregion

# region Init
'''
    Work before loop
'''
def splash():
    userio.get('''
██████╗ ██╗   ██╗ ██████╗██╗  ██╗ ██████╗██╗     ██╗███████╗███╗   ██╗████████╗
██╔══██╗╚██╗ ██╔╝██╔════╝╚██╗██╔╝██╔════╝██║     ██║██╔════╝████╗  ██║╚══██╔══╝
██████╔╝ ╚████╔╝ ██║      ╚███╔╝ ██║     ██║     ██║█████╗  ██╔██╗ ██║   ██║   
██╔═══╝   ╚██╔╝  ██║      ██╔██╗ ██║     ██║     ██║██╔══╝  ██║╚██╗██║   ██║   
██║        ██║   ╚██████╗██╔╝ ██╗╚██████╗███████╗██║███████╗██║ ╚████║   ██║   
╚═╝        ╚═╝    ╚═════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   
                                           Python 实现的超星学习通多合一客户端                                        
使用说明：                                              by greats3an@gmail.com
    · 按 q 随时返回上一级
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
                logging.debug(e)
                break
    return wrapper


def A(actions):
    '''`A:Action`,prompts user to select a action of choice'''
    userio.listout(actions, foreach=lambda x: x.__name__, title='可用操作')
    action = actions[int(userio.get('输入操作【序号】'))]
    return action


def 进入课堂列表():
    course = selectCourse()

    def 进入课程列表(course):
        class_ = selectClass(course)

        def 进入任务列表(class_):
            task = selectTask(class_)

            def 进入任务点列表(task):
                taskpoint = selectTaskPoint(task)
                print('\n'.join([
                    f"任务点状态{'_' * 50}",
                    f"  名称：{taskpoint['attachment']['property']['name']}",
                    f"  类型：{taskpoint['attachment']['type']}",
                    f"通过状态：{['未通过 / 未知','已通过'][taskpoint['status']['isPassed']]}"
                ]))

                AS = getTaskSupportedOperations(
                    task, taskpoint['attachment'], taskpoint['status'])
                L(A(AS))()

            AS = [进入任务点列表]
            L(A(AS))(task)

        AS = [进入任务列表]
        L(A(AS))(class_)

    AS = [进入课程列表]
    L(A(AS))(course)


def entryPoint():
    '''Entry point to the looper'''
    AS = [进入课堂列表]
    # AS:ActionS to be emurated
    L(A(AS))()

# endregion

if __name__ == "__main__":
    # Enters entery point once startup
    splash()
    init()
    L(entryPoint)()