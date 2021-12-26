import urllib.request, urllib.error
from PIL import Image, ImageOps
import os
import argparse

# to get the input from command line
parser = argparse.ArgumentParser(
    description='Enter a URL')
parser.add_argument('-u','--url', metavar='URL',
                    help='URL of Image')
args = parser.parse_args()

# function to return the human readable size
def get_readable_size(file):
    size = os.stat(file).st_size # size of file in B
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']:
        if size < 1024.0 or unit == 'PiB':
            break
        size /= 1024.0
    return '{size:.2f} {unit}'.format(size=size, unit=unit)

# function to resize the image into given size (w, h)
def resize_image(file, size):
    img = Image.open(file)
    thumbnail = ImageOps.contain(img, size) # resize the image by retailing the aspect ration to fit in given size
    ext = file.split('.')[1] # storing the extension of file to save the resized image with same extension
    thumbnail_file = 'thumbnail.{ext}'.format(ext=ext)
    thumbnail.save(thumbnail_file) # saving the new resized image
    return thumbnail_file


# function to get resolution of image in w(px), h(px)
def get_resolution(file):
    img = Image.open(file)
    w, h = img.size 
    return w, h

# todo function
def todo(file):
    # dictionary to store data
    dic = {}
    # resized image file name after geting image file resized with given size (250,250)

    print("Enter the size of resized image in pixels: ")
    try:
        w = int(input("w: "))
    except:
        print("given input is not integer")
    try:
        h = int(input("h: "))
    except:
        print("given input is not integer")
    thumbnail_file = resize_image(file, (w, h))
    # path of resized image
    path = os.path.abspath(thumbnail_file)
    # store path
    dic['thumbnail_path'] = path
    # store original image file size
    dic['original_size'] = get_readable_size(file)
    # store resized image file
    dic['thumbnail_size'] = get_readable_size(thumbnail_file)
    # get resolution of image file in (w, h)
    file_w, file_h = get_resolution(file)
    # store resolution of image
    dic['original_resolution'] = "({w}x{h})".format(w=file_w, h=file_h)
    # get resolution of resized image file in (w, h)
    thumbnail_w, thumbnail_h = get_resolution(thumbnail_file)
    # store resolution of resized image file 
    dic['thumbnail_resolution'] = "({w}x{h})".format(w=thumbnail_w, h=thumbnail_h)
    print(dic)
    

# for url
def check_url(url):
    try:
        # check if given input is url
        response = urllib.request.urlopen(url)
        # get content type 
        is_image = response.info().get_content_type().split('/')[0]
        # check if content type is of image
        if (is_image == 'image'):
            # getting the extension of image eg: jpg, png, jpeg
            ext = response.info().get_content_type().split('/')[1]
            file_name = 'image.{ext}'.format(ext=ext)
            # download image
            urllib.request.urlretrieve(url, file_name)
            # calling the todo function
            todo(file_name)
        else:
            # the given url is not of a image
            return 'URL is not of a image'
    except:
        # the given input is not url
        return "Not a URL"


# url = 'https://www.google.com/logos/doodles/2021/uefa-euro-2020-6753651837109267-l.png'



if __name__ == '__main__':
    # if input is not given from command line
    if (args.url is None):
        url = input("Enter URL: ")
    else:
        url = args.url
    # validating url
    check_url(url)
