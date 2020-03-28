'''
# SerachUnits Module

    Serach units via filter given
'''
from . import session
from base64 import b64encode
from json import loads
def SearchUnits(filter):
    '''
        Returns a `dict` object containing nearest results to the filter given
    '''
    response = session.get(
        'https://passport2.chaoxing.com/org/searchUnis',
        params={
            'filter':filter,
            'product':44
        }
    )
    return loads(response.text)
