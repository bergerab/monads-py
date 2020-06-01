from .monad import Monad
from .unit import Unit

class State(Monad):
    '''
    State s a
    Do some computation with some implicitly kept state
    The state is s, and the computation's value is a

    The initial state "s" is given when ~state.run~ is called.
    '''
    def __init__(self, run):
        self.run = run
        
    @staticmethod
    def lift(x):
        return State(lambda s: (x, s))

    def bind(self, f):
        def run(s):
            (_a, _s) = self.run(s)
            return f(_a).run(_s)
        return State(run)

    @staticmethod
    def put(x):
        '''
        put :: s -> State ()
        Set the state value
        '''
        return State(lambda _: (Unit(), x))

    @staticmethod
    def get():
        '''
        get :: State s
        Access the state value
        '''
        return State(lambda s: (s, s))
