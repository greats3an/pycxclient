'''
# UserIO module

    provides some handy functions for command line interfacing
'''
import unicodedata,logging
cancel = 'q'
logger = logging.getLogger('UserIO')
class UserCannceledException(Exception):
    def __init__(self, *args, **kwargs):
        logger.warn('Intercepted user canncel action')
        super().__init__(*args, **kwargs)

def get(*args,**kwargs):
    '''Input but wrapped with print() and added interruptions''' 
    print(*args,**{'end':'>>>',**kwargs})
    try:
        result = input()
    except KeyboardInterrupt:
        result = cancel
    if result == cancel:raise UserCannceledException('Cannceled.')
    return result

def scrlen(s):
    return sum([2 if unicodedata.east_asian_width(i) in 'WFA' else 1 for i in s])

def listout(items,foreach=lambda x: x,title='LIST'):
    '''Prints a list of dictionaries with their index and value processed by `foreach`'''
    print(title,'_' * (50 - scrlen(title)),sep='')
    items = list(items)
    for index in range(0,len(items)):
        item = items[index]
        try:
            print('',str(index).ljust(5),foreach(item))
        except Exception as e:
            print('',str(index).ljust(5),'-')
    print('_' * 50)