import flet as ft
from components import FileManagerGUI  # Импортируем наш компонент из components.py

def main(page: ft.Page):
    page.title = "Файловый Менеджер"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Инициализация интерфейса из components.py
    file_manager_gui = FileManagerGUI(page)

if __name__ == "__main__":
    ft.app(target=main)
