import swine
import swine.gui
import swine.shape
import swine.physics

import kytten
import pyglet
from pyglet.window import key
from pyglet.window import mouse
import pymunk

window = swine.Window()
window.title("Test")

scene_one = swine.Scene(window, gravity=pymunk.Vec2d(0, -900), drag=0.1)
# scene_two = swine.Scene(window)

# label_one = swine.gui.Label(scene_one, text="Hello World!", x=window.width // 2, y=window.height // 2, layer=2)
# label_two = swine.gui.Label(scene_two, text="Bye World!", x=window.width // 2, y=window.height // 2)


class FPSLabel(swine.gui.Label):
    def update(self, dt=None):
        self.text = str(round(pyglet.clock.get_fps(), 1))


fps = FPSLabel(scene_one, x=10, y=10)


class AnimatedLabel(swine.gui.Label):
    def __init__(self, scene, x, y):
        swine.gui.Label.__init__(self, scene, text="", x=x, y=y, layer=0)
        self.frames = ["[+---------]", "[-+--------]", "[--+-------]", "[---+------]", "[----+-----]", "[-----+----]", "[------+---]", "[-------+--]", "[--------+-]", "[---------+]"]

        self.current = 0

    def update(self, dt=None):
        if self.current < len(self.frames) - 1:
            self.current += 1

        else:
            self.current = 0

        self.text = self.frames[self.current]


# anim_label = AnimatedLabel(scene_one, x=window.width // 2, y=window.height // 2 - 30)


class Pig(swine.physics.PhysicsSprite):
    image = pyglet.image.load("swine/swine.png")
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

    def __init__(self):
        swine.physics.PhysicsSprite.__init__(self, scene_one, Pig.image, y=100, scale=6, layer=1)
        # self.x = self.window.width // 2
        # self.y = self.window.height // 2
        # self.body.position = self.window.width // 2, self.window.height // 2
        self.shape.elasticity = 0.5

        self.scale_x = 1

        self.is_grounded = False

        self.count_flip = False
        self.flip_counter = 60
        self.is_flipping = False
        self.flip_direction = None

    def update(self, dt=None):
        speed = 300  # dt * swine.Globals.FPS

        force = pymunk.Vec2d(0, 0)

        if self.keys[key.LSHIFT]:
            speed *= 2

        if self.keys[key.A]:
            # print("A")
            # self.body.force = pymunk.Vec2d(-speed, 0)
            force.x = -speed
            self.scale_x = -1

        if self.keys[key.D]:
            # print("D")
            # self.body.force = pymunk.Vec2d(speed, 0)
            force.x = speed
            self.scale_x = 1

        if self.keys[key.SPACE]:
            # print("W")
            # self.body.force = pymunk.Vec2d(0, 4000)
            if self.is_grounded:
                self.body.velocity = pymunk.Vec2d(force.x, speed)

        self.body.force = force

        if -4 < self.body.angle < -3 or 4 > self.body.angle > 3:
            # print("The pig has been flipped!")
            self.count_flip = True
            self.is_grounded = False

        else:
            self.count_flip = False
            self.flip_counter = 60
            self.flip_direction = None

        if self.count_flip:
            self.flip_counter -= 1

        if self.flip_counter <= 0:
            self.count_flip = False
            self.flip_counter = 60

            self.body.velocity = pymunk.Vec2d(0, speed * 4)

            self.is_flipping = True

        if self.is_flipping:
            if self.body.angle < 0:
                self.body.angle += 0.05

            elif self.body.angle > 0:
                self.body.angle -= 0.05

    def collision_enter(self, collider):
        self.is_grounded = True

        self.is_flipping = False

    def collision_exit(self, collider):
        self.is_grounded = False

    # def key_press(self, symbol, modifiers):
    #     print(key.symbol_string(symbol))
    #
    # def mouse_press(self, x, y, button, modifiers):
    #     print(mouse.buttons_string(button))


pig = Pig()

# box = pymunk.Segment(scene_one.space.static_body, (0, 80), (window.width, 80), 3)
# box.friction = 0.5
# box.elasticity = 0.8
# scene_one.space.add(box)

