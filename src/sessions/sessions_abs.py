from abc import ABC, abstractmethod


class SessionsAbs(ABC):

    @abstractmethod
    def get_state_or_create_session(self, chat_id):
        pass

    @abstractmethod
    def set_state(self, chat_id, state):
        pass
