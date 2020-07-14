import requests
import pprint
from PIL import Image
import glob
import os
import sys
import time
from io import open
from instabot import Bot
from os import listdir
from dotenv import load_dotenv
import os.path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def download_picture():
    filename = os.path.join(BASE_DIR, 'space-pictures', 'images', 'hubble.jpg')
    url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch():
    url = "https://api.spacexdata.com/v3/launches/latest"
    response = requests.get(url)
    response.raise_for_status()
    spacex_pictures = response.json()['links']['flickr_images']

    for picture_number, picture in enumerate(spacex_pictures):
        file_with_picture = os.path.join(BASE_DIR, 'space-pictures', 'images', 'spacex{}.jpg'.format(picture_number))
        response = requests.get(spacex_pictures[picture_number])

        with open(file_with_picture, 'wb') as file:
            file.write(response.content)


def download_hubble_pictures(id_image):
    url = "http://hubblesite.org/api/v3/image/" + id_image
    response = requests.get(url)
    response.raise_for_status()
    hubble_pictures = response.json()['image_files']

    for picture in hubble_pictures:
        link = picture['file_url']
        url = "https:" + link
        split_pictures = link.split('.')
        filename = os.path.join(BASE_DIR, 'space-pictures', 'images', 'hubble{}.{}'.format(id_image, split_pictures[-1]))
        response = requests.get(url)
        response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)


def download_hubble_collection(collection):
    url = "http://hubblesite.org/api/v3/images/" + collection
    response = requests.get(url)
    response.raise_for_status()
    hubble_collection = response.json()

    for picture in hubble_collection:
        image_id = picture['id']
        url = "http://hubblesite.org/api/v3/image/" + str(image_id)
        response = requests.get(url)
        response.raise_for_status()
        hubble_collection = response.json()['image_files']

        for picture in hubble_collection:
            link = picture['file_url']
            url = "https:" + link
            filename = os.path.join(BASE_DIR, 'space-pictures', 'collection', 'hubble-{}-{}.jpg'.format(collection, image_id))
            response = requests.get(url)
            response.raise_for_status()

            with open(filename, 'wb') as file:
                file.write(response.content)


def main():
    load_dotenv()
    download_picture()
    download_hubble_pictures("1")
    download_hubble_collection("spacecraft")
    fetch_spacex_last_launch()

    insta_login = os.getenv("LOGIN")
    insta_password = os.getenv("PASSWORD")
    bot = Bot()
    bot.login(username=insta_login, password=insta_password)

    folder = []

    for i in os.walk(os.path.join(BASE_DIR, 'space-pictures', 'images')):
        folder.append(i)

    for i in os.walk(os.path.join(BASE_DIR, 'space-pictures', 'collection')):
        folder.append(i)

    for address, dirs, files in folder:
        for file in files:
            instagram_image = Image.open(address+'/'+file)
            instagram_image.thumbnail((1080, 1080))
            instagram_image.save(address+'/'+file)
            bot.upload_photo(address+'/'+file)


if __name__ == '__main__':
    main()
