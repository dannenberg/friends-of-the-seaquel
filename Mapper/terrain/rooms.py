import random
import pygame

from terrain import Room
from ui.map_ui import RoomDS
from sprites.goblin import GoblinAI
from sprites.elemental import ElementalAI
from sprites.block import BlockAI
from sprites.door import DoorAI
from sprites.teleport import TeleportAI


class Grasslands(Room):
    TILESET = pygame.image.load("imgs/grasslands.png")
    def __init__(self, room):
        map_data, entities = self.generate_room(room)
        impassible = tuple((x, y) for x in xrange(6) for y in xrange(4)
            if (x, y) not in ((0, 0), (4, 3), (4, 2), (4, 0)))
        super(Grasslands, self).__init__(map_data, impassible, room, entities)
        self.entities.add(ElementalAI(
            (random.randint(1, room.w * Room.TPS - 10) * 50,
            random.randint(1, room.h * Room.TPS) * 50)))

    def generate_room(self, room):
        width = room.w * Room.TPS
        height = room.h * Room.TPS
        toR = [[(1, 0)] * width] + [
            [(1, 0)] + [(0, 0)] * (width - 2) + [(1, 0)]
            for _ in xrange(height - 2)] + [[(1, 0)] * width]

        toR[7][7] = (4, 0)

        for x, y, dr in room.paths_iter():
            if (room.x, room.y) == (0, 0):
                print x, y, dr
            x = int((x + .5) * Room.TPS)
            y = int((y + .5) * Room.TPS)
            if dr == 1:
                toR[0][x - 1] = (0, 0)
                toR[0][x] = (0, 0)
                toR[0][x + 1] = (0, 0)
            elif dr == 2:
                toR[y - 1][-1] = (0, 0)
                toR[y][-1] = (0, 0)
                toR[y + 1][-1] = (0, 0)
            elif dr == 4:
                toR[-1][x - 1] = (0, 0)
                toR[-1][x] = (0, 0)
                toR[-1][x + 1] = (0, 0)
            elif dr == 8:
                toR[y - 1][0] = (0, 0)
                toR[y][0] = (0, 0)
                toR[y + 1][0] = (0, 0)
        entities = self.build_house(toR)
        return toR, entities

    def build_house(self, toR):
        toR[1][-2] = (5, 1)
        toR[2][-2] = (5, 2)
        toR[3][-2] = (5, 3)

        toR[1][-3] = (4, 1)
        toR[2][-3] = (4, 2)
        toR[3][-3] = (4, 3)

        toR[1][-4] = (1, 1)
        toR[2][-4] = (1, 2)
        toR[3][-4] = (1, 3)

        toR[1][-5] = (0, 1)
        toR[2][-5] = (0, 2)
        toR[3][-5] = (0, 3)
        return [TeleportAI(
            map(lambda q: q * 50, (len(toR[0]) - 3, 2.5)),
            (50, 50))]


class Inside(Room):
    TILESET = pygame.image.load("imgs/inside.png")
    def __init__(self, room_toR, player_toR):
        self.room_toR = room_toR
        self.player_toR = player_toR
        room = RoomDS((0, 0), (1, 1))
        map_data = self.generate_room(room)
        impassible = ((0, 0), (1, 0), (3, 0), (0, 1), (3, 1), (0, 2), (2, 2), (3, 2))
        super(Inside, self).__init__(map_data, impassible, room)
        self.entities.add(GoblinAI((200, 50)))

    def generate_room(self, room):
        width = room.w * 12
        height = room.h * 9
        toR = [[(0, 0)] + [(1, 0)] * (width - 2) + [(3, 0)]] + [
            [(0, 1)] + [(1, 1)] * (width - 2) + [(3, 1)]
            for _ in xrange(height - 2)] + [
            [(0, 2), (1, 2)] + [(2, 2)] * (width - 3) + [(3, 2)]] + [
            [(2, 0), (2, 1)] + [(2, 0)] * (width - 2)]

        return toR


