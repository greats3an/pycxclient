'''
# atom Module

    Unpacks a video's QuickTime ATOM (`moov`) info via its ATOM header / footer

    reference:https://developer.apple.com/library/archive/documentation/QuickTime/QTFF/QTFFChap2/qtff2.html (fig.2-3)
'''
import struct
import io


class ATOM:
    '''
        # ATOM Movie header object
        see:https://developer.apple.com/library/archive/documentation/QuickTime/QTFF/QTFFChap2/qtff2.html
    '''
    def __init__(self):
        self.ATOM_SIZE = 0
        """A 32-bit integer that specifies the number of bytes in this movie header atom"""
        self.ATOM_TYPE = 0
        """A 32-bit integer that identifies the atom type; must be set to 'mvhd'."""
        self.ATOM_VERSION = 0
        """A 1-byte specification of the version of this movie header atom."""
        self.ATOM_FLAGS = 0
        """Three bytes of space for future movie header flags."""
        self.ATOM_CREATION_TIME = 0
        """
        A 32-bit integer that specifies the calendar date and time (in seconds since midnight, January 1, 1904) 
        when the movie atom was created. It is strongly recommended that this value should be specified using coordinated universal time (UTC).
        """
        self.ATOM_MODIFICATION_TIME = 0
        """
        A 32-bit integer that specifies the calendar date and time (in seconds since midnight, January 1, 1904) 
        when the movie atom was changed. BooleanIt is strongly recommended that this value should be specified using coordinated universal time (UTC).
        """
        self.ATOM_TIMESCALE = 0
        """
        A time value that indicates the time scale for this movie—that is, 
        the number of time units that pass per second in its time coordinate system. 
        A time coordinate system that measures time in sixtieths of a second, for example, has a time scale of 60.
        """
        self.ATOM_DURATION = 0
        """
        A time value that indicates the duration of the movie in time scale units. 
        Note that this property is derived from the movie’s tracks. The value of this field corresponds to the duration of the longest track in the movie.
        """
        self.ATOM_PREFERED_RATE = 0
        """A 32-bit fixed-point number that specifies the rate at which to play this movie. A value of 1.0 indicates normal rate."""
        self.ATOM_PREFERED_VOLUME = 0
        """A 16-bit fixed-point number that specifies how loud to play this movie’s sound. A value of 1.0 indicates full volume."""
        self.ATOM_RESERVED = 0
        """Ten bytes reserved for use by Apple. Set to 0."""
        self.ATOM_MATRIX_STRUCT = 0
        """
        The matrix structure associated with this movie. A matrix shows how to map points from one coordinate space into another. 
        """
        self.ATOM_PREVIEW_TIME = 0
        """The time value in the movie at which the preview begins."""
        self.ATOM_PREVIEW_DURATION = 0
        """The duration of the movie preview in movie time scale units."""
        self.ATOM_POSTER_TIME = 0
        """The time value of the time of the movie poster."""
        self.ATOM_SELECTION_TIME = 0
        """The time value for the start time of the current selection."""
        self.ATOM_SELECTION_DURATION = 0
        """The duration of the current selection in movie time scale units."""
        self.ATOM_CURRENT_TIME = 0
        """The time value for current time position within the movie."""
        self.ATOM_NEXT = 0
        """A 32-bit integer that indicates a value to use for the track ID number of the next track added to this movie. Note that 0 is not a valid track ID value."""
        self.ATOM_DURATION_SEC = 0
        """The duration (in seconds) of the movie"""
        super().__init__()


def _index(subiter, mainiter) -> int:
    '''
        Indexing a iterable from another iterable
    '''
    for i in range(0, len(mainiter) - len(subiter)):
        if mainiter[i:i+len(subiter)] == subiter:
            return i
    return -1


def _locate(pack, header='mvhd') -> int:
    '''
        Locates ATOM Header index
    '''
    header_index = _index(header.encode(), pack) - len(header)
    # Locating header
    if header_index < 0:
        raise Exception(f"{header} Header not found")
    return header_index


def _load(pack) -> io.BytesIO:
    '''
        Turns bytearray into a full MVHD header ByteIO object
    '''
    header_index = _locate(pack)
    ATOM_SIZE = bytearray(pack[header_index:header_index + 4])
    ATOM_SIZE = struct.unpack('>I', ATOM_SIZE)[0]
    # ATOM size,should be 108 bytes in most cases
    pack = io.BytesIO(bytearray(pack[header_index:header_index + ATOM_SIZE]))
    return pack


def unpack(pack) -> type(ATOM):
    '''
        Unpacks MVHD ATOM header into a ATOM object
    '''
    header = _load(pack)
    atom = ATOM()
    atom.ATOM_SIZE = struct.unpack('>I', header.read(4))[0]
    atom.ATOM_TYPE = header.read(4).decode()
    atom.ATOM_VERSION = struct.unpack('>B', header.read(1))[0]
    atom.ATOM_FLAGS = header.read(3)
    atom.ATOM_CREATION_TIME = struct.unpack('>I', header.read(4))[0]
    atom.ATOM_MODIFICATION_TIME = struct.unpack('>I', header.read(4))[0]
    atom.ATOM_TIMESCALE = struct.unpack('>I', header.read(4))[0]
    atom.ATOM_DURATION = struct.unpack('>I', header.read(4))[0]
    atom.ATOM_PREFERED_RATE = struct.unpack('>f', header.read(4))[0]
    atom.ATOM_PREFERED_VOLUME = struct.unpack('>h', header.read(2))[0]
    atom.ATOM_RESERVED = header.read(10)
    atom.ATOM_MATRIX_STRUCT = header.read(36)
    atom.ATOM_PREVIEW_TIME = struct.unpack('>I', header.read(4))[0]
    atom.ATOM_PREVIEW_DURATION = struct.unpack('>I', header.read(4))[0]
    atom.ATOM_POSTER_TIME = struct.unpack('>I', header.read(4))[0]
    atom.ATOM_SELECTION_TIME = struct.unpack('>I', header.read(4))[0]
    atom.ATOM_SELECTION_DURATION = struct.unpack('>I', header.read(4))[0]
    atom.ATOM_CURRENT_TIME = struct.unpack('>I', header.read(4))[0]
    atom.ATOM_NEXT = struct.unpack('>I', header.read(4))[0]
    atom.ATOM_DURATION_SEC = atom.ATOM_DURATION / atom.ATOM_TIMESCALE
    return atom


if __name__ == "__main__":
    path = input('Media file path >>>').replace("\"", '')
    header = open(path, 'rb').read(256)
    atom = unpack(header)
    print('#'*50)
    for key in dir(atom):
        if 'ATOM' in key:
            print(key.ljust(24),getattr(atom,key))
    print('#'*50)
    input('Press ENTER to exit.')