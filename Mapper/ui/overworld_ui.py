import pygame

import ui
from ui.map_ui import MapUI
from ui.panels import UsersInfoPanel
from terrain import Room
from terrain.rooms import *
from sprites.slime import SlimeAI
from sprites.goblin import GoblinAI
from sprites.elemental import ElementalAI
from sprites.door import DoorAI

SCREEN_SIZE = (600, 450)


class GameplayUI(ui.UI):
    def __init__(self, main, parent):
        super(GameplayUI, self).__init__(main, parent)
        self.slime = SlimeAI((50, 50))

        self.terrain = []
        self.load_rooms_around((25, 25))
        self.ui = []

        self.draw_hitboxes = False

        self.redraw()

    def load_rooms_around(self, (px, py)):
        (rx, ry), (w, h) = self.main.map.get_at((px, py)).get_rect()
        for x, y in self.main.map.surround_iter((rx, ry), (w, h)):
            self.load_room((x, y))
        try:
            self.room_data.entities.discard(self.slime)
        except AttributeError:
            pass
        self.room_data = self.load_room((rx, ry))
        self.room_data.entities.add(self.slime)

    def load_room(self, (x, y)):
        room = self.main.map.get_at((x, y))
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
            room_obj = Dungeon(room)
        else:
            room_obj = Ocean(room)
        self.terrain.append(room_obj)
        self.terrain = self.terrain[-16:]  # limit the list to 16 elements
        return room_obj

    def redraw(self):
        pass

    def reblit(self, surf, time_passed):
        super(GameplayUI, self).reblit(surf, time_passed)
        #center = self.slime.centerx - 300, self.slime.centery - 225
        #for t in self.terrain:
        #    t.reblit(surf, time_passed, center, self.room_data.pos)
        #for u in self.ui:
        #    u.reblit(surf)

    def handle_key(self, event):
        if event.key == pygame.K_m:
            self.main.ui_push(MapUI)
        if event.key == pygame.K_TAB:
            self.ui.append(UsersInfoPanel())
        if event.key == pygame.K_o:
            for x in self.room_data.entities:
                if x.animations.name == "opened":
                    x.close()
                elif x.animations.name == "closed":
                    x.open()
        if event.key == pygame.K_h:
            self.draw_hitboxes ^= True

    def handle_key_up(self, event):
        if event.key == pygame.K_TAB:
            self.ui = []  # TODO: NO NO NO NO NO

    def update(self):
        """ Not used by Server, only locally """
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
            ret = self.move_player(self.room_data, xoff, yoff)
            if ret == "room":
                self.room_data.entities.discard(self.slime)
                self.room_data = Inside(self.room_data.pos, self.slime.pos)
                self.room_data.entities.add(self.slime)
                self.terrain = [self.room_data]
                self.slime.pos = (50, 360)
                return
            elif ret == "out":
                self.slime.pos = self.room_data.player_toR
                self.load_rooms_around(self.room_data.room_toR)

            newx = int(self.slime.centerx // (Room.TPS * 50))
            newy = int(self.slime.centery // (Room.TPS * 50))
            if not (0 <= newx < self.room_data.w and
                    0 <= newy < self.room_data.h):
                x, y = self.room_data.pos  # keep the current room's position
                self.load_rooms_around((newx + self.room_data.x,
                        newy + self.room_data.y))
                # readjust for the new room
                self.slime.x += (x - self.room_data.x) * Room.TPS * 50
                self.slime.y += (y - self.room_data.y) * Room.TPS * 50
        elif self.slime.animations.name[1] != "idle":
            self.slime.animations.cur_animation = (
                self.slime.animations.name[0], "idle")

    def tile_coords(self, (x, y)):
        return map(lambda q: q // 50, (x, y))

    def move_player(self, room, xoff=0, yoff=0):
        dirc = (["upleft", "up", "upright", "left", "", "right",
                "downleft", "down", "downright"][xoff + yoff * 3 + 4], "")
        slime = self.slime
        if dirc != slime.animations.name:
            slime.animations.set_animation(dirc)
        mult = slime.diag if xoff and yoff else slime.speed
        hittin = None
        if xoff < 0:
            hittin = room.get_at(self.tile_coords((slime.left + xoff * mult, slime.centery)))
        elif xoff > 0:
            hittin = room.get_at(self.tile_coords((slime.right + xoff * mult, slime.centery)))

        if hittin in room.impassible:
            xoff = 0


        hittin = None
        if yoff < 0:
            hittin = room.get_at(self.tile_coords((slime.centerx, slime.top + yoff * mult)))
        elif yoff > 0:
            hittin = room.get_at(self.tile_coords((slime.centerx, slime.bottom + yoff * mult)))

        if hittin in room.impassible:
            yoff = 0

        if hittin in room.transitions:
            return room.transitions[hittin]

        slime.x += xoff * mult
        slime.y += yoff * mult

        for e in self.room_data.entities:
            if e is not slime and slime.hitbox.intersects(e.hitbox):
                slime.x -= xoff * mult
                slime.y -= yoff * mult
                break


class OverworldUI(GameplayUI):
    def reblit(self, surf, time_passed):
        super(OverworldUI, self).reblit(surf, time_passed)
        center = self.slime.centerx - 300, self.slime.centery - 225
        center = map(int, center)
        for t in self.terrain:
            t.reblit(surf, time_passed, center, self.room_data.pos, self.draw_hitboxes)
        for u in self.ui:
            u.reblit(surf)


class DungeonUI(GameplayUI):
    def reblit(self, surf, time_passed):
        super(DungeonUI, self).reblit(surf, time_passed)
        center = self.slime.centerx - 300, self.slime.centery - 225
        center = map(int, center)
        #center = min(max(center[0], 0), Room.TPS * 50 * self.room_data.w - 600),\
        #         min(max(center[1], 0), Room.TPS * 50 * self.room_data.h - 450)
        self.room_data.reblit(surf, time_passed, center, self.room_data.pos, self.draw_hitboxes)
        for u in self.ui:
            u.reblit(surf)
