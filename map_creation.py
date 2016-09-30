import libtcodpy as libtcod
import numpy as np
import Objects as Objects

class Biome:
    def __init__(self, x, y, char, name, color, blocks=False, blocks_sight=False):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocks = blocks
        self.blocks_sight = blocks_sight

    def draw(self, con):
        #only show if it's visible to the player; or it's set to "always visible" and on an explored tile
        # if (libtcod.map_is_in_fov(fov_map, self.x, self.y) or
        #         (self.always_visible and map[self.x][self.y].explored)):
        #set the color and then draw the character that represents this object at its position
        libtcod.console_set_default_foreground(con, self.color)
        libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)
        #print "draw"
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
        if self.scope == "planet":
            self.make_planet("mountain", 100)

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

    def make_planet(self, planet_type, size):
        forest = Biome(0, 0, "!", "forest", libtcod.Color(0, 150, 0), False, True)
        plains = Biome(0, 0, "=", "plains", libtcod.Color(20, 200, 10), False, False)
        desert = Biome(0, 0, "#", "desert", libtcod.Color(0, 150, 0), False, False)

        elevation_array = np.zeros((self.x, self.y), dtype=object)
        temp_array = np.zeros((self.x, self.y), dtype=object)
        humidity_array = np.zeros((self.x, self.y), dtype=object)

        elevation_array = Map.make_elevation(self, 5, elevation_array)
        self.map_array = elevation_array
        self.map_array = Map.make_water(self, 3, elevation_array)
         
        for x in range(self.x):
            #print x
            for y in range(self.y):
                #print y
                #print self.map_array[x][y]
                if self.map_array[x][y] > 30 and self.map_array[x][y] < 80:
                    self.map_array[x][y] = Biome(x, y, "m", "hills", libtcod.Color(100, 200, 40), False, True)
                elif self.map_array[x][y] > 80 and self.map_array[x][y] < 200:
                    self.map_array[x][y] = Biome(x, y, "M", "mountain", libtcod.Color(200, 200, 200), True, True)
                elif self.map_array[x][y] == "200":
                    self.map_array[x][y] = Biome(x, y, "W", "water", libtcod.Color(0, 0, 255), True, False)
        #self.map_array = Map.make_water(self, 5, water_array, completed_elevation_array)

    def make_elevation(self, seeds, array):
        while seeds > 0:
            random_x = libtcod.random_get_int(0, 0, self.x-1)
            random_y = libtcod.random_get_int(0, 0, self.y-1)
            new_array = array
            steps = 100
            while steps <= 100:
                if random_x >= self.x-1 or random_y >= self.y-1 or random_x < -64 or random_y < -64:
                    break
                else:
                    random_x = random_x + libtcod.random_get_int(0, -1, 1)
                    #print random_x
                    random_y = random_y + libtcod.random_get_int(0, -1, 1)
                    #print random_y
                    new_array[random_x][random_y] += 10
                    #print array
                    steps -= 1
            seeds -= 1
        #print new_array
        return new_array

    def make_water(self, seeds, elevation_array):
        while seeds > 0:
            random_x = libtcod.random_get_int(0, 0, self.x-1)
            random_y = libtcod.random_get_int(0, 0, self.y-1)
            steps = 100
            new_array = elevation_array
            while steps <= 100:
                if random_x >= self.x-1 or random_y >= self.y-1 or random_x < -64 or random_y < -64:
                    break
                elif new_array[random_x][random_y] > 30 and new_array[random_x][random_y] < 200:
                    break
                else:
                    random_x = random_x + libtcod.random_get_int(0, -1, 1)
                    print random_x
                    random_y = random_y + libtcod.random_get_int(0, -1, 1)
                    print random_y
                    new_array[random_x][random_y] = "200"
                    print new_array[random_x][random_y]
                    #print new_array
                    steps -= 1
            seeds -= 1
        return new_array


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




