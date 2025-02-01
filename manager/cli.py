import argparse
from manager.commands import (copy_file, delete_file, count_files, find_files,
                              add_creation_date, analyse_folder, move_ebooks)
import sys

def main():
    """
    Main function to handle the command-line interface (CLI) commands.
    This function uses argparse to parse user input, determine the desired action,a
    and call the corresponding function from the 'commands' module.

    Available commands:
    - copy: Copy a file from source to destination.
    - delete: Delete a file or directory.
    - count: Count the number of files in a directory.
    - find: Find files based on a pattern in a directory.
    - add_date: Add the creation date to the filenames in a directory.
    - analyse: Analyse the size of a directory.
    - move_ebooks: Move ebooks to a "MyBooks" folder.
    """
    parser = argparse.ArgumentParser(description="File management CLI")

    # Define the commands and their arguments
    subparsers = parser.add_subparsers(dest='command')

    # Command to copy a file
    copy_parser = subparsers.add_parser('copy', help="Copy a file")
    copy_parser.add_argument('src', help="Source file path")
    copy_parser.add_argument('dest', help="Destination file path")

    # Command to delete a file or directory
    delete_parser = subparsers.add_parser('delete', help="Delete a file or directory")
    delete_parser.add_argument('path', help="Path to the file or directory to delete")

    # Command to count files in a directory
    count_parser = subparsers.add_parser('count', help="Count the number of files in a directory")
    count_parser.add_argument('folder', help="Folder path")
    count_parser.add_argument('--recursive', action='store_false', help="Count files recursively")

    # Command to find files matching a pattern
    find_parser = subparsers.add_parser('find', help="Find files based on a pattern")
    find_parser.add_argument('folder', help="Folder path")
    find_parser.add_argument('pattern', help="Pattern to search for")
    find_parser.add_argument('--recursive', action='store_true', help="Search files recursively")

    # Command to add creation date to filenames
    add_date_parser = subparsers.add_parser('add_date', help="Add creation date to filenames")
    add_date_parser.add_argument('folder', help="Folder path")
    add_date_parser.add_argument('--recursive', action='store_true', help="Add date recursively")

    # Command to analyze folder size
    analyse_parser = subparsers.add_parser('analyse', help="Analyze the size of a folder")
    analyse_parser.add_argument('folder', help="Folder path to analyze")

    # Command to move ebooks to 'MyBooks' folder
    move_ebooks_parser = subparsers.add_parser('move_ebooks', help="Move ebooks to 'MyBooks' folder")
    move_ebooks_parser.add_argument('folder', help="Folder path to search for ebooks")

    # Parse the arguments and call the appropriate function
    args = parser.parse_args()

    if args.command == 'copy':
        print(copy_file(args.src, args.dest))
    elif args.command == 'delete':
        print(delete_file(args.path))
    elif args.command == 'count':
        print(count_files(args.folder, args.recursive))
    elif args.command == 'find':
        print(find_files(args.folder, args.pattern, args.recursive))
    elif args.command == 'add_date':
        print(add_creation_date(args.folder, args.recursive))
    elif args.command == 'analyse':
        print(analyse_folder(args.folder))
    elif args.command == 'move_ebooks':
        print(move_ebooks(args.folder))
    else:
        parser.print_help(sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
