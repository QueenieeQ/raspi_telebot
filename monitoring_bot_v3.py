import os
import re
import psutil
import subprocess
import datetime
import logging
import socket
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler


#Replace TOKEN get from botfather
TOKEN = ''
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Hello! I am your Raspberry Pi monitor bot of Ninh Xuan Quy. How can I assist you?')

async def status(update: Update, context):
    cpu_percent = psutil.cpu_percent()
    memory_used = round((psutil.virtual_memory().used)/ (1024 ** 2), 2)
    swap_used = round(psutil.swap_memory().used/ (1024 ** 2), 2)
    # memory_usage_mb = round(memory_percent )
    disk_percent = psutil.disk_usage('/').percent
    disk_io_read = round((psutil.disk_io_counters(perdisk=False).read_bytes)/ (1024 ** 2), 2)
    disk_io_write = round((psutil.disk_io_counters(perdisk=False).write_bytes)/ (1024 ** 2), 2)
    message = f"CPU Usage: {cpu_percent}%\nMemory Usage: {memory_used} MB\nSwap Usage: {swap_used} MB\nDisk Usage: {disk_percent}%\nDisk Read: {disk_io_read}MB\nDisk Write: {disk_io_write}MB"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def network(update: Update, context):
    message = ""
    net_io_counters = psutil.net_io_counters(pernic=True)
    found_ipv4 = False  # Flag to track if IPv4 address found
    
    for interface_name, addresses in psutil.net_if_addrs().items():
        for address in addresses:
            if address.family == socket.AF_INET:
                message += f"Interface: {interface_name}\n"
                message += f"  IP Address: {address.address}\n"
                message += f"  Netmask: {address.netmask}\n"
                message += f"  Broadcast IP: {address.broadcast}\n"

                # Get network I/O statistics for the interface
                interface_stats = net_io_counters.get(interface_name)
                message += f"  Bytes Sent: {round(interface_stats.bytes_sent/ (1024 ** 2), 2)} MB\n"
                message += f"  Bytes Received: {round(interface_stats.bytes_recv/ (1024 ** 2), 2)} MB\n"
                message += f"  Packets Sent: {round(interface_stats.packets_sent/ (1024 ** 2), 2)} MB\n"
                message += f"  Packets Received: {round(interface_stats.packets_recv/ (1024 ** 2), 2)} MB\n"

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

async def docker_info(update: Update, context):
    try:
        completed_process = subprocess.run(["docker", "ps"], capture_output=True, text=True)
        
        # Check if the command was successful
        if completed_process.returncode == 0:
            output = completed_process.stdout
            # Extract name and uptime from output
            container_info = []
            lines = output.strip().split('\n')[1:]  # Skip the header
            for line in lines:
                parts = line.split()
                container_name = parts[-1]  # Last part contains the container name
                uptime = parts[-3]  # Second-to-last part contains the uptime
                container_info.append((container_name, uptime))

            # Send the information through Telegram bot
            if container_info:
                message = "Docker Container Information:\n"
                for name, uptime in container_info:
                    message += f"{name} uptime: {uptime} days ago\n"
                await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="No Docker containers found.")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to run 'docker ps' command")
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error: {e}")


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    status_handler = CommandHandler('status', status)
    network_handler = CommandHandler('network', network)
    temperature_handler = CommandHandler('temperature', temperature)
    uptime_handler = CommandHandler('uptime', uptime)
    docker_handler = CommandHandler('docker',docker_info)

    application.add_handler(start_handler)
    application.add_handler(status_handler)
    application.add_handler(network_handler)
    application.add_handler(temperature_handler)
    application.add_handler(uptime_handler)
    application.add_handler(docker_handler)
    
    application.run_polling()

