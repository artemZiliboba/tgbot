from instaloader import Instaloader, Profile
from datetime import datetime
from itertools import dropwhile, takewhile
import telebot
import socket
import os

TOKEN = str(os.environ.get('BOT_TOKEN'))
PROFILE = os.environ.get('PROFILE')
CHAT_ID = os.environ.get('CHAT_ID')
INSTA_LOGIN = os.environ.get('INSTA_LOGIN')
INSTA_PASS = os.environ.get('INSTA_PASS')

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    sent = bot.send_message(CHAT_ID, 'Hi, boss')
    bot.register_next_step_handler(sent, insta)


def insta(message):
    loader = Instaloader()
    loader.login(INSTA_LOGIN, INSTA_PASS)
    list_post = {}
    posts = Profile.from_username(loader.context, PROFILE).get_posts()

    since = datetime.today()
    until = datetime(2021, 3, 1)

    for post in takewhile(lambda p: p.date > until, dropwhile(lambda p: p.date > since, posts)):
        list_post[post.likes] = post.url

    print('MAX likes is post : {} : {}'.format(str(max(list_post.keys())), str(list_post.get(max(list_post.keys())))))
    bot.send_photo(CHAT_ID, str(list_post.get(max(list_post.keys()))),
                   'L | ' + str(max(list_post.keys())) + '\n' +
                   'P | ' + PROFILE)


@bot.message_handler(commands=['status'])
def state(message):
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    sent = bot.send_message(CHAT_ID, 'IP : ' + local_ip
                            + '\nBOT_TOKEN: ' + str(os.environ.get('BOT_TOKEN'))
                            + '\nCHAT_ID : ' + str(os.environ.get('CHAT_ID'))
                            )


bot.polling(none_stop=True)
