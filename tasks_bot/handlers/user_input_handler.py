import requests, json
from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message, CallbackQuery
from keyboards.menu_keyboard import menu_kb
from states.tasks_states import TasksState


TASKS_URL = "http://localhost:8000/tasks"

router = Router()


@router.message(CommandStart())
async def start_bot(m: Message, state: FSMContext):
    await state.set_state(TasksState.default_state)
    await m.answer('Привет я бот задач. Выбери действие', reply_markup=menu_kb)


@router.callback_query(lambda cb: cb.data == 'add_task_btn_pressed')
async def add_task_btn_pressed(cb: CallbackQuery, state: FSMContext):
    await cb.message.answer('Введите текст задачи')
    await state.set_state(TasksState.add_task_text_state)


@router.message(StateFilter('TasksState:add_task_text_state'))
async def add_task_txt(message: Message, state: FSMContext):
    task = await state.get_value('task', {})
    task['text'] = message.text
    await state.update_data(task=task)
    await state.set_state(TasksState.add_task_date_state)
    await message.answer(f'Введите дедлайн (ДД.ММ.ГГГГ).')


@router.message(StateFilter('TasksState:add_task_date_state'))
async def add_task_date(message: Message, state: FSMContext):
    task = await state.get_value('task', {})
    task['date'] = message.text
    response = requests.post(TASKS_URL, json=task)
    if response.status_code != 200:
        raise Exception(response.status_code)
    await message.answer(f'Задача {task} добавлена')
    await start_bot(message, state)


@router.callback_query(lambda cb: cb.data == 'delete_task_btn_pressed')
async def delete_task_btn_pressed(cb: CallbackQuery, state: FSMContext):
    await state.set_state(TasksState.delete_task_state)
    tasks = requests.get(TASKS_URL).json()
    keys = [[InlineKeyboardButton(text=get_task_repr(task), callback_data=json.dumps(task))] for task in tasks]
    tasks_kb = InlineKeyboardMarkup(
        inline_keyboard=keys
    )

    await cb.message.answer(text='Выберите заметку для удаления', reply_markup=tasks_kb)


@router.callback_query(StateFilter('TasksState:delete_task_state'))
async def delete_task(cb: CallbackQuery, state: FSMContext):
    response = requests.delete(TASKS_URL, json=json.loads(cb.data))
    if response.status_code != 200:
        raise Exception(response)

    await cb.message.answer(f'Задача {cb.data} удалена')
    await start_bot(cb.message, state)


@router.callback_query(lambda cb: cb.data == 'show_tasks_btn_pressed')
async def show_tasks(cb: CallbackQuery):
    tasks = requests.get(TASKS_URL).json()
    keys = [[InlineKeyboardButton(text=get_task_repr(task), callback_data=str(task['id']))] for task in tasks]
    tasks_kb = InlineKeyboardMarkup(
        inline_keyboard=keys
    )
    await cb.message.answer(text='Ваши задачи', reply_markup=tasks_kb)


def get_task_repr(task: dict):
    return task['text'] + '. Дедлайн: ' + task['date']