class Ocean(Room):
    TILESET = pygame.image.load("imgs/ocean.png")
    def __init__(self, room):
        map_data = self.generate_room(room)
        impassible = ((1, 0), )
        super(Ocean, self).__init__(map_data, impassible, room)

    def generate_room(self, room):
        width = room.w * Room.TPS
        height = room.h * Room.TPS
        toR = [[(1, 0)] * width] + [
            [(1, 0)] + [(0, 0)] * (width - 2) + [(1, 0)]
            for _ in xrange(height - 2)] + [[(1, 0)] * width]

        for x, y, dr in room.paths_iter():
            if (room.x, room.y) == (0, 0):
                print x, y, dr
            x = int((x + .5) * Room.TPS)
            y = int((y + .5) * Room.TPS)
            if dr == 1:
                toR[0][x - 1] = (0, 0)
                toR[0][x] = (0, 0)
                toR[0][x + 1] = (0, 0)
            elif dr == 2:
                toR[y - 1][-1] = (0, 0)
                toR[y][-1] = (0, 0)
                toR[y + 1][-1] = (0, 0)
            elif dr == 4:
                toR[-1][x - 1] = (0, 0)
                toR[-1][x] = (0, 0)
                toR[-1][x + 1] = (0, 0)
            elif dr == 8:
                toR[y - 1][0] = (0, 0)
                toR[y][0] = (0, 0)
                toR[y + 1][0] = (0, 0)
        return toR


class Dungeon(Room):
    TILESET = pygame.image.load("imgs/dungeon_blu.png")
    def __init__(self, room):
        map_data, entities = self.generate_room(room)
        impassible = tuple(((x, y) for x in xrange(9) for y in xrange(7)
            if (x, y) not in ((2, 1), )))
        super(Dungeon, self).__init__(map_data, impassible,
            room, entities)

    def generate_room(self, room):
        entities = set([BlockAI((300, 300))])
        width = room.w * Room.TPS
        height = room.h * Room.TPS

        wall_lookup = {Room.ALL & ~Room.DOWNRIGHT: (0, 0),
                       Room.ALL & ~Room.DOWNLEFT: (8, 0),
                       Room.ALL & ~Room.UPRIGHT: (0, 6),
                       Room.ALL & ~Room.UPLEFT: (8, 6),
                       Room.ALL & ~(Room.DOWNRIGHT | Room.RIGHT | Room.UPRIGHT): (0, 1),
                       Room.ALL & ~(Room.DOWNRIGHT | Room.DOWN | Room.DOWNLEFT): (2, 0),
                       Room.ALL & ~(Room.UPRIGHT | Room.UP | Room.UPLEFT): (1, 6),
                       Room.ALL & ~(Room.DOWNLEFT | Room.LEFT | Room.UPLEFT): (8, 1),
                       Room.ALL & ~(Room.DOWNRIGHT | Room.RIGHT): (0, 1),
                       Room.ALL & ~(Room.RIGHT | Room.UPRIGHT): (0, 1),
                       Room.ALL & ~(Room.DOWN | Room.DOWNLEFT): (2, 0),
                       Room.ALL & ~(Room.DOWN | Room.DOWNRIGHT): (2, 0),
                       Room.ALL & ~(Room.UPRIGHT | Room.UP): (1, 6),
                       Room.ALL & ~(Room.UP | Room.UPLEFT): (1, 6),
                       Room.ALL & ~(Room.DOWNLEFT | Room.LEFT): (8, 1),
                       Room.ALL & ~(Room.LEFT | Room.UPLEFT): (8, 1)}

        toR = ([[1] * width] +
            [[1] + [(2, 1)] * (width - 2) + [1] for _ in xrange(height - 2)] +
            [[1] * width])
        toR = self.convert_walls(toR, 1, wall_lookup)

        toR[1][1] = (1, 1)
        toR[0][1] = (1, 0)

        toR[1][-2] = (7, 1)
        toR[0][-2] = (7, 0)

        toR[-2][1] = (1, 1)
        toR[-3][1] = (1, 2)

        toR[-2][-2] = (7, 1)
        toR[-3][-2] = (7, 2)

        for x, y, dr in room.paths_iter():
            if (room.x, room.y) == (0, 0):
                print x, y, dr
            x = int((x + .5) * Room.TPS)
            y = int((y + .5) * Room.TPS)
            if dr == 1:
                toR[0][x - 1] = (3, 0)
                toR[0][x] = (2, 1)
                toR[0][x + 1] = (2, 1)
                toR[0][x + 2] = (6, 0)
                entities.add(DoorAI(map(lambda q: q * 50, (x, -1)), 0))
            elif dr == 2:
                toR[y - 1][-1] = (8, 2)
                toR[y][-1] = (2, 1)
                toR[y + 1][-1] = (2, 1)
                toR[y + 2][-1] = (8, 5)
                entities.add(DoorAI(map(lambda q: q * 50, (width - 1, y)), 3))
            elif dr == 4:
                toR[-1][x - 1] = (3, 6)
                toR[-1][x] = (2, 1)
                toR[-1][x + 1] = (2, 1)
                toR[-1][x + 2] = (6, 6)
                entities.add(DoorAI(map(lambda q: q * 50, (x, height - 1)), 1))
            elif dr == 8:
                toR[y - 1][0] = (0, 2)
                toR[y][0] = (2, 1)
                toR[y + 1][0] = (2, 1)
                toR[y + 2][0] = (0, 5)
                entities.add(DoorAI(map(lambda q: q * 50, (-1, y)), 2))

        return toR, entities


