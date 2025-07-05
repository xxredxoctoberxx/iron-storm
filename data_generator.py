import os
from os import listdir
import glob
import time
import random
import randomname
import pandas as pd
import time

from info_logger import Info_Logger as il

#load metadata
def load_metadata():
    '''
    Loads lists of meta data to use -> returns list dict().
    Available Keys: generic_name_list, color_list, letters, unisex_names, emojis,links
    '''
    meta_dict = dict()
    all_files = glob.glob(r'C:\Users\danil\PythonFiles\IronStorm\meta_data\*.csv')
    for csv_file in all_files:
        df = pd.read_csv(csv_file,header=None)
        data_list = df[df.columns[0]].values.tolist()
        data_list_name = data_list[0]
        data_list = data_list[1:]
        meta_dict[f'{data_list_name}'] = data_list
    il.bot_log('Meta Data fully loaded.')
    return meta_dict

metadata = load_metadata()

def tag_generator():
    '''
    Create a tag for your user
    Rules:
    Your tag can't exceed 30 characters
    It can only contain letters, numbers, and periods
    It can't contain symbols or punctuation marks
    It needs to be unique
    '''

    generic_list = metadata['generic_name_list']
    color_list = metadata['color_list']
    letters = metadata['letters']

    random_n = random.randint(0, 10)
    if random_n > 8:
        first = color_list[random.randint(0,len(color_list)-1)] + '_'
        second = generic_list[random.randint(0,len(generic_list)-1)]
        third = '_' + str(random.randint(0,100))
        tag = first + second + third
    elif 6 < random_n < 9:
        first = letters[random.randint(0,len(letters)-1)] + '_'
        second = letters[random.randint(0,len(letters)-1)]
        third = '_' + generic_list[random.randint(0,len(generic_list)-1)]
        tag = first + second + third
    elif 4 < random_n < 7:
        first = letters[random.randint(0,len(letters)-1)]
        second = str(random.randint(0,1000))
        third = generic_list[random.randint(0,len(generic_list)-1)]
        tag = first + second + third
    elif 2 < random_n < 5:
        first = generic_list[random.randint(0,len(generic_list)-1)]
        second = str(random.randint(0,1000)) + letters[random.randint(0,len(letters)-1)]
        third = generic_list[random.randint(0,len(generic_list)-1)]
        tag = first + second + third
    else:
        first = letters[random.randint(0,len(letters)-1)] + str(random.randint(0,10))
        second = generic_list[random.randint(0,len(generic_list)-1)]
        third = first
        tag = first + second + third
    
    tag = tag[:29]
    return tag

def bio_generator():
    '''
    Emojis, /n, quotes, exetra, profession, classes.
    '''

    quotes = ['im the best']
    emojis = metadata['emojis']
    
    random_n = random.randint(0, 10)
    if random_n > 7:
        rand_emoji = emojis[random.randint(0,len(emojis)-1)]
        bio = rand_emoji + quotes[random.randint(0,len(quotes)-1)] + ' ' + rand_emoji
    elif 4 < random_n < 8:
        bio = quotes[random.randint(0,len(quotes)-1)]
    else:
        bio = (emojis[random.randint(0,len(emojis)-1)] + ' ')
    
    return bio

def pfp_generator(dir:str):
    '''
    Returns random image path from specified directory.
    Supports the formats: .png, .jpg, .jpeg
    '''

    image_list = []
    for image in os.listdir(dir):
        
        # check if the image ends with png or jpg or jpeg
        if (image.endswith(".png") or image.endswith(".jpg")\
            or image.endswith(".jpeg")):
            image_list.append(image)

    select_rand_image = image_list[random.randint(0,len(image_list)-1)]
    rand_image = dir + '\\' + select_rand_image

    return rand_image


def link_generator():
    '''
    Generates random link.
    '''

    links = metadata['links']
    rand_link = links[random.randint(0,len(links)-1)]
    return rand_link

def name_generator():
    '''
    Generic names/nick names generator
    '''

    unisex_names = metadata['letters']
    emojis = metadata['emojis']

    random_n = random.randint(0, 10)
    if random_n > 7:
        name = randomname.get_name(sep=' ')
    elif 4 < random_n < 8:
        name = unisex_names[random.randint(0,len(unisex_names)-1)]
    else:
        name = (emojis[random.randint(0,len(emojis)-1)] + ' ') * 3

    return name

#load a list out of csv column
#df = pd.read_csv('quotes.csv',header=None) 
#somefilelist = df[df.columns[0]].values.tolist()
#print(somefilelist)

#for meta_list in [hashtags_pa,comments]:
 #  df = pd.DataFrame()
  # list_name = meta_list[0]
  # df[f'{list_name}'] = meta_list
  # df.to_csv(f"{list_name}.csv", header=False, index=False)
  # print(f'{list_name} file created.')









