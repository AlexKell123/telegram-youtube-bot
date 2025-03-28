import os

from dotenv import load_dotenv


def load_config():
    load_dotenv()
    config = {'bot_token': os.getenv('BOT_TOKEN')}
    return config
