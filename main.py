import requests
import schedule
import time
from Notifier import Notifier


telegram_bot = Notifier()
previous = None


def manager():
    print("Manager called")
    logic()
    schedule.every(15).seconds.do(logic)
    while True:
        schedule.run_pending()
        time.sleep(1)


def logic():
    global previous
    telegram_bot.sniff_messages()
    request_address = "https://player.rogersradio.ca/ckis/widget/now_playing"
    result = requests.get(request_address).json()
    info = [result['artist'], result['song_title']]

    if 'Justin Bieber' in info[0] and info[0] != previous:
        telegram_bot.send_message("Jb is playing! " + "Song: " + info[1])
        print('Sent message about jb')
    else:
        print('not the artist')
    print(info)
    print('------------')
    previous = info[0]


manager()
