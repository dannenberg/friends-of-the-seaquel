import pygame
 
pygame.init()

if pygame.joystick.get_count():
    jst = pygame.joystick.Joystick(0)
    jst.init()
    print jst.get_name(), "connected"
else:
    print "No joystick connected!"

class XBoxComponent(pygame.Surface):
    def __init__(self, parent, x, y, w, h):
        super(XBoxComponent, self).__init__((w, h))
        self.parent = parent
        self.x = x
        self.y = y
        self.parent.dirty.append(self)

    def dirty(self):
        if self not in self.parent.dirty:
            self.parent.dirty.append(self)


class XBoxButton(XBoxComponent):
    def __init__(self, parent, (x, y), color, radius=15):
        super(XBoxButton, self).__init__(parent, x - radius, y - radius, radius * 2, radius * 2)
        self.radius = radius
        self.transparent = (0xFF, 0, 0xFF) if tuple(color) != (0xFF, 0, 0xFF) else (0, 0xFF, 0)
        self.set_colorkey(self.transparent)
        self.color = tuple(color)
        self.fill(self.transparent)
        self.down()
        self.up()

    def down(self):
        pygame.draw.circle(self, self.color, (self.radius, ) * 2, self.radius)
        self.dirty()

    def up(self):
        pygame.draw.circle(self, self.transparent, (self.radius, ) * 2, self.radius - 1)
        self.dirty()


class XBoxBumper(XBoxComponent):
    WIDTH = 66
    HEIGHT = 25
    COLOR = (0xBB, ) * 3
    TRANSPARENT = (0xFF, 0, 0xFF)

    def __init__(self, parent, (x, y)):
        super(XBoxBumper, self).__init__(parent, x, y, self.WIDTH, self.HEIGHT)
        self.set_colorkey(self.TRANSPARENT)
        self.fill(self.TRANSPARENT)
        self.down()
        self.up()

    def down(self):
        self.fill(self.COLOR)
        self.dirty()

    def up(self):
        self.fill(self.TRANSPARENT, (1, 1, self.WIDTH - 2, self.HEIGHT - 2))
        self.dirty()


class XBoxStick(XBoxComponent):
    STICK_DIST = 20
    NUB_SIZE = 30
    STICK_AREA = 40
    TRANSPARENT = (0xFF, 0, 0xFF)
    def __init__(self, parent, (x, y)):
        max_rad = max(self.STICK_DIST + self.NUB_SIZE, self.STICK_AREA)
        self.max_rad = max_rad
        super(XBoxStick, self).__init__(parent, x - max_rad, y - max_rad, max_rad * 2, max_rad * 2)
        self.set_colorkey(self.TRANSPARENT)
        self.position = [0, 0]
        self.up()

    def stick_pos(self):
        return (self.position[0] * self.STICK_DIST + self.max_rad, 
            self.position[1] * self.STICK_DIST + self.max_rad)

    def redraw(self):
        self.fill(self.TRANSPARENT)
        pygame.draw.circle(self, (0x22, ) * 3, (self.max_rad, ) * 2, self.STICK_AREA)
        pygame.draw.circle(self, self.color, self.stick_pos(), self.NUB_SIZE)
        self.dirty()

    def set(self, x=None, y=None):
        if x is not None:
            self.position[0] = x
        if y is not None:
            self.position[1] = y
        self.dirty()

    def down(self):
        self.color = (0xFF, 0, 0)
        self.redraw()

    def up(self):
        self.color = (0xCC, ) * 3
        self.redraw()


class XBoxController(pygame.Surface):
    def __init__(self):
        super(XBoxController, self).__init__((800, 600))
        self.dirty = []
        self.A = XBoxButton(self, (600, 250), (0, 0x88, 0x11))
        self.B = XBoxButton(self, (650, 200), (0x88, 0, 0))
        self.X = XBoxButton(self, (550, 200), (0, 0, 0x88))
        self.Y = XBoxButton(self, (600, 150), (0x88, 0x88, 0))
        self.LB = XBoxBumper(self, (150, 75))
        self.RB = XBoxBumper(self, (584, 75))
        self.select = XBoxButton(self, (330, 200), (0xBB, ) * 3, 10)
        self.start = XBoxButton(self, (470, 200), (0xBB, ) * 3, 10)
        self.LS = XBoxStick(self, (200, 200))
        self.RS = XBoxStick(self, (500, 350))

        self.button_list = [self.A, self.B, self.X, self.Y, self.LB, self.RB,
            self.select, self.start, self.LS, self.RS]

        pygame.draw.circle(self, (0x99, ) * 3, (400, 200), 30)
        pygame.draw.line(self, (0, 0xBB, 0), (370, 170), (430, 230), 3)
        pygame.draw.line(self, (0, 0xBB, 0), (370, 230), (430, 170), 3)

    def reblit(self, surf):
        if self.dirty:
            for d in self.dirty:
                self.fill((0, 0, 0), (d.x, d.y, d.get_width(), d.get_height()))
                self.blit(d, (d.x, d.y))
            self.dirty = []
        surf.blit(self, (0, 0))


class Main(object):
    def __init__(self):
        self.size = (800, 600)
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill((0, 0, 0))
        self.clock = pygame.time.Clock()
        self.done = False

        self.controller = XBoxController()

    def run(self):
        while not self.done:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.JOYAXISMOTION:
                    if event.axis == 0:  # ls l- r+
                        self.controller.LS.set(x=event.value)
                    elif event.axis == 1:  # ls u- d+
                        self.controller.LS.set(y=event.value)
                    elif self.axis == 2:  # triggers L+ R-
                        pass
                    elif self.axis == 3:  # RS U- D+
                        self.controller.RS.set(y=event.value)
                    elif self.axis == 4:  # RS l- r+
                        self.controller.RS.set(x=event.value)
                elif event.type == pygame.JOYHATMOTION:
                    # event.value = (amt right, amt up)
                    # print event.type
                    # print event
                    pass
                elif event.type == pygame.JOYBUTTONUP:
                    self.controller.button_list[event.button].up()
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.controller.button_list[event.button].down()
                else:
                    print event.type
                    print event
            self.controller.reblit(self.screen)
            pygame.display.flip()
        pygame.quit()

Main().run()