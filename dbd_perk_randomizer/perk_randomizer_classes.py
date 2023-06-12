# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 12:26:36 2020

@author: boczek
"""
'''
dbd wiki: https://deadbydaylight.fandom.com
'''
#import re
import threading
#import concurrent.futures
import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import time
import os
import pathlib

DBD_WIKI_URL = 'https://deadbydaylight.fandom.com'
DBD_WIKI_PERKS_URL = 'https://deadbydaylight.fandom.com/wiki/Perks'
FILE_PATH = f'{pathlib.Path(__file__).parent.resolve()}'

def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer

def timer_foo(foo):
    def wrap_foo(*args, **kwargs):
        start = time.time()
        result = foo(*args,**kwargs)
        end = time.time()
        print(f'Function {foo.__name__!r} executed in {(end-start):.4f}s')
        return result
    return wrap_foo


# File handling class used mostly to save and load characters, perks and other informations
class FileHandling:
    def __init__(self, path=FILE_PATH):
        self.__to_save = []
        self.__save_path = path
        self.__to_load = []
    
    def add_to_save(self, new_data):
        self.__to_save.append(new_data)
    
    def get_save_info(self):
        return self.__to_save
    
    def get_load_info(self):
        return self.__to_load
    
    def get_path(self):
        return self.__save_path
        
    def save_to_file(self, filename, path=FILE_PATH):
        with open(os.path.join(path, filename), 'w') as save_file:
            for i in self.__to_save:
                for j in i:
                    if type(j)==str or type(j)==float or type(j)==int or type(j)==bool:
                        save_file.write(str(j))
                        save_file.write('\t')
                    elif type(j)==dict or type(j)==list or type(j)==tuple():
                        if type(j)==list or type(j)==tuple:
                            for k in j:
                                save_file.write(k)
                                save_file.write('&')
                            save_file.write('\t')
                        elif type(j)==dict:
                            for k in range(len(j)):
                                save_file.write(list(j.keys())[k])
                                save_file.write('$')
                                save_file.write(list(j.values()[k]))
                                save_file.write('&')
                            save_file.write('\t')
                        else:
                            pass
                    else:
                        pass
        save_file.close()
        
    def load_from_file(self, filename, path=FILE_PATH):
        with open(os.path.join(path, filename), 'r') as load_file:
            load_data = load_file.readlines()
            
        load_file.close()
            
            
        
        
# !!! IMPORTANT !!! REPRESENTATION OF INFO WHILE CREATING CHARACTER CLASSES: KILLER AND SURVIVOR ALSO USE IT     
# info = [name, url, perks, imageUrl]
class Character:
    def __init__(self, info):
        self.__name = ''
        self.__perks = []
        self.__lore = ''
        self.__gender = False
        self.__nationality = ''
        self.__voiceActor = ''
        self.__charUrl = ''
        self.__imgUrl = ''
        self.__infos = []
        
        if len(info)==1:
            self.__name = info[0]
        else:
            self.__name = info[0]
            self.__perks = info[2]
            self.__charUrl = info[1]
            self.__imgUrl = info[3]
    
    def __repr__(self):
        try:
            charName = 'Name: {}'.format(self.__name)
            charPerks = 'Perks: {0}, {1}, {2}'.format(*self.__perks)
            rep = '{}\n{}\n'.format(charName,charPerks)
        except:
            rep = self.__name
        return rep
    
    def __str__(self):
        return self.__name
    
    def change_url(self, url):
        self.__charUrl = url
    
    def get_url(self):
        return self.__charUrl
    
    def get_name(self):
        return self.name
    
    def get_infos(self):
        return self.infos
    
    def download_image(self, download_dir):
        img_bytes = requests.get(self.__imgUrl).content
        img_name = f'{self.__name}.jpg'
        download_dir = os.path.join(download_dir, img_name)
        with open(download_dir, 'wb') as img_file:
            img_file.write(img_bytes)
    
    def get_info(self, check = True):
        charSite = BeautifulSoup(requests.get(self.get_url()).content, 'html.parser',parse_only=SoupStrainer("table"))
        infoTable = charSite.find('table', class_='infoboxtable').findAll('tr')
        if check:
            info = [i.get_text().split('\n') for i in infoTable[:17]]
            self.infos = info
        else:
            pass
    
class Killer(Character):
    def __init__(self, info):
        super().__init__(info)
        self.trueName = ''
        self.aliases = []
        self.realm = ''
        self.power = ''
        self.powerAttackType = ''
        self.weapon = ''
        self.movementSpeed = 0
        self.alternateMovementSpeed = 0
        self.terrorRadius = 0
        self.alternateTerrorRadius = 0
        self.height = 0
                 

class Survivor(Character):
    def __init__(self, info):
        super().__init__(info) 
        self.role = ''


# info = [name, desc, type, character name, perkUrl, imgUrl] type - True for survivor | False for killer
# type - survivor, killer
class Perk:
    def __init__(self, info = []):  
        try:
            self.__name = info[0]
            self.__description = info[1]
            self.__type = info[2]
            self.__character = info[3]
            self.__perkUrl = info[4]
            self.__imgUrl = info[5]
        except:
            self.__name = ''
            self.__description = ''
            self.__type = ''
            self.__character = ''
            self.__perkUrl = ''
            self.__imgUrl = ''        
        self.__img_dir = os.path.join(FILE_PATH,os.path.join('images','perks'))
        
    def __str__(self):
        return self.__name
    
    def get_description(self):
        return self.__description
    
    def get_name(self):
        return self.__name
    
    def get_character(self):
        return self.__character
    
    def get_url(self):
        return self.__perk_url

    def get_img_dir(self):
        return self.__img_dir
    
    def perk_type(self):
        if self.type:
            return 'Survivor'
        else:
            return 'Killer'
    
    def show_perk_info(self):
        print(self.__name)
        print("\n")
        print(self.__description)
        print("\n")
        print(self.__character)
        print("\n")
        print(self.__perkUrl)
        
    def download_image(self):
        img_bytes = requests.get(self.__imgUrl).content
        img_name = f'{self.__name}.jpg'
        download_dir = os.path.join(self.__img_dir, img_name)
        with open(download_dir, 'wb') as img_file:
            img_file.write(img_bytes)
        
        
    def update_perk(self, content):
        pass
        
    def prepare_to_save(self):
        return [self.__name, self.__description, self.__type, self.__character, self.__perkUrl, self.__imgUrl]
        
        
class Info:
    def __init__(self):
        #self.survivorsContent = dbdWiki.findAll(class_ = 'fplinks charSection')[1]
        #self.survivorsContent = survivorsContent.findAll(class_='fplink charMainPageBox plainlinks image')
        self.__directories = {'killers':['images','characters','killers'],
                            'survivors':['images','characters','survivors'],
                            'perks':['images','perks']}
        for new_dir in self.__directories.values():
            Info.create_images_dir(new_dir)
        self.__killersList = dict()
        self.__killerUrl = dict()
        self.__survivorsList = dict()
        self.__survivorUrl = dict()
        self.__perksList = dict()
        self.__dbdWiki = None
        self.__information = None
        self.__file_handler = FileHandling()
    
    def get_killersList(self):
        return self.__killersList
    
    def get_survivorsList(self):
        return self.__survivorsList
    
    def get_perksList(self):
        return self.__perksList
    
    @staticmethod
    def create_images_dir(*args):
        path_dir = FILE_PATH
        for arg in args:
            for i in arg:
                if i in os.listdir(path_dir):
                    path_dir = os.path.join(path_dir, i)
                else:
                    path_dir = os.path.join(path_dir, i)
                    os.mkdir(path_dir)
            path_dir = FILE_PATH
    
    def print_char(self, char_name):
        name_check = False
        if char_name.lower() == 'bubba':
            print(self.__killersList['The Cannibal'])
        else:
            for i in self.__killersList.values():
                if char_name.capitalize() == str(i)[4:]:
                    print(i)
                    name_check = True
                    break
            if name_check == False:
                for i in self.__survivorsList.values():
                    if char_name.capitalize() == str(i).split()[0] or char_name.capitalize() == str(i).split()[1]:
                        print(i)
                        name_check = True
                        break
            if name_check == False:
                print('Character is not in databese.')
            
    def print_chars(self):
        print(30*'#')
        print('Killers:\n', 30*'#',sep='')
        for killer in self.__killersList.values():
            print(killer)
        print(30*'#')
        print('Survivors:\n', 30*'#',sep='')
        for survivor in self.__survivorsList.values():
            print(survivor)        
            
    @timer_foo
    def __update_killers(self, content):
        threads = []
        for character in content:
            info = ['', '', [], '']
            info[0] = character.get_text()
            info[1] = DBD_WIKI_URL + character.find('a')['href']
            perks = character.find(class_='charPerkBox').findAll('a')
            info[2] = [perk['title'] for perk in perks]
            info[3] = character.find('img')['data-src']
            killer = Killer(info)
            images_path = os.path.join(FILE_PATH,os.path.join('images','characters'))
            t = threading.Thread(target=killer.download_image, args=(os.path.join(images_path,'killers'),))
            t.start()
            threads.append(t)
            self.__killersList[info[0]] = killer
        for thread in threads:
            thread.join()
        
    @timer_foo
    def __update_survivors(self, content):
        threads = []
        for character in content:
            info = ['', '', [], '']
            info[0] = character.get_text()
            info[1] = DBD_WIKI_URL + character.find('a')['href']
            perks = character.find(class_='charPerkBox').findAll('a')
            info[2] = [perk['title'] for perk in perks]
            info[3] = character.find('img')['data-src']
            survivor = Survivor(info)
            images_path = os.path.join(FILE_PATH,os.path.join('images','characters'))
            t = threading.Thread(target=survivor.download_image, args=(os.path.join(images_path,'survivors'),))
            t.start()
            threads.append(t)
            self.__survivorsList[info[0]] = survivor
        for thread in threads:
            thread.join()
    
    @timer_foo
    def __update_perks(self, content):
        # Helper function to get info about perks from site content
        def get_perk_info(site_content, perk_type):
            name = site_content.find('a').get('title')
            desc = ''
            perk_url = DBD_WIKI_URL + site_content.findAll('th')[1].find('a').get('href')
            img_url = site_content.find('a').get('href')
            character_name=''
            try:
                character_name = site_content.findAll('th')[2].find('a').get('title')
            except:
                character_name = 'All'
                perk_type = perk_type            
            return [name, desc, perk_type, character_name, perk_url, img_url]
        
        threads = []  
        perks_list = lambda x: x.find('tbody').findAll('tr')
        surv_perks = perks_list(content[0])[1:]
        killer_perks = perks_list(content[1])[1:]
        for i in surv_perks:
            perk_info = get_perk_info(i, 'survivor')
            perk = Perk(perk_info)
            t = threading.Thread(target=perk.download_image)
            threads.append(t)
            t.start()
            self.__perksList[perk_info[0]] = perk
        for i in killer_perks:
            perk_info = get_perk_info(i, 'killer')
            perk = Perk(perk_info)
            t = threading.Thread(target=perk.download_image)
            threads.append(t)
            t.start()
            self.__perksList[perk_info[0]] = perk
        for thread in threads:
            thread.join()

        
            
    @timer_foo
    def update(self):
        dbdWikiContent = BeautifulSoup(requests.get(DBD_WIKI_URL).content, 'lxml', parse_only=SoupStrainer(class_='fplinks charSection'))
        dbdWikiContent = dbdWikiContent.findAll(class_='fplinks charSection')
        killersContent = dbdWikiContent[0].findAll(class_='fplink charMainPageBox plainlinks image')
        survivorsContent = dbdWikiContent[1].findAll(class_='fplink charMainPageBox plainlinks image')
        dbdWikiPerksContent = BeautifulSoup(requests.get(DBD_WIKI_PERKS_URL).content, 'lxml', parse_only = SoupStrainer('table')).findAll('table')
        self.__update_perks(dbdWikiPerksContent)
        self.__update_killers(killersContent)
        self.__update_survivors(survivorsContent)
        
        
dbdWikiContent = BeautifulSoup(requests.get(DBD_WIKI_URL).content, 'lxml', parse_only=SoupStrainer(class_='fplinks charSection'))
dbdWikiContent = dbdWikiContent.findAll(class_='fplinks charSection')
killersContent = dbdWikiContent[0].findAll(class_='fplink charMainPageBox plainlinks image')
killers = [[i.get_text(), 'https://deadbydaylight.fandom.com'+i.find('a')['href']] for i in killersContent]
killersInfo = dict()
dbdwikiperks = BeautifulSoup(requests.get(DBD_WIKI_PERKS_URL).content, 'lxml', parse_only = SoupStrainer('table')).findAll('table')
for i in killers:
    temp = i[0][4:]
    killersInfo[temp] = Killer([temp])   
    killersInfo[temp].change_url(i[1])

perks_list = lambda x: x.find('tbody').findAll('tr')
surv_perks = perks_list(dbdwikiperks[0])[1:]
killer_perks = perks_list(dbdwikiperks[1])[1:]

pkp = Info()

