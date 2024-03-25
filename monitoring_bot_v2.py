import os
import psutil
import datetime
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, ContextTypes

# Telegram Bot Token
TOKEN = '6322785482:AAGSqlfNTlUus2g9ZTrPeicb13BRh5jFGuY'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Hello! I am your Raspberry Pi monitor bot. How can I assist you?')

async def status(update: Update, context: CallbackContext):
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    message = f"CPU Usage: {cpu_percent}%\nMemory Usage: {memory_percent}%\nDisk Usage: {disk_percent}%"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def network(update: Update, context: CallbackContext):
    if_addrs = psutil.net_if_addrs()
    message = ""
    for interface_name, addresses in if_addrs.items():
        for address in addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                message += f"Interface: {interface_name}\n"
                message += f"  IP Address: {address.address}\n"
                message += f"  Netmask: {address.netmask}\n"
                message += f"  Broadcast IP: {address.broadcast}\n"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def temperature(update: Update, context: CallbackContext):
    temp = os.popen("vcgencmd measure_temp").readline()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Temperature: {temp.replace('temp=', '')}")

async def uptime(update: Update, context: CallbackContext):
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Uptime: {str(uptime).split('.')[0]}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Define command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("network", network))
    dp.add_handler(CommandHandler("temperature", temperature))
    dp.add_handler(CommandHandler("uptime", uptime))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
