import flet as ft
from db import main_db

def main(page: ft.Page):
    page.title = 'Todo List'
    page.padding = 40
    page.window.maximizable = True

    task_list = ft.Column(spacing=10)

    def load_tasks():
        task_list.controls.clear()
        for task_id, task_text, create_time in main_db.get_tasks():
            task_list.controls.append(create_task_row(task_id, task_text, create_time))
        page.update()

    def create_task_row(task_id, task_text, create_time):
        task_field = ft.TextField(value=f"{task_text} ({create_time})", expand=True, dense=True, read_only=True)

        def enable_edit(e):
            task_field.read_only = False
            page.update()

        def save_edit(e):
            main_db.update_task_db(task_id, task_field.value)
            task_field.read_only = True
            load_tasks()

        return ft.Row([
            task_field,
            ft.IconButton(ft.icons.EDIT, icon_color=ft.colors.YELLOW_400, on_click=enable_edit),
            ft.IconButton(ft.icons.SAVE, icon_color=ft.colors.GREEN_400, on_click=save_edit),
            ft.IconButton(ft.icons.DELETE, icon_color=ft.colors.RED_400, on_click=lambda e: delete_task(task_id))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    warning_text = ft.Text('', color=ft.colors.RED_400)

    def on_input_change(e):
        if len(task_input.value) > 100:
            warning_text.value = "Нельзя ввести больше 100 символов!"
            task_input.value = task_input.value[:100]
        else:
            warning_text.value = ""
        page.update()

    def add_task(e):
        if task_input.value.strip():
            task_id, create_time = main_db.add_task_db(task_input.value)
            task_list.controls.append(create_task_row(task_id, task_input.value, create_time))
            task_input.value = ""
            warning_text.value = ""
            page.update()

    def delete_task(task_id):
        main_db.delete_task_db(task_id)
        load_tasks()

    task_input = ft.TextField(
        hint_text='Добавьте задачу',
        expand=True,
        dense=True,
        on_change=on_input_change,
        on_submit=add_task
    )
    add_button = ft.ElevatedButton("Добавить", on_click=add_task, icon=ft.icons.ADD)

    content = ft.Container(
        content=ft.Column([
            ft.Row([task_input, add_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            warning_text,
            task_list
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=20,
        alignment=ft.alignment.center
    )

    background_image = ft.Image(
        src='/home/diorbek90/my_flet_project/background.jpeg',
        fit=ft.ImageFit.FILL,
        width=page.width,
        height=page.height
    )

    background = ft.Stack([background_image, content])

    def on_resize(e):
        background_image.width = page.width
        background_image.height = page.height
        page.update()

    page.add(background)
    page.on_resized = on_resize

    load_tasks()

if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)
