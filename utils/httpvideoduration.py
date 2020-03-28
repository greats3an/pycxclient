'''
# HTTPVideoDuration Module

    Gets a HTTP video's length via its ATOM header / footer

    Note that the video resource must support `HTTP 206 Partial-Content`
'''
from . import atom, sessionextensions
from requests import Session
blocksize = 2048
# Content length in bytes at minium to contain MVHD info

def GetHTTPVideoDuration(url, session: Session, headers={}, params={}):
    '''
    Gets a HTTP video's length via its ATOM header / footer

    Returns a `dict` containing such info
    '''
    length = int(sessionextensions.GetHeaders(url, session, headers, params)['Content-Length'])
    # Total content length in bytes

    try:
        # First try to read 2k from the bottom,since most encoders do this
        atomheader = sessionextensions.PartialGet(url, session, length - blocksize, blocksize, headers, params).content
        atomheader = atom.GetDuration(atomheader)
    except Exception as e:
        # Then fallbacks to read-from-the-top mode if no MVHD header is found
        atomheader = sessionextensions.PartialGet(url, session, 0, blocksize, headers, params).content
        atomheader = atom.GetDuration(atomheader)

    return atomheader
