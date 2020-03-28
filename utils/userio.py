'''
# UserIO module

    provides some handy functions for command line interfacing
'''
import unicodedata
def get(*args,**kwargs):
    '''Input but wrapped with print()'''    
    print(*args,**{'end':'>>>',**kwargs})
    return input()

def scrlen(s):
    return sum([2 if unicodedata.east_asian_width(i) in 'WFA' else 1 for i in s])

def listout(items,foreach=lambda x: x,title='LIST'):
    '''Prints a list of dictionaries with their index and value processed by `foreach`'''
    print(title,'_' * (50 - scrlen(title)))
    items = list(items)
    for index in range(0,len(items)):
        item = items[index]
        try:
            print('',str(index).ljust(5),foreach(item))
        except Exception as e:
            print('',str(index).ljust(5),'-')
    print('_' * 50)