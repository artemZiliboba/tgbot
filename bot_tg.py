from instaloader import Instaloader, Profile
from datetime import datetime
from itertools import dropwhile, takewhile
from urllib.parse import urlparse
import time
import telebot
import socket
import os

TOKEN = str(os.environ.get('BOT_TOKEN'))
PROFILE = str(os.environ.get('PROFILE'))
CHAT_ID = str(os.environ.get('CHAT_ID'))
LOGIN_AUTH = os.environ.get('LOGIN_AUTH')
INSTA_LOGIN = str(os.environ.get('INSTA_LOGIN'))
INSTA_PASS = str(os.environ.get('INSTA_PASS'))

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    sent = bot.send_message(CHAT_ID, 'Hi, boss')
    bot.register_next_step_handler(sent, insta)


@bot.message_handler(commands=['get'])
def start(message):
    sent = bot.send_message(CHAT_ID, 'Get me URL profile')
    bot.register_next_step_handler(sent, top)


def insta(message):
    loader = Instaloader()
    print('LOGIN_AUTH = ' + LOGIN_AUTH)
    if LOGIN_AUTH == '1':
        loader.login(INSTA_LOGIN, INSTA_PASS)
    list_post = {}
    posts = Profile.from_username(loader.context, PROFILE).get_posts()

    since = datetime.today()
    until = datetime(2021, 3, 1)
    count = 0

    for post in takewhile(lambda p: p.date > until, dropwhile(lambda p: p.date > since, posts)):
        print(str(str(count) + '→' + datetime.now()) + ' → ' + post.url)
        list_post[post.likes] = post.url
        # time.sleep(3)
        count = count + 1
        if count == 9:
            loader.login(INSTA_LOGIN, INSTA_PASS)
            count = 0
            print('New login. Count is ' + str(count))

    print('MAX likes is post : {} : {}'.format(str(max(list_post.keys())), str(list_post.get(max(list_post.keys())))))
    bot.send_photo(CHAT_ID, str(list_post.get(max(list_post.keys()))),
                   'L | ' + str(max(list_post.keys())) + '\n' +
                   'P | ' + PROFILE)


@bot.message_handler(commands=['status'])
def state(message):
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    bot.send_message(CHAT_ID, 'IP : ' + local_ip
                     + '\nBOT_TOKEN: ' + str(os.environ.get('BOT_TOKEN'))
                     + '\nCHAT_ID : ' + str(os.environ.get('CHAT_ID'))
                     )


def top(message):
    loader = Instaloader()
    if LOGIN_AUTH == '1':
        loader.login(INSTA_LOGIN, INSTA_PASS)
    list_post = {}
    o = urlparse(message.text)
    posts = Profile.from_username(loader.context, o.path.replace('/', '')).get_posts()

    since = datetime.today()
    until = datetime(2020, 4, 1)

    for post in takewhile(lambda p: p.date > until, dropwhile(lambda p: p.date > since, posts)):
        list_post[post.likes] = post.url

    print('MAX likes is post : {} : {}'.format(str(max(list_post.keys())), str(list_post.get(max(list_post.keys())))))
    bot.send_photo(CHAT_ID, str(list_post.get(max(list_post.keys()))),
                   'L | ' + str(max(list_post.keys())) + '\n' +
                   'P | ' + o.path.replace('/', ''))


bot.polling(none_stop=True)
