'''
PyCxClient

    Python-based all in one Chaoxing learning helper,put to test

    by mos9527 @ mos9527.tooo.top
'''
from apis import numericalcaptcha, login, serachunits, studentcourses,courseclasses, knowledgeargs,objectstatus, multimedialog,documentpoint,session
from utils import userio
import logging,coloredlogs,sys,os,json
coloredlogs.install(logging.DEBUG)
# Selecting user's `unit`
settings = {
    'username':'',
    'password':'',
    'schoolid':''
}
# Set-up these strings to login semi-automaticly (you still need to pass Captcha)
def GetSchoolID():
    '''Seraches unit's ID then let the user choose'''
    units = serachunits.SearchUnits(userio.get('''需要登录：
    请输入您所在机构的名称进行模糊搜索（如：XX中学）'''))
    userio.listout(units['froms'],foreach=lambda item:item['name'],title='机构列表')
    unit = units['froms'][int(userio.get('输入您所处机构的【序号】'))]
    return unit['schoolid']

# Prompt the user to input the captcha code
# Renewing captcha,which will also give us a new JSESSIONID
captcha = numericalcaptcha.RenewCaptcha(True,True)
# User should login now
result = login.UnitLogin(
    settings['schoolid'] if settings['schoolid'] else GetSchoolID(),
    settings['username'] if settings['username'] else userio.get('输入您于该机构中的【学号 / 工号】'),
    settings['password'] if settings['password'] else userio.get('输入您的密码'),
    captcha
)

if not 'url' in result.keys():
    logging.fatal('Failed to login:%s' % result['mes'] if 'mes' in result.keys() else '原因未知')
    input()
    sys.exit()
# We have logged in,now,list all the courses the user has
logging.info('User logged in')
courses = studentcourses.LoadCourses()
userio.listout(courses,foreach=lambda item:item["title"] + ' (' + item["description"][0] + ')',title='课堂列表')
course = courses[int(userio.get('输入课堂【序号】'))]
# Now the user should choose one of those courses to view the classes inside of which
logging.debug('Loading course %s' % course['title'])
classes = courseclasses.LoadClasses(course['url'])
# User can now select one of the classes to start 'learning'
userio.listout(classes.keys(),title='课程列表')
task = classes[list(classes.keys())[int(userio.get('输入课程【序号】'))]]
# Sub class must be selected
userio.listout(task,foreach=lambda x: x['title'],title='子课程列表')
subtask = task[int(userio.get('输入子课程【序号】'))]
# Now we load the info of such sub task
logging.debug('Loading task %s' % subtask['title'])
taskargs = knowledgeargs.LoadKnowledgeArgs(subtask['knowledge_url'])
# List out all 'task points'
userio.listout(taskargs['attachments'],foreach=lambda x: x['property']['name'],title='任务点')
attachment = taskargs['attachments'][int(userio.get('输入任务点【序号】'))]
status = objectstatus.GetObjectStatus(attachment['property']['objectid'])
# Define funtions per data type
print(f"""
任务点状态{'_' * 50}
    名称：{attachment['property']['name']}
    类型：{attachment['type']}
""")
def 退出():sys.exit()
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
    print('视频总时长：',status['duration'],'s')

    set_duration = userio.get('欲调节到的观看时长')
    result = multimedialog.MultimediaLog(
        taskargs['defaults']['reportUrl'],
        set_duration,
        status['duration'],
        status['dtoken'],
        taskargs['defaults']['clazzId'],
        attachment['property']['objectid'],
        attachment['otherInfo'],
        attachment['property']['jobid']
    ) 
    return f'''
返回值：{result}
结果：{'播放已结束' if 'true' in result else '播放未结束' if 'false' in result else '修改失败'}
'''
def 设置考核点():
    print('警告： 该操作不可逆，请慎重使用')
    userio.get('按下回车键',end='[确定]')
    result = documentpoint.SetDocumentPoint(
        attachment['property']['jobid'],
        taskargs['defaults']['knowledgeid'],
        taskargs['defaults']['courseid'],
        taskargs['defaults']['clazzId'],
        attachment['jtoken']
    )
    return f'''
信息：{result["msg"]}
结果：{'设置成功' if result['status'] else '设置失败' }
'''
operations = {
    '*':[退出,获取下载链接],
    'video':[获取封面,下载为MP3,设置观看时长],
    'document':[设置考核点]
}
availables = operations['*'] + operations[attachment['type']]
while True:
    userio.listout(availables,foreach=lambda x: x.__name__,title='可用操作')
    operation = availables[int(userio.get('输入操作【序号】'))]
    print(operation())
    userio.get('执行完毕，按回车键',end='[继续]')
