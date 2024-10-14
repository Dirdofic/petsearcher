from aiogram import Bot, Dispatcher, executor, types
from config import *
API_TOKEN = BOT_API_TOKEN
from parser import kinpet_parser
from smart_search import SmartSearch
from db import *
import pickle
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

data_parser = None
searcher = None

async def on_startup(dp):
    global data_parser
    global searcher
    with open('data_parser.pickle', 'rb') as f:
        data_parser = pickle.load(f)

    # Load searcher from a pickle file
    with open('searcher.pickle', 'rb') as f:
        searcher = pickle.load(f)
    print('Started!')

@dp.message_handler(commands=['start'])
async def send_start(message: types.Message):
    await message.reply("Welcome to our bot! Type /help for more information.")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Here are the available commands:\n"
                        "/start - Start the bot\n"
                        "/help - Show this help message\n"
                        "/lost <args> - Report a lost pet and search for similar pets\n"
                        "/found <args> - Report a found pet\n"
                        "/found_pets - Show all found pets\n"
                        "/lost_pets - Show all lost pets")

@dp.message_handler(commands=['lost'])
async def report_lost(message: types.Message):
    args = message.get_args()
    if not args:
        await message.reply("Please provide some information about the lost pet, such as its name, breed, and location.")
    else:
        await message.reply(f"Thank you for reporting a lost pet we will search for it: {args}")
        write_lost_pet_to_csv(message.from_user.username, args)
        search_results = searcher.search_pet(args,'f').values
        if len(search_results) > 0:
            response = "Similar pets:\n"
            for i, pet in enumerate(search_results, 1):
                response = response +  f'{i}. {", ".join(map(str, pet[1:]))} \n'
            await message.reply(response)
        else:
            await message.reply("No similar lost pets found.")

@dp.message_handler(commands=['found'])
async def report_found(message: types.Message):
    args = message.get_args()
    if not args:
        await message.reply("Please provide some information about the found pet, such as its name, breed, and location.")
    else:
        write_found_pet_to_csv(message.from_user.username, args)
        await message.reply(f"Thank you for reporting a found pet: {args}")

@dp.message_handler(commands=['found_pets'])
async def show_found_pets(message: types.Message):
    df = read_found_pets_csv()
    found_pets = df.values.tolist()
    response = "Found pets:\n"
    for pet in found_pets:
        response += f"Telegram Username: {pet[0]}, Pet Info: {pet[1]}\n"
    await message.reply(response)

@dp.message_handler(commands=['lost_pets'])
async def show_lost_pets(message: types.Message):
    df = read_lost_pets_csv()
    lost_pets = df.values.tolist()
    response = "Lost pets:\n"
    for pet in lost_pets:
        response += f"Telegram Username: {pet[0]}, Pet Info: {pet[1]}\n"
    await message.reply(response)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)