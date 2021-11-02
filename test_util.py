import unittest

from util import to_file_name


class UtilTestCase(unittest.TestCase):
    def test_to_file_name(self):
        names = [
            '1: hello world',
            'hello (world)',
            '  hello (world)  ',
            '(hello world)',
            'hello(world)',
            'hello – world',
            'hello’world',
            'Hello world',
            'hello.world',
            'hello/world',
        ]

        for name in names:
            self.assertEqual(to_file_name(name), 'hello_world')


if __name__ == '__main__':
    unittest.main()
