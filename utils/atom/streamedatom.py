'''
# Streamedatom Module

    Gets a HTTP video's length via its ATOM header / footer

    Note that the video resource must support `HTTP 206 Partial-Content`
'''
from . import atom

from requests import Session
blocksize = 2048
# Content length in bytes at minium to contain MVHD info

def GetHeaders(url, session: Session, headers={}, params={}):
    '''
    Gets HTTP headers,then closes the connection without transmitting any data

    Returns the headers in `dict`
    '''
    r = session.get(url, stream=True, headers=headers, params=params)   
    r.close()
    return r.headers

def PartialGet(url, session: Session, seek=0, length=0, headers={}, params={}):
    '''
    Partialy reads `HTTP 206 Partial-Content` supported resources via `Range` header
    
    Returns a `requests.Response` object
    '''
    response_headers = GetHeaders(url,session,headers,params)
    if not 'Accept-Ranges' in response_headers.keys():raise Exception('Resource does NOT support partial transmission!')
    # Not partial transmission support
    cl = response_headers['Content-Length']
    if length == 0:
        length = cl - seek
    # Length not spiceified:transmits all the data
    headers={**headers, 'Range': 'bytes=%s-%s' % (seek, seek + length)}

    co = session.get(url, headers=headers, params=params)
    return co

def GetHTTPVideoHeader(url, session: Session, headers={}, params={}):
    '''
    Gets a HTTP video's ATOM header / footer
    '''
    header = GetHeaders(url, session, headers, params)
    length = int(header['Content-Length'])
    # Total content length in bytes

    try:
        # First try to read 2k from the bottom,since most encoders do this
        atomheader = PartialGet(url, session, length - blocksize, blocksize, headers, params).content
        atomheader = atom.unpack(atomheader)
    except Exception as e:
        # Then fallbacks to read-from-the-top mode if no MVHD header is found
        atomheader = PartialGet(url, session, 0, blocksize, headers, params).content
        atomheader = atom.unpack(atomheader)

    return {'atom':atomheader,'http':header}

if  __name__ == "__main__":
    session = Session()
    url = input("Video URL:")
    atom = GetHTTPVideoHeader(url,session)
    print('#'*50)
    for key in dir(atom):
        if 'ATOM' in key:
            print(key.ljust(24),getattr(atom,key))
    print('#'*50)
    input('Press ENTER to exit.')