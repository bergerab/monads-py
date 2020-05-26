from monad.identity import Identity

if __name__ == '__main__':
    assert Identity.lift(3).bind(lambda x:
    		      Identity.lift(2).bind(lambda y: Identity.lift(x + y))).get() == 5
    assert Identity.lift(lambda x: x + 2).app(Identity.lift(4)).get() == 6
