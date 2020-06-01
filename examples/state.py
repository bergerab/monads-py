from monad.state import State

lift = lambda f: State.get().bind(lambda s: State.put(f(s)))
'''
Lifts a function to apply it to the state
'''

inc = lift(lambda s: s + 1)
'''
Increments the state by one
'''

g = inc.bind(lambda v: State.get())
'''
State Int Int
Increments the State
'''

main = g.bind(lambda v: lift(lambda v: v + v))
'''
Increment the state using State monad ~g~, then add with itself.
'''

if __name__ == '__main__':
    assert main.run(4)[1] == 10
    '''
    Executes some state-dependent imperative code like:

    s = 4
    def g():
        s += 1
    def main():
        s += s
        return s
    '''
