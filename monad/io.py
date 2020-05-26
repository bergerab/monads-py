from .monad import Monad
from .unit import Unit

class IO(Monad):
    def __init__(self, x):
        self.x = x
    
    @staticmethod
    def lift(x):
        return IO(x)

    def bind(self, f):
        '''
        bind :: IO a -> (a -> IO b) -> IO b
        '''
        return f(self.run())

    def fmap(self, f):
        '''
        fmap :: IO a -> (a -> b) -> IO b
        '''
        return f(self.run())

    def app(self, other):
        '''
        app :: IO (a -> b) -> IO a -> IO b
        '''
        return IO.lift(self.run()(other.val()))

    def run(self):
        if isinstance(self, IOInput):
            return input()
        elif isinstance(self, IOOutput):
            if not self.handle:
                print(self.x, end='')
            else:
                self.handle.write(self.x)
            return Unit()
        elif isinstance(self, IOFile):
            return open(self.file_path, self.io_mode)
        elif isinstance(self, IOClose):
            self.handle.close()
            return Unit()

class IOInput(IO):
    def __init__(self):
        pass
class IOOutput(IO):
    def __init__(self, x, handle):
        self.x = x
        self.handle = handle
class IOFile(IO):
    def __init__(self, file_path, io_mode):
        self.file_path = file_path
        self.io_mode = io_mode
class IOClose(IO):
    def __init__(self, handle):
        self.handle = handle

def io_print(x):
    '''
    io_print :: a -> IO ()
    '''
    return IOOutput(x, None)

def io_println(x):
    '''
    io_println :: a -> IO ()
    '''
    return IOOutput(x + '\n', None)
        
def io_write(handle, x):
    '''
    io_write :: Handle -> a -> IO ()
    '''
    return IOOutput(x, handle)

def io_close(handle):
    '''
    io_close :: Handle -> IO ()
    '''
    return IOClose(handle)

def io_input():
    '''
    io_input :: IO String
    '''
    return IOInput()

def io_open(file_path, io_mode='r'):
    '''
    type FilePath = String;
    type IOMode = String;
    io_open :: FilePath -> IOMode -> IO Handle
    '''
    return IOFile(file_path, io_mode)

if __name__ == '__main__':
    io_print('Enter some text: ') \
    .then(io_input()) \
        .bind(lambda text: io_open('test_file.txt', 'w') \
              .bind(lambda handle: io_write(handle, text + '!') \
                    .then(io_close(handle)) \
                    .then(io_print('Done'))))
