from abc import ABC, abstractmethod

class BotAbs(ABC):

    @abstractmethod
    def start(self, service):
        pass

    @abstractmethod
    def send_message(self, chat_id, text):
        pass

    @abstractmethod
    def send_video(self, chat_id, file_name):
        pass
