class Monad:
    def then(self, other):
        '''
        then :: m a -> m b -> m b
        '''
        return self.bind(lambda _: other)
