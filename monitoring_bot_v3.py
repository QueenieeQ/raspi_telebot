import os
import psutil
import datetime
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Hello! I am your Raspberry Pi monitor bot. How can I assist you?')

async def status(update: Update, context):
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    message = f"CPU Usage: {cpu_percent}%\nMemory Usage: {memory_percent}%\nDisk Usage: {disk_percent}%"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def network(update: Update, context):
    message = ""
    found_ipv4 = False  # Flag to track if IPv4 address found
    
    for interface_name, addresses in psutil.net_if_addrs().items():
        for address in addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                message += f"Interface: {interface_name}\n"
                message += f"  IP Address: {address.address}\n"
                message += f"  Netmask: {address.netmask}\n"
                message += f"  Broadcast IP: {address.broadcast}\n"
                found_ipv4 = True  # Set flag if IPv4 address found

    if found_ipv4:  # Check if flag is set before sending message
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No IPv4 addresses found")


async def temperature(update: Update, context):
    temp = os.popen("vcgencmd measure_temp").readline()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Temperature: {temp.replace('temp=', '')}")

async def uptime(update: Update, context):
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Uptime: {str(uptime).split('.')[0]}")

if __name__ == '__main__':
    application = ApplicationBuilder().token('6322785482:AAGSqlfNTlUus2g9ZTrPeicb13BRh5jFGuY').build()
    
    start_handler = CommandHandler('start', start)
    status_handler = CommandHandler('status', status)
    network_handler = CommandHandler('network', network)
    temperature_handler = CommandHandler('temperature', temperature)
    uptime_handler = CommandHandler('uptime', uptime)
    
    application.add_handler(start_handler)
    application.add_handler(status_handler)
    application.add_handler(network_handler)
    application.add_handler(temperature_handler)
    application.add_handler(uptime_handler)
    
    application.run_polling()

