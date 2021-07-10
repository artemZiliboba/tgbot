import yadisk
from telebot.types import InputMediaPhoto


def get_images(auth_token, str_path):
    medias = []
    y = yadisk.YaDisk(token=auth_token)
    path = "disk:/GT5/images/" + str_path
    fields = [("photo", i.file) for i in y.listdir(path, fields=["media_type", "file"])]

    for n, item in fields:
        medias.append(InputMediaPhoto(media=item, caption=None))

    return medias
