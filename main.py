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

def download_pictures(): 
    filename = "images/hubble.jpg"
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
      file_with_picture = "images/spacex{}.jpg".format(picture_number)
      response = requests.get(spacex_pictures[picture_number])
      
      with open(file_with_picture, 'wb') as file:
        file.write(response.content)

def download_hubble_pictures():
    id_image = "1"
    url = "http://hubblesite.org/api/v3/image/" + id_image
    response = requests.get(url)
    response.raise_for_status()
    hubble_pictures = response.json()['image_files']

    for picture in hubble_pictures:
      links = picture['file_url']
      url = "https:" + links
      split_pictures = links.split('.')
      filename = "images/hubble{}.{}".format(id_image, split_pictures[-1])
      response = requests.get(url)
      response.raise_for_status()
      
    with open(filename, 'wb') as file:
       file.write(response.content)


def download_hubble_collection():
    collection = "spacecraft"
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
        links = picture['file_url']
        url = "https:" + links
        filename = "collection/hubble-{}-{}.jpg".format(collection, image_id)
        response = requests.get(url)
        response.raise_for_status()
        
        with open(filename, 'wb') as file:
          file.write(response.content)

def main():
    load_dotenv()
    download_pictures()    
    download_hubble_pictures()
    download_hubble_collection()
    fetch_spacex_last_launch()

    insta_login = os.getenv("LOGIN")
    insta_password = os.getenv("PASSWORD")
    bot = Bot()
    bot.login(username=insta_login, password=insta_password)

    for image in listdir("images"):
      path = "images/" + image
      instagram_image = Image.open(path)
      instagram_image.thumbnail((1080, 1080))
      instagram_image.save(path)
      bot.upload_photo(path)

    for image in listdir("collection"):
      path = "collection/" + image
      instagram_image = Image.open(path)
      instagram_image.thumbnail((1080, 1080))
      instagram_image.save(path)
      bot.upload_photo(path)

if __name__ == '__main__':
    main()