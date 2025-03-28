class Service:
    def __init__(self, bot, downloader, validator, sessions, file_manager):
        self._bot = bot
        self._downloader = downloader
        self._validator = validator
        self._sessions = sessions
        self._file_manager = file_manager

        self._commands = {'/video': {'method': self._command_get_video,
                                      'hint': 'скачивает видео с YouTube',
                                      },
                           '/audio': {'method': self._command_get_audio,
                                      'hint': 'скачивает аудиодорожку из YouTube-видео',
                                      },
                           '/help': {'method': self._command_help,
                                     'hint': 'список команд с их описанием',
                                     }
                           }

    def start(self):
        self._bot.start(self)

    def on_start_message(self, chat_id):
        self._send_message(chat_id, 'Привет! Я могу скачать видео с YouTube, если он не замедлен.')
        self._command_help(chat_id)

    def on_message(self, chat_id, text):
        state = self._sessions.get_state_or_create_session(chat_id)

        if state == 'ready':
            self._run_command(chat_id, text)
        if state == 'downloading':
            self._send_message(chat_id, 'Подождите, скачивается предыдущий файл')
        if state == 'waiting_video_link':
            self._get_file(chat_id, text, '.mp4')
        if state == 'waiting_audio_link':
            self._get_file(chat_id, text, '.mp3')


    def _run_command(self, chat_id, text):
        command = self._commands.get(text)
        if command:
            command['method'](chat_id)
        else:
            self._unknown_command(chat_id, text)

    def _command_get_video(self, chat_id):
        self._sessions.set_state(chat_id, 'waiting_video_link')
        self._send_message(chat_id, 'Для получения видео отправьте ссылку')

    def _command_get_audio(self, chat_id):
        self._sessions.set_state(chat_id, 'waiting_audio_link')
        self._send_message(chat_id, 'Для получения аудиодорожки отправьте ссылку')

    def _command_help(self, chat_id):
        self._send_message(chat_id, f'Список доступных команд:\n' + self._get_commands_info())

    def _unknown_command(self, chat_id, text):
        self._send_message(chat_id, f' Неизвестная команда: {text}')
        self._command_help(chat_id)


    def _send_message(self, chat_id, msg):
        self._bot.send_message(chat_id, msg)

    def _send_video(self, chat_id, file_name):
        self._bot.send_video(chat_id, file_name)

    def _get_file(self, chat_id, url, ext):
        self._sessions.set_state(chat_id,'downloading')

        try:
            video_id = self._validator.url_to_valid(url)
            file_name = video_id + ext
            self._send_message(chat_id, 'Скачиваем: ' + file_name)
            self._downloader.download(video_id, ext)
            self._send_message(chat_id, 'Отправляем: ' + file_name)
            self._send_video(chat_id, file_name)
            self._send_message(chat_id, 'Готово.')
            self._file_manager.delete_file(file_name)

        except Exception as e:
            self._send_message(chat_id, f'Ошибка: `{e}`')

        finally:
            self._sessions.set_state(chat_id,'ready')

    def _get_commands_info(self):
        info = ''
        for command, value in self._commands.items():
            info += f'{command} - {value['hint']} \n'
        return info
