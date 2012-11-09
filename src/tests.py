import unittest

from steps import i_put_a_file, i_get_a_file

class HallOfMirrorsTests(unittest.TestCase):
    def test_everything(self):
        expected_title, expected_contents, expected_type = i_put_a_file()
        actual_title, actual_contents, actual_type = i_get_a_file()
        self.assertEqual(expected_title, actual_title)
        self.assertEqual(expected_contents, actual_contents)
        self.assertEqual(expected_type, actual_type)

if __name__ == '__main__':
    unittest.main()
