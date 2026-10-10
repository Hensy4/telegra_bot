import asyncio
import os
from dotenv import load_dotenv # Берёт инструмент для чтения .env
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

load_dotenv() # Открывает .env и загружает все переменные в память
TOKEN = os.getenv("BOT_TOKEN")  # Достаёт значение BOT_TOKEN из памяти

bot = Bot(token=TOKEN) # это как ссылка куда общаться 
dp = Dispatcher() # берем данные с класса деспачер

@dp.message(Command("start"))
async def start(message):
    await message.answer("Привет")

@dp.message(Command("help"))
async def help(message):
    await message.answer("я могу то то то ")

    
async def main():
    print("🤖 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



