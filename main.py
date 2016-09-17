import libtcodpy as libtcod
import map_creation as mc

SCREEN_HEIGHT = 65
SCREEN_WIDTH = 110

MAP_WIDTH = SCREEN_WIDTH
MAP_HEIGHT = SCREEN_HEIGHT

def display_map(Map):
    for y in range(Map.y):
        for x in range(Map.x):
            #print Map.map_array[x, y]
            if Map.map_array[x, y] > 0:
                libtcod.console_set_char_background(con, x, y, libtcod.Color(255, 255, 255), libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(con, x, y, libtcod.Color(0, 0, 0), libtcod.BKGND_SET)


galaxy_map = mc.Map(MAP_WIDTH, MAP_HEIGHT, "galaxy_map")

while not libtcod.console_is_window_closed():
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
    con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)
    display_map(galaxy_map)
    libtcod.console_blit(con, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0, 0, 0)
    libtcod.console_flush()
