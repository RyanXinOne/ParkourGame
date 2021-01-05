'''All object classes, including main character and barriers'''

from tkinter import PhotoImage
import random


class UserCharacter:
    '''The main character that controled by user'''

    def __init__(self, cv, cv_w, cv_h, x, y, race):
        '''Initialize main character.'''
        self.cv = cv
        self.cv_w = cv_w
        self.cv_h = cv_h
        self.width = 80
        self.height = 110
        self.x = x
        self.y = y
        self.isjumping = False
        self.gravity = 0.9
        self.maxspeed = 24.3
        self.y_speed = 0
        self.imageKind = race
        self.run_image_index = 0
        self.frame_gap = 8
        self.frame_count = 0
        self.isCheated = False
        self.initialize_images()
        self.last_img = self.cv.create_image(
            self.x, self.y,
            image=self.run_images[self.run_image_index],
            anchor='center')

    def initialize_images(self):
        '''initialize media resources.'''
        '''character assets were downloaded from
        (https://www.kenney.nl/assets/toon-characters-1)'''
        self.run_images = [
            PhotoImage(
                file='images/' + self.imageKind +
                '/run' + str(i) + '.png') for i in range(3)]
        self.jump_image = PhotoImage(
            file='images/' + self.imageKind + '/jump.png')
        self.fall_image = PhotoImage(
            file='images/' + self.imageKind + '/fall.png')

    def to_next(self):
        '''calculate next position of the character'''
        ground = self.cv_h - self.height / 2 - 5
        # change position y according to current y_speed with a ceiling set
        self.y += self.y_speed if self.y + self.y_speed >= -self.height else 0
        # update according to different positions
        if self.y == ground:
            # the character is on the ground
            self.y_speed = 0
            self.isjumping = False
        elif self.y < ground:
            # the character is jumping in the air
            # change y_speed by gravity
            self.y_speed += self.gravity if self.y_speed + \
                self.gravity <= self.maxspeed else 0
        else:
            # the character is under the ground (This should not happen, so it
            # needs to be on the ground)
            self.y = ground  # move to the ground
            self.y_speed = 0
            self.isjumping = False

    def draw(self):
        '''delete last image and draw a new image
        according to current pos x, pos y'''
        # delete last image
        self.cv.delete(self.last_img)
        # draw new image
        if self.isjumping:  # jumping
            if self.y_speed <= 5:  # rise
                self.last_img = self.cv.create_image(
                    self.x, self.y, image=self.jump_image, anchor='center')
            else:  # fall
                self.last_img = self.cv.create_image(
                    self.x, self.y, image=self.fall_image, anchor='center')
        else:  # running
            self.last_img = self.cv.create_image(
                self.x, self.y,
                image=self.run_images[self.run_image_index],
                anchor='center')
            if self.frame_count == self.frame_gap:
                self.run_image_index = self.run_image_index + \
                    1 if self.run_image_index + 1 < len(self.run_images) else 0
                self.frame_count = 0
            self.frame_count += 1

    def jump(self):
        '''initiate a jump motion'''
        # only allow jump when on the ground
        if self.isCheated or not self.isjumping:
            self.isjumping = True
            # update y_speed to jump
            self.y_speed = -self.maxspeed

    def clear(self):
        '''clear itself'''
        return False

    def __getstate__(self):
        '''Export status parameters'''
        status = {'cv_w': self.cv_w,
                  'cv_h': self.cv_h,
                  'width': self.width,
                  'height': self.height,
                  'x': self.x,
                  'y': self.y,
                  'isjumping': self.isjumping,
                  'gravity': self.gravity,
                  'maxspeed': self.maxspeed,
                  'y_speed': self.y_speed,
                  'imageKind': self.imageKind,
                  'run_image_index': self.run_image_index,
                  'frame_gap': self.frame_gap,
                  'frame_count': self.frame_count,
                  'isCheated': self.isCheated
                  }
        return status

    def __setstate__(self, state):
        '''Import status parameters'''
        self.__dict__.update(state)
        self.initialize_images()

    def re_init(self, cv):
        '''When new state was imported, this should be
        called to reinitialize object on the canvas'''
        self.cv = cv
        self.last_img = self.cv.create_image(
            self.x, self.y,
            image=self.run_images[self.run_image_index],
            anchor='center')


