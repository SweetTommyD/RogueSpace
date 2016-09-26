import libtcodpy as libtcod
import map_creation as mc
import Objects

SCREEN_HEIGHT = 65
SCREEN_WIDTH = 110

MAP_WIDTH = SCREEN_WIDTH
MAP_HEIGHT = SCREEN_HEIGHT

key = libtcod.Key()
mouse = libtcod.Mouse()

def display_map(Map):
    for y in range(Map.y):
        for x in range(Map.x):
            #print Map.map_array[x, y]
            o = Map.map_array[x, y]
            #print o
            if o != 0:
                object_type = o.object_type
                print object_type
            else:
                object_type = ""
            if object_type == "star":
                o.draw(con)
            if object_type == "moon":
                o.draw(con)
            if object_type == "planet":
                o.draw(con)
            # elif Map.map_array[x, y] == 2:
            #     libtcod.console_set_char_background(con, x, y, libtcod.Color(0, 0, 255), libtcod.BKGND_SET)
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

player = Objects.Ship(10, 10, "A", "player", libtcod.Color(255, 0, 0), False, True, 10, 10, 1, 1)

system_map = mc.Map(MAP_WIDTH, MAP_HEIGHT, "star_system")

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
