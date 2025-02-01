import os
import re
import shutil
import time


# 1. Функция для копирования файла в новое место
def copy_file(src, dest):
    """
    Функция для копирования файла из источника в назначение.m

    Эта функция копирует файл из указанного источника (src) в указанное назначение (dest).
    Если файл с таким именем уже существует в целевой папке, он будет перезаписан.
    В случае успешного завершения операция копирования возвращает строку с подтверждением успешного копирования.
    В случае возникновения ошибки (например, если исходный файл не найден)
    будет выброшено исключение с соответствующим сообщением.

    :param src: Путь к исходному файлу.
    :param dest: Путь к файлу назначения, куда будет скопирован файл.
    :return: Сообщение о том, что файл успешно скопирован.
    :raises FileNotFoundError: Если исходный файл не найден.
    :raises PermissionError: Если у пользователя нет прав для чтения или записи.
    """
    try:
        shutil.copy(src, dest)
        return f"File {src} copied successfully to {dest}"
    except FileNotFoundError:
        raise FileNotFoundError(f"Source file {src} not found")
    except PermissionError:
        raise PermissionError(f"Permission denied for copying {src} to {dest}")


# 2. Функция для удаления файла или папки
def delete_file(path):
    """
    Функция для удаления файла или папки.

    Эта функция удаляет указанный файл или папку. Если путь указывает на папку, она будет удалена вместе
    с содержимым (рекурсивно). Если путь указывает на файл, будет удалён только файл.
    При возникновении ошибок (например, если файл не найден или нет прав на удаление)
    будет выброшено соответствующее исключение.

    :param path: Путь к файлу или папке для удаления.
    :return: Сообщение о том, что файл или папка была успешно удалена.
    :raises FileNotFoundError: Если указанный путь не существует.
    :raises PermissionError: Если у пользователя нет прав на удаление.
    """
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)  # Удаляем директорию и все её содержимое
            return f"Directory {path} and its contents deleted successfully"
        elif os.path.isfile(path):
            os.remove(path)  # Удаляем только файл
            return f"File {path} deleted successfully"
    except FileNotFoundError:
        raise FileNotFoundError(f"Path {path} not found")
    except PermissionError:
        raise PermissionError(f"Permission denied for deleting {path}")


# 3. Функция для подсчёта количества файлов в папке
def count_files(folder_path, recursive=False):
    """
    Функция для подсчёта файлов в папке.
    При включении рекурсии считает файлы во вложенных папках.

    :param folder_path: Путь к папке, в которой нужно посчитать файлы.
    :param recursive: Если True, то рекурсивно учитываются файлы в подкаталогах.
    :return: Количество файлов в указанной папке (и подкаталогах, если рекурсия включена).
    """
    file_count = 0

    # Проверяем, существует ли папка
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Папка {folder_path} не найдена")

    # Если не нужна рекурсия, просто считаем файлы в данной папке
    if not recursive:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                file_count += 1
    else:
        # Рекурсивный подсчёт файлов в папке и всех её подкаталогах
        for root, dirs, files in os.walk(folder_path):
            file_count += len(files)

    return file_count


# 4. Функция для поиска файлов, соответствующих регулярному выражению
def find_files(folder_path, pattern, recursive=False):
    """
    Функция для поиска файлов, соответствующих регулярному выражению.
    При включении рекурсии поиск будет выполняться, в том числе, и во вложенных папках.

    :param folder_path: Путь к папке, в которой нужно искать файлы.
    :param pattern: Регулярное выражение для поиска файлов.
    :param recursive: Если True, поиск будет происходить в подкаталогах.
    :return: Список файлов, которые соответствуют регулярному выражению.
    """
    matching_files = []

    # Проверяем, существует ли папка
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Папка {folder_path} не найдена")

    # Если не нужна рекурсия, ищем файлы только в данной папке
    if not recursive:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path) and re.search(pattern, item):
                matching_files.append(item_path)  # Добавляем полный путь
    else:
        # Рекурсивный поиск в папке и всех её подкаталогах
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if re.search(pattern, file):
                    matching_files.append(os.path.join(root, file))  # Добавляем полный путь

    return matching_files


