import unittest

from transform import Transform


class TransformTestCase(unittest.TestCase):
    def test_to_title(self):
        pass

    def test_start_instruct(self):
        self.assertEqual(Transform.instruct('end', 'document'), '\\end{document}')
        self.assertEqual(Transform.instruct('makeindex'), '\\makeindex')
        self.assertEqual(Transform.instruct('date', ''), '\\date{}')
        self.assertEqual(Transform.instruct('setcounter', 'tocdepth', '3'), '\\setcounter{tocdepth}{3}')


if __name__ == '__main__':
    unittest.main()
