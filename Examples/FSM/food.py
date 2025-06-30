from enum import Enum, auto

from FloriaTelegramBotAPI.Types import DefaultTypes
from FloriaTelegramBotAPI.Types.EasyTypes import *
from FloriaTelegramBotAPI.Types.EasyTypes.Keyboards.Keyboard import *
from FloriaTelegramBotAPI.FSM import *

from FloriaTelegramBotAPI.Filters import *
from FloriaTelegramBotAPI.Enums import *


def MakeKeyboard(items: list[str]) -> DefaultTypes.ReplyKeyboardMarkup:
    return Keyboard(
        *[
            Button(text)
            for text in items
        ],
        resize=True
    ).As_Markup()

available_food_names = ["Суши", "Спагетти", "Хачапури"]
available_food_sizes = ["Маленькую", "Среднюю", "Большую"]

class OrderFood(Enum):
    choosing_food_name = auto()
    choosing_food_size = auto()


fsm = FSM(Chat(ChatType.PRIVATE))

@fsm.Message(Command('start'))
async def _(message: Message, state: FSMContext):
    state.Clear()
    await message.Answer(
        text="Выберите, что хотите заказать: "
             "блюда (/food) или напитки (/drinks).",
        reply_markup=RemoveKeyboard()
    )

@fsm.Message(State(None), Or(Command("cancel"), InSequence('отмена')))
async def _(message: Message, state: FSMContext):
    state.ClearData()
    await message.Answer(
        text="Нечего отменять",
        reply_markup=RemoveKeyboard()
    )

@fsm.Message(Not(State(None)), Or(Command("cancel"), InSequence('отмена')))
async def _(message: Message, state: FSMContext):
    state.Clear()
    await message.Answer(
        text="Действие отменено",
        reply_markup=RemoveKeyboard()
    )


@fsm.Message(Command('state'))
async def _(message: Message, context: FSMContext):
    await message.Answer(f'{context.state=}')

@fsm.Message(Command('data'))
async def _(message: Message, context: FSMContext):
    await message.Answer(f'{context.data=}')


@fsm.Message(State(None), Command('food'))
async def _(message: Message, state: FSMContext):
    await message.Answer(
        text="Выберите блюдо:",
        reply_markup=MakeKeyboard(available_food_names)
    )
    state.SetState(OrderFood.choosing_food_name)


@fsm.Message(State(OrderFood.choosing_food_name), InSequence(*available_food_names))
async def _(message: Message, state: FSMContext):
    state.SetData(chosen_food=message.text.lower())
    await message.Answer(
        text="Спасибо. Теперь, пожалуйста, выберите размер порции:",
        reply_markup=MakeKeyboard(available_food_sizes)
    )
    state.SetState(OrderFood.choosing_food_size)

@fsm.Message(State(OrderFood.choosing_food_name))
async def _(message: Message):
    await message.Answer(
        text="Я не знаю такого блюда.\n\n"
             "Пожалуйста, выберите одно из названий из списка ниже:",
        reply_markup=MakeKeyboard(available_food_names)
    )


@fsm.Message(State(OrderFood.choosing_food_size), InSequence(*available_food_sizes))
async def _(message: Message, state: FSMContext):
    user_data = state.GetData()
    state.Clear()
    await message.Answer(
        text=f"Вы выбрали {message.text.lower()} порцию {user_data['chosen_food']}.\n"
             f"Попробуйте теперь заказать напитки: /drinks",
        reply_markup=RemoveKeyboard()
    )

@fsm.Message(State(OrderFood.choosing_food_size))
async def _(message: Message):
    await message.Answer(
        text="Я не знаю такого размера порции.\n\n"
             "Пожалуйста, выберите один из вариантов из списка ниже:",
        reply_markup=MakeKeyboard(available_food_sizes)
    )
