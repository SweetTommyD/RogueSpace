import libtcodpy as libtcod
import numpy as np
import Objects as Objects


class Map:

    galaxy_size = 0

    def __init__(self, x_size, y_size, scope, area=None):
        self.scope = scope
        self.area = area
        self.x = x_size
        self.y = y_size

        self.map_array = np.zeros((self.x, self.y), dtype=object)

        star_size = 8
        planet_size = 4
        moon_size = 1

        if self.scope == "galaxy_map":
            self.make_galaxy(50, 75)
        if self.scope == "star_system":
            self.make_system("system", 10, 15, star_size, planet_size, moon_size)

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
            star_x = libtcod.random_get_int(0, 0, self.x-1)
            star_y = libtcod.random_get_int(0, 0, self.y-1)

            star = Objects.CelestialObject(star_x, star_y, "S", "star", libtcod.Color(255, 255, 255), False, True,
                                           "star", 1, 1, "stuff", "stuff", "Stuff", "stuff")

            self.map_array[star_x][star_y] = star
            star_count -= 1

        return self.map_array

    def make_system(self, area, planet_number, moon_number, star_size, planet_size, moon_size):
        centerx = (self.x/2) - (star_size/2)
        centery = (self.y/2) - (star_size/2)

        star = Objects.CelestialObject(centerx, centery, "S", "star", libtcod.Color(255, 255, 255), False, True,
                                       "star", 1, star_size, "stuff", "stuff", "Stuff", "stuff")

        self.map_array[centerx][centery] = star

        while planet_number > 0:
            planet_x = libtcod.random_get_int(0, 0, self.x-planet_size)
            planet_y = libtcod.random_get_int(0, 20, self.y-planet_size-20)
            planet = Objects.CelestialObject(planet_x, planet_y, "P", "planet", libtcod.Color(0, 255, 255), False, True,
                                             "planet", 1, planet_size, "stuff", "stuff", "Stuff", "stuff")
            self.map_array[planet_x][planet_y] = planet
            planet_number -= 1

        while moon_number > 0:
            moon_x = libtcod.random_get_int(0, 0, self.x-moon_size)
            moon_y = libtcod.random_get_int(0, 20, self.y-moon_size-20)
            moon = Objects.CelestialObject(moon_x, moon_y, "M", "moon", libtcod.Color(255, 0, 255), False, True,
                                           "moon", 1, moon_size, "stuff", "stuff", "Stuff", "stuff")
            self.map_array[moon_x][moon_y] = moon
            moon_number -= 1

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




