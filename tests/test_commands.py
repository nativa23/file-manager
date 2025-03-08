import unittest
import os
import shutil
from manager.commands import (
    copy_file, delete_file, count_files, find_files,
    add_creation_date, analyse_folder, move_ebooks
)

class TestCommands(unittest.TestCase):

    def setUp(self):
        """Этот метод вызывается перед каждым тестом."""
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

    def test_copy_file(self):
        """Тестирует копирование файла"""
        copy_file(self.source_file, self.dest_file)

        # Проверка, что файл действительно создан
        self.assertTrue(os.path.exists(self.dest_file))

        # Проверка, что содержимое скопировано корректно
        with open(self.source_file, 'r') as src, open(self.dest_file, 'r') as dest:
            self.assertEqual(src.read(), dest.read())

    def test_delete_file(self):
        """Тестирование удаления файла."""
        file_to_delete = os.path.join(self.test_dir, 'file.txt')
        delete_file(file_to_delete)
        self.assertFalse(os.path.exists(file_to_delete))

    def test_count_files(self):
        """Тестирование подсчёта файлов в директории."""
        count = count_files(self.test_dir)
        self.assertEqual(count, 3)  # Ожидаем, что в директории 3 файла

    def test_find_files(self):
        """Тестирование поиска файлов с определённым расширением."""
        found_files = find_files(self.test_dir, r'.*\.txt$')  # исправленный шаблон

        # Проверка, что полный путь к файлам присутствует в списке найденных
        self.assertIn(os.path.join(self.test_dir, 'source.txt'), found_files)
        self.assertIn(os.path.join(self.test_dir, 'file.txt'), found_files)
        self.assertIn(os.path.join(self.test_dir, 'file2.txt'), found_files)

    def test_add_creation_date(self):
        """Тестирование добавления даты создания в имена файлов."""
        add_creation_date(self.test_dir)
        files = os.listdir(self.test_dir)
        self.assertTrue(any('source' in file for file in files))

    def test_analyse_folder(self):
        """Тестирование анализа папки."""
        result = analyse_folder(self.test_dir)
        self.assertIn('Full size:', result)

    def test_move_ebooks(self):
        """Тестирование перемещения eBooks в папку MyBooks."""
        # Создание eBook-файла
        ebook_file = os.path.join(self.test_dir, 'test_book.epub')
        with open(ebook_file, 'w') as f:
            f.write('Ebook content')

        move_ebooks(self.test_dir)

        # Проверка, что MyBooks создана и файл туда перемещён
        mybooks_dir = os.path.join(self.test_dir, 'MyBooks')
        self.assertTrue(os.path.exists(mybooks_dir))
        self.assertTrue(os.path.exists(os.path.join(mybooks_dir, 'test_book.epub')))

# Запуск тестов
if __name__ == '__main__':
    unittest.main()
