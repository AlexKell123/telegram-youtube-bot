import os
import telebot
import re
import youtube_dl
# в библиотеке youtube_dl нужно закомментировать строчку 1794 в файле youtube_dl/extractor/youtube.py, иначе не работает

with open('token.txt', 'r', encoding='utf-8') as f:
    token = f.read()

bot = telebot.TeleBot(token)
bot.state = ''


def get_answer(message):
    if bot.state == 'download':
        return 'Подождите, скачивается предыдущий файл'
    if bot.state == 'wait_video_link':
        return download(message, '.mp4')
    if bot.state == 'wait_audio_link':
        return download(message, '.mp3')

    if message.text == '/video':
        bot.state = 'wait_video_link'
        return 'Для получения видео отправьте ссылку'
    if message.text == '/audio':
        bot.state = 'wait_audio_link'
        return 'Для получения аудио отправьте ссылку'
    else:
        return ('Список доступных команд:\n\
        /video - скачивает и присылает видео с YouTube\n\
        /audio - скачивает и присылает аудиодорожку из YouTube-видео\n\
        ')


def to_valid(url):
    youtube_regex = (r'(https?://)?(www\.)?' 
                     '(youtube|youtu|youtube-nocookie)\.(com|be)/'
                     '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match.group(6)
    else:
        raise Exception('NOT_VALID_URL')


def set_ydl_opts(video_id, ext):
    if ext == '.mp4':
        return {'max_filesize': 20000000000, 'format': 'best', 'outtmpl': video_id + ext, 'output': video_id + ext}
    elif ext == '.mp3':
        return {'format': 'bestaudio/best', 'outtmpl': video_id + ext, 'output': video_id + ext}


def download(message, ext):
    bot.state = 'download'
    try:
        video_id = to_valid(message.text)
        bot.send_message(message.chat.id, 'Начинаем загрузку: ' + video_id)
        ydl_opts = set_ydl_opts(video_id, ext)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_id])
        bot.send_message(message.chat.id, 'Скачано: ' + video_id)
        bot.send_video(message.chat.id, video=open(video_id + ext, 'rb'), supports_streaming=True)
        os.remove(video_id + ext)
        return 'Готово'

    except Exception as e:
        return f'Ошибка: `{e}`'

    finally:
        bot.state = ''


@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, get_answer(message))


bot.polling(none_stop=True, interval=0)
