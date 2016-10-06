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

        if self.scope == "galaxy":
            self.make_galaxy(50, 75)
        if self.scope == "star":
            self.make_system("system", 10, 15, star_size, planet_size, moon_size)
        if self.scope == "planet":
            self.make_planet(100, self.area)

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

    def make_planet(self, size, planet_type="temperate"):

        elevation_array = np.zeros((self.x, self.y), dtype=object)
        tempr_array = np.zeros((self.x, self.y), dtype=object)
        humidity_array = np.zeros((self.x, self.y), dtype=object)

        if planet_type == "temperate":

            elevation_array = Map.make_elevation(self, 7, elevation_array)
            water_array = Map.make_water(self, 3, elevation_array)
            tempr_array = Map.make_temp(self, water_array, tempr_array)
            humidity_array = Map.make_humidity(self, water_array, humidity_array)
            self.map_array = water_array

            #self.map_array = Map.make_temp(self, 1000, elevation_array, tempr_array)

            for x in range(self.x):
                #print x
                for y in range(self.y):
                    #print y
                    #print self.map_array[x][y]
                    humidity = humidity_array[x][y]
                    if self.map_array[x][y] > 30 and self.map_array[x][y] < 80:
                        self.map_array[x][y] = Biome(x, y, "m", "hills", libtcod.Color(100, 100, 100), False, True)
                    elif self.map_array[x][y] > 80 and self.map_array[x][y] < 200:
                        self.map_array[x][y] = Biome(x, y, "M", "mountain", libtcod.Color(200, 200, 200), True, True)
                    elif self.map_array[x][y] == "200":
                        self.map_array[x][y] = Biome(x, y, "W", "water", libtcod.Color(0, 0, 255), True, False)
                    elif tempr_array[x][y] > 80 and humidity < 20:
                        self.map_array[x][y] = Biome(x, y, "#", "desert", libtcod.Color(200, 100, 0), False, False)
                    elif tempr_array[x][y] < 40 and humidity < 50:
                        self.map_array[x][y] = Biome(x, y, "_", "tundra", libtcod.Color(0, 100, 200), False, False)
                    elif tempr_array[x][y] > 80 and humidity > 90:
                        self.map_array[x][y] = Biome(x, y, "$", "jungle", libtcod.Color(0, 255, 0), False, True)
                    elif tempr_array[x][y] > 40 and humidity > 60:
                        self.map_array[x][y] = Biome(x, y, "!", "forest", libtcod.Color(0, 150, 50), False, True)
                    else:
                        self.map_array[x][y] = Biome(x, y, "=", "plains", libtcod.Color(100, 200, 50), False, False)

        if planet_type == "arid":

            elevation_array = Map.make_elevation(self, 7, elevation_array)
            water_array = Map.make_water(self, 1, elevation_array)
            tempr_array = Map.make_temp(self, water_array, tempr_array)
            humidity_array = Map.make_humidity(self, water_array, humidity_array)
            self.map_array = water_array

            #self.map_array = Map.make_temp(self, 1000, elevation_array, tempr_array)

            for x in range(self.x):
                for y in range(self.y):
                    humidity = humidity_array[x][y] - 40
                    temperature = tempr_array[x][y] + 40

                    if self.map_array[x][y] > 30 and self.map_array[x][y] < 80:
                        self.map_array[x][y] = Biome(x, y, "m", "hills", libtcod.Color(100, 100, 100), False, True)
                    elif self.map_array[x][y] > 80 and self.map_array[x][y] < 200:
                        self.map_array[x][y] = Biome(x, y, "M", "mountain", libtcod.Color(200, 200, 200), True, True)
                    elif self.map_array[x][y] == "200":
                        self.map_array[x][y] = Biome(x, y, "W", "water", libtcod.Color(0, 0, 255), True, False)
                    elif temperature > 80 and humidity < 20:
                        self.map_array[x][y] = Biome(x, y, "x", "wastes", libtcod.Color(200, 100, 0), False, False)
                    elif temperature < 40 and humidity < 50:
                        self.map_array[x][y] = Biome(x, y, "_", "tundra", libtcod.Color(200, 200, 200), False, False)
                    elif temperature > 40 and humidity > 40:
                        self.map_array[x][y] = Biome(x, y, "=", "desert", libtcod.Color(150, 150, 50), False, False)
                    else:
                        self.map_array[x][y] = Biome(x, y, "#", "scrub", libtcod.Color(255, 200, 50), False, True)

        if planet_type == "water":

            elevation_array = Map.make_elevation(self, 7, elevation_array)
            water_array = Map.make_water(self, 3, elevation_array)
            tempr_array = Map.make_temp(self, water_array, tempr_array)
            humidity_array = Map.make_humidity(self, water_array, humidity_array)
            self.map_array = water_array

            #self.map_array = Map.make_temp(self, 1000, elevation_array, tempr_array)

            for x in range(self.x):
                #print x
                for y in range(self.y):
                    #print y
                    #print self.map_array[x][y]
                    if self.map_array[x][y] > 30 and self.map_array[x][y] < 80:
                        self.map_array[x][y] = Biome(x, y, "m", "hills", libtcod.Color(100, 100, 100), False, True)
                    elif self.map_array[x][y] > 80 and self.map_array[x][y] < 200:
                        self.map_array[x][y] = Biome(x, y, "M", "mountain", libtcod.Color(200, 200, 200), True, True)
                    elif self.map_array[x][y] == "200":
                        self.map_array[x][y] = Biome(x, y, "W", "water", libtcod.Color(0, 0, 255), True, False)
                    elif tempr_array[x][y] > 80 and humidity < 20:
                        self.map_array[x][y] = Biome(x, y, "#", "desert", libtcod.Color(200, 100, 0), False, False)
                    elif tempr_array[x][y] < 40 and humidity < 50:
                        self.map_array[x][y] = Biome(x, y, "_", "tundra", libtcod.Color(0, 100, 200), False, False)
                    elif tempr_array[x][y] > 80 and humidity > 80:
                        self.map_array[x][y] = Biome(x, y, "$", "jungle", libtcod.Color(0, 255, 0), False, True)
                    elif tempr_array[x][y] > 40 and humidity > 60:
                        self.map_array[x][y] = Biome(x, y, "!", "forest", libtcod.Color(0, 150, 50), False, True)
                    else:
                        self.map_array[x][y] = Biome(x, y, "=", "plains", libtcod.Color(100, 200, 50), False, False)

        if planet_type == "forest":

            elevation_array = Map.make_elevation(self, 7, elevation_array)
            water_array = Map.make_water(self, 3, elevation_array)
            tempr_array = Map.make_temp(self, water_array, tempr_array)
            humidity_array = Map.make_humidity(self, water_array, humidity_array)
            self.map_array = water_array

            #self.map_array = Map.make_temp(self, 1000, elevation_array, tempr_array)

            for x in range(self.x):
                #print x
                for y in range(self.y):
                    humidity = humidity_array[x][y] + 60
                    #print y
                    #print self.map_array[x][y]
                    if self.map_array[x][y] > 30 and self.map_array[x][y] < 80:
                        self.map_array[x][y] = Biome(x, y, "m", "hills", libtcod.Color(100, 100, 100), False, True)
                    elif self.map_array[x][y] > 80 and self.map_array[x][y] < 200:
                        self.map_array[x][y] = Biome(x, y, "M", "mountain", libtcod.Color(200, 200, 200), True, True)
                    elif self.map_array[x][y] == "200":
                        self.map_array[x][y] = Biome(x, y, "W", "water", libtcod.Color(0, 0, 255), True, False)
                    elif tempr_array[x][y] > 80 and humidity < 20:
                        self.map_array[x][y] = Biome(x, y, "#", "desert", libtcod.Color(200, 100, 0), False, False)
                    elif tempr_array[x][y] < 40 and humidity < 50:
                        self.map_array[x][y] = Biome(x, y, "_", "tundra", libtcod.Color(0, 100, 200), False, False)
                    elif tempr_array[x][y] > 80 and humidity > 80:
                        self.map_array[x][y] = Biome(x, y, "$", "jungle", libtcod.Color(0, 255, 0), False, True)
                    elif tempr_array[x][y] > 40 and humidity > 60:
                        self.map_array[x][y] = Biome(x, y, "!", "forest", libtcod.Color(0, 150, 50), False, True)
                    else:
                        self.map_array[x][y] = Biome(x, y, "=", "plains", libtcod.Color(100, 200, 50), False, False)

        if planet_type == "ice":

            elevation_array = Map.make_elevation(self, 7, elevation_array)
            water_array = Map.make_water(self, 3, elevation_array)
            tempr_array = Map.make_temp(self, water_array, tempr_array)
            humidity_array = Map.make_humidity(self, water_array, humidity_array)
            self.map_array = water_array

            #self.map_array = Map.make_temp(self, 1000, elevation_array, tempr_array)

            for x in range(self.x):
                #print x
                for y in range(self.y):
                    humidity = humidity_array[x][y] - 20
                    temperature = tempr_array[x][y] - 70
                    #print y
                    #print self.map_array[x][y]
                    if self.map_array[x][y] > 30 and self.map_array[x][y] < 80:
                        self.map_array[x][y] = Biome(x, y, "m", "hills", libtcod.Color(100, 100, 100), False, True)
                    elif self.map_array[x][y] > 80 and self.map_array[x][y] < 200:
                        self.map_array[x][y] = Biome(x, y, "M", "mountain", libtcod.Color(200, 200, 200), True, True)
                    elif temperature < 20 and self.map_array[x][y] == "200":
                        self.map_array[x][y] = Biome(x, y, "i", "ice", libtcod.Color(0, 100, 100), False, False)
                    elif self.map_array[x][y] == "200":
                        self.map_array[x][y] = Biome(x, y, "W", "water", libtcod.Color(0, 0, 255), True, False)
                    elif temperature < 20 and humidity < 20:
                        self.map_array[x][y] = Biome(x, y, "_", "tundra", libtcod.Color(0, 100, 200), False, True)
                    elif temperature < 40 and humidity < 50:
                        self.map_array[x][y] = Biome(x, y, "^", "steppe", libtcod.Color(50, 50, 200), False, False)
                    elif temperature > 40 and humidity > 60:
                        self.map_array[x][y] = Biome(x, y, "!", "forest", libtcod.Color(0, 150, 50), False, True)
                    else:
                        self.map_array[x][y] = Biome(x, y, "*", "snow", libtcod.Color(255, 255, 255), False, False)

        if planet_type == "barren":

            elevation_array = Map.make_elevation(self, 7, elevation_array)
            #water_array = Map.make_water(self, 3, elevation_array)
            #tempr_array = Map.make_temp(self, water_array, tempr_array)
            #humidity_array = Map.make_humidity(self, water_array, humidity_array)
            self.map_array = elevation_array

            #self.map_array = Map.make_temp(self, 1000, elevation_array, tempr_array)

            for x in range(self.x):
                #print x
                for y in range(self.y):
                    #humidity = humidity_array[x][y] - 20
                    #temperature = tempr_array[x][y] - 70
                    #print y
                    #print self.map_array[x][y]
                    if self.map_array[x][y] > 30 and self.map_array[x][y] < 80:
                        self.map_array[x][y] = Biome(x, y, "m", "hills", libtcod.Color(100, 100, 100), False, True)
                    elif self.map_array[x][y] > 80 and self.map_array[x][y] < 200:
                        self.map_array[x][y] = Biome(x, y, "M", "mountain", libtcod.Color(200, 200, 200), True, True)
                    else:
                        self.map_array[x][y] = Biome(x, y, "-", "barren", libtcod.Color(255, 255, 255), False, False)

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
                    #print random_x
                    random_y = random_y + libtcod.random_get_int(0, -1, 1)
                    #print random_y
                    new_array[random_x][random_y] = "200"
                    #print new_array[random_x][random_y]
                    #print new_array
                    steps -= 1
            seeds -= 1
        return new_array

    def make_temp(self, elevation_array, tempr_array):
        center_y = self.y/2
        center_x = self.x/2
        #print "center y " + str(center_y)
        step = 100
        tempr_const = 5
        tempr = 0

        for y in range(self.y-1):
            for x in range(self.x-1):
                if y < center_y:
                    #print tempr
                    tempr = y * tempr_const
                    tempr_array[x][y] = tempr
                if y >= center_y:
                    #print tempr
                    tempr = (self.y - y) * tempr_const
                    tempr_array[x][y] = tempr
                if elevation_array[x][y] > 0 and elevation_array[x][y] < 200:
                    tempr -= elevation_array[x][y]
                    tempr_array[x][y] = tempr
                if elevation_array[x][y] == "200":
                    tempr -= 5
                    tempr_array[x][y] = tempr

            #smoothing
        for y in range(self.y-1):
            for x in range(self.x-1):
                point0 = tempr_array[x][y]
                point1 = tempr_array[x+1][y]
                if y < center_y:
                    if point0 != y:
                        point1 = (point0+point1)/2
                        tempr_array[x+1][y] = point1
                if y >= center_y:
                    if point0!= (self.y - y) * tempr_const:
                        point1 = (point0+point1)/2
                        tempr_array[x+1][y] = point1

        for y in range(self.y):
            for x in range(self.x):
                greatest = np.amax(tempr_array)
                least = np.amin(tempr_array)

                cal_greatest = abs(least) + greatest

                new_o = float(float(tempr_array[x, y] - least)/float(cal_greatest))*100

                print new_o

                tempr_array[x][y] = int(new_o)

        return tempr_array

    def make_humidity(self, elevation_array, humidity_array):
        # random_x = libtcod.random_get_int(0, 0, self.x-1)
        # random_y = libtcod.random_get_int(0, 0, self.y-1)
        #
        # seed = 2000
        #
        # humidity = 0
        # humidity1 = 0
        #
        # while seed > 0:
        #     if random_x > self.x-1 or random_y > self.y-1:
        #         break
        #     else:
        #         if elevation_array[random_x][random_y] > 0 and elevation_array[random_x][random_y] < 200:
        #             humidity += elevation_array[random_x][random_y]
        #             humidity1 -= elevation_array[random_x][random_y]
        #             humidity_array[random_x-1][random_y] = humidity
        #             humidity_array[random_x+1][random_y] = humidity1
        #         elif elevation_array[random_x][random_y] == "200":
        #             humidity += 40
        #             humidity_array[random_x][random_y] = humidity
        #         else:
        #             humidity -= 20
        #             humidity_array[random_x][random_y] = humidity
        #
        #         random_x += libtcod.random_get_int(0, -1, 1)
        #         random_y += libtcod.random_get_int(0, -1, 1)
        #         seed -= 1

        for y in range(self.y-1):
            humidity = 0
            humidity1 = 0
            for x in range(self.x-1):
                if elevation_array[x][y] > 0 and elevation_array[x][y] < 200:
                    humidity += elevation_array[x][y]
                    humidity1 -= elevation_array[x][y]
                    humidity_array[x-1][y] = humidity
                    humidity_array[x+1][y] = humidity1
                elif elevation_array[x][y] == "200":
                    humidity += 20
                    humidity = humidity
                else:
                    humidity -= 20
                    humidity = humidity

        for y in range(self.y-1):
            for x in range(self.x-1):
                point0 = humidity
                point1 = humidity_array[x+1][y]

                point1 = (point0+point1)/2
                humidity_array[x+1][y] = point1

        for y in range(self.y):
            for x in range(self.x):
                greatest = np.amax(humidity_array)
                least = np.amin(humidity_array)

                cal_greatest = abs(least) + greatest

                new_o = float(float(humidity_array[x, y] - least)/float(cal_greatest))*100

                humidity = int(new_o)

        return humidity_array

        # for y in range(self.y):
        #     for x in range(self.x):
        #         if y < center_y:
        #             print tempr
        #             tempr = y * tempr_const
        #             tempr_array[x][y] = tempr
        #         if y >= center_y:
        #             print tempr
        #             tempr = (self.y - y) * tempr_const
        #             tempr_array[x][y] = tempr
        #         if elevation_array[x][y] > 0 and elevation_array[x][y] < 200:
        #             tempr -= elevation_array[x][y]
        #             tempr_array[x][y] = tempr
        #             if x >= self.x-1 or y >= self.y-1 or x < -64 or y < -64:
        #                 x += libtcod.random_get_int(0, -1, 0)
        #                 y += libtcod.random_get_int(0, -1, 1)
        #             # else:
        #             #     x = x
        #             #     y = y
        #         if elevation_array[x][y] == "200":
        #             tempr -= 1
        #             tempr_array[x][y] = tempr

        #print tempr_array



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