box = swine.physics.PhysicsShape(scene_one, swine.shape.Line(scene_one, 10, 700, colours=swine.RED), 0, -200, static=True)
box.shape.friction = 0.5
box.shape.elasticity = 0.8

box = pymunk.Segment(scene_one.space.static_body, (500, 10), (600, 400), 3)
box.friction = 0.5
box.elasticity = 0.8
scene_one.space.add(box)

box = pymunk.Segment(scene_one.space.static_body, (100, 10), (10, 400), 3)
box.friction = 0.5
box.elasticity = 0.8
scene_one.space.add(box)

# line = swine.shape.Line(scene_one, 100, 5, 100, 50, 0, [swine.RED])
# rect = swine.shape.Rectangle(scene_one, 100, 50, True, 50, 50, 0, swine.GREEN)
# squ = swine.shape.Square(scene_one, 50, True, 25, 20, 0, [swine.BLUE, swine.RED])
# tri = swine.shape.Triangle(scene_one, 50, 70, "center", False, 20, 120, 0, [swine.RED, swine.GREEN, swine.BLUE])
# par = swine.shape.Parallelogram(scene_one, 70, 50, 10, "right", True, 200, 50, 0, [swine.BLUE])
# cir = swine.shape.Circle(scene_one, 50, 25, False, 180, 180, 0, [swine.RED, swine.BLUE, swine.GREEN, swine.BLUE, swine.RED] * (25 // 5))
# ell = swine.shape.Ellipse(scene_one, 50, 25, 25, True, 125, 150, 0, swine.GREEN)
# tra = swine.shape.Trapezoid(scene_one, 70, 50, 25, "out", True, 70, 200, 0, swine.RED)
# rho = swine.shape.Rhombus(scene_one, 50, 100, True, 50, 250, 0, swine.GREEN)
# pen = swine.shape.Pentagon(scene_one, 50, 50, True, 125, 280, 0, swine.RED)


class ContextMenu(swine.GameObject):
    def __init__(self, scene, options):
        swine.GameObject.__init__(self, scene)
        self.scene = scene
        self.options = options

        self.menu = None
        self.is_open = False

    def mouse_press(self, x, y, button, modifiers):
        if button == 4:
            self.remove()
            if self.is_open:
                self.mouse_press(x, y, button, modifiers)

            else:
                pos = self.window.mouse_position()
                self.menu = swine.gui.Menu(self.scene, self.options, command=self.select, x=pos[0] + 20, y=pos[1] - 30)
                self.is_open = True

        elif button == 1:
            self.remove()

    def select(self, event=None):
        print(event)
        self.remove()

    def remove(self):
        if self.is_open:
            self.menu.teardown()
            self.is_open = False
            self.menu = None


def click(event=None):
    print("Click!")


# button = swine.gui.Button(scene_one, "Click!", command=click, x=50)
# checkbox = swine.gui.Checkbox(scene_one, "Check", x=-50, y=50)
# input_ = swine.gui.Input(scene_one, "Entry", x=70, y=50)
# slider = swine.gui.Slider(scene_one, y=-70)
# dropdown = swine.gui.Dropdown(scene_one, ["One", "Two", "Three"], x=-60, y=-20)

# window2 = swine.gui.Window(scene_one, "Window",
#                            kytten.VerticalLayout([
#                                kytten.Button("Click!", on_click=click)
#                            ]), 50, -50)

# right_click = ContextMenu(scene_one, ["One", "Two", "Three"])

# physics = swine.PhysicsObject(scene_one, 0)
# physics_sprite = swine.PhysicsSprite(scene_one, pyglet.image.load("swine/swine.png"))

# shape = swine.shape.Circle(scene_one, 30, 25, colours=swine.RED)
# physics_shape = swine.physics.PhysicsShape(scene_one, shape, 70)
# physics_shape.shape.friction = 0.5
# physics_shape.shape.elasticity = 0.8

# physics_square = swine.physics.PhysicsShape(scene_one, swine.shape.Square(scene_one, 50, colours=[swine.RED, swine.BLUE]))
# physics_square.shape.friction = 0.5
# physics_square.shape.elasticity = 0.8


# window.benchmark(time=10)

window.mainloop()
