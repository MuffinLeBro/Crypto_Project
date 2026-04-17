class CLIHistory:
    def __init__(self):
        self._messages = []  # (direction, msg_type, text)

    def append(self, direction, msg_type, text):
        self._messages.append((direction, msg_type, text))

    def get_last(self, n):
        return self._messages[-n:]

    def get(self, idx):
        if idx < 0 or idx >= len(self._messages):
            return None
        return self._messages[idx]

    def __len__(self):
        return len(self._messages)