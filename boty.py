from aiogram import Bot, Dispatcher, executor, types
from config import *
API_TOKEN = BOT_API_TOKEN
from db import *
import asyncio


data_parser = None
searcher = None


import pickle

# Load data_parser from a pickle file
with open('data_parser.pickle', 'rb') as f:
    data_parser = pickle.load(f)

# Load searcher from a pickle file
with open('searcher.pickle', 'rb') as f:
    searcher = pickle.load(f)
print('Started!')

class botyki():
    def __init__(self):
        self.botyk = Bot(token=API_TOKEN)

    async def show_lost_pets(self, message):
        df = read_lost_pets_csv()
        lost_pets = df.values.tolist()
        response = "Lost pets:\n"
        for pet in lost_pets:
            response += f"Telegram Username: {pet[0]}, Pet Info: {pet[1]}\n"
        await self.botyk.send_message(ADMIN_ID, response)
    async def show_found_pets(self, message):
        df = read_found_pets_csv()
        found_pets = df.values.tolist()
        response = "Found pets:\n"
        for pet in found_pets:
            response += f"Telegram Username: {pet[0]}, Pet Info: {pet[1]}\n"
        await self.botyk.send_message(ADMIN_ID, response)
    async def report_found(self,message):
        args = message
        if not args:
            await self.botyk.send_message(ADMIN_ID,"Please provide some information about the found pet, such as its name, breed, and location.")
        else:
            write_found_pet_to_csv("Telthy", args)
            await   self.botyk.send_message(ADMIN_ID,f"Thank you for reporting a found pet: {args}")
    async def report_lost(self, message):
        args = message
        if not args:
            await   self.botyk.send_message(ADMIN_ID,"Please provide some information about the lost pet, such as its name, breed, and location.")
        else:
            await self.botyk.send_message(ADMIN_ID,f"Thank you for reporting a lost pet we will search for it: {args}")
            write_lost_pet_to_csv('Telthy', args)
            search_results = searcher.search_pet(args,'f').values
            if len(search_results) > 0:
                response = "Similar pets:\n"
                for i, pet in enumerate(search_results, 1):
                    response = response +  f'{i}. {", ".join(map(str, pet[1:]))} \n'
                await self.botyk.send_message(ADMIN_ID,response)
            else:
                await self.botyk.send_message(ADMIN_ID,"No similar lost pets found.")
