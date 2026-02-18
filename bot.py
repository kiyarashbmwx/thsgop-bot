import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv("8436681390:AAGqcUZ2I2ybqkTOx9hQ5y0nhoFJhN34l7c")
PROFIT_PERCENT = 5

bot = Bot(token=TOKEN)
dp = Dispatcher()

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💎 خرید USDT"), KeyboardButton(text="🟣 خرید TON")],
        [KeyboardButton(text="⚡ خرید TRX")]
    ],
    resize_keyboard=True
)

async def get_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        timeout = aiohttp.ClientTimeout(total=10)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    print("API Status Error:", resp.status)
                    return None

                data = await resp.json()

                if "price" not in data:
                    print("API Invalid Response:", data)
                    return None

                return float(data["price"])

    except Exception as e:
        print("API Exception:", e)
        return None

def add_profit(price):
    return price + (price * PROFIT_PERCENT / 100)

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("ربات فروش فعال شد ✅", reply_markup=keyboard)

@dp.message()
async def handle_buttons(message: types.Message):
    if "USDT" in message.text:
        price = await get_price("BTCUSDT")
        final_price = add_profit(price)
        await message.answer(f"💎 قیمت با سود:\n{final_price:.4f}")

async def main():
    await dp.start_polling(bot)

if name == "main":

    asyncio.run(main())
