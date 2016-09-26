import libtcodpy as libtcod
import math

class Object:
    #this is a generic object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen.
    def __init__(self, x, y, char, name, color, blocks=False, always_visible=False):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocks = blocks
        self.always_visible = always_visible

    def move(self, dx, dy):
            self.x += dx
            self.y += dy

    def move_towards(self, target_x, target_y):
        #vector from this object to the target, and distance
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        #normalize it to length 1 (preserving direction), then round it and
        #convert to integer so the movement is restricted to the map grid
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy)

    def distance_to(self, other):
        #return the distance to another object
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def distance(self, x, y):
        #return the distance to some coordinates
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def draw(self, con):
        #only show if it's visible to the player; or it's set to "always visible" and on an explored tile
        # if (libtcod.map_is_in_fov(fov_map, self.x, self.y) or
        #         (self.always_visible and map[self.x][self.y].explored)):
            #set the color and then draw the character that represents this object at its position
        libtcod.console_set_default_foreground(con, self.color)
        libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

class Item(Object):
    def __init__(self, x, y, char, name, color, blocks, always_visible, effect, duration, aoe, message, use_self=False,
                 use_friend=False, use_foe=False):
        Object.__init__(self, x, y, char, name, color, blocks, always_visible)
        self.effect = effect
        self.duration = duration
        self. aoe = aoe
        self.message = message
        self.use_self = use_self
        self.use_friend = use_friend
        self.use_foe = use_foe

        #def enact_effect
        #def calculate_effect:
        # while < duration
        #   if_use_self = false
        #       if aoe < distance_to(friend, foe) return false
        #           else:
        #               enact_effect

class Equipment(Object):
    def __init__(self, x, y, char, name, color, blocks, always_visible, effect, stat_change, ship_eq, player_eq,
                 equipped=False):
        Object.__init__(self, x, y, char, name, color, blocks, always_visible)
        self.effect = effect
        self.stat_change = stat_change
        self.ship_eq = ship_eq
        self.player_eq = player_eq
        self.equipped = equipped

        #def enact_effect
        #def stat_delta
        #if ship_eq and equipped:
        #   enact_effect(Ship)
        #   stat_delta(Ship)
        #elif player_eq and equipped:
        #   enact_effect(Player)
        #   stat_delta(Player)

class Ship(Object):
    def __init__(self, x, y, char, name, color, blocks, always_visible, hp, sp, scope, speed):
        Object.__init__(self, x, y, char, name, color, blocks, always_visible)
        self. hp = hp
        self.sp = sp
        self.scope = scope
        self.speed = speed

class Player(Object):
    def __init__(self, x, y, char, name, color, blocks, always_visible, hp, xp, speed):
        Object.__init__(self, x, y, char, name, color, blocks, always_visible)
        self.hp = hp
        self.xp = xp
        self.speed = speed

class CelestialObject(Object):
    def __init__(self, x, y, char, name, color, blocks, always_visible, object_type, scope, size, resources, atmosphere,
                habitated, description):
        Object.__init__(self, x, y, char, name, color, blocks, always_visible)
        self.scope = scope
        self.object_type = object_type
        self.size= size
        self.resources = resources
        self.atmosphere = atmosphere
        self.habitated = habitated
        self.description = description

    def get_scope(self):
        return self.scope

    def get_resources(self):
        return self.resources

    def get_atmosphere(self):
        return self.atmosphere

    def get_habitated(self):
        return self.habitated

    def get_description(self):
        return self.description

    def draw(self, con):
        if self.size >= 1:
            for x in range(self.x, self.x+self.size):
                print str(self.size)
                for y in range(self.y, self.y+self.size):
                    libtcod.console_set_char_background(con, x, y, self.color, libtcod.BKGND_SET)


# class Star(CelestialObject):
#     def __init__(self, x, y, char, name, color, blocks, always_visible, scope, atmosphere, habitated,
#                  description, star_mass=8, resources=False):
#         CelestialObject.__init__(self, x, y, char, name, color, blocks, always_visible, scope, resources, atmosphere,
#                                   habitated, description)
#
# class Planet(CelestialObject):
#     def __init__(self, x, y, char, name, color, blocks, always_visible, scope, atmosphere, habitated,
#                  description, star_mass=8, resources=False):
#         CelestialObject.__init__(self, x, y, char, name, color, blocks, always_visible, scope, resources, atmosphere,
#                                   habitated, description)
#
# class Moon(CelestialObject):
#     def __init__(self, x, y, char, name, color, blocks, always_visible, scope, atmosphere, habitated,
#                  description, star_mass=8, resources=False):
#         CelestialObject.__init__(self, x, y, char, name, color, blocks, always_visible, scope, resources, atmosphere,
#                                   habitated, description)


#testing

