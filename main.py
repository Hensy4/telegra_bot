import asyncio
import aiohttp
import os
from dotenv import load_dotenv # Берёт инструмент для чтения .env
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv() # Открывает .env и загружает все переменные в память
TOKEN = os.getenv("BOT_TOKEN")  # Достаёт значение BOT_TOKEN из памяти
API_KEY = os.getenv("NEWS_API_KEY")
WEATHER_API = os.getenv("WEATHER_API_KEY")

bot = Bot(token=TOKEN) # это как ссылка куда общаться 
dp = Dispatcher() # берем данные с класса деспачер






@dp.callback_query()
async def callback(call_back):
    if call_back.data == "help":
        await call_back.message.answer("Введите /help для получения новостей.")
    elif call_back.data == "crypto":
        await call_back.message.answer("Введите /crypto для получнния крипты")
    elif call_back.data == "weather":
        await call_back.message.answer("Введите /weather + город для получения погоды")
    elif call_back.data == "news":
        await call_back.message.answer("Введите /news для получения новостей")
    
    await call_back.answer()
    
@dp.message(Command("menu"))
async def menu(message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Помощь", callback_data="help")],
    [InlineKeyboardButton(text="Крипта", callback_data="crypto")],
    [InlineKeyboardButton(text="Погода", callback_data="weather")],
    [InlineKeyboardButton(text="Новости", callback_data="news")]])
    
    await message.answer("Выберите действие", reply_markup=keyboard)

    
@dp.message(Command("start"))
async def start(message):
    await message.answer(f"🤖 Я бот-помощник\n"
                        "____________________________________________________\n\n"
                        f"👋 Привет, {message.from_user.first_name}\n"
                        f"📋 Введит /help, чтобы узнать что я умею\n\n"
                        "____________________________________________________\n\n"
                        )
    
@dp.message(Command("help"))
async def help(message):
    await message.answer(
        "🤖 <b>Что умеет бот</b>\n"
        "____________________________________________________\n\n"
        "🌤️ <b>/weather</b> + город (Покажет погоду)\n"  
        "      Пример: <code>/weather Уфа</code>\n\n"
        "📰 <b>/news</b> (Свежие новости)\n"
        "      Пример: <code>/news</code>\n\n"
        "🪙 <b>/crypto</b> (Курс крипты)\n"
        "      Пример: <code>/crypto</code>\n\n"
        "____________________________________________________\n",
        parse_mode="HTML")
    


    
@dp.message(Command("crypto"))
async def crypto(message):
    async with aiohttp.ClientSession() as call_web:
        try:
            async with call_web.get(f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,cardano,dogecoin&vs_currencies=usd&include_24hr_change=true") as open_web:
                data = await open_web.json()
                
                all_coin  = []
                image = {"bitcoin" : "🟠",
                        "ethereum" : "🔷",
                        "solana" : "🟣",
                        "cardano" : "🔵",
                        "dogecoin" : "🐕"
                        }
                for coin in data:
                
                    price = data[coin]['usd']
                    change  = data[coin]['usd_24h_change']
                    inon  =  "📈" if change > 0 else "📉"
                    ex  = f"{image[coin]} {coin[0].upper()}{coin[1:]} ${price:,.2f} ({inon} {change:+.2f}%)"
                    all_coin.append(ex)
                
                result = "\n\n".join(all_coin)
                await message.answer(f"Курс крипты\n{'_'*30}\n\n{result}\n\n{'_'*30}")
        except asyncio.TimeoutError:
            await message.answer("Ошибка: времени")
        except aiohttp.ClientError:
            await message.answer("Ошибка: вызва")
        except Exception as ex:
            await message.answer(f"Ошибка: {ex}")

    
@dp.message(Command("weather"))
async def weather(message: types.Message, command: CommandObject):
    
    city = command.args
    if not city:
        await message.answer("Бро введи город \n(пример /weather Уфа)")
        return
    try:
        async with aiohttp.ClientSession() as call_web:
            async with call_web.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric&lang=ru") as open_web:
                if open_web.status == 200:
                    data = await open_web.json()
                    await message.answer(f"🌍 Погода в городе {data['name']}\n{'_'*50}\n\n☁️ Описание: {data['weather'][0]['description']}, \n🌡️ Температура: {data['main']['temp']:.1f} °C, \n💧 Влажность: {data['main']['humidity']}%\n\n{'_'*50}")
                else:
                    await message.answer(f"❌ Город '{city}' не найден")
    except asyncio.TimeoutError:
        await message.answer("Ошибка: времени")
    except aiohttp.ClientError:
        await message.answer("Ошибка: вызва")
    except Exception as ex:
        await message.answer(f"Ошибка: {ex}")

        
        
        
@dp.message(Command("news"))
async def news(message):
    async with aiohttp.ClientSession() as call_web:
        try:
            async with call_web.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}") as open_web:
                data = await open_web.json()
            
            for words in [f"{data['articles'][0]['title']} \n\n{data['articles'][0]['url']}",
                          f"{data['articles'][1]['title']} \n\n{data['articles'][1]['url']}",
                          f"{data['articles'][2]['title']} \n\n{data['articles'][2]['url']}",
                          f"{data['articles'][3]['title']} \n\n{data['articles'][3]['url']}",
                          f"{data['articles'][4]['title']} \n\n{data['articles'][4]['url']}"
                          ]:
                async with call_web.get(f"https://api.mymemory.translated.net/get?q={words}&langpair=en|ru") as open_web_tran:
                    data = await open_web_tran.json()
                    await message.answer(data['responseData']['translatedText'])
                
                
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


