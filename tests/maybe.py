import unittest
from ..maybe import Just, Nothing

class TestMaybe(unittest.TestCase):
    def test_fmap(self):
        self.assertEqual(
            Just(1).fmap(lambda x: x + 1),
            2)

        

if __name__ == '__main__':
    unittest.main()
