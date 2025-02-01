# File Management Script

This Python script provides a set of functions to manage files in various ways. The script includes operations such as copying, deleting, counting, renaming files, and analyzing directories. It also supports recursive operations when needed.
README is also available in [Russian](README.ru.md)

## Functions Overview

### 1. Copy File
   - **Function**: `copy_file`
   - **Description**: This function copies a file from the source path to the destination path.
   - **Arguments**:
     - `source` (str): The path of the file to be copied. This can be a relative or absolute path.
     - `destination` (str): The path where the file will be copied. This can be a relative or absolute path.
   - **Returns**: A success message upon successful copying.
   - **Example usage**:
     ```python
     copy_file('source.txt', 'destination.txt')
     ```

### 2. Delete File
   - **Function**: `delete_file`
   - **Description**: Deletes the specified file.
   - **Arguments**:
     - `file_path` (str): The path to the file to be deleted. This can be a relative or absolute path.
   - **Returns**: A success message indicating that the file was deleted successfully.
   - **Example usage**:
     ```python
     delete_file('file.txt')
     ```

### 3. Count Files in Directory
   - **Function**: `count_files`
   - **Description**: Counts the number of files in a directory.
   - **Arguments**:
     - `directory_path` (str): The path to the directory where the files will be counted.
     - `recursive` (bool, optional): If set to `True`, the function will also count files in subdirectories. Default is `False`.
   - **Returns**: A message indicating the total number of files found in the specified directory (and its subdirectories if `recursive=True`).
   - **Example usage**:
     ```python
     count_files('test_directory', recursive=True)
     ```

### 4. Find Files in Directory
   - **Function**: `find_files`
   - **Description**: Finds all files in the specified directory matching a given pattern.
   - **Arguments**:
     - `directory_path` (str): The path to the directory where the search will be performed.
     - `pattern` (str): The pattern used for the search (e.g., `*.txt` to find all `.txt` files).
   - **Returns**: A list of files that match the specified pattern.
   - **Example usage**:
     ```python
     find_files('test_directory', '*.txt')
     ```

### 5. Add Creation Date to Files
   - **Function**: `add_creation_date`
   - **Description**: Renames all files in a directory by adding the creation date of each file to the filename.
   - **Arguments**:
     - `directory_path` (str): The path to the directory where the files will be renamed.
   - **Returns**: A message indicating that the files were renamed with their creation dates.
   - **Example usage**:
     ```python
     add_creation_date('test_directory')
     ```

### 6. Analyze Folder Size
   - **Function**: `analyse_folder`
   - **Description**: Analyzes the total size of a folder and its contents.
   - **Arguments**:
     - `directory_path` (str): The path to the directory that will be analyzed.
   - **Returns**: A message indicating the total size of the directory and the number of files it contains.
   - **Example usage**:
     ```python
     analyse_folder('test_directory')
     ```

### 7. Move eBooks to 'MyBooks' Folder
   - **Function**: `move_ebooks`
   - **Description**: This function moves all files with typical eBook extensions (`.epub`, `.mobi`, `.pdf`, etc.) from the specified directory to a folder named `MyBooks`. If the folder does not exist, it will be created. The function supports recursive operations, meaning it can also move eBooks from subdirectories if `recursive=True` is passed.
   - **Arguments**:
     - `directory_path` (str): The path to the directory where the eBooks are located.
     - `recursive` (bool, optional): If set to `True`, the function will recursively search subdirectories for eBooks. Default is `True`.
   - **Returns**: A message indicating that the eBooks were moved to the `MyBooks` folder.
   - **Example usage**:
     ```python
     move_ebooks('test_directory', recursive=True)
     ```
## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your_user/your_repository.git
    ```

2. Navigate to the project folder:
    ```bash
    cd your_repository
    ```

3. Install the required dependencies (if listed in `requirements.txt`):
    ```bash
    pip install -r requirements.txt
    ```

Your project is now ready to use!

## License

This project is open and available for use without any restrictions. You are free to use, modify, and distribute the code.
