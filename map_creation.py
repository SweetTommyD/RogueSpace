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

        star_mass = 8
        planet_mass = 4
        moon_mass = 1

        if self.scope == "galaxy_map":
            self.make_galaxy(50, 75)
        if self.scope == "star_system":
            self.make_system("system", 10, 15, star_mass, planet_mass, moon_mass)

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

    def make_system(self, area, planet_number, moon_number, star_mass, planet_mass, moon_mass):
        centerx = self.x/2
        centery = self.y/2

        for x in range(centerx, centerx+star_mass):
            for y in range(centery, centery+star_mass):
                self.map_array[x][y] = 1

        while planet_number > 0:
            planet_x = libtcod.random_get_int(0, 0, self.x-planet_mass)
            planet_y = libtcod.random_get_int(0, 0, self.y-planet_mass)
            for x in range(planet_x, planet_x+planet_mass):
                for y in range(planet_y, planet_y+planet_mass):
                    self.map_array[x][y] = 2
            planet_number -= 1

        while moon_number > 0:
            moon_x = libtcod.random_get_int(0, 0, self.x-moon_mass)
            moon_y = libtcod.random_get_int(0, 0, self.y-moon_mass)
            for x in range(moon_x, moon_x+moon_mass):
                for y in range(moon_y, moon_y+moon_mass):
                    self.map_array[x][y] = 3
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




