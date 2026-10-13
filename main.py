import asyncio
import aiohttp
import os
from dotenv import load_dotenv # Берёт инструмент для чтения .env
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

load_dotenv() # Открывает .env и загружает все переменные в память
TOKEN = os.getenv("BOT_TOKEN")  # Достаёт значение BOT_TOKEN из памяти
API_KEY = os.getenv("NEWS_API_KEY")

bot = Bot(token=TOKEN) # это как ссылка куда общаться 
dp = Dispatcher() # берем данные с класса деспачер

@dp.message(Command("start"))
async def start(message):
    await message.answer("Привет")

@dp.message(Command("help"))
async def help(message):
    await message.answer("я могу то то то ")

@dp.message(Command("news"))
async def news(message):
    async with aiohttp.ClientSession() as call_web:
        try:
            async with call_web.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}") as open_web:
                data = await open_web.json()
                st = f"📰 {data['articles'][0]['title']}.\n\n📰 {data['articles'][1]['title']}.\n\n📰 {data['articles'][2]['title']}.\n\n📰 {data['articles'][3]['title']}.\n\n📰 {data['articles'][4]['title']}"
                await message.answer(st)
        except aiohttp.ClientError:
            await message.answer("Ошибка соединения. Попробуйте позже")
        except asyncio.TimeoutError:
            await message.answer("Превышено время ожидания")
        except KeyError:
            await message.answer("Нет новостей")
        except IndexError:
            await message.answer("Недостаточно новостей (меньше 5)")
        except Exception as ex:
            print(f"Ошибка: {ex}")
            await message.answer(f"Что-то пошло не так.")
            
async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())