class DungeonMaze(Room):
    TILESET = pygame.image.load("imgs/dungeon_blu.png")
    def __init__(self, room):
        self.impassible = tuple(((x, y) for x in xrange(9) for y in xrange(7)
            if (x, y) not in ((2, 1), )))
        map_data, entities = self.generate_room(room)
        assert len(map_data) == room.h * Room.TPS,\
            str(len(map_data)) + " vs " + str(room.h * Room.TPS)
        assert len(map_data[0]) == room.w * Room.TPS,\
            str(len(map_data[0])) + " vs " + str(room.w * Room.TPS)
        super(DungeonMaze, self).__init__(map_data, self.impassible,
            room, entities)

    def generate_room(self, room):
        entities = set()
        width = room.w * Room.TPS
        height = room.h * Room.TPS

        wall_lookup = {Room.ALL & ~Room.DOWNRIGHT: (0, 0),
                       Room.ALL & ~Room.DOWNLEFT: (8, 0),
                       Room.ALL & ~Room.UPRIGHT: (0, 6),
                       Room.ALL & ~Room.UPLEFT: (8, 6),
                       Room.ALL & ~(Room.DOWNRIGHT | Room.RIGHT | Room.UPRIGHT): (0, 1),
                       Room.ALL & ~(Room.DOWNRIGHT | Room.DOWN | Room.DOWNLEFT): (2, 0),
                       Room.ALL & ~(Room.UPRIGHT | Room.UP | Room.UPLEFT): (1, 6),
                       Room.ALL & ~(Room.DOWNLEFT | Room.LEFT | Room.UPLEFT): (8, 1),
                       Room.ALL & ~(Room.DOWNRIGHT | Room.RIGHT): (0, 1),
                       Room.ALL & ~(Room.RIGHT | Room.UPRIGHT): (0, 1),
                       Room.ALL & ~(Room.DOWN | Room.DOWNLEFT): (2, 0),
                       Room.ALL & ~(Room.DOWN | Room.DOWNRIGHT): (2, 0),
                       Room.ALL & ~(Room.UPRIGHT | Room.UP): (1, 6),
                       Room.ALL & ~(Room.UP | Room.UPLEFT): (1, 6),
                       Room.ALL & ~(Room.DOWNLEFT | Room.LEFT): (8, 1),
                       Room.ALL & ~(Room.LEFT | Room.UPLEFT): (8, 1),
                       Room.DOWN | Room.RIGHT | Room.DOWNRIGHT: (6, 5),
                       Room.DOWN | Room.LEFT | Room.DOWNLEFT: (3, 5),
                       Room.UP | Room.RIGHT | Room.UPRIGHT: (6, 1),
                       Room.UP | Room.LEFT | Room.UPLEFT: (3, 1),
                       Room.ALL: (2, 2)}

        # toR = ([[1] * width] +
        #     [[1] + [(2, 1)] * (width - 2) + [1] for _ in xrange(height - 2)] +
        #     [[1] * width])

        w = width // 2 + 1  # +1 because we remove the edges
        h = height // 2 + 1
        #print w, h
        board = ([[1] * w] +
            [[1] + [2] * (w - 2) + [1] for _ in xrange(h - 2)] +
            [[1] * w])
        def dfs((x, y)):
            board[y][x] = 0
            next = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            random.shuffle(next)
            for ex, ey in next:
                if (board[y + ey][x + ex] == 2 and
                        board[y + ey * 2][x + ex * 2] == 2):
                    board[y + ey][x + ex] = 0
                    dfs((x + ex * 2, y + ey * 2))

        dfs((1, 1))

        toR = [[1] * width]
        for i, row in enumerate(board[1:-1]):
            toS = [1]
            for j, c in enumerate(row[1:-1]):
                if c == 0:
                    toS.append((2, 1))
                    toS.append((2, 1))
                    if j == w // 2 and width % 2:
                        toS.append((2, 1))
                else:
                    toS.append(1)
                    toS.append(1)
                    if j == w // 2 and width % 2:
                        toS.append(1)

            toS.append(1)
            toR.append(toS[:])
            toR.append(toS[:])
            if i == h // 2 and height % 2:
                toR.append(toS[:])
        toR.append([1] * width)

        for x, y, dr in room.paths_iter():
            if (room.x, room.y) == (0, 0):
                print x, y, dr
            x = int((x + .5) * Room.TPS)
            y = int((y + .5) * Room.TPS)
            if dr == 1:
                toR[0][x - 1] = (3, 0)
                toR[0][x] = (2, 1)
                toR[0][x + 1] = (2, 1)
                toR[0][x + 2] = (6, 0)
                toR[1][x] = (2, 1)
                toR[1][x + 1] = (2, 1)
                toR[2][x] = (2, 1)
                toR[2][x + 1] = (2, 1)
                toR[1][x - 1] = (2, 1)
                toR[1][x + 2] = (2, 1)
                toR[2][x - 1] = (2, 1)
                toR[2][x + 2] = (2, 1)
                entities.add(DoorAI(map(lambda q: q * 50, (x, -1)), 0))
            elif dr == 2:
                toR[y - 1][-1] = (8, 2)
                toR[y][-1] = (2, 1)
                toR[y + 1][-1] = (2, 1)
                toR[y + 2][-1] = (8, 5)
                toR[y][-2] = (2, 1)
                toR[y][-3] = (2, 1)
                toR[y + 1][-2] = (2, 1)
                toR[y + 1][-3] = (2, 1)
                toR[y - 1][-2] = (2, 1)
                toR[y - 1][-3] = (2, 1)
                toR[y + 2][-2] = (2, 1)
                toR[y + 2][-3] = (2, 1)
                entities.add(DoorAI(map(lambda q: q * 50, (width - 1, y)), 3))
            elif dr == 4:
                toR[-1][x - 1] = (3, 6)
                toR[-1][x] = (2, 1)
                toR[-1][x + 1] = (2, 1)
                toR[-1][x + 2] = (6, 6)
                toR[-2][x] = (2, 1)
                toR[-3][x] = (2, 1)
                toR[-2][x + 1] = (2, 1)
                toR[-3][x + 1] = (2, 1)
                toR[-2][x - 1] = (2, 1)
                toR[-3][x - 1] = (2, 1)
                toR[-2][x + 2] = (2, 1)
                toR[-3][x + 2] = (2, 1)
                entities.add(DoorAI(map(lambda q: q * 50, (x, height - 1)), 1))
            elif dr == 8:
                toR[y - 1][0] = (0, 2)
                toR[y][0] = (2, 1)
                toR[y + 1][0] = (2, 1)
                toR[y + 2][0] = (0, 5)
                toR[y][1] = (2, 1)
                toR[y][2] = (2, 1)
                toR[y + 1][1] = (2, 1)
                toR[y + 1][2] = (2, 1)
                toR[y - 1][1] = (2, 1)
                toR[y - 1][2] = (2, 1)
                toR[y + 2][1] = (2, 1)
                toR[y + 2][2] = (2, 1)
                entities.add(DoorAI(map(lambda q: q * 50, (-1, y)), 2))

        toR = self.convert_walls(toR, 1, wall_lookup, self.impassible)
        return toR, entities


class TestRoom(Room):
    TILESET = pygame.image.load("imgs/test.png")
    def __init__(self, room):
        impassible = set()
        if isinstance(room, RoomDS):
            map_data, entities = self.generate_room(room)
        else:
            map_data, entities = room, set()
        super(TestRoom, self).__init__(map_data, impassible,
            room, entities)

    def generate_room(self, room):
        return ([(random.randint(0, 3), random.randint(0, 3))
            for x in xrange(room.w * Room.TPS)
            for y in xrange(room.h * Room.TPS)], set())


ALL_ROOM_TYPES = [Grasslands, Inside, Ocean, Dungeon, TestRoom, DungeonMaze]
assert(len(ALL_ROOM_TYPES) < 256)  # the way we save rooms currently does not allow for this
