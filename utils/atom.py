'''
# atom Module

    Gets a video's ATOM info via its ATOM header / footer

    reference:https://developer.apple.com/library/archive/documentation/QuickTime/QTFF/QTFFChap2/qtff2.html (fig.2-3)
'''
import struct
import io


def _index(sublist: list, mainlist: list):
    '''
        Indexing a iterable from another iterable
    '''
    for i in range(0, len(mainlist) - len(sublist)):
        if mainlist[i:i+len(sublist)] == sublist:
            return i
    return -1
def GetDuration(header):
    '''
        Gets duration info from ATOM header / footer given

        Returns a `dict` containing such info
    '''
    header_index = _index(b'mvhd', header) - 4
    # Locating 'mvhd' header
    if header_index < 0:
        raise Exception("MVHD Header not found")
    ATOM_SIZE = bytearray(header[header_index:header_index + 4])
    ATOM_SIZE = struct.unpack('>I', ATOM_SIZE)[0]
    # ATOM size,should be 108 bytes in most cases

    header = io.BytesIO(
        bytearray(header[header_index:header_index + ATOM_SIZE]))

    header.seek(20)
    # Skipping some of the headers

    ATOM_TIMESCALE = struct.unpack('>I', header.read(4))[0]
    # ATOM Timescale

    ATOM_DURATION = struct.unpack('>I', header.read(4))[0]
    # ATOM Duration

    DURATION = ATOM_DURATION / ATOM_TIMESCALE

    return {
        'atom_timescale': ATOM_TIMESCALE,
        'atom_duration': ATOM_DURATION,
        'duration': DURATION
    }
