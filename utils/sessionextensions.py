'''
# SessionExtensions Module

    Extends some functions for the `requests.Session`
'''
from requests import Session

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
