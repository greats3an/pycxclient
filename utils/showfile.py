'''
# Showfile Module

    Shows user a file (filepath,url,bytearray) on most OSes
'''
import logging,os,random,threading,requests,time
logger = logging.getLogger('ShowFile')

buffersize = 2048

tempname_length = 8


class NotSupportedFormatException(Exception):
    def __init__(self,filename):
        super().__init__('Unable to show file %s:Not supported' % filename)

def _TimedDestroy(path,lifetime):
    '''Deletes the file after `lifetime`s'''
    def destory():
        if lifetime < 0:
            logger.debug('File %s will NOT be destoryed' % path)
            return
        logger.debug('File %s will be destoryed in %s s' % (path,lifetime))
        time.sleep(lifetime)
        try:
            os.remove(path)
            logger.debug('Successfuly deleted file %s' % path)
        except Exception as e:
            logger.warn('Unable to delete file %s:%s'% (path,e))
    threading.Thread(target=destory).start()
    # Starts a thread to delete the created file,fire and forget

def _GenerateRandomFilename(ext=''):
    '''Generates a random file name consisting the extension given'''
    randname = ''.join([random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRST0123456789') for i in range(0,tempname_length)])
    randname = randname + '.' + ext
    if os.path.exists(randname):
        logger.debug('%s exisits already,changeing file name' % randname)
        randname = _GenerateRandomFilename(ext)
    return randname

def _Show(path):
    '''
        Base method which shows a local file on all non-tty only OSes (including Termux)
    '''
    logger.debug('Opening file %s' % path)
    if 'termux' in str(os.environ):
        # Special compatibility fix for Termux,the android terminal emulator:
        # View file via termux-open,which will open the file 
        os.system('termux-open %s' % path)
    else:
        # For other terminals,which in most cases can directly view such file
        # Using their own file viewer
        os.startfile(path)

def ShowPath(url,ext='bin',lifetime=5,**kwargs):
    '''
        Shows an file of a URL (local / http),then destroys it after a certain amount of time
    '''
    if os.path.exists(url):
        '''Local file,directly shows the file without destroying it'''
        _Show(url)
    else:
        '''Not a local file,is it a web resourse?'''
        if not ('http' in url):raise NotSupportedFormatException(url)
        # A web resourse,fetch it via requests byte iterating over the file
        n = _GenerateRandomFilename(ext)
        r = requests.get(url,**{**kwargs,'stream':True})
        f = open(n,'wb')
        logger.debug('Start downloading file of size %s to temp %s' % (r.headers['Content-Length'] if 'Content-Length' in r.headers.keys() else 'UNKNOWN',n))
        for block in r.iter_content(buffersize):
            f.write(block)
        logger.debug('Download complete')
        f.flush()
        f.close()
        _Show(n)
        _TimedDestroy(n,lifetime)

def ShowBytes(data:bytearray,ext='bin',lifetime=5):
    '''
        Shows an file of a byte array,then destroys it after a certain amount of time
    '''
    randname = _GenerateRandomFilename(ext)
    open(randname,'wb').write(data)
    _TimedDestroy(randname,lifetime)
    _Show(randname)