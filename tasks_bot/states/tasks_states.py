from aiogram.fsm.state import State, StatesGroup


class TasksState(StatesGroup):
    default_state = State('default_state')
    add_task_text_state = State('add_task_text_state')
    add_task_date_state = State('add_task_date_state')
    delete_task_state = State('delete_task_state')
