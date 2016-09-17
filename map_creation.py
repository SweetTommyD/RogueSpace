import libtcodpy as libtcod
import numpy as np

class Map:

    galaxy_size = 0

    def __init__(self, x_size, y_size, scope, area=None):
        self.scope = scope
        self.area = area
        self.x = x_size
        self.y = y_size

        self.map_array = np.zeros((self.x, self.y), dtype=object)

        if self.scope == "galaxy_map":
            self.make_galaxy(50, 75)

    def scope(self):
        return self.scope

    def return_map_array(self):
        return self.map_array

    #Different methods for various scope and area types.  Scope refers to the map level.
    #Area is a special type of level, i.e. blackhole or nebula at the system level.
    def make_galaxy(self, size_min, size_max):

        global galaxy_size

        galaxy_size = libtcod.random_get_int(0, size_min, size_max)

        star_count = galaxy_size

        print "Galaxy size " + str(galaxy_size)

        while star_count > 0:
            self.map_array[libtcod.random_get_int(0, 0, self.x-1), libtcod.random_get_int(0, 0, self.y-1)] = 1
            star_count -= 1

        return self.map_array

    # def draw_lanes(map_array, lane_number=4):
    #
    #     global galaxy_size
    #
    #     lane_array = np.array(int)
    #
    #     start_x = self.x
    #     start_y = self.y
    #
    #     star_count = galaxy_size
    #     lane_count = lane_number
    #
    #     print star_count
    #
    #     while star_count > 0:
    #         print "lanecount- " + str(lane_count)
    #         for y in range(start_y):
    #             for x in range(start_x):
    #                 while lane_count > 0:
    #                     if map_array[x, y] > 0:
    #                         origin = [x, y]
    #                         print "origin" + str(origin)
    #                         np.append(lane_array, origin)
    #                         lane_count -= 1
    #                     if lane_count == 1:
    #                         start_x = x
    #                         print start_x
    #                         start_y = y
    #                         print start_y
    #
    #         for x in (lane_array[0], lane_array[2], ++4):
    #             x1 = lane_array[0]
    #             y1 = lane_array[1]
    #             x2 = lane_array[2]
    #             y2 = lane_array[3]
    #             libtcod.line_init(x1, y1, x2, y2)
    #             x, y = libtcod.line_step()
    #             print "step"
    #             libtcod.console_set_char_background(con, x, y, libtcod.Color(255, 255, 255), libtcod.BKGND_SET)
    #
    #         star_count -= 1

        #draw_lanes(self.map_array, libtcod.random_get_int(0, 1, 4))

    # def make_system(self.area):
    #
    # def make_planet(self.area):
    #
    # def make_area(self.area):

        #draw_lanes(self.map_array, libtcod.random_get_int(0, 1, 4))

    # if scope=="system_map":
    #     make_system(self.area)
    #     return self
    #
    # if scope=="planet_map":
    #     make_planet(self.area)
    #     return self
    #
    # if scope is None and self.area == "caves":
    #     make_area("caves")
    #     return self

    #etc.




