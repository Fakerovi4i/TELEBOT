from telebot.handler_backends import State, StatesGroup



class ChoiceFilters(StatesGroup):
   waiting_filters = State()
   waiting_year = State()

