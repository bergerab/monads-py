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

if __name__ == '__main__':
   assert Identity.lift(3).bind(lambda x:
                         Identity.lift(2).bind(lambda y: Identity.lift(x + y))).x == 5
   assert Identity.lift(lambda x: x + 2).app(Identity.lift(4)).x == 6
