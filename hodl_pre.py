import os
from datetime import datetime
from coinex.coinex import CoinEx
from coinex.coinex import CoinExApiError
from dotenv import load_dotenv, find_dotenv
import telegram

# load environment variables
_ = load_dotenv(find_dotenv())  # read local .env file

coinex = CoinEx(os.getenv("access_id"), os.getenv("secret"))

LAST_EXECUTION_PATH = os.getenv("LAST_EXECUTION_PATH")

def get_last_execution_time():
    try:
        with open(LAST_EXECUTION_PATH, "r") as file:
            last_execution_str = file.read()
            if last_execution_str:
                return datetime.fromisoformat(last_execution_str)
    except FileNotFoundError:
        pass
    return datetime.min


def set_last_execution_time(timestamp):
    with open(LAST_EXECUTION_PATH, "w") as file:
        file.write(timestamp.isoformat())


def is_same_day(date1, date2):
    return date1.date() == date2.date()


async def send_telegram_message(message):
    bot = telegram.Bot(token=os.getenv("bot_token"))
    await bot.send_message(chat_id=os.getenv("chat_id"), text=message)


async def main():
    last_execution_time = get_last_execution_time()

    if not is_same_day(datetime.now(), last_execution_time):
        try:
            message = "Order executed!"
            message += f"\nOrder Result:\n{coinex.order_market('PREUSDT', 'buy', 5.0)}"
            message += f"\nBalance Info:\n{coinex.balance_info()}"

            await send_telegram_message(message)

            set_last_execution_time(datetime.now())

        except CoinExApiError as error:
            await send_telegram_message(str(error))
        except Exception as e:  # handle other unexpected errors
            await send_telegram_message(f"Unexpected error: {e}")
    else:
        balance_info = coinex.balance_info()
        await send_telegram_message(f"Order already executed today... your current balance is below: {balance_info}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
