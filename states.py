from aiogram.dispatcher.filters.state import State, StatesGroup

class main_menu(StatesGroup):
    welcome = State()

class choice_sneakers(StatesGroup):
   main_stage = State()
   show_all = State()
   show_find = State()