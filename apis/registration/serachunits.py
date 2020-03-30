'''
# SerachUnits Module

    Serach units via filter given
'''
from .. import session
from base64 import b64encode
from json import loads
import logging
logger = logging.getLogger('SerachUnits')
def SearchUnits(filter) -> list:
    '''
        Returns a `list` object containing nearest results to the filter given
    '''
    logger.debug('Searching units related to %s' % filter)
    response = session.get(
        'https://passport2.chaoxing.com/org/searchUnis',
        params={
            'filter':filter,
            'product':44
        }
    )
    return loads(response.text)
