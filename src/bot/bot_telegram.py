import telebot


from src.bot.bot_abs import BotAbs


class Bot(BotAbs):
    def __init__(self, bot_token):
        self._bot = telebot.TeleBot(bot_token)

    def start(self, service):
        self._set_handlers(service)
        self._bot.polling(none_stop=True, interval=0)

    def _set_handlers(self, service):
        @self._bot.message_handler(commands=["start"], chat_types=["private"])
        def handle_start(message):
            service.on_start_message(message.chat.id)

        @self._bot.message_handler(content_types=["text"])
        def handle_text(message):
            service.on_message(message.chat.id, message.text)

    def send_message(self, chat_id, text):
        self._bot.send_chat_action(chat_id, "typing")
        self._bot.send_message(chat_id, text)

    def send_video(self, chat_id, file_name):
        self._bot.send_video(chat_id, video=open(file_name, 'rb'), supports_streaming=True, timeout=600)
