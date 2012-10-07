import struct
import os

from ui.map_ui import MapUI, MapDS
from mapper import Main
from terrain.rooms import ALL_ROOM_TYPES

world_name = "TestWorld"
url = os.path.join("..", "saves", world_name, "")
room_url = lambda x, y: ''.join(url, "room_data", os.sep, "r.", str(x), ".", str(y), ".dat")

def load_roomlayout():
    md = MapDS()  # empty landingpad
    with open(url + "room_layout.dat", "rb") as f:
        byte = f.read(1)
        data = []
        #count = 0
        while byte:
            data.append(struct.unpack('B', byte)[0])
            if len(data) == 4:
                md.add_room(data[:2], data[2:])
                data = []
            byte = f.read(1)
    return md

def save_roomlayout(mds):
    with open(url + "room_layout.dat", "wb") as f:
        for room in mds.all_rooms:
            for num in (room.x, room.y, room.w, room.h):
                f.write(struct.pack('B', num))

def save_room(room):
    (x, y), (w, h) = room.roomds.get_rect()
    with open(room_url(x, y), "wb") as f:
        f.write(struct.pack('B', ALL_ROOM_TYPES.index(room.__class__)))  # The type of room
        for row in room.map:  # do not encode hints for room size
            for tileset_x, tileset_y in row:
                f.write(struct.pack('B', tileset_x))
                f.write(struct.pack('B', tileset_y))

def load_room((rx, ry)):
    room_size = md.get_at((rx, ry))
    (x, y), (w, h) = room_size.get_rect()
    with open(room_url(x, y), "rb") as f:
        byte = f.read(1)
        room_type = ALL_ROOM_TYPES[byte]
        map_data = []
        for row in xrange(h):
            map_data.append([])
            for col in xrange(w):
                byte1 = struct.unpack('B', f.read(1))[0]
                byte2 = struct.unpack('B', f.read(1))[0]
                map_data[-1].append((byte1, byte2))
    return room_type((map_data, set()))

if __name__ == "__main__":
    print "'l' to test loading a room\n's' to test saving a room"
    do = raw_input(">")
    if do == "s":
        md = MapDS()
        md.expand_room()
        save_roomlayout(md)
    elif do == "l":
        md = load_roomlayout()
    else:
        exit()
    main = Main()
    main.map = md
    main.run()
