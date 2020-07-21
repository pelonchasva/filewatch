import main
import unittest

class TestFileHandling(unittest.TestCase):
    def test_create_folder_if_not_exists(self):
        """
        """
        path = "~/Downloads/Text"
        self.assertTrue(main.create_folder(path))

    def test_get_file_name(self):
        """
        """
        path = "~/Downloads/test.txt"
        self.assertEqual(main.get_file_name(path), "test.txt")

if __name__ == "__main__":
    unittest.main()