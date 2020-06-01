from .monad import Monad

class Cont(Monad):
    @staticmethod
    def lift(x):
        pass

    def bind(self, f):
        pass


def plus(a, b, k):
    k(a + b)

def div(a, b, k):
    if b == 0:
        return 'Error'
    else:
        k(a / b)

div(3, 0, lambda x: print(x))
