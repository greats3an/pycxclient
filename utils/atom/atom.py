'''
# atom Module

    Unpacks a video's QuickTime ATOM (`moov`) info via its ATOM header / footer

    reference:https://developer.apple.com/library/archive/documentation/QuickTime/QTFF/QTFFChap2/qtff2.html (fig.2-3)
'''
import struct
import io

def prop(func):
    @property
    def wrapper(self):
        return getattr(self,'_' + func.__name__)
    @wrapper.setter
    def wrapper():
        raise Exception("Writing ATOM headers is not currently supported")
    return wrapper

class ATOM:
    '''
        # ATOM Movie header object
        Parses a standard `mvhd` ATOM header

        Usage:

            mvhdbytes = ATOM.extract(videoblock)
            mvhdheads = ATOM(mvhdbytes)
        
        see:https://developer.apple.com/library/archive/documentation/QuickTime/QTFF/QTFFChap2/qtff2.html
    '''
    def __init__(self,mvhd : bytearray):
        '''Parses ATOM values'''
        mvhd = io.BytesIO(mvhd)
        # Converts into BytesIO for further convinence
        self._ATOM_SIZE = struct.unpack('>I', mvhd.read(4))[0]
        self._ATOM_TYPE = mvhd.read(4).decode()
        self._ATOM_VERSION = struct.unpack('>B', mvhd.read(1))[0]
        self._ATOM_FLAGS = mvhd.read(3)
        self._ATOM_CREATION_TIME = struct.unpack('>I', mvhd.read(4))[0]
        self._ATOM_MODIFICATION_TIME = struct.unpack('>I', mvhd.read(4))[0]
        self._ATOM_TIMESCALE = struct.unpack('>I', mvhd.read(4))[0]
        self._ATOM_DURATION = struct.unpack('>I', mvhd.read(4))[0]
        self._ATOM_PREFERED_RATE = struct.unpack('>f', mvhd.read(4))[0]
        self._ATOM_PREFERED_VOLUME = struct.unpack('>h', mvhd.read(2))[0]
        self._ATOM_RESERVED = mvhd.read(10)
        self._ATOM_MATRIX_STRUCT = mvhd.read(36)
        self._ATOM_PREVIEW_TIME = struct.unpack('>I', mvhd.read(4))[0]
        self._ATOM_PREVIEW_DURATION = struct.unpack('>I', mvhd.read(4))[0]
        self._ATOM_POSTER_TIME = struct.unpack('>I', mvhd.read(4))[0]
        self._ATOM_SELECTION_TIME = struct.unpack('>I', mvhd.read(4))[0]
        self._ATOM_SELECTION_DURATION = struct.unpack('>I', mvhd.read(4))[0]
        self._ATOM_CURRENT_TIME = struct.unpack('>I', mvhd.read(4))[0]
        self._ATOM_NEXT = struct.unpack('>I', mvhd.read(4))[0]
        self._ATOM_DURATION_SEC = self._ATOM_DURATION / self._ATOM_TIMESCALE        
        super().__init__()

    # region Staticmethods
    @staticmethod
    def _index(subiter, mainiter) -> int:
        '''
            Indexing a iterable from another iterable
        '''
        for i in range(0, len(mainiter) - len(subiter)):
            if mainiter[i:i+len(subiter)] == subiter:
                return i
        return -1

    @staticmethod
    def _locate(pack, header='mvhd') -> int:
        '''
            Locates ATOM Header index
        '''
        header_index = ATOM._index(header.encode(), pack) - len(header)
        # Locating header
        if header_index < 0:
            raise Exception(f"{header} Header not found")
        return header_index
    
    @staticmethod
    def extract(pack) -> bytearray:
        '''
            Extracts bytesarray to get mvhd header
        '''
        header_index = ATOM._locate(pack)
        ATOM_SIZE = bytearray(pack[header_index:header_index + 4])
        ATOM_SIZE = struct.unpack('>I', ATOM_SIZE)[0]
        # ATOM size,should be 108 bytes in most cases
        pack = bytearray(pack[header_index:header_index + ATOM_SIZE])
        return pack

    # endregion

    # region Properties
    
    @prop
    def ATOM_SIZE(self):
        """A 32-bit integer that specifies the number of bytes in this movie header atom"""
        pass
    @prop
    def ATOM_TYPE(self):
        """A 32-bit integer that identifies the atom type; must be set to 'mvhd'."""
        pass
    @prop
    def ATOM_VERSION(self):
        """A 1-byte specification of the version of this movie header atom."""
        pass
    @prop
    def ATOM_FLAGS(self):
        """Three bytes of space for future movie header flags."""
        pass
    @prop
    def ATOM_CREATION_TIME(self):
        """
        A 32-bit integer that specifies the calendar date and time (in seconds since midnight, January 1, 1904) 
        when the movie atom was created. It is strongly recommended that this value should be specified using coordinated universal time (UTC).
        """
        pass
    @prop
    def ATOM_MODIFICATION_TIME(self):
        """
        A 32-bit integer that specifies the calendar date and time (in seconds since midnight, January 1, 1904) 
        when the movie atom was changed. BooleanIt is strongly recommended that this value should be specified using coordinated universal time (UTC).
        """
        pass
    @prop
    def ATOM_TIMESCALE(self):
        """
        A time value that indicates the time scale for this movie—that is, 
        the number of time units that pass per second in its time coordinate system. 
        A time coordinate system that measures time in sixtieths of a second, for example, has a time scale of 60.
        """
        pass
    @prop
    def ATOM_DURATION(self):
        """
        A time value that indicates the duration of the movie in time scale units. 
        Note that this property is derived from the movie’s tracks. The value of this field corresponds to the duration of the longest track in the movie.
        """
        pass
    @prop
    def ATOM_PREFERED_RATE(self):
        """A 32-bit fixed-point number that specifies the rate at which to play this movie. A value of 1.0 indicates normal rate."""
        pass
    @prop
    def ATOM_PREFERED_VOLUME(self):
        """A 16-bit fixed-point number that specifies how loud to play this movie’s sound. A value of 1.0 indicates full volume."""
        pass
    @prop
    def ATOM_RESERVED(self):
        """Ten bytes reserved for use by Apple. Set to 0."""
        pass
    @prop
    def ATOM_MATRIX_STRUCT(self):
        """
        The matrix structure associated with this movie. A matrix shows how to map points from one coordinate space into another. 
        """
        pass
    @prop
    def ATOM_PREVIEW_TIME(self):
        """The time value in the movie at which the preview begins."""
        pass
    @prop
    def ATOM_PREVIEW_DURATION(self):
        """The duration of the movie preview in movie time scale units."""
        pass
    @prop
    def ATOM_POSTER_TIME(self):
        """The time value of the time of the movie poster."""
        pass
    @prop
    def ATOM_SELECTION_TIME(self):
        """The time value for the start time of the current selection."""
        pass
    @prop
    def ATOM_SELECTION_DURATION(self):
        """The duration of the current selection in movie time scale units."""
        pass
    @prop
    def ATOM_CURRENT_TIME(self):
        """The time value for current time position within the movie."""
        pass
    @prop
    def ATOM_NEXT(self):
        """A 32-bit integer that indicates a value to use for the track ID number of the next track added to this movie. Note that 0 is not a valid track ID value."""
        pass
    @prop
    def ATOM_DURATION_SEC(self):
        """The duration (in seconds) of the movie"""
        pass
    # endregion

def unpack(block:bytearray) -> ATOM:
    '''Unpacks the ATOM header from a bytearray block'''
    return ATOM(ATOM.extract(block))

if __name__ == "__main__":
    path = input('Media file path >>>').replace("\"", '')
    header = open(path, 'rb').read(256)
    atom = unpack(header)
    print('#'*50)
    for key in dir(atom):
        if key[:4] == 'ATOM':
            print(key.ljust(24),getattr(atom,key))
    print('#'*50)
    input('Press ENTER to exit.')
