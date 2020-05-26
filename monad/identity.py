from .monad import Monad

class Identity(Monad):
    def __init__(self, x):
        self.x = x

    @staticmethod
    def lift(x):
        return Identity(x)

    def bind(self, f):
        return f(self.x)

    def fmap(self, f):
        return Identity.lift(f(self.x))

    def app(self, other):
        return Identity.lift(self.x(other.x))

    def get(self):
        '''
        Extracts the value from the monad
        '''
        return self.x