class WelcomeCharacter(UserCharacter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # run in place at the beginning
        self.x_speed = 0

    def to_next(self):
        '''let the welcome character run at a specific speed'''
        self.x += self.x_speed
        super().to_next()


class Tree:
    '''A Tree barrier that block the path'''

    def __init__(self, cv, cv_w, cv_h):
        '''Initialize a tree barrier'''
        self.cv = cv
        self.cv_w = cv_w
        self.cv_h = cv_h
        # randomly pick one kind of tree
        tree_kind = random.choice([
            {'imageKind': 'treeLong', 'width': 82, 'height': 249},
            {'imageKind': 'treeLongOrange', 'width': 82, 'height': 249},
            {'imageKind': 'tree', 'width': 94 - 8, 'height': 204},
            {'imageKind': 'treeOrange', 'width': 101 - 16, 'height': 259}])
        self.imageKind = tree_kind['imageKind']
        self.width = tree_kind['width']
        self.height = tree_kind['height']
        self.x = self.cv_w + self.width / 2
        self.y = self.cv_h - self.height / 2
        self.x_speed = 7
        self.initialize_images()
        self.last_img = self.cv.create_image(
            self.x, self.y, image=self.image_tree, anchor='center')

    def initialize_images(self):
        '''initialize media resources. Tree image'''
        '''character assets were downloaded from
        (https://www.kenney.nl/assets/background-elements-redux)'''
        self.image_tree = PhotoImage(
            file='images/barriers/' + self.imageKind + '.png')

    def to_next(self):
        '''calculate next position of the barrier (move horizontally)'''
        # update position x according to x_speed
        self.x -= self.x_speed

    def draw(self):
        '''move the tree barrier to pos x, y'''
        # delete last image
        self.cv.delete(self.last_img)
        # draw new image
        self.last_img = self.cv.create_image(
            self.x, self.y, image=self.image_tree, anchor='center')

    def collision_detect(self, character):
        '''detect collision with the character. In this case,
            detect the collision between a circle-like and a rectangle'''
        left = self.x - self.width / 2 + 10
        right = self.x + self.width / 2 - 10
        top = self.y - self.height / 2 + 5
        if character.y >= top:
            if character.x >= left - character.width / \
                    2 and character.x <= right + character.width / 2:
                return True
        elif character.y >= top - character.height / 2 and character.y <= top:
            if character.x >= left - character.width / \
                    2 and character.x <= right + character.width / 2:
                if (character.x >= left and character.x <= right) or \
                        pow(character.x - left, 2) + \
                        pow(character.y - top, 2) <= \
                        pow(character.width / 2, 2) or \
                        pow(character.x - right, 2) + \
                        pow(character.y - top, 2) <= \
                        pow(character.width / 2, 2):
                    return True
        return False

    def clear(self):
        '''clear itself'''
        self.cv.delete(self.last_img)

    def __getstate__(self):
        '''Export status parameters'''
        status = {'cv_w': self.cv_w,
                  'cv_h': self.cv_h,
                  'imageKind': self.imageKind,
                  'width': self.width,
                  'height': self.height,
                  'x': self.x,
                  'y': self.y,
                  'x_speed': self.x_speed
                  }
        return status

    def __setstate__(self, state):
        '''Import status parameters'''
        self.__dict__.update(state)
        self.initialize_images()

    def re_init(self, cv):
        '''When new state was imported, this should be
        called to reinitialize object on the canvas'''
        self.cv = cv
        self.last_img = self.cv.create_image(
            self.x, self.y, image=self.image_tree, anchor='center')


class Fence:
    '''Small Fence barrier that block the path'''

    def __init__(self, cv, cv_w, cv_h):
        '''Initialize a fence barrier'''
        self.cv = cv
        self.cv_w = cv_w
        self.cv_h = cv_h
        # randomly pick a kind of fence
        fence_kind = random.choice([
            {'imageKind': 'fence', 'width': 104, 'height': 77},
            {'imageKind': 'fenceIron', 'width': 120, 'height': 121}])
        self.imageKind = fence_kind['imageKind']
        self.width = fence_kind['width']
        self.height = fence_kind['height']
        self.x = self.cv_w + self.width / 2
        self.y = self.cv_h - self.height / 2
        self.x_speed = 7
        self.initialize_images()
        self.last_img = self.cv.create_image(
            self.x, self.y, image=self.image_fence, anchor='center')

    def initialize_images(self):
        '''initialize media resources. Fance image.'''
        '''character assets were downloaded from
        (https://www.kenney.nl/assets/background-elements-redux)'''
        self.image_fence = PhotoImage(
            file='images/barriers/' + self.imageKind + '.png')

    def to_next(self):
        '''calculate next position of the barrier (move horizontally)'''
        # update position x according to x_speed
        self.x -= self.x_speed

    def draw(self):
        '''move the fence barrier to pos x, y'''
        # delete last image
        self.cv.delete(self.last_img)
        # draw new image
        self.last_img = self.cv.create_image(
            self.x, self.y, image=self.image_fence, anchor='center')

    def collision_detect(self, character):
        '''detect collision with the character. In this case,
            detect the collision between two rectangles'''
        left = self.x - self.width / 2 + 3
        right = self.x + self.width / 2 - 3
        top = self.y - self.height / 2 + 5
        return character.x >= left - character.width / 2 and \
            character.x <= right + character.width / 2 and \
            character.y >= top - character.height / 2

    def clear(self):
        '''clear itself'''
        self.cv.delete(self.last_img)

    def __getstate__(self):
        '''Export status parameters'''
        status = {'cv_w': self.cv_w,
                  'cv_h': self.cv_h,
                  'imageKind': self.imageKind,
                  'width': self.width,
                  'height': self.height,
                  'x': self.x,
                  'y': self.y,
                  'x_speed': self.x_speed
                  }
        return status

    def __setstate__(self, state):
        '''Import status parameters'''
        self.__dict__.update(state)
        self.initialize_images()

    def re_init(self, cv):
        '''When new state was imported, this should be
        called to reinitialize object on the canvas'''
        self.cv = cv
        self.last_img = self.cv.create_image(
            self.x, self.y,
            image=self.image_fence,
            anchor='center')


class Pinball:
    '''A pin ball who wants to hit the character.
    This is a shape(circle) rather than image'''

    def __init__(self, cv, cv_w, cv_h):
        '''Initialize a bouncing pin ball barrier.'''
        self.cv = cv
        self.cv_w = cv_w
        self.cv_h = cv_h
        self.radius = 20
        self.width = self.radius * 2
        self.color = '#%02X%02X%02X' % (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255))
        self.x = self.cv_w + self.radius
        self.y = cv_h - 400
        self.x_speed = 7
        self.y_speed = 0
        self.gravity = 0.1 + (random.random() / 3) * 2
        self.g_attenuation = 1
        self.last_img = self.cv.create_oval(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
            fill=self.color,
            outline='black')

    def to_next(self):
        '''calculate next position of the pinball, which would bounce'''
        if self.y + self.y_speed > self.cv_h - self.radius:
            self.y_speed = -self.y_speed / self.g_attenuation
        else:
            self.y_speed += self.gravity
        self.x -= self.x_speed
        self.y += self.y_speed
        if self.y > self.cv_h - self.radius:
            self.y = self.cv_h - self.radius

    def draw(self):
        '''move the pinball to pos x, y'''
        # delete last image
        self.cv.delete(self.last_img)
        # draw new image
        self.last_img = self.cv.create_oval(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
            fill=self.color,
            outline='black')

    def collision_detect(self, character):
        '''detect collision with the character. In this case,
        between a rectangle and a circle'''
        left = character.x - character.width / 2 + 15
        right = character.x + character.width / 2 - 13
        top = character.y - character.height / 2 + 20
        bottom = character.y + character.height / 2 + 7
        if self.y >= top and self.y <= bottom:
            if self.x >= left - self.radius and self.x <= right + self.radius:
                return True
        elif self.y >= top - self.radius and self.y <= top:
            if self.x >= left - self.radius and self.x <= right + self.radius:
                if (self.x >= left and self.x <= right) or \
                        pow(self.x - left, 2) + pow(self.y - top, 2) <= \
                        self.radius ** 2 or \
                        pow(self.x - right, 2) + pow(self.y - top, 2) <= \
                        self.radius ** 2:
                    return True
        elif self.y >= bottom and self.y <= bottom + self.radius:
            if self.x >= left - self.radius and self.x <= right + self.radius:
                if (self.x >= left and self.x <= right) or \
                        pow(self.x - left, 2) + pow(self.y - bottom, 2) <= \
                        self.radius ** 2 or \
                        pow(self.x - right, 2) + pow(self.y - bottom, 2) <= \
                        self.radius ** 2:
                    return True
        return False

    def clear(self):
        '''clear itself'''
        self.cv.delete(self.last_img)

    def __getstate__(self):
        '''Export status parameters'''
        status = {'cv_w': self.cv_w,
                  'cv_h': self.cv_h,
                  'radius': self.radius,
                  'width': self.width,
                  'color': self.color,
                  'x': self.x,
                  'y': self.y,
                  'x_speed': self.x_speed,
                  'y_speed': self.y_speed,
                  'gravity': self.gravity,
                  'g_attenuation': self.g_attenuation
                  }
        return status

    def __setstate__(self, state):
        '''Import status parameters'''
        self.__dict__.update(state)

    def re_init(self, cv):
        '''When new state was imported, this should be
        called to reinitialize object on the canvas'''
        self.cv = cv
        self.last_img = self.cv.create_oval(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
            fill=self.color,
            outline='black')
