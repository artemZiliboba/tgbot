import os
from instabot import Bot
import requests

INSTA_NAME = str(os.environ.get('INAME'))
INSTA_PASS = str(os.environ.get('IPASS'))
INSTA_CONF = str(os.environ.get('ICONF'))

if os.path.isfile(INSTA_CONF):
    print("[INFO] Delete config file")
    os.remove(INSTA_CONF)
else:  # Show an error
    print("[INFO] Config %s not found, continue" % INSTA_CONF)
instaBot = Bot()
instaBot.login(username=INSTA_NAME, password=INSTA_PASS)


def get_photo(url):
    try:
        os.mkdir('photo')
    except FileExistsError as exc:
        print(exc)
    chose_media = instaBot.get_media_id_from_link(url)
    download_photo(chose_media, "photo/img_")


def check_dirs():
    for root, dirs, files in os.walk('photo'):
        for file in files:
            os.remove(f'photo/{file}')
    for root, dirs, files in os.walk('video'):
        for file in files:
            os.remove(f'video/{file}')


def download_photo(media_id, filename):
    media = instaBot.get_media_info(media_id)[0]
    print()
    if 'image_versions2' in media.keys() and 'video_versions' not in media.keys():
        url = media['image_versions2']['candidates'][0]['url']
        response = requests.get(url)
        with open(filename + ".jpg", "wb") as f:
            response.raw.decode_content = True
            f.write(response.content)
    if "carousel_media" in media.keys():
        for e, element in enumerate(media["carousel_media"]):
            url = element['image_versions2']["candidates"][0]["url"]
            response = requests.get(url)
            with open(filename + str(e) + ".jpg", "wb") as f:
                response.raw.decode_content = True
                f.write(response.content)
