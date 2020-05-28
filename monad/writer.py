from .unit import Unit
from .monad import Monad

class Writer(Monad):
    def __init__(self, t):
        self.t = t
        '''
        A tuple of (x, w) -- for Python it might have been better to use a lambda.
        That way, "running" the monad makes more sense. You could control evaluation.
        This way, evaluation is immediate.
        '''

    @staticmethod
    def lift(x, w=[]):
        '''
        By default, this is a ListWriter monad, but you can pass w here to make use another type.
        (so long as that type works with __add__)
        __add__ is used as mappend.
        The w parameter here is used as mempty.
        '''
        return Writer((x, w))

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
        This is called ~wpass~ because ~pass~ is reserved in Python.
        '''
        t, w = self.t
        x, f = t
        return Writer((x, f(w)))

    def censor(self, f):
        '''
        censor :: m a -> (w -> w) -> m a
        Executes ~self~ applies ~f~ to its output (the monoid ~w~).
        This is a helper to use the ~pass~ function without lifting tuples into a writer.
        '''
        x, w = self.t
        return Writer((x, f)).wpass()

    def run(self):
        return self.t

    def listen(self):
        '''
        listen :: Writer w a -> Writer w (a, w)
        (the type parameter for Writer is flipped in the runWriter function)

        Executes the given writer, and gives access to the value and monoid in the returned writer.
        '''
        x, w = self.t 
        return Writer(((x, w), w))

    def listens(self, f):
        '''
        listens :: m a -> (w -> b) -> m (a, b)
        Maps a function over the writer's output value, and includes that in the next writer.
        I have the arguments flipped here, because Python always has ~self~ as the first argument in methods.
        '''
        return self.listen().bind(lambda t: Writer.lift(t[0], f(t[1])))
