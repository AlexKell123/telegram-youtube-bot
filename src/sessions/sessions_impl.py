from src.sessions.sessions_abs import SessionsAbs


class Sessions(SessionsAbs):
    def __init__(self):
        self._sessions = {}

    def get_state_or_create_session(self, chat_id):
        return self._sessions.setdefault(chat_id, 'ready')

    def set_state(self, chat_id, state):
        self._sessions[chat_id] = state
