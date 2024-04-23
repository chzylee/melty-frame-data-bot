import unittest
from commands import teatime

class TestTeatime(unittest.TestCase):
    def test_have_teatime_does_return_message(self):
        self.assertIsNotNone(teatime.have_teatime())


if __name__ == '__main__':
    unittest.main()
