import swine
import swine.gui
import swine.shape

import kytten
import pyglet
from pyglet.window import key
from pyglet.window import mouse

window = swine.Window()
window.title("Test")

scene_one = swine.Scene(window)
scene_two = swine.Scene(window)

label_one = swine.gui.Label(scene_one, text="Hello World!", x=window.width // 2, y=window.height // 2, layer=2)
label_two = swine.gui.Label(scene_two, text="Bye World!", x=window.width // 2, y=window.height // 2)


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


anim_label = AnimatedLabel(scene_one, x=window.width // 2, y=window.height // 2 - 30)


class Pig(swine.Sprite):
    image = pyglet.image.load("swine/swine.png")
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

    def __init__(self):
        swine.Sprite.__init__(self, scene_one, Pig.image, 6, layer=1)
        self.x = self.window.width // 2
        self.y = self.window.height // 2

        self.scale_x = 1

    def update(self, dt=None):
        speed = dt * swine.Globals.FPS

        if self.keys[key.LSHIFT]:
            speed *= 2

        if self.keys[key.W]:
            # print("W")
            self.y += speed

        if self.keys[key.A]:
            # print("A")
            self.x -= speed
            self.scale_x = -1

        if self.keys[key.S]:
            # print("S")
            self.y -= speed

        if self.keys[key.D]:
            # print("D")
            self.x += speed
            self.scale_x = 1

    def key_press(self, symbol, modifiers):
        print(key.symbol_string(symbol))

    def mouse_press(self, x, y, button, modifiers):
        print(mouse.buttons_string(button))


pig = Pig()

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

window2 = swine.gui.Window(scene_one, "Window",
                           kytten.VerticalLayout([
                               kytten.Button("Click!", on_click=click)
                           ]), 50, -50)

right_click = ContextMenu(scene_one, ["One", "Two", "Three"])

window.mainloop()
