from .unit import Unit
from .monad import Monad

class Writer(Monad):
    '''
    A ListWriter monad (w in (Writer a w) is always a list)
    '''
    def __init__(self, x, w=None):
        self.x = x
        self.w = w if w else []

    @staticmethod
    def lift(x):
        return Writer(x)

    def fmap(self, f):
        return Writer(f(self.x), self.w)

    def app(self, other):
        return other.fmap(self.x)

    def tell(self, ws):
        return Writer(Unit(), self.w + self.ws)

    def listen(self):
        return Writer((self.x, self.w), self.w)

    def bind(self, f):
        m = f(self.x)
        return Writer(m.x, m.msg)
    
    def get(self):
        '''
        Extracts the value from the monad
        '''
        return self.x
