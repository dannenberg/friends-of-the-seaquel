import pygame


class Tile(object):
    def __init__(self):
        pass

class SpriteList(object):
    def __init__(self, entities=[], **kwargs):
        self.default_layer = 0
        if "default_layer" in kwargs:
            self.default_layer = kwargs["default_layer"]

        self._entities = []  # kept as a sorted dict: [(layer, [elements])]
        for x in entities:
            self.add(x)

    def add(self, sprite, layer=None):
        if layer is None:  # layer > sprite_layer > default layer
            layer = self.default_layer
            if "layer" in sprite.__dict__:
                layer = sprite.layer
        sprite.layer = layer

        exists, ind = self.index(layer)
        if not exists:
            self._entities.insert(ind, (layer, []))
        self._entities[ind][1].append(sprite)

    def index(self, layer):
        top = 0
        bot = len(self._entities)

        while top < bot:
            mid = (bot - top) // 2 + top
            mid_layer = self._entities[mid][0]
            if mid_layer < layer:  # go lower
                top = mid + 1
            elif mid_layer > layer: # go higher
                bot = mid
            else:
                return (True, mid)
        return (False, bot)

    def __iter__(self):
        for _, layer in self._entities:
            for x in layer:
                yield x

    def discard(self, sprite):
        exists, ind = self.index(sprite.layer)
        if not exists:
            return False
        for i, x in enumerate(self._entities[ind][1]):
            if x is sprite:
                del self._entities[ind][1][i]
                return True
        return False


class Room(object):
    TPS = 16  # Tiles per Square
    UP, UPRIGHT, RIGHT, DOWNRIGHT, DOWN, DOWNLEFT, LEFT, UPLEFT, ALL = (
        2 ** x for x in xrange(9))
    ALL -= 1

    def __init__(self, map_data, impassible, roomds, entities=[]):
        self.map = [d[:] for d in map_data]
        self.tile_map = self.__class__.TILESET
        self.surface = pygame.Surface(
            map(self.resize, (len(self.map[0]), len(self.map))))
        self.impassible = impassible
        self.roomds = roomds
        self._entities = SpriteList(entities)
        self.transitions = {}
        self.redraw()

    entities = property(lambda self: self._entities)  # prevents magic: feel free to remove when all magic has been eliminated
    pos = property(lambda self: (self.roomds.x, self.roomds.y))
    x = property(lambda self: self.roomds.x)
    y = property(lambda self: self.roomds.y)
    w = property(lambda self: self.roomds.w)
    h = property(lambda self: self.roomds.h)

    def __contains__(self, (x, y)):
        return (0 <= x - self.x < self.w) and (0 <= y - self.y < self.h)

    def convert_walls(self, room, wall, wall_lookup, alsowall=[]):
        alsowall = list(alsowall) + [wall]
        def anonaway(e, (x, y)):
            if e != wall:
                return e
            val = 0
            for i, (ax, ay) in enumerate(((0, -1), (1, -1), (1, 0), (1, 1),
                    (0, 1), (-1, 1), (-1, 0), (-1, -1))):
                ax += x
                ay += y
                if (not (0 <= ay < len(room) and 0 <= ax < len(room[ay])) or
                        room[ay][ax] in alsowall):
                    val |= 2 ** i
            return wall_lookup[val]  # wall_lookup.get(val, (1, 1))
        return [[anonaway(e, (x, y)) for x, e in enumerate(row)]
            for y, row in enumerate(room)]

    @staticmethod
    def resize(x):
        return 50 * x

    def is_impassible_at(self, **kwargs):
        # if a mix of pixel and tile is given, sum them
        px, py = kwargs["pixel"] if ("pixel" in kwargs) else (0, 0)
        tx, ty = kwargs["tile"] if ("tile" in kwargs) else (0, 0)

        return self.get_at((px // 50 + tx, py // 50 + ty)) in self.impassible

    def get_at(self, (x, y)):
        """ In terms of character tile position from the top left of this room """
        if 0 <= y < len(self.map) and 0 <= x < len(self.map[int(y)]):
            return self.map[int(y)][int(x)]
        return None

    def get_abs(self, (x, y)):
        """ In terms of character tile position from the top left room """
        return self.get_at((x - self.x * Room.TPS, y - self.y * Room.TPS))

    def reblit(self, surf, time_passed, (vx, vy), (tlrx, tlry), draw_hitboxes=False):
        pos = (vx - (self.x - tlrx) * 50 * Room.TPS,
               vy - (self.y - tlry) * 50 * Room.TPS)
        surf.blit(self.surface, map(lambda q: -q, pos))
        for e in self.entities:
            e.act()
            e.reblit(surf, time_passed, pos, draw_hitboxes)

    def redraw(self):
        for y, row in enumerate(self.map):
            for x, elem in enumerate(row):
                self.surface.blit(self.tile_map,
                    map(self.resize, (x, y)),
                    (map(self.resize, elem), map(self.resize, (1, 1))))

    def __repr__(self):
        return "Room: " + str(self.x) + ", " + str(self.y)
