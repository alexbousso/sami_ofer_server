from Subscribers import Subscribers
import unittest
import os
import os.path


class TestSubscribers(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSubscribers, self).__init__(*args, **kwargs)
        if os.path.exists('subscribers') and os.path.isfile('subscribers'):
            os.remove('subscribers')
        self.subscribers = Subscribers()

    def test_check_if_email(self):
        self.subscribers.__check_if_email__('a@b.com')
        with self.assertRaises(ValueError):
            self.subscribers.__check_if_email__('Hello world!')
        with self.assertRaises(ValueError):
            self.subscribers.__check_if_email__('a@b')
        with self.assertRaises(ValueError):
            self.subscribers.__check_if_email__('@.com')
        with self.assertRaises(ValueError):
            self.subscribers.__check_if_email__(42)

    def test_add(self):
        self.subscribers.add('a@b.com')
        self.subscribers.add('a@b.co.il')
        with self.assertRaises(Exception):
            self.subscribers.add('a@b.com')
        s = Subscribers()
        with self.assertRaises(Exception):
            s.add('a@b.com')
        s.add('hello@world.com')
        with self.assertRaises(Exception):
            s.add('hello@world.com')


if __name__ == '__main__':
    unittest.main()
