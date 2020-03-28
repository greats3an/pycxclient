from apis import numericalcaptcha, login, serachunits, studentcourses,courseclasses, knowledgeargs,objectstatus, session
import logging
import coloredlogs
import sys
import clipboard
import os
import threading
import json

coloredlogs.install(logging.DEBUG)

# 找到学校ID
unit_code = serachunits.SearchUnits('歙县新安中学')['froms'][0]['schoolid']
# 获取验证码
logging.info('请记下图示验证码，按下 Enter 继续；进入后按下 q 退出')
input()
numericalcaptcha.RenewCaptcha().show()
captcha_code = input('>>>')
result = login.UnitLogin('341021200412120058',
                         's654321', captcha_code, unit_code)
if not 'url' in result.keys():
    logging.error('登录失败!')
    sys.exit()
print(result)
logging.info('登录成功')
# 重定向到学习页面

course = studentcourses.LoadCourses()[0]['url']
task = list(courseclasses.LoadClasses(course).values())[0]
args = knowledgeargs.LoadKnowledgeArgs(task[0]['knowledge_url'])
status = objectstatus.GetObjectStatus(args['attachments'][0]['property']['objectid'])
clipboard.copy(json.dumps(status))
assert False