import libtcodpy as libtcod
import map_creation as mc
import Objects
import numpy as np

SCREEN_HEIGHT = 65
SCREEN_WIDTH = 110

MAP_WIDTH = SCREEN_WIDTH
MAP_HEIGHT = SCREEN_HEIGHT

key = libtcod.Key()
mouse = libtcod.Mouse()

def display_map(Map):
    for y in range(Map.y):
        #print "this is y " + str(y)
        for x in range(Map.x):
            #print "this is x " + str(x)
            #print Map.map_array[x, y]
            o = Map.map_array[x, y]

            if isinstance(o, Objects.Object):
                o.draw(con)
            elif isinstance(o, mc.Biome):
                o.draw(con)

            # print "new_o= " + str(new_o)
            # if new_o <= 33:
            #     b = int(new_o)
            # if new_o > 33 and new_o <= 66:
            #     g = int(new_o)
            # if new_o > 66:
            #     r = int(new_o)
            #
            # # R = int(o)/256 ^ 2
            # #
            # # G = int(o)/256 % 256 ^ 2
            # #
            # # B = int(o) % 256
            # # #print new_o
            # libtcod.console_set_char_background(con, x, y, libtcod.Color(r, g, b), libtcod.BKGND_SET)

            #libtcod.console_set_char_background(con, x, y, libtcod.Color(0, 0, o), libtcod.BKGND_SET)

            # elif Map.map_array[x, y] == 3:
            #     libtcod.console_set_char_background(con, x, y, libtcod.Color(255, 255, 0), libtcod.BKGND_SET)
            # else:
            #     libtcod.console_set_char_background(con, x, y, libtcod.Color(0, 0, 0), libtcod.BKGND_SET)

def handle_keys():
    global key

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    elif key.vk == libtcod.KEY_ESCAPE:
        return 'exit'  #exit game

    if game_state == 'playing':
        #movement keys
        if key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
            player.move(0, -1)
        elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
            player.move(0, 1)
        elif key.vk == libtcod.KEY_LEFT or key.vk == libtcod.KEY_KP4:
            player.move(-1, 0)
        elif key.vk == libtcod.KEY_RIGHT or key.vk == libtcod.KEY_KP6:
            player.move(1, 0)
        elif key.vk == libtcod.KEY_HOME or key.vk == libtcod.KEY_KP7:
            player.move(-1, -1)
        elif key.vk == libtcod.KEY_PAGEUP or key.vk == libtcod.KEY_KP9:
            player.move(1, -1)
        elif key.vk == libtcod.KEY_END or key.vk == libtcod.KEY_KP1:
            player.move(-1, 1)
        elif key.vk == libtcod.KEY_PAGEDOWN or key.vk == libtcod.KEY_KP3:
            player.move(1, 1)
        elif key.vk == libtcod.KEY_KP5:
            pass  #do nothing ie wait for the monster to come to you
        else:
            #test for other keys
            key_char = chr(key.c)
            #if key_char == '<':
                #go down stairs, if the player is on them


player = Objects.Ship(10, 10, "A", "player", libtcod.Color(255, 0, 0), False, True, 10, 10, 1, 1)

system_map = mc.Map(MAP_WIDTH, MAP_HEIGHT, "planet", "ice")

while not libtcod.console_is_window_closed():
    game_state = "playing"
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
    con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)
    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
    display_map(system_map)
    player.draw(con)
    handle_keys()
    libtcod.console_blit(con, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0, 0, 0)
    libtcod.console_flush()
