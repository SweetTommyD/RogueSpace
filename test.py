import libtcodpy as libtcod
import numpy as np

SCREEN_HEIGHT = 50
SCREEN_WIDTH = 100

MAP_WIDTH = SCREEN_WIDTH
MAP_HEIGHT = SCREEN_HEIGHT

def make_galaxy(size_min, size_max, mapx, mapy):

    map_array = np.zeros((mapx, mapy), dtype=object)

    galaxy_size = libtcod.random_get_int(0, size_min, size_max)
    print "Galaxy size " + str(galaxy_size)

    while galaxy_size > 0:
        map_array[libtcod.random_get_int(0, 0, MAP_WIDTH-1), libtcod.random_get_int(0, 0, MAP_HEIGHT-1)] = 1
        galaxy_size -= 1

    return map_array

def display_map(map):
    for y in range(map):
        for x in range(map):
            print map.map_array[x, y]
            if map.map_array[x, y] > 0:
                libtcod.console_set_char_background(con, x, y, libtcod.Color(0, 0, 0), libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(con, x, y, libtcod.Color(255, 255, 255), libtcod.BKGND_SET)


galaxy_map = make_galaxy(10, 20, MAP_WIDTH, MAP_HEIGHT)


while not libtcod.console_is_window_closed():
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
    con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)
    libtcod.console_blit(con, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0, 0, 0)
    display_map(galaxy_map)
    libtcod.console_flush()

