import flet as ft
from manager.commands import copy_file, delete_file, count_files, find_files, add_creation_date, analyse_folder, \
    move_ebooks


class FileManagerGUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Файловый Менеджер"
        self.page.scroll = "adaptive"
        self.page.vertical_alignment = ft.MainAxisAlignment.START

        # Фиксированный размер окна
        self.page.window.center()
        self.page.window.width = 800
        self.page.window.height = 550
        self.page.window_resizable = True
        self.page.window_maximizable = True

        # Поля для выбора файла и директории
        self.selected_path = None
        self.path_display = ft.Text("", color="#333333", size=14, weight=ft.FontWeight.BOLD)

        self.file_picker = ft.FilePicker(on_result=self.on_file_selected)
        self.page.overlay.append(self.file_picker)

        # Стили кнопок
        button_style = ft.ButtonStyle(
            bgcolor="#7D3C98",
            color="white",
            shape=ft.RoundedRectangleBorder(radius=8),
            overlay_color="#AF7AC5",
        )

        # Кнопки выбора файла и папки рядом
        self.file_picker_button = ft.ElevatedButton("Выбрать файл", style=button_style, on_click=self.pick_file)
        self.dir_picker_button = ft.ElevatedButton("Выбрать папку", style=button_style, on_click=self.pick_directory)
        self.path_row = ft.Row([self.file_picker_button, self.dir_picker_button])

        # Выпадающий список инструментов (всегда полный)
        self.tool_select = ft.Dropdown(
            label="Выберите инструмент",
            options=[
                ft.dropdown.Option("Копировать файл"),
                ft.dropdown.Option("Удалить файл"),
                ft.dropdown.Option("Добавить дату в имя файла"),
                ft.dropdown.Option("Найти файлы"),
                ft.dropdown.Option("Анализировать папку"),
                ft.dropdown.Option("Переместить книги"),
                ft.dropdown.Option("Подсчитать файлы"),
            ],
            on_change=self.on_tool_selected,
            border_color = "#7D3C98",
            focused_border_color = "#AF7AC5",
            color = "#333333",
        )

        # Поля для аргументов (по умолчанию скрыты)
        self.args_input1 = ft.TextField(label="Аргумент 1", visible=False)
        self.args_recursive = ft.Checkbox(label="Обходить рекурсивно?", visible=False)

        self.run_button = ft.ElevatedButton("Запустить", style=button_style, on_click=self.run_tool, visible=False)
        self.output_text = ft.Text()

        # Результаты работы
        self.result_container = ft.Container(
            content=ft.Column([
                ft.Text("Результаты работы", color="#333333", weight=ft.FontWeight.BOLD),
                self.output_text
            ]),
            border=ft.border.all(1, color='#7D3C98'),
            padding=10,
            margin=5,
            width=790,
            border_radius = 8,
            visible=False
        )

        # Добавляем компоненты на страницу
        self.page.add(
            self.path_row,
            self.path_display,
            self.tool_select,
            self.args_input1,
            self.args_recursive,
            self.run_button,
            self.output_text,
            self.result_container
        )

    def pick_file(self, e):
        self.file_picker.pick_files(allow_multiple=False)

    def pick_directory(self, e):
        self.file_picker.get_directory_path()

    def on_file_selected(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.selected_path = e.files[0].path
        elif e.path:
            self.selected_path = e.path
        else:
            self.selected_path = None
            self.path_display.value = "Не выбран файл или директория"
            self.path_display.update()
            return

        self.path_display.value = f"Выбрано: {self.selected_path}"
        self.path_display.update()

    def on_tool_selected(self, e):
        tool = self.tool_select.value
        self.args_input1.value = ""

        # Скрываем оба поля
        self.args_input1.visible = False
        self.args_recursive.visible = False
        self.output_text.value = ""
        self.output_text.update()

        # Настроим поля аргументов
        tool_args = {
            "Копировать файл": ("Введите путь назначения", True, False),
            "Удалить файл": (None, False, False),
            "Добавить дату в имя файла": (None, False, True),
            "Найти файлы": ("Введите шаблон (например, txt)", True, True),
            "Анализировать папку": (None, False, True),
            "Переместить книги": (None, False, False),
            "Подсчитать файлы": (None, False, True),
        }

        if tool in tool_args:
            hint, needs_arg1, needs_recursive_checkbox = tool_args[tool]
            if needs_arg1:
                self.args_input1.label = hint
                self.args_input1.visible = True
            if needs_recursive_checkbox:
                self.args_recursive.visible = True

        self.args_input1.update()
        self.args_recursive.update()

        self.run_button.visible = True
        self.run_button.update()

    def run_tool(self, e):
        tool = self.tool_select.value
        arg1 = self.args_input1.value
        arg_recursive = self.args_recursive.value

        if not self.selected_path:
            self.output_text.value = "Не выбран файл или папка"
            self.output_text.update()
            return

        try:
            if tool == "Копировать файл":
                result = copy_file(self.selected_path, arg1)
            elif tool == "Удалить файл":
                result = delete_file(self.selected_path)
            elif tool == "Подсчитать файлы":
                result = f"Количество файлов: {count_files(self.selected_path, recursive=arg_recursive)}"
            elif tool == "Найти файлы":
                result = f"Найдено файлов: {len(find_files(self.selected_path, arg1, recursive=arg_recursive))}"
            elif tool == "Добавить дату в имя файла":
                result = f"Переименовано файлов: {len(add_creation_date(self.selected_path, recursive=arg_recursive))}"
            elif tool == "Анализировать папку":
                result = analyse_folder(self.selected_path)
            elif tool == "Переместить книги":
                result = move_ebooks(self.selected_path)
            else:
                result = "Неизвестный инструмент"
        except Exception as ex:
            result = str(ex)

        self.output_text.value = result
        self.output_text.update()
        self.result_container.visible = True
        self.result_container.update()


def main(page: ft.Page):
    FileManagerGUI(page)


if __name__ == "__main__":
    ft.app(target=main)
