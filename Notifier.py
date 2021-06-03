import telegram
import pickle
import os.path
import token


class Notifier:

    def __init__(self):
        self._bot = None
        self._chats = None
        self.startup()

    def startup(self):
        self._bot = telegram.Bot(token=token.get_token())
        self._chats = load_data('chatId.pickle') or set()
        self.sniff_messages()

    def sniff_messages(self):
        self.check_stop()
        self.check_start()
        self.save_chats()
        print(self._chats)

    def check_stop(self):
        try:
            updates = self._bot.get_updates()
        except:
            print("Failure to receive updates")
            return
        context = updates[-1]['message']['text'].lower()
        chat = updates[-1]['message']['chat']['id']
        if context == 'stop' and chat in self._chats:
            self._chats.remove(chat)
            self.send_individual_message(chat, 'Stopped')

    def check_start(self):
        updates = self._bot.get_updates()
        context = updates[-1]['message']['text'].lower()
        chat = updates[-1]['message']['chat']['id']
        if context == 'start' and chat not in self._chats:
            self._chats.add(chat)
            self.send_individual_message(chat, 'Started')

    def save_chats(self):
        try:
            save_data('chatId.pickle', self._chats)
        except:
            print("Failure to save")

    def send_individual_message(self, chat, message):
        self._bot.send_message(chat_id=chat, text=message)

    def send_message(self, message):
        for chat in self._chats:
            self._bot.send_message(chat_id=chat, text=message)
        self.sniff_messages()


def load_data(filename):
    if not os.path.isfile(filename):
        return None
    with open(filename, 'rb') as f:
        return pickle.load(f)


def save_data(filename, value):
    if not os.path.isfile(filename):
        with open(filename, 'wb+') as f:
            pickle.dump(value, f)
    else:
        with open(filename, 'wb') as f:
            pickle.dump(value, f)
