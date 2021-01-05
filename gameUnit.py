'''An independent game process class'''

from tkinter import Canvas, PhotoImage
import random
from objects import UserCharacter, Tree, Fence, Pinball


class GameUnit:
    '''An independent game unit with a canvas'''

    def __init__(self, window, x, y, cv_w, cv_h, background, race, keybind):
        '''Initialize a game unit. Put canvas with background
        and generate the character.'''
        self.window = window
        self.x = x
        self.y = y
        self.cv_w = cv_w
        self.cv_h = cv_h
        self.keybind = keybind

        # draw frames on the canvas
        self.cv = Canvas(
            self.window,
            width=self.cv_w,
            height=self.cv_h,
            cursor='circle',
            highlightthickness=0)

        self.bg_img = background
        self.draw_background()

        self.objects = []  # store all objects on the canvas

        # user character object
        main_character = UserCharacter(
            self.cv, self.cv_w, self.cv_h, 200, self.cv_h - 60, race)
        self.objects.append(main_character)

        self.cv.place(x=self.x, y=self.y)

        # to control the number of barriers
        self.last_add = 100

    def enable_key_bind(self, flag):
        '''enable key bind when flag is True, otherwise disable'''
        if flag:
            # press correspondent key to jump
            self.bind_func = self.window.bind(
                self.keybind, lambda x: self.objects[0].jump())
        else:
            self.window.unbind(self.keybind, self.bind_func)

    def draw_background(self):
        '''draw background image of canvas'''
        '''background images were downloaded from
        (https://www.kenney.nl/assets/background-elements-redux)'''
        if self.cv_w == 1600 and self.cv_h == 900:
            self.image_bg = PhotoImage(
                file='images/backgrounds/' + self.bg_img + '_HD.png')
            self.cv.create_image(0, 0, image=self.image_bg, anchor='nw')
        elif self.cv_w == 1600 and self.cv_h == 450:
            self.image_bg = PhotoImage(
                file='images/backgrounds/' + self.bg_img + '.png')
            self.cv.create_image(0, 0, image=self.image_bg, anchor='nw')
            self.cv.create_image(800, 0, image=self.image_bg, anchor='nw')

    def unit_loop(self, gradient):
        '''game unit loop of the single canvas to refresh objects and frame.
        return True if collision is detected'''
        self.add_barrier(gradient)

        retain_objects = []
        # calculate next position
        for obj in self.objects:
            obj.to_next()
            if obj.x >= -obj.width:
                retain_objects.append(obj)
            else:
                obj.clear()
        # retain valid objects
        self.objects = retain_objects

        # draw objects
        for obj in self.objects:
            obj.draw()
        # detect collision
        for obj in self.objects[1:]:
            if obj.collision_detect(self.objects[0]):
                return True
        return False

    def add_barrier(self, gradient):
        '''Add barrier on the road, the number and speed will
        increase according to difficulty gradient'''
        # use last_add to limit minimum spacing
        self.last_add += 1
        if self.last_add > 80 - gradient * 3 and \
                random.randint(0, int(100 - gradient * 2)) == 0:
            fence = Fence(self.cv, self.cv_w, self.cv_h)
            fence.x_speed += gradient
            self.objects.append(fence)
            self.last_add = 0
        elif self.last_add > 80 - gradient * 3 and \
                random.randint(0, int(120 - gradient * 2)) == 0:
            tree = Tree(self.cv, self.cv_w, self.cv_h)
            tree.x_speed += gradient
            self.objects.append(tree)
            self.last_add = 0
        elif gradient >= 0.5 and self.last_add > 80 - gradient * 3 and \
                random.randint(0, int(200 - gradient * 2)) == 0:
            # pinball will not occur during first 50 m
            pinball = Pinball(self.cv, self.cv_w, self.cv_h)
            pinball.x_speed += gradient
            pinball.gravity += gradient * 0.06
            self.objects.append(pinball)
            self.last_add = 0

    def cheat(self):
        '''turn on / off cheating, which allows infinite jump'''
        self.objects[0].isCheated = not self.objects[0].isCheated

    def __getstate__(self):
        '''Export status parameters'''
        status = {'x': self.x,
                  'y': self.y,
                  'cv_w': self.cv_w,
                  'cv_h': self.cv_h,
                  'bg_img': self.bg_img,
                  'objects': self.objects,
                  'last_add': self.last_add}
        return status

    def __setstate__(self, state):
        '''Import status parameters'''
        self.__dict__.update(state)

    def re_init(self, window, keybind):
        '''When new state was imported, this should be called
        to reinitialize game unit on the window'''
        self.window = window
        self.keybind = keybind
        self.cv = Canvas(
            self.window,
            width=self.cv_w,
            height=self.cv_h,
            cursor='circle',
            highlightthickness=0)
        self.draw_background()
        for ob in self.objects:
            ob.re_init(self.cv)
        self.cv.place(x=self.x, y=self.y)
