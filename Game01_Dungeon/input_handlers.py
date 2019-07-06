# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 22:43:34 2019

@author: boczek
"""

import tcod as libtcod

def handle_keys(key):
    key_char = chr(key.c)
    
    # Movement keys    
    if key.vk == libtcod.KEY_UP or key_char == 'w':
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == 's':
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'a':
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'd':
        return {'move': (1, 0)}
    
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toogle full screen
        return {'fullscreen': True}
    
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}
    
    # No key was pressed
    return {}      