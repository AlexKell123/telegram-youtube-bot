from src.bot.bot_telegram import Bot
from src.downloader.downloader_yt_dlp import Downloader
from src.file_manager.file_manager import FileManager
from src.service.service import Service
from src.sessions.sessions_impl import Sessions
from src.validator.validator import Validator
from src.config.load_config import load_config


config = load_config()

app = Service(Bot(config['bot_token']), Downloader(), Validator(), Sessions(), FileManager())
app.start()
