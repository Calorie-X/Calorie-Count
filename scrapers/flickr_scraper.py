import flickrapi
import urllib as ulib
from os import environ
from hashlib import md5
from time import localtime
import random

# must register with flickr dev API to get key and secret
api_key = u' '
api_secret = u' '
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# fetch URLs of the correct sizes of images returned from flickr.photos.search() endpoint
def get_sizes(page, ppage, tag):
    # fetch list of URLs
    photos = flickr.photos.search(tags=tag, page=str(page), per_page=str(ppage))
    photo_list = photos['photos']['photo']
    p_ids = [photo_list[j]['id'] for j in range(len(photo_list))]
    siz = [flickr.photos.getSizes(photo_id = j) for j in p_ids]
    myurls = [ siz[j]['sizes']['size'][4]['source'] for j in range(len(siz)) ]
    return myurls

# randomize filenames
def add_prefix(name):
    return "%s_%s" % (md5(str(localtime()).encode('utf-8')).hexdigest(), name)

# download the files
def download_pics(myurls, save_to):
    for j in range(len(myurls)):
        k = random.randint(0,100000+j)
        name = 'pic'+str(k)
        name = add_prefix(name)
        name = name + '.jpg'
        img = ulib.request.urlopen(myurls[j]).read()
        imgfile = open(environ['HOME'] + save_to + name, 'wb')
        imgfile.write(img)
        imgfile.close()
    print('finished!')


# sample usage by calling these functions
'''
    page = 3
    how_many = 10
    tag = 'pie'
    save_to = '/algos/img_clf/data/train/'
    sizes = get_sizes(page, how_many, tag)
    download_pics(sizes, save_to)
'''
