from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

add_task_btn = InlineKeyboardButton(text='Добавить задачи', callback_data='add_task_btn_pressed')
delete_task_btn = InlineKeyboardButton(text='Удалить задачи', callback_data='delete_task_btn_pressed')
show_tasks_btn = InlineKeyboardButton(text='Показать мои задачи', callback_data='show_tasks_btn_pressed')

menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [add_task_btn], [delete_task_btn], [show_tasks_btn]
])
