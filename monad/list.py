from .monad import Monad

class List:
    def __init__(self, xs):
        self.xs = xs
    
    @staticmethod
    def lift(x):
        return List([x])

    def fmap(self, f):
        return List(list(map(f, self.xs)))

    def app(self, other):
        ys = []
        for f in self.xs:
            for x in other.xs:
                ys.append(f(x))
        return List(ys)

    def bind(self, f):
        xs = []
        for ys in self.fmap(f).xs:
            xs += ys.xs
        return List(xs)

    def filter(self, f):
        return List(filter(f, self.xs))

    def get(self):
        '''
        Extracts the value from the monad
        '''
        return self.xs
