from .unit import Unit
from .monad import Monad

class Writer(Monad):
    '''
    A ListWriter monad (w in (Writer a w) is always a list)
    '''
    def __init__(self, t):
        self.t = t

    @staticmethod
    def lift(x):
        return Writer((x, []))

    def fmap(self, f):
        x, w = self.t
        return Writer((f(x), w))

    def app(self, other):
        x, w = self.t
        return other.fmap(x)

    def bind(self, f):
        x1, w1 = self.t
        m = f(x1)        
        x2, w2 = m.t
        return Writer((x2, w1 + w2))

    @staticmethod
    def tell(w):
        return Writer((Unit(), w))

    def wpass(self):
        '''
        pass :: Writer (a, w -> w) -> Writer a
        '''
        t, w = self.t
        x, f = t
        return Writer((x, f(w)))

    def censor(self, f):
        x, w = self.t        
        return Writer((x, f)).wpass()

    def run(self):
        return self.t

    def listen(self):
        '''
        listen :: Writer w a -> Writer w (a, w)
        (the type parameter for Writer is flipped in the runWriter function)
        '''
        x, w = self.t 
        return Writer(((x, w), w))
