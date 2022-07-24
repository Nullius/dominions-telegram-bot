import os
import sys
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dotenv import load_dotenv
import commands
import helpers

load_dotenv()
bot_token = os.getenv("TELEGRAM_TOKEN")
if not bot_token:
    sys.exit("Error: no token")

bot = Bot(token=bot_token)
storage = MemoryStorage() 
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands="start")
async def botstart(message: types.Message):
    # TODO основные кнопки? (список игр)
    pass

'''
Выводит список игр с кнопкой "статус"
'''
@dp.message_handler(commands="list")
async def gamelist(message: types.Message):
    games = commands.gamelist()
    buttons = [] 
    for game in games:
        buttons.append([game, game]) # [button_text, button_callback_data]

    row_btns = (types.InlineKeyboardButton(text, callback_data='game_{}'.format(data)) for text, data in buttons)

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.row(*row_btns)
    await message.answer("game list:", reply_markup=keyboard)

@dp.callback_query_handler(Text(startswith="game_"))
async def gameinfo(call: types.CallbackQuery):
    print(call.message)
    game_name = call.data.split('_')[1]
    buttons = [
        ['Undone', 'gameundone_{}'.format(game_name)],
        ['Ritual of sootqee', 'gamesettimer_{}'.format(game_name)],
        ['Subscribe', 'gamesubscribe_{}'.format(game_name)],
        ['Settings', 'gamesettings_{}'.format(game_name)],
    ]

    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in buttons)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(*row_btns)

    gamestatus = commands.status(game_name)
    status = gamestatus['status']
    undone = gamestatus['undone']
    timer = gamestatus['timer']
    
    message = ['Game info:', status]
    if len(undone) > 0:
        message.append(undone[0])
    if len(timer) > 0:
        message.append(timer)

    await call.message.answer('\n'.join(message), reply_markup=keyboard)
    await call.answer()

@dp.callback_query_handler(Text(startswith="gameundone_"))
async def gamestatus(call: types.CallbackQuery):
    print(call.message)
    game_name = call.data.split('_')[1]
    status = commands.status(game_name)
    if status['undone']:
        await call.message.answer('\n'.join(status['undone']))
    await call.answer()

@dp.callback_query_handler(Text(startswith="gamesubscribe_"))
async def gamesubscribe(call: types.CallbackQuery):
    await call.message.answer('Command not implemented yet')
    await call.answer()

@dp.callback_query_handler(Text(startswith="gamesettings_"))
async def gamesettings(call: types.CallbackQuery):
    await call.message.answer('Command not implemented yet')
    await call.answer()

# @dp.callback_query_handler(Text(startswith='gamesettimer_'))
async def sootqee(call: types.CallbackQuery):
    game_name = call.data.split('_')[1]
    timer = 24
    commands.settimer(game_name, int(timer))
    await call.answer(("Таймер установлен на {} часов".format(timer)))
    await call.answer()

'''
Game state
TODO move to separate file
'''
class GameState(StatesGroup):
    name = State()
    port = State()
    era = State()
    masterpass = State()

'''
Создать игру
'''
# @dp.message_handler(commands="newgame")
async def newgame(message: types.Message):
    await GameState.name.set()
    await message.answer("Enter game name:")

@dp.message_handler(state=GameState.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await GameState.next()
    await message.answer("Enter game port:")

@dp.message_handler(state=GameState.port)
async def process_port(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['port'] = message.text

    await GameState.next()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('1', '2', '3')
    await message.answer("Enter era (1-3):", reply_markup=keyboard)

# async def valid_era(message: types.Message):
#     return await message.text.strip() in ['1','2','3']

# @dp.message_handler(not valid_era, state=GameState.era)
# async def process_era_invalid(message: types.Message):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add('1', '2', '3')
#     await message.answer("Enter era (1-3):", reply_markup=keyboard)

@dp.message_handler(state=GameState.era)
async def process_era(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['era'] = message.text.strip()

    await GameState.next()
    await message.answer("Enter master password:", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=GameState.masterpass)
async def process_masterpass(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['masterpass'] = message.text

        game = data['name']
        game.port = data['port']
        game.era = data['era']
        game.masterpass = data['masterpass']
        game.save()
    
    await state.finish()

'''
Choose map
'''
async def process_map(message: types.Message):
    # buttons: set[str] = helpers.mapslist()
    buttons = ['Random']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    await message.answer("Choose map: {}".format(', '.join(buttons)), reply_markup=keyboard)

'''
Status command
TODO убрать копипасту с gameinfo
'''
@dp.message_handler(commands="status")
async def status_command(message: types.Message):
    game_name = message.text.split(' ')[1]
    gamestatus = commands.status(game_name)
    status = gamestatus['status']
    undone = gamestatus['undone']
    timer = gamestatus['timer']
    
    text = ['Game info:', status]
    if len(undone) > 0:
        text.append(undone[0])
    if len(timer) > 0:
        text.append(timer)

    await message.answer('\n'.join(text))

@dp.message_handler(commands="undone")
async def undone_command(message: types.Message):
    game_name = message.text.split(' ')[1]
    gamestatus = commands.status(game_name)
    undone = gamestatus['undone']
    if len(undone) > 0:
        await message.answer('\n'.join(undone))

'''
TODO удалить
'''
@dp.message_handler(commands="time")
async def time_command(message: types.Message):
    game_name = 'UnboundedJotun'
    gamestatus = commands.status(game_name)
    status = gamestatus['status']
    undone = gamestatus['undone']
    timer = gamestatus['timer']
    
    text = ['Game info:', status]
    if len(undone) > 0:
        text.append(undone[0])
    if len(timer) > 0:
        text.append(timer)

    await message.answer('\n'.join(text))

# @dp.message_handler(commands="settimer")
async def settimer_command(message: types.Message):
    game_name = message.text.split(' ')[1]
    timer = message.text.split(' ')[2]
    commands.settimer(game_name, int(timer))
    await message.answer(("Таймер установлен на {} часов".format(timer)))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