# 5. Функция для добавления даты создания к именам файлов
def add_creation_date(folder_path, recursive=False):
    """
    Функция для добавления даты создания к именам файлов в указанной папке.
    При включении рекурсии, дата будет добавляться ко всем файлам во вложенных папках.

    :param folder_path: Путь к папке, в которой нужно добавить дату создания.
    :param recursive: Если True, добавление даты будет происходить и во вложенных папках.
    :return: Список файлов, к которым была добавлена дата создания.
    """
    renamed_files = []

    # Проверяем, существует ли папка
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Папка {folder_path} не найдена")

    # Если не нужна рекурсия, добавляем дату только для файлов в текущей папке
    if not recursive:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                # Получаем дату создания файла
                creation_time = os.path.getctime(item_path)
                creation_date = time.strftime('%Y-%m-%d', time.localtime(creation_time))
                new_name = f"{creation_date}_{item}"
                new_path = os.path.join(folder_path, new_name)

                # Переименовываем файл
                os.rename(item_path, new_path)
                renamed_files.append(new_path)
    else:
        # Рекурсивно обрабатываем все файлы в папке и подкаталогах
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Получаем дату создания файла
                creation_time = os.path.getctime(file_path)
                creation_date = time.strftime('%Y-%m-%d', time.localtime(creation_time))
                new_name = f"{creation_date}_{file}"
                new_path = os.path.join(root, new_name)

                # Переименовываем файл
                os.rename(file_path, new_path)
                renamed_files.append(new_path)

    return renamed_files


# 6. Функция для анализа размера папки
def analyse_folder(folder):
    """
    Функция для анализа размера папки и её содержимого.

    Эта функция анализирует размер указанной папки, включая все вложенные папки и файлы.
    Для каждого файла и папки выводится их размер, а также общий размер всей папки.

    :param folder: Путь к папке, которую нужно проанализировать.
    :return: Сообщение о размере всей папки и её содержимого.
    """
    try:
        total_size = 0
        folder_sizes = {}  # Словарь для хранения размеров папок
        file_sizes = []  # Список для хранения информации о размерах файлов

        # Проходим по всем файлам и папкам в указанной директории
        for dirpath, _, filenames in os.walk(folder):
            folder_size = 0  # Размер текущей папки
            # Анализируем каждый файл в папке
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                file_size = os.path.getsize(filepath)  # Размер файла
                total_size += file_size
                folder_size += file_size
                file_sizes.append((filepath, file_size))  # Добавляем информацию о файле

            # Добавляем размер текущей папки в словарь
            folder_sizes[dirpath] = folder_size

        # Формируем строку с итоговым выводом
        result = f"Full size: {total_size / (1024 ** 3):.2f} GB\n"  # Общий размер в гигабайтах
        # Для каждой папки и её содержимого добавляем информацию
        for folder, size in folder_sizes.items():
            result += f"> - {folder} {size / (1024 ** 3):.2f} GB\n"
        # Для каждого файла добавляем информацию о его размере
        for filepath, size in file_sizes:
            result += f"> - {filepath} {size / (1024 ** 2):.2f} MB\n"

        return result
    except Exception as e:
        # В случае ошибки выводим сообщение об ошибке
        return f"Error: {e}"


# 7. Функция для перемещения электронных книг в папку "MyBooks"

def move_ebooks(folder):
    """Функция для перемещения электронных книг в папку "MyBooks".
    Данная функция рекурсивно обходит все вложенные папки в указанном каталоге
    и перемещает файлы с расширениями, соответствующими электронным книгам (например, .epub, .pdf, .mobi),
    в директорию "MyBooks" внутри указанной папки.

    Если папка "MyBooks" ещё не существует, она будет создана автоматически.
    Если в папке нет файлов с подходящими расширениями для перемещения,
    будет возвращено сообщение об отсутствии таких файлов.

    Аргументы:
      folder (str): Путь к папке, в которой будет производиться поиск и перемещение файлов.

    Возвращаемое значение:
      str: Сообщение о результате выполнения функции. Если перемещение прошло успешно,
           будет возвращено сообщение о том, что все электронные книги были перемещены в папку "MyBooks".
           В случае ошибок или отсутствия файлов с нужными расширениями будет возвращено соответствующее сообщение.

    Исключения:
      Если возникает ошибка в процессе выполнения (например, проблемы с правами доступа, файловой системой и т.д.),
      будет возвращено сообщение с описанием ошибки.
    """
    try:
        # Создаём папку "MyBooks", если её нет
        mybooks_folder = os.path.join(folder, "MyBooks")
        if not os.path.exists(mybooks_folder):
            os.makedirs(mybooks_folder)

        # Перечень расширений для электронных книг
        ebook_extensions = [".epub", ".pdf", ".mobi"]
        moved_files = []

        # Рекурсивно проходим по всем папкам и файлам
        for dirpath, _, filenames in os.walk(folder):
            for file in filenames:
                file_path = os.path.join(dirpath, file)
                # Если файл подходит по расширению, перемещаем его в папку "MyBooks"
                if any(file.endswith(ext) for ext in ebook_extensions):
                    shutil.move(file_path, os.path.join(mybooks_folder, file))  # Перемещаем файл
                    moved_files.append(file)

        # Если не перемещено ни одного файла, возвращаем сообщение
        if not moved_files:
            return f"В папке '{folder}' нет электронных книг для перемещения"

        return f"Все электронные книги перемещены в '{mybooks_folder}'."

    except Exception as e:
        # В случае ошибки возвращаем сообщение об ошибке
        return f"Ошибка: {e}"
