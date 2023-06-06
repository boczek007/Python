# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 17:53:56 2020

@author: boczek
"""

#from perk_randomizer_classes import *



import threading
from multiprocessing import Process, Value, Array
import concurrent.futures
import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import time

dbdWikiUrl = 'https://deadbydaylight.fandom.com'

def foo(killer):
    killer.get_info
    
class Character:
    def __init__(self, name):
        self.__name = name
        self.__perks = []
        self.__description = ''
        self.__gender = False
        self.__nationality = ''
        self.__voiceActor = ''
        self.__charUrl = ''
        
    def change_url(self, url):
        self.__charUrl = url
    
    def get_url(self):
        return self.__charUrl
    
    def get_name(self):
        return self.__name
    
    
class Killer(Character):
    def __init__(self, name):
        super().__init__(name)
        self.trueName = name
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
        self.infos = []
        self.threads = []
        self.charContet = None
        
    def get_info(self):
        times = []
        charSite = BeautifulSoup(requests.get(self.get_url()).content, 'html.parser',parse_only=SoupStrainer("table"))
        infoTable = charSite.find('table', class_='infoboxtable').findAll('tr')
        info = [i.get_text().split('\n') for i in infoTable[:17]]
        self.infos.append(info)
        return info
            

class Survivor(Character):
    def __init__(self, name):
        super().__init__(self, name)
        self.role = ''