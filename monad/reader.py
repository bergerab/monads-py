from monad import Monad

class Reader(Monad):
    '''
    Reader e a
    '''
    def __init__(self, run):
        self.run = run
        
    @staticmethod
    def lift(x):
        '''
        lift :: a -> Reader e a
        Makes a reader that ignore environment and return x
        '''
        return Reader(lambda e: x)

    def ask(self):
        '''
        ask :: Reader e a -> Reader e e
        Makes a reader that gives the environment
        '''
        return Reader(lambda e: e)

    def local(self, f):
        '''
        local :: Reader e a -> (e -> e) -> Reader e a
        '''
        return Reader(lambda e: self.run(f(e)))

    def bind(self, f):
        '''
        bind :: (Reader e a) -> (a -> Reader e b) -> (Reader e b)
        '''
        return Reader(lambda e: f(self.run(e)).run(e))

    def fmap(self, f):
        '''
        fmap :: Reader e a -> Reader e b
        '''
        return Reader(lambda e: f(self.run(e)))

    def app(self, other):
        '''
        <*> :: Reader e (a -> b) -> Reader e a -> Reader e b
        '''
        return Reader(lambda e: self.run(e)(other.run(e)))

def test_reader():
    x = Reader() \
        .run({ 'lives': 1 })
    print(x)
