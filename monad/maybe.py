from monad import Monad

class Maybe(Monad):
    '''
    Maybe a
    '''
    @staticmethod
    def lift(x):
        '''
        lift :: a -> Maybe a
        '''
        return Just(x)

    def bind(self, f):
        '''
        bind :: (Maybe a) -> (a -> Maybe b) -> (Maybe b)
        '''
        if isinstance(self, Nothing):
            return self
        return f(self.x)

    def fmap(self, f):
        '''
        fmap :: (Maybe a) -> (a -> b) -> (Maybe b)
        '''
        if isinstance(self, Just):
            return Just(f(self.x))
        return self

    def app(self, other):
        '''
        <*> :: Maybe (a -> b) -> Maybe a -> Maybe b
        app isn't very useful without currying.
        You can't do things like  ~pure (+) <*> pure (*2) <*> pure (*4)~
        '''
        if isinstance(self, Just):
            return other.fmap(self.x)
        return self

class Nothing(Maybe):
    pass
class Just(Maybe):
    def __init__(self, x):
        self.x = x

def test_maybe():
    Just(lambda x: x + 2) \
        .app(Just(3)) \
        .bind(lambda x: Just(str(x))) \
        .bind(lambda x: Just(x + '!')) \
        .fmap(lambda x: print(x))
