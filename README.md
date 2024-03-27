# Getting Started with Monitoring Bot
## Prerequisites
You'll need an API token to communicate with Telegram's servers. Follow the instructions [here](https://stackoverflow.com/posts/43317562/revisions)

##  Creating a Virtual Environment

    `python - m venv name_your_venv`
    
   This creates a virtual environment directory named `name_your_venv`.

##  Activating the Virtual Environment

    `source name_your_venv/bin/activate`

To confirm the virtual environment is activated, check the location of your Python interpreter:

    `which python`

Once activated, your terminal prompt will usually change to indicate the active virtual environment:
    `(name_your_venv)user@machine:)`
    `.name_your_venv/bin/python`

##  Install package using pip
While the virtual environment is active, install the required packages using pip:

    `python -m pip install requests python-telegram-bot`

## Run
Make sure you have replaced `token` in `monitoring_bot_v3.py` with your actual Telegram bot API token

    `python  monitoring_bot_v3.py`