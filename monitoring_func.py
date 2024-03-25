import os
import psutil
import datetime
from telegram.ext import Updater, CommandHandler

# Telegram Bot Token
TOKEN = ''

# Function to handle the /start command
def start(update, context):
    update.message.reply_text('Hello! I am your Raspberry Pi monitor bot. How can I assist you?')

# Function to send system status
def status(update, context):
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    message = f"CPU Usage: {cpu_percent}%\nMemory Usage: {memory_percent}%\nDisk Usage: {disk_percent}%"
    update.message.reply_text(message)

# Function to send network status
def network(update, context):
    if_addrs = psutil.net_if_addrs()
    message = ""
    for interface_name, addresses in if_addrs.items():
        for address in addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                message += f"Interface: {interface_name}\n"
                message += f"  IP Address: {address.address}\n"
                message += f"  Netmask: {address.netmask}\n"
                message += f"  Broadcast IP: {address.broadcast}\n"
    update.message.reply_text(message)

# Function to send temperature status
def temperature(update, context):
    temp = os.popen("vcgencmd measure_temp").readline()
    update.message.reply_text(f"Temperature: {temp.replace('temp=', '')}")

# Function to send uptime status
def uptime(update, context):
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    update.message.reply_text(f"Uptime: {str(uptime).split('.')[0]}")

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
