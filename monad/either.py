from monad import Monad

class Either(Monad):
    def __init__(self, x):
        self.x = x
        
    @staticmethod
    def lift(x):
        return Right(x)

    def fmap(self, f):
        '''
        fmap :: Either a b -> (b -> c) -> Either a c
        '''
        if isinstance(self, Right):
            return Right(f(self.x))
        return self
    
    def app(self, other):
        '''
        <*> :: Either a (b -> c) -> Either a b -> Either a c
        '''
        if isinstance(self, Right):
            return Right(other.fmap(self.x))
        return self

    def bind(self, f):
        '''
        bind :: Either a b -> (b -> Either a c) -> Either a c
        '''
        if isinstance(self, Right):
            return f(self.x)
        return self

class Left(Either): pass

class Right(Either): pass
