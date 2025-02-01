import unittest
from unittest.mock import patch
import sys
import io
import os
import shutil
from manager.cli import main
from manager.commands import (copy_file, delete_file, count_files, find_files,
                              add_creation_date, analyse_folder, move_ebooks)

class TestCLI(unittest.TestCase):
    def setUp(self):
        """Этот метод вызывается перед каждым тестом"""
        # Создание временной директории для тестов
        self.test_dir = os.path.abspath('test_directory')
        self.source_file = os.path.join(self.test_dir, 'source.txt')
        self.dest_file = os.path.join(self.test_dir, 'destination.txt')
        os.makedirs(self.test_dir, exist_ok=True)

        # Создание файлов для тестирования
        with open(self.source_file, 'w') as f:
            f.write('This is a test file')
        with open(os.path.join(self.test_dir, 'file.txt'), 'w') as f:
            f.write('Another test file')
        with open(os.path.join(self.test_dir, 'file2.txt'), 'w') as f:
            f.write('Yet another test file')

    def tearDown(self):
        """Этот метод вызывается после каждого теста."""
        # Удаление тестовой директории и её содержимого
        shutil.rmtree(self.test_dir, ignore_errors=True)

    @patch('manager.cli.copy_file')
    def test_copy_file(self, mock_copy_file):
        mock_copy_file.side_effect = lambda src, dest: print("File source.txt copied successfully to destination.txt")
        test_args = ['cli.py', 'copy', self.source_file, self.dest_file]
        sys.argv = test_args

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()

        self.assertIn("File source.txt copied successfully to destination.txt", output)

    @patch('manager.cli.delete_file')
    def test_delete_file(self, mock_delete_file):
        # Mock the behavior of the delete_file function
        mock_delete_file.side_effect = lambda file_path: print(f"File {file_path} deleted successfully")

        test_args = ['cli.py', 'delete', os.path.join(self.test_dir, 'file.txt')]
        sys.argv = test_args

        # Capture the output
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()

        self.assertIn(f"File {os.path.join(self.test_dir, 'file.txt')} deleted successfully", output)

    @patch('manager.cli.count_files')
    def test_count_files(self, mock_count_files):
        # Mock the behavior of the count_files function
        mock_count_files.side_effect = lambda dir_path, _: print("3 files found")

        test_args = ['cli.py', 'count', self.test_dir]
        sys.argv = test_args

        # Capture the output
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()

        self.assertIn("3 files found", output)

    @patch('manager.cli.find_files')
    def test_find_files(self, mock_find_files):
        # Mock the behavior of the find_files function
        mock_find_files.return_value = "Found source.txt"

        test_args = ['cli.py', 'find', self.test_dir, '.*.txt']
        sys.argv = test_args

        # Capture the output
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()

        self.assertIn("Found source.txt", output)

    @patch('manager.cli.add_creation_date')
    def test_add_creation_date(self, mock_add_creation_date):
        # Mock the behavior of the add_creation_date function
        mock_add_creation_date.return_value = "Files renamed with creation date"

        test_args = ['cli.py', 'add_date', self.test_dir]
        sys.argv = test_args

        # Capture the output
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()

        self.assertIn("Files renamed with creation date", output)

    @patch('manager.cli.analyse_folder')
    def test_analyse_folder(self, mock_analyse_folder):
        # Mock the behavior of the analyse_folder function
        mock_analyse_folder.return_value = "Full size: 10MB"

        test_args = ['cli.py', 'analyse', self.test_dir]
        sys.argv = test_args

        # Capture the output
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()

        self.assertIn("Full size:", output)

    @patch('manager.cli.move_ebooks')
    def test_move_ebooks(self, mock_move_ebooks):
        # Mock the behavior of the move_ebooks function
        mock_move_ebooks.return_value = "All eBooks moved to 'MyBooks'"

        test_args = ['cli.py', 'move_ebooks', self.test_dir]
        sys.argv = test_args

        # Capture the output
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()

        self.assertIn("All eBooks moved to 'MyBooks'", output)


if __name__ == "__main__":
    unittest.main()
