import pygame
import threading

import ui
from ui.map_ui import MapUI
from ui.panels import UsersInfoPanel
from terrain import Room
from terrain.rooms import *
from sprites.slime import SlimeAI
from sprites.goblin import GoblinAI
from sprites.elemental import ElementalAI

SCREEN_SIZE = (600, 450)


class GetRooms(threading.Thread):
    def __init__(self, ui, (x, y)):
        threading.Thread.__init__(self)
        self.ui = ui
        self.loc = x, y

    def run(self):
        return self.load_rooms_around(self.loc)

    def load_rooms_around(self, (px, py)):
        # lockme
        self.terrain = self.ui.terrain[:]
        # unlockme

        (rx, ry), (w, h) = self.ui.main.map.get_at((px, py)).get_rect()
        for x, y in self.ui.main.map.surround_iter((rx, ry), (w, h)):
            self.load_room((x, y))

        cur_room = self.load_room((rx, ry))
        cur_room.entities.add(self.ui.slime)
        if self.ui.room_data is None:
            self.ui.room_data = cur_room
        self.ui.terrain = self.terrain
        print "Done"
        return cur_room

        #try:
        #    self.room_data.entities.discard(self.ui.slime)
        #except AttributeError:
        #    pass
        #self.room_data.entities.add(self.ui.slime)

    def load_room(self, (x, y)):
        room = self.ui.main.map.get_at((x, y))
        if room is None:
            print "Could not load room at (", x, ", ", y, ")"
            return False
        (x, y), (w, h) = room.get_rect()

        for i, item in enumerate(self.terrain):
            if (x, y) == (item.x, item.y):
                del self.terrain[i]
                self.terrain.append(item)
                return item

        if (x - 25) ** 2 + (y - 25) ** 2 < 625:
            room_obj = Grasslands(room)
        else:
            room_obj = Ocean(room)
        self.terrain.append(room_obj)
        self.terrain = self.terrain[-16:]  # limit the list to 16 elements
        return room_obj


class OverworldUI(ui.UI):
    def __init__(self, main, parent):
        super(OverworldUI, self).__init__(main, parent)
        self.slime = SlimeAI((50, 50))
        self.room_data = None

        self.terrain = []
        self.load_rooms_around((25, 25))
        self.ui = []

        self.redraw()

    def load_rooms_around(self, (px, py)):
        """
        if self.room_data is None:
            #self.room_data.entities.discard(self.slime)
            return GetRooms(self, (px, py)).run()

        room = None
        for room in self.terrain:
            if (px, py) in room:
                toR = room
                break

        GetRooms(self, (px, py)).start()
        return toR"""

    def redraw(self):
        pass

    def reblit(self, surf, time_passed):
        super(OverworldUI, self).reblit(surf, time_passed)
        center = self.slime.centerx - 300, self.slime.centery - 225
        if self.room_data is not None:
            for t in self.terrain:
                t.reblit(surf, time_passed, center, self.room_data.pos)
        for u in self.ui:
            u.reblit(surf)

    def handle_key(self, event):
        if event.key == pygame.K_m:
            self.main.ui_push(MapUI)
        if event.key == pygame.K_TAB:
            self.ui.append(UsersInfoPanel())

    def handle_key_up(self, event):
        if event.key == pygame.K_TAB:
            self.ui = []  # TODO: NO NO NO NO NO

    def update(self):
        xoff, yoff = 0, 0
        if self.main.keys & set((pygame.K_a, pygame.K_LEFT)):
            xoff -= 1
        if self.main.keys & set((pygame.K_d, pygame.K_RIGHT)):
            xoff += 1
        if self.main.keys & set((pygame.K_w, pygame.K_UP)):
            yoff -= 1
        if self.main.keys & set((pygame.K_s, pygame.K_DOWN)):
            yoff += 1
        if not (xoff == yoff == 0):  # there is movement
            self.main.client.send("MOVE", xoff, yoff)
            return
            ret = self.slime.move(self.room_data, xoff, yoff)
            if ret == "room":
                self.room_data.entities.discard(self.slime)
                self.room_data = Inside(self.room_data.pos, self.slime.pos)
                self.room_data.entities.add(self.slime)
                self.terrain = [self.room_data]
                self.slime.pos = (50, 360)
                return
            elif ret == "out":
                self.slime.pos = self.room_data.player_toR
                pos = self.room_data.room_toR
                self.room_data = None
                self.load_rooms_around(pos)
                return

            newx = int(self.slime.centerx // (Room.TPS * 50))
            newy = int(self.slime.centery // (Room.TPS * 50))
            if not (0 <= newx < self.room_data.w and
                    0 <= newy < self.room_data.h):
                x, y = self.room_data.pos  # keep the current room's position
                self.room_data.entities.discard(self.slime)
                self.room_data = self.load_rooms_around((newx + self.room_data.x,
                        newy + self.room_data.y))
                self.room_data.entities.add(self.slime)
                # readjust for the new room
                self.slime.x += (x - self.room_data.x) * Room.TPS * 50
                self.slime.y += (y - self.room_data.y) * Room.TPS * 50
        elif self.slime.animations.name[1] != "idle":
            self.slime.animations.cur_animation = (
                self.slime.animations.name[0], "idle")
