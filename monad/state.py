from .monad import Monad
from .unit import Unit

class State(Monad):
    '''
    State s a
    Takes an initial state s, yields a value a
    '''
    def __init__(self, run):
        self.run = run
        
    @staticmethod
    def lift(x):
        return State(lambda _: (Unit(), x))

    def bind(self, run):
        pass

    def put(self, f):
        pass

    def get(self):
        pass
