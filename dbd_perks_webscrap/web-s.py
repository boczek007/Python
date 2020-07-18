# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 14:29:36 2020

@author: boczek
"""

from urllib.request import urlopen as uReq
import unicodedata
from bs4 import BeautifulSoup as soup

my_url = 'https://deadbydaylight.gamepedia.com/Perks'

# opening ip connection, grabbing the page
uClient = uReq(my_url)
page_html = uClient.read().decode(uClient.headers.get_content_charset())
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")

containers = page_soup.findAll("table", {"class":"wikitable sortable"})
s = containers[0].tbody
survivors = s.findAll("tr")[1:]
k = containers[1].tbody
killers = k.findAll("tr")[1:]

perks = dict()
survivors_perks = []
killers_perks = []

filename = "perks.csv"
f = open(filename, "w", encoding="utf-8")

headers = "perk_name, description, character\n"

f.write(headers)

for survivor in survivors:
    temp = survivor.findAll("th")
    perk_name = unicodedata.normalize("NFKD",temp[1].a["title"]).encode("ascii","ignore").decode("utf-8")
    description = ''.join([i.text.strip() for i in survivor.td.findAll(["p", "ul"])]).replace("\xa0", " ").replace(".", ". ").replace("—", "-")
    if(temp[2].text.strip() == 'All'):
        character = temp[2].text.strip()
    else:
        character = temp[2].a["title"]
    survivors_perks.append([perk_name,  description,  character])
    f.write(perk_name + "," + description.replace(",","|").replace("\n", " ") + "," + character + "\n")

for killer in killers:
    temp2 = killer.findAll("th")
    perk_name = unicodedata.normalize("NFKD",temp2[1].a["title"]).encode("ascii","ignore").decode("utf-8")
    description = ''.join([i.text.strip() for i in killer.td.findAll(["p", "ul"])]).replace("\xa0", " ").replace(".", ". ").replace("—", "-")
    if(temp2[2].text.strip() == 'All'):
        character = temp2[2].text.strip()
    else:
        character = temp2[2].a["title"]
    killers_perks.append([perk_name,  description,  character])
    f.write(perk_name + "," + description.replace(",","|").replace("\n", " ") + "," + character + "\n")

f.close()
perks['killers'] = killers_perks
perks['survivors'] = survivors_perks
