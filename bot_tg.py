import os
import socket

import telebot

from db_data import get_db_data, update_publish_yn, insert_log
from db_data import get_tags
from yd_data import get_images
from insta import get_photo

# Static
TOKEN = str(os.environ.get('BOT_TOKEN'))
PROFILE = str(os.environ.get('PROFILE'))
CHAT_ID = str(os.environ.get('CHAT_ID'))
CHANNEL_ID = str(os.environ.get('CHANNEL_ID'))

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['check'])
def check(message):
    desc_car(1, CHAT_ID)


@bot.message_handler(commands=['start'])
def start(message):
    if str(message.chat.id) != CHAT_ID:
        bot.send_message(message.chat.id, 'Sorry, but :')
        img = open('out.jpg', 'rb')
        bot.send_photo(message.chat.id, img, caption=None)
        img.close()
        bot.send_message(CHAT_ID, 'Strange request from : ' + str(message.chat.id))
        insert_log(os.environ.get('DB'), os.environ.get('DB_USER'), os.environ.get('DB_PASS'),
                   os.environ.get('DB_HOST'),
                   os.environ.get('DB_PORT'), CHAT_ID, message.chat.id)
    else:
        bot.send_message(CHAT_ID, 'Hi, boss')


@bot.message_handler(commands=['status'])
def state(message):
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    bot.send_message(CHAT_ID, 'IP : ' + local_ip
                     + '\nBOT_TOKEN: ' + str(os.environ.get('BOT_TOKEN'))
                     + '\nCHAT_ID : ' + str(os.environ.get('CHAT_ID'))
                     )


def desc_car(hash_tag, chat_to):
    car_info = get_db_data(os.environ.get('DB'), os.environ.get('DB_USER'), os.environ.get('DB_PASS'),
                           os.environ.get('DB_HOST'), os.environ.get('DB_PORT'), hash_tag)
    label_hashtag = label_tag(car_info)
    bot.send_message(chat_to, str(car_info) + "\n\n🏎📷⤵️", parse_mode='Markdown')
    bot.send_media_group(chat_to, media=get_images(os.environ.get('YD_TOKEN'), yd_path(car_info)),
                         disable_notification=None)

    tags = get_tags(os.environ.get('DB'), os.environ.get('DB_USER'), os.environ.get('DB_PASS'),
                    os.environ.get('DB_HOST'), os.environ.get('DB_PORT'))
    if hash_tag == 1:
        bot.send_message(chat_to, str(tags) + " " + label_hashtag, parse_mode='Markdown')
    else:
        update_publish_yn(os.environ.get('DB'), os.environ.get('DB_USER'), os.environ.get('DB_PASS'),
                          os.environ.get('DB_HOST'), os.environ.get('DB_PORT'), yd_path(car_info))


def label_tag(desc):
    label = desc.split('\n', 1)[0]
    label = label.split(' ', 1)[0]
    label = label.replace('*', '')
    return '#' + label.lower()


def yd_path(desc):
    label = desc.split('\n', 1)[0]
    label = label.replace('*', '')
    return label


@bot.message_handler(commands=['img'])
def load_images(car_label):
    bot.send_media_group(CHAT_ID, media=get_images(os.environ.get('YD_TOKEN'), "Infiniti G35 COUPE '06"),
                         disable_notification=None)


@bot.message_handler(commands=['prom'])
def publish(message):
    print('Input text:', message.text)
    desc_car(0, CHANNEL_ID)


@bot.message_handler(content_types=['text'])
def write_media_for_url(message):
    insert_log(os.environ.get('DB'), os.environ.get('DB_USER'), os.environ.get('DB_PASS'),
               os.environ.get('DB_HOST'),
               os.environ.get('DB_PORT'), message.text, message.chat.id)
    get_photo(message.text)
    try:
        os.mkdir('test77')
    except FileExistsError as exc:
        bot.send_message(message.chat.id, exc)
        print(exc)
    bot.send_message(message.chat.id, 'test check')
    text = '/photo'
    path = text.split('/')
    for root, dirs, files in os.walk(path[1]):
        for file in files:
            with open(f'{path[1]}/{file}', 'rb') as obj:
                bot.send_photo(message.chat.id, obj)


bot.polling(none_stop=True)
