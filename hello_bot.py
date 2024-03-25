import asyncio
import telegram


async def main():
    bot = telegram.Bot("")
    async with bot:
        await bot.send_message(text='Hi Quy!', chat_id=535742672)
if __name__ == '__main__':
    asyncio.run(main())
