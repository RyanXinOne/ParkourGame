'''Game window class file'''

from tkinter import Tk, Canvas, Button, Entry, PhotoImage, font, messagebox
import time
import random
import os
import pickle
from gameUnit import GameUnit
from objects import WelcomeCharacter


class GameWindow:
    '''main window of the Parkour game'''
    window_width = 1600
    window_height = 900
    frame_interval = 1000 // 100
    default_cursor = 'circle'
    active_cursor = 'plus'
    default_key_settings = {
        'pause': '<Escape>',
        'jump1': '<space>',
        'jump2': '<Up>',
        'cheat': '<r>',
        'boss': '<b>'}

    def __init__(self):
        '''initialize game window'''
        self.window = Tk()
        self.window.title("Parkour")
        self.window.geometry(str(self.window_width) +
                             "x" + str(self.window_height))
        # prevent user resize window
        self.window.resizable(width=False, height=False)
        self.window.attributes("-fullscreen", True)  # enter fullscreen mode
        try:
            # The .ico format only works at Windows
            self.window.iconbitmap("images/icons/parkour.ico")
            self.isAllowIcon = True
        except BaseException:
            self.isAllowIcon = False
            print("Failed to set icon due to OS compatibility. Never Mind~")

        # Screen resolution check
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        if screen_width != self.window_width or \
                screen_height != self.window_height:
            message = 'Notice: Your screen resolution is ' + \
                str(screen_width) + 'x' + str(screen_height) + \
                ', which is not the recommended resolution ' + \
                str(self.window_width) + 'x' + str(self.window_height) + \
                ' and your gaming experience may be affected. ' + \
                'Do you still want to play in full screen?'
            ans = messagebox.askquestion(
                title="Bad Resolution", message=message)
            if ans == 'no':
                self.window.attributes("-fullscreen", False)
                self.window.geometry(str(self.window_width) + "x" +
                                     str(self.window_height) + "+" +
                                     str((screen_width // 2) -
                                         (self.window_width // 2)) + "+" +
                                     str((screen_height // 2) -
                                         (self.window_height // 2)))

        # read user key setting file
        if os.path.exists("data/setting.pickle"):
            try:
                with open("data/setting.pickle", 'rb') as f:
                    self.keySettings = pickle.load(f)
            except BaseException:
                self.keySettings = self.default_key_settings.copy()
        else:
            self.keySettings = self.default_key_settings.copy()

        # font settings
        self.titleFont = font.Font(
            family='Arial',
            size=30,
            weight=font.BOLD,
            slant=font.ITALIC)
        self.menuFont = font.Font(
            family='Arial',
            size=20,
            weight=font.BOLD,
            slant=font.ROMAN)

        # this can help decide whether it is playing the game
        self.isPaused = None
        self.hide = False
        # boss key bind
        self.bind_boss = self.window.bind(
            self.keySettings['boss'],
            lambda e: self.boss_key())

        self.display_menu()

        self.window.mainloop()

    def boss_key(self):
        '''pause, hide and camouflage the whole game
        into a word document in the background'''
        self.hide = not self.hide
        if self.hide:
            if self.isPaused is False:
                self.game_pause()
            # do not set cursor for the hideCV
            self.hideCV = Canvas(
                self.window,
                width=self.window_width,
                height=self.window_height,
                highlightthickness=0)
            '''This camouflage picture is a screenshot of the word document'''
            self.hide_bg = PhotoImage(file='images/camouflage.png')
            self.hideCV.create_image(0, 0, image=self.hide_bg, anchor='nw')
            self.hideCV.place(x=0, y=0)
            self.window.title("New Microsoft Word Document.docx")
            if self.isAllowIcon:
                self.window.iconbitmap("images/icons/wordicon.ico")
            # make window completely transparent
            self.window.attributes("-alpha", 0)
        else:
            self.hideCV.destroy()
            self.window.title("Parkour")
            if self.isAllowIcon:
                self.window.iconbitmap("images/icons/parkour.ico")
            self.window.attributes("-alpha", 1)

    def display_menu(self):
        '''display menu page'''
        # menu canvas
        self.menuCV = Canvas(
            self.window,
            width=self.window_width,
            height=self.window_height,
            cursor=self.default_cursor,
            highlightthickness=0)

        '''background image was downloaded from
        (https://www.kenney.nl/assets/background-elements-redux)'''
        self.image_menu_bg = PhotoImage(
            file='images/backgrounds/ColorGrass_HD.png')
        self.menuCV.create_image(0, 0, image=self.image_menu_bg, anchor='nw')

        # show title
        self.menuCV.create_text(
            100,
            50,
            anchor='nw',
            text='Welcome to Parkour',
            font=self.titleFont,
            fill='black',
            activefill='red')

        self.menuCV.place(x=0, y=0)

        self.btn_m_new = HoverButton(
            self.window,
            anchor='center',
            text="New Game",
            font=self.menuFont,
            width=10,
            command=lambda: clear_to_next('new'),
            background='lightgreen',
            activebackground='lightyellow',
            foreground='black',
            cursor=self.active_cursor)
        self.btn_m_new.place(x=520, y=170)
        self.btn_m_continue = HoverButton(
            self.window,
            anchor='center',
            text="Continue",
            font=self.menuFont,
            width=10,
            command=lambda: clear_to_next('continue'),
            background='lightgreen',
            activebackground='lightyellow',
            foreground='black',
            cursor=self.active_cursor)
        self.btn_m_continue.place(x=520, y=250)
        self.btn_m_rank = HoverButton(
            self.window,
            anchor='center',
            text="Top 10",
            font=self.menuFont,
            width=10,
            command=lambda: self.show_ranking(callfrom='menu'),
            background='lightgreen',
            activebackground='lightyellow',
            foreground='black',
            cursor=self.active_cursor)
        self.btn_m_rank.place(x=520, y=330)
        self.btn_m_key = HoverButton(
            self.window,
            anchor='center',
            text="Key Setting",
            font=self.menuFont,
            width=10,
            command=lambda: self.key_setting(callfrom='menu'),
            background='lightgreen',
            activebackground='lightyellow',
            foreground='black',
            cursor=self.active_cursor)
        self.btn_m_key.place(x=520, y=410)
        self.btn_m_quit = HoverButton(
            self.window,
            anchor='center',
            text="Quit",
            font=self.menuFont,
            width=10,
            command=lambda: self.window.quit(),
            background='lightblue',
            activebackground='lightgrey',
            foreground='black',
            cursor=self.active_cursor)
        self.btn_m_quit.place(x=1320, y=780)

        # load last saved game
        if os.path.exists("data/save.pickle"):
            try:
                with open("data/save.pickle", "rb") as f:
                    self.savedData = pickle.load(f)
            except BaseException:
                self.btn_m_continue.configure(state='disabled')
        else:
            self.btn_m_continue.configure(state='disabled')

        # show welcome character
        self.welcome_animation()

        def clear_to_next(point):
            '''clear widgets in the menu and to the next screen'''
            # clear widgets in the menu
            self.btn_m_new.destroy()
            self.btn_m_continue.destroy()
            self.btn_m_rank.destroy()
            self.btn_m_key.destroy()
            self.btn_m_quit.destroy()
            if point == 'new':
                self.new_game()
            elif point == 'continue':
                # stop welcome animation
                self.window.after_cancel(self.clock)
                self.playingAnima = False
                # destroy current menu
                self.menuCV.destroy()
                self.game_continue()

    def key_setting(self, callfrom):
        '''key setting page'''
        if callfrom == 'game':
            # temporarily unbind pause key if in the game
            self.window.unbind(self.keySettings['pause'], self.bind_pause)

        # create a new canvas
        self.keysetCV = Canvas(
            self.window,
            width=self.window_width,
            height=self.window_height,
            cursor=self.default_cursor,
            highlightthickness=0)
        self.keysetCV.create_image(0, 0, image=self.image_menu_bg, anchor='nw')

        self.keysetCV.create_text(
            100,
            50,
            anchor='nw',
            text='Key Setting Page',
            font=self.titleFont,
            fill='black',
            activefill='red')

        # button Character 1 Jump
        self.keysetCV.create_text(
            450,
            180,
            anchor='center',
            text='Character 1 Jump',
            font=self.menuFont,
            fill='black',
            activefill='red')
        self.btn_s_c1key = HoverButton(
            self.window,
            anchor='center',
            text=self.keySettings['jump1'],
            font=self.menuFont,
            width=12,
            command=lambda: btn_press('jump1'),
            background='lightblue',
            activebackground='lightgrey',
            foreground='black',
            cursor=self.active_cursor)
        self.btn_s_c1key.place(x=760, y=180, anchor='center')
        # button Character 2 Jump
        self.keysetCV.create_text(
            450,
            260,
            anchor='center',
            text='Character 2 Jump',
            font=self.menuFont,
            fill='black',
            activefill='red')
        self.btn_s_c2key = HoverButton(
            self.window,
            anchor='center',
            text=self.keySettings['jump2'],
            font=self.menuFont,
            width=12,
            command=lambda: btn_press('jump2'),
            background='lightblue',
            activebackground='lightgrey',
            foreground='black',
            cursor=self.active_cursor)
        self.btn_s_c2key.place(x=760, y=260, anchor='center')
        # button Pause / Resume
        self.keysetCV.create_text(
            450,
            340,
            anchor='center',
            text='Pause / Resume',
            font=self.menuFont,
            fill='black',
            activefill='red')
        self.btn_s_pkey = HoverButton(
            self.window,
            anchor='center',
            text=self.keySettings['pause'],
            font=self.menuFont,
            width=12,
            command=lambda: btn_press('pause'),
            background='lightblue',
            activebackground='lightgrey',
            foreground='black',
            cursor=self.active_cursor)
        self.btn_s_pkey.place(x=760, y=340, anchor='center')
        # button cheat
        self.keysetCV.create_text(
            450,
            420,
            anchor='center',
            text='Cheat (Unlimited Jump)',
            font=self.menuFont,
            fill='black',
            activefill='red')
        self.btn_s_cheat = HoverButton(
            self.window,
            anchor='center',
            text=self.keySettings['cheat'],
            font=self.menuFont,
            width=12,
            command=lambda: btn_press('cheat'),
            background='lightblue',
            activebackground='lightgrey',
            foreground='black',
            cursor=self.active_cursor)
        self.btn_s_cheat.place(x=760, y=420, anchor='center')
        # button boss key
        self.keysetCV.create_text(
            450,
            500,
            anchor='center',
            text='Boss Key',
            font=self.menuFont,
            fill='black',
            activefill='red')
        self.btn_s_boss = HoverButton(
            self.window,
            anchor='center',
            text=self.keySettings['boss'],
            font=self.menuFont,
            width=12,
            command=lambda: btn_press('boss'),
            background='lightblue',
            activebackground='lightgrey',
            foreground='black',
            cursor=self.active_cursor)
        self.btn_s_boss.place(x=760, y=500, anchor='center')

        self.keysetCV.place(x=0, y=0)

        # restore to default setting button
        self.btn_s_reset = HoverButton(
            self.window,
            anchor='center',
            text="Reset",
            font=self.menuFont,
            command=lambda: reset(),
            background='lightblue',
            activebackground='lightgrey',
            foreground='black',
            cursor=self.active_cursor)
        self.btn_s_reset.place(x=100, y=780)
        # button back
        self.btn_s_back = HoverButton(self.window,
                                      anchor='center',
                                      text="Back to " +
                                      callfrom[0].upper() + callfrom[1:],
                                      font=self.menuFont,
                                      command=lambda: back(),
                                      background='pink',
                                      activebackground='lightgrey',
                                      foreground='black',
                                      cursor=self.active_cursor)
        self.btn_s_back.place(x=1300, y=780)

        def btn_press(key):
            '''update button color on click and bind the event'''
            if key == 'jump1':
                self.btn_s_c1key.configure(
                    background='pink', text='Press any key')
                self.btn_s_c2key.configure(
                    background='lightblue',
                    text=self.keySettings['jump2'])
                self.btn_s_pkey.configure(
                    background='lightblue',
                    text=self.keySettings['pause'])
                self.btn_s_cheat.configure(
                    background='lightblue',
                    text=self.keySettings['cheat'])
                self.btn_s_boss.configure(
                    background='lightblue',
                    text=self.keySettings['boss'])
            elif key == 'jump2':
                self.btn_s_c1key.configure(
                    background='lightblue',
                    text=self.keySettings['jump1'])
                self.btn_s_c2key.configure(
                    background='pink', text='Press any key')
                self.btn_s_pkey.configure(
                    background='lightblue',
                    text=self.keySettings['pause'])
                self.btn_s_cheat.configure(
                    background='lightblue',
                    text=self.keySettings['cheat'])
                self.btn_s_boss.configure(
                    background='lightblue',
                    text=self.keySettings['boss'])
            elif key == 'pause':
                self.btn_s_c1key.configure(
                    background='lightblue',
                    text=self.keySettings['jump1'])
                self.btn_s_c2key.configure(
                    background='lightblue',
                    text=self.keySettings['jump2'])
                self.btn_s_pkey.configure(
                    background='pink', text='Press any key')
                self.btn_s_cheat.configure(
                    background='lightblue',
                    text=self.keySettings['cheat'])
                self.btn_s_boss.configure(
                    background='lightblue',
                    text=self.keySettings['boss'])
            elif key == 'cheat':
                self.btn_s_c1key.configure(
                    background='lightblue',
                    text=self.keySettings['jump1'])
                self.btn_s_c2key.configure(
                    background='lightblue',
                    text=self.keySettings['jump2'])
                self.btn_s_pkey.configure(
                    background='lightblue',
                    text=self.keySettings['pause'])
                self.btn_s_cheat.configure(
                    background='pink', text='Press any key')
                self.btn_s_boss.configure(
                    background='lightblue',
                    text=self.keySettings['boss'])
            elif key == 'boss':
                self.btn_s_c1key.configure(
                    background='lightblue',
                    text=self.keySettings['jump1'])
                self.btn_s_c2key.configure(
                    background='lightblue',
                    text=self.keySettings['jump2'])
                self.btn_s_pkey.configure(
                    background='lightblue',
                    text=self.keySettings['pause'])
                self.btn_s_cheat.configure(
                    background='lightblue',
                    text=self.keySettings['cheat'])
                self.btn_s_boss.configure(
                    background='pink', text='Press any key')
            self.bind_changeKey = self.window.bind(
                '<Key>', lambda e: change_key(e, key))

        def update_key_setting_file():
            '''write user setting into setting file'''
            if not os.path.exists('data/'):
                os.mkdir('data')
            with open("data/setting.pickle", "wb") as f:
                pickle.dump(self.keySettings, f)

        def change_key(event, key):
            '''set key'''
            keyname = '<' + event.keysym + '>'
            if keyname == '<??>':
                # encounter an unknown key
                if key == 'jump1':
                    self.btn_s_c1key.configure(text='Failed!')
                elif key == 'jump2':
                    self.btn_s_c2key.configure(text='Failed!')
                elif key == 'pause':
                    self.btn_s_pkey.configure(text='Failed!')
                elif key == 'cheat':
                    self.btn_s_cheat.configure(text='Failed!')
                elif key == 'boss':
                    self.btn_s_boss.configure(text='Failed!')
            elif keyname in self.keySettings.values():
                # deal with key conflicts
                if key == 'jump1':
                    self.btn_s_c1key.configure(text='Conflict!')
                elif key == 'jump2':
                    self.btn_s_c2key.configure(text='Conflict!')
                elif key == 'pause':
                    self.btn_s_pkey.configure(text='Conflict!')
                elif key == 'cheat':
                    self.btn_s_cheat.configure(text='Conflict!')
                elif key == 'boss':
                    self.btn_s_boss.configure(text='Conflict!')
            else:
                self.window.unbind('<Key>', self.bind_changeKey)
                if key == 'jump1':
                    self.btn_s_c1key.configure(
                        background='lightblue', text=keyname)
                elif key == 'jump2':
                    self.btn_s_c2key.configure(
                        background='lightblue', text=keyname)
                elif key == 'pause':
                    self.btn_s_pkey.configure(
                        background='lightblue', text=keyname)
                elif key == 'cheat':
                    self.btn_s_cheat.configure(
                        background='lightblue', text=keyname)
                elif key == 'boss':
                    self.btn_s_boss.configure(
                        background='lightblue', text=keyname)
                    self.window.unbind(
                        self.keySettings['boss'], self.bind_boss)
                    self.bind_boss = self.window.bind(
                        keyname, lambda e: self.boss_key())
                self.keySettings[key] = keyname
                update_key_setting_file()

        def reset():
            '''reset key settings'''
            self.window.unbind('<Key>')
            self.window.unbind(self.keySettings['boss'], self.bind_boss)
            self.keySettings = self.default_key_settings.copy()
            self.bind_boss = self.window.bind(
                self.keySettings['boss'], lambda e: self.boss_key())
            self.btn_s_c1key.configure(
                background='lightblue',
                text=self.keySettings['jump1'])
            self.btn_s_c2key.configure(
                background='lightblue',
                text=self.keySettings['jump2'])
            self.btn_s_pkey.configure(
                background='lightblue',
                text=self.keySettings['pause'])
            self.btn_s_cheat.configure(
                background='lightblue',
                text=self.keySettings['cheat'])
            self.btn_s_boss.configure(
                background='lightblue',
                text=self.keySettings['boss'])
            update_key_setting_file()

        def back():
            '''clear itself and back to where it is called'''
            self.window.unbind('<Key>')
            self.btn_s_c1key.destroy()
            self.btn_s_c2key.destroy()
            self.btn_s_pkey.destroy()
            self.btn_s_cheat.destroy()
            self.btn_s_boss.destroy()
            self.keysetCV.destroy()
            self.btn_s_back.destroy()
            self.btn_s_reset.destroy()
            if callfrom == 'game':
                # restore key bind of pausing
                self.bind_pause = self.window.bind(
                    self.keySettings['pause'], lambda e: self.game_pause())
                # set new jump key for game units
                for i, unit in enumerate(self.gameUnits):
                    unit.keybind = self.keySettings['jump' + str(i + 1)]

    def new_game(self):
        '''start a new game, let user select difficulty'''
        # show level select text
        self.menuCV.create_text(
            400,
            200,
            anchor='nw',
            text='Please select game difficulty.',
            font=self.menuFont,
            fill='black',
            activefill='red')
        # level selection button
        self.btn_n_easy = HoverButton(
            self.window,
            anchor='center',
            text="Normal",
            width=7,
            font=self.menuFont,
            command=lambda: select_level('normal'),
            background='lightblue',
            activebackground='lightgrey',
            foreground='black',
            cursor=self.active_cursor)
        self.btn_n_easy.place(x=450, y=250)
        self.btn_n_hard = HoverButton(
            self.window,
            anchor='center',
            text="Hard",
            width=7,
            font=self.menuFont,
            command=lambda: select_level('hard'),
            background='lightblue',
            activebackground='lightgrey',
            foreground='black',
            cursor=self.active_cursor)
        self.btn_n_hard.place(x=610, y=250)
        # button back
        self.btn_n_back = HoverButton(
            self.window,
            anchor='center',
            text="Back to Menu",
            font=self.menuFont,
            command=lambda: clear_back(),
            background='pink',
            activebackground='lightgrey',
            foreground='black',
            cursor=self.active_cursor)
        self.btn_n_back.place(x=1300, y=780)

        self.first_select = False

        def select_level(level):
            '''select game difficulty according to button clicked'''
            self.level = level
            if level == 'normal':
                self.btn_n_easy.configure(background='lightgreen')
                self.btn_n_hard.configure(background='lightblue')
            elif level == 'hard':
                self.btn_n_hard.configure(background='pink')
                self.btn_n_easy.configure(background='lightblue')
            if not self.first_select:
                # show ready texts
                self.menuCV.create_text(
                    400,
                    350,
                    anchor='nw',
                    text='Ready to start?',
                    font=self.menuFont,
                    fill='black',
                    activefill='red')
                self.continue_text = self.menuCV.create_text(
                    450,
                    400,
                    anchor='nw',
                    text='Press any key to continue...',
                    font=self.menuFont,
                    fill='black',
                    activefill='red')
                self.bind_ready = self.window.bind(
                    '<Key>', lambda x: clear_to_next())
                self.first_select = True

        def clear_to_next():
            '''clear it self and ready to enter the game (watch animation!)'''
            self.window.unbind('<Key>', self.bind_ready)
            self.btn_n_easy.configure(state='disabled')
            self.btn_n_hard.configure(state='disabled')
            self.menuCV.itemconfig(
                self.continue_text,
                text="Let's Parkour around the world...")
            # destroy back to menu button
            self.btn_n_back.destroy()
            # make the welcome character run
            self.welCharacter.x_speed = 8

        def clear_back():
            '''clear it self and back to main menu'''
            self.window.unbind('<Key>')
            # destroy widgets
            self.btn_n_easy.destroy()
            self.btn_n_hard.destroy()
            self.btn_n_back.destroy()
            # stop welcome animation
            self.window.after_cancel(self.clock)
            self.playingAnima = False
            # destroy current menu
            self.menuCV.destroy()
            # display new menu
            self.display_menu()

    def welcome_animation(self):
        '''play running character who welcomes user'''
        # play start animation
        race = random.choice(['femaleAdventurer',
                              'femalePerson',
                              'maleAdventurer',
                              'malePerson',
                              'robot',
                              'zombie'])
        self.welCharacter = WelcomeCharacter(
            self.menuCV,
            self.window_width,
            self.window_height,
            100,
            self.window_height - 60,
            race)
        self.playingAnima = True

        def run_over():
            if not self.playingAnima:
                return
            if self.welCharacter.x < self.window_width + \
                    self.welCharacter.width / 2:
                if self.welCharacter.x >= 300 and self.welCharacter.x <= 307:
                    # jump once in the middle
                    self.welCharacter.jump()
                # running...
                self.welCharacter.to_next()
                self.welCharacter.draw()
                # refresh animation
                self.window.update_idletasks()
            else:
                # stop animation
                self.window.after_cancel(self.clock)
                self.playingAnima = False
                # clear menu widgets
                self.btn_n_easy.destroy()
                self.btn_n_hard.destroy()
                self.menuCV.destroy()
                # start main game
                self.game_start()

        self.loop_clock(run_over)

    def loop_clock(self, func):
        '''This method is used to act as an external clock and
        non-blockingly call game_loop to achieve stable fps performance.
        To stop this clock, use "self.window.after_cancel(self.clock)"'''
        # non-blockingly call game_loop
        self.window.after_idle(func)
        # A timer
        self.clock = self.window.after(
            self.frame_interval, self.loop_clock, func)

    def game_start(self):
        '''start the main game loop'''
        # use time to generate a unique gameID to correctly delete
        # corresponding saved record when saved game is over
        self.gameID = time.time()

        # store game units
        self.gameUnits = []
        self.jump_tips = []
        # random background and character image
        backgrounds = ['Castles', 'ColorDesert', 'Desert', 'Forest', 'Empty']
        random.shuffle(backgrounds)
        races = [
            'femaleAdventurer',
            'femalePerson',
            'maleAdventurer',
            'malePerson',
            'robot',
            'zombie']
        random.shuffle(races)
        # show scenes according to game level
        if self.level == 'hard':
            # hard screen
            self.gameUnits.append(
                GameUnit(
                    self.window,
                    0,
                    0,
                    self.window_width,
                    self.window_height / 2,
                    background=backgrounds.pop(),
                    race=races.pop(),
                    keybind=self.keySettings['jump1']))
            self.gameUnits.append(
                GameUnit(
                    self.window,
                    0,
                    self.window_height / 2,
                    self.window_width,
                    self.window_height / 2,
                    background=backgrounds.pop(),
                    race=races.pop(),
                    keybind=self.keySettings['jump2']))
            self.jump_tips.append(
                self.gameUnits[0].cv.create_text(
                    self.window_width /
                    2,
                    100,
                    anchor='center',
                    text='Press key ' +
                    self.keySettings['jump1'] +
                    ' to jump.',
                    font=self.menuFont,
                    fill='black',
                    activefill='red'))
            self.jump_tips.append(
                self.gameUnits[1].cv.create_text(
                    self.window_width /
                    2,
                    100,
                    anchor='center',
                    text='Press key ' +
                    self.keySettings['jump2'] +
                    ' to jump.',
                    font=self.menuFont,
                    fill='black',
                    activefill='red'))
        else:
            # normal screen
            self.gameUnits.append(
                GameUnit(
                    self.window,
                    0,
                    0,
                    self.window_width,
                    self.window_height,
                    background=backgrounds.pop(),
                    race=races.pop(),
                    keybind=self.keySettings['jump1']))
            self.jump_tips.append(
                self.gameUnits[0].cv.create_text(
                    self.window_width /
                    2,
                    100,
                    anchor='center',
                    text='Press key ' +
                    self.keySettings['jump1'] +
                    ' to jump.',
                    font=self.menuFont,
                    fill='black',
                    activefill='red'))

        # start prompt
        self.first_start = [
            self.gameUnits[0].cv.create_text(
                self.window_width /
                2,
                300,
                anchor='center',
                text='Press pause key ' +
                self.keySettings['pause'] +
                ' to start.',
                font=self.menuFont,
                fill='red')]

        self.last_distance_board = self.gameUnits[0].cv.create_text(
            1590, 10, anchor='ne', text=None, font=self.menuFont, fill='red')
        self.fps_board = self.gameUnits[0].cv.create_text(
            10, 10, anchor='nw', text=None, font=self.menuFont, fill='black')
        self.distance = 0
        self.isPaused = True  # pause initially
        # key bind of pausing
        self.bind_pause = self.window.bind(
            self.keySettings['pause'],
            lambda e: self.game_pause())

    def game_continue(self):
        '''continue last saved game'''
        # get game ID
        self.gameID = self.savedData['id']
        # get saved game units
        self.gameUnits = self.savedData['units']

        self.jump_tips = []
        for i, unit in enumerate(self.gameUnits):
            # reinitialize game unit
            unit.re_init(self.window,
                         keybind=self.keySettings['jump' + str(i + 1)])
            self.jump_tips.append(
                self.gameUnits[i].cv.create_text(self.window_width / 2,
                                                 100,
                                                 anchor='center',
                                                 text='Press key ' +
                                                 self.keySettings['jump' + str(
                                                     i + 1)] + ' to jump.',
                                                 font=self.menuFont,
                                                 fill='black',
                                                 activefill='red'))

        # get game level
        self.level = 'normal' if len(self.gameUnits) == 1 else 'hard'

        # start prompt
        self.first_start = [
            self.gameUnits[0].cv.create_text(
                self.window_width /
                2,
                300,
                anchor='center',
                text='Press pause key ' +
                self.keySettings['pause'] +
                ' to start.',
                font=self.menuFont,
                fill='red')]

        self.distance = self.savedData['distance']
        self.last_distance_board = self.gameUnits[0].cv.create_text(
            1590, 10, anchor='ne',
            text='Distance: ' + str(int(self.distance)) + 'm',
            font=self.menuFont, fill='red')
        self.fps_board = self.gameUnits[0].cv.create_text(
            10, 10, anchor='nw', text=None, font=self.menuFont, fill='black')
        self.isPaused = True  # pause initially
        # key bind of pausing
        self.bind_pause = self.window.bind(
            self.keySettings['pause'],
            lambda e: self.game_pause())

    def game_pause(self):
        '''pause/resume the whole game'''
        def back_to_menu():
            '''clear pause screen and back to main menu'''
            # unbind pause key
            self.window.unbind(self.keySettings['pause'], self.bind_pause)
            self.isPaused = None
            destroy_pause_menu()
            # destroy game canvas
            for unit in self.gameUnits:
                unit.cv.destroy()
            self.display_menu()

        def save_game():
            '''save current game progress and dump into local file'''
            if not os.path.exists('data/'):
                os.mkdir('data')
            with open("data/save.pickle", "wb") as f:
                pickle.dump(
                    {'id': self.gameID,
                     'distance': self.distance,
                     'units': self.gameUnits}, f)
            self.btn_p_save.configure(text='Saved', state='disabled')

        def display_pause_menu():
            '''show pause menu options'''
            # display pause title
            self.pause_prompt = self.gameUnits[0].cv.create_text(
                self.window_width / 2,
                100,
                anchor='center',
                text='Game Paused',
                font=self.titleFont,
                fill='black',
                activefill='red')
            # place pause options
            self.btn_p_resume = HoverButton(
                self.window,
                anchor='center',
                text="Resume",
                font=self.menuFont,
                width=11,
                command=self.game_pause,
                background='lightgreen',
                activebackground='lightgrey',
                foreground='black',
                cursor=self.active_cursor)
            self.btn_p_resume.place(
                x=self.window_width / 2, y=230, anchor='center')
            self.btn_p_keyset = HoverButton(
                self.window,
                anchor='center',
                text="Key Setting",
                font=self.menuFont,
                width=11,
                command=lambda: self.key_setting(
                    callfrom='game'),
                background='lightgreen',
                activebackground='lightgrey',
                foreground='black',
                cursor=self.active_cursor)
            self.btn_p_keyset.place(
                x=self.window_width / 2, y=330, anchor='center')
            self.btn_p_save = HoverButton(
                self.window,
                anchor='center',
                text="Save",
                font=self.menuFont,
                width=11,
                command=save_game,
                background='lightgreen',
                activebackground='lightgrey',
                foreground='black',
                cursor=self.active_cursor)
            self.btn_p_save.place(
                x=self.window_width / 2, y=430, anchor='center')
            self.btn_p_back = HoverButton(
                self.window,
                anchor='center',
                text="Back to Menu",
                font=self.menuFont,
                width=11,
                command=back_to_menu,
                background='lightgreen',
                activebackground='lightgrey',
                foreground='black',
                cursor=self.active_cursor)
            self.btn_p_back.place(
                x=self.window_width / 2, y=530, anchor='center')
            self.btn_p_quit = HoverButton(
                self.window,
                anchor='center',
                text="Quit",
                font=self.menuFont,
                width=10,
                command=lambda: self.window.quit(),
                background='pink',
                activebackground='lightgrey',
                foreground='black',
                cursor=self.active_cursor)
            self.btn_p_quit.place(x=1320, y=780)

        def destroy_pause_menu():
            '''clear pause menu'''
            # destroy pause title and options
            self.gameUnits[0].cv.delete(self.pause_prompt)
            self.btn_p_resume.destroy()
            self.btn_p_keyset.destroy()
            self.btn_p_save.destroy()
            self.btn_p_back.destroy()
            self.btn_p_quit.destroy()

        self.isPaused = not self.isPaused
        if not self.isPaused:
            # continue to play
            if self.first_start:
                # remove start prompt
                self.gameUnits[0].cv.delete(self.first_start[0])
                # remove jump tip
                for i, tip in enumerate(self.jump_tips):
                    self.gameUnits[i].cv.delete(tip)
                self.first_start = False
            else:
                destroy_pause_menu()

            for unit in self.gameUnits:
                # hide cursor
                unit.cv.configure(cursor='none')
                # enable keybind
                unit.enable_key_bind(True)
            # bind cheat key
            self.bind_cheat = self.window.bind(
                self.keySettings['cheat'], lambda e: self.cheat())
            # continue game loop
            self.fps_frame = 0
            self.last_counter = time.perf_counter()
            self.loop_clock(self.game_loop)
        else:
            # pause whole game
            # hide/display cursor
            for unit in self.gameUnits:
                # dislay cursor
                unit.cv.configure(cursor=self.default_cursor)
                # disable keybind
                unit.enable_key_bind(False)
            # unbind cheat key
            self.window.unbind(self.keySettings['cheat'], self.bind_cheat)
            # calcel loop clock
            self.window.after_cancel(self.clock)
            # hide fps board when paused
            self.gameUnits[0].cv.itemconfigure(self.fps_board, text='')
            display_pause_menu()

    def cheat(self):
        '''turn on / off cheating, which allows infinite jump'''
        for unit in self.gameUnits:
            unit.cheat()

    def game_loop(self):
        '''main game loop that controls all unit loops'''
        def update_distance():
            '''update running distance of the character'''
            self.gameUnits[0].cv.itemconfigure(
                self.last_distance_board,
                text='Distance: ' + str(int(self.distance)) + 'm')

        def show_fps():
            '''calculate and show real time FPS'''
            self.fps_frame += 1
            if self.fps_frame == 20:
                # update fps output per 20 frames (this is average)
                this_counter = time.perf_counter()
                fps = (1 / (this_counter - self.last_counter)) * self.fps_frame
                # dynamic fps adjust
                if fps > 75:
                    self.frame_interval += 1
                self.gameUnits[0].cv.itemconfigure(
                    self.fps_board, text='{:.1f}'.format(fps) + 'fps')
                self.fps_frame = 0
                self.last_counter = this_counter

        # gradually increasing difficulty gradient
        gradient = self.distance / 100 if self.distance / 100 <= 20 else 20
        for unit in self.gameUnits:
            if unit.unit_loop(gradient):
                # if it is game over, jump to end screen
                self.window.after_cancel(self.clock)
                self.end_screen()
                return
        # increase distance
        self.distance += 0.1 + 0.01 * gradient
        update_distance()
        # refresh the whole window
        self.window.update_idletasks()
        # calculate FPS
        show_fps()

    def end_screen(self):
        '''end the game process'''
        # unbind gaming keys
        for unit in self.gameUnits:
            unit.enable_key_bind(False)
        self.window.unbind(self.keySettings['pause'], self.bind_pause)
        self.window.unbind(self.keySettings['cheat'], self.bind_cheat)
        self.isPaused = None

        # delete saved game record if this record is finished (game over)
        if os.path.exists("data/save.pickle"):
            try:
                with open("data/save.pickle", "rb") as f:
                    gid = pickle.load(f)['id']
            except BaseException:
                gid = None
            if gid and self.gameID == gid:
                os.remove("data/save.pickle")

        # show result
        self.gameUnits[0].cv.delete(self.last_distance_board)
        self.gameUnits[0].cv.delete(self.fps_board)
        self.gameUnits[0].cv.create_text(
            self.window_width / 2,
            220,
            anchor='center',
            text='Game Over!',
            font=self.menuFont,
            fill='red')
        self.gameUnits[0].cv.create_text(self.window_width /
                                         2, 280,
                                         anchor='center',
                                         text='Your travel distance: ' +
                                         str(int(self.distance)) + 'm',
                                         font=self.menuFont,
                                         fill='red')
        # ask for name
        self.gameUnits[0].cv.create_text(
            560,
            360,
            anchor='center',
            text='Your Name:',
            font=self.menuFont,
            fill='black',
            activefill='red')
        self.name_entry = Entry(
            self.window,
            font=self.menuFont,
            relief='flat',
            selectbackground='green',
            width=15,
            background='white',
            foreground='black')
        self.name_entry.place(x=800, y=360, anchor='center')
        self.name_entry.focus_set()
        self.bind_name = self.name_entry.bind('<Return>', lambda e: submit())
        self.btn_e_name = HoverButton(
            self.window,
            anchor='center',
            text="Confirm",
            font=self.menuFont,
            command=lambda: submit(),
            background='lightgreen',
            activebackground='lightgrey',
            foreground='black',
            cursor=self.active_cursor)
        self.btn_e_name.place(x=1030, y=360, anchor='center')
        self.name_warning = self.gameUnits[0].cv.create_text(
            685,
            400,
            anchor='nw',
            text=None,
            font=self.menuFont,
            fill='black',
            activefill='red')

        # display cursor
        for unit in self.gameUnits:
            unit.cv.configure(cursor=self.default_cursor)

        def submit():
            '''record results, clear itself and show ranking page'''
            user_name = self.name_entry.get().strip()
            if not user_name:
                # name can not be empty
                self.gameUnits[0].cv.itemconfigure(
                    self.name_warning, text='Name cannot be empty.')
                return
            elif len(user_name) > 18:
                # maximum name length
                self.gameUnits[0].cv.itemconfigure(
                    self.name_warning, text='Name is too long.')
                return

            # read rank file
            self.read_rank()
            # update rank file
            info = {
                'name': user_name,
                'distance': self.distance,
                'time': time.asctime(
                    time.localtime(
                        time.time()))[4:]}
            # Insert in descending order
            for i, dat in enumerate(self.ranks[self.level]):
                dat = dat['distance']
                if self.distance > dat:
                    self.ranks[self.level].insert(i, info)
                    self.rank = i + 1
                    break
            else:
                # Insert at the end
                self.ranks[self.level].append(info)
                self.rank = len(self.ranks[self.level])
            # write into rank file
            if not os.path.exists('data/'):
                os.mkdir('data')
            with open("data/rank.pickle", 'wb') as f:
                pickle.dump(self.ranks, f)

            # unbind <Return>
            self.name_entry.unbind('<Return>', self.bind_name)
            # destroy entry and button
            self.name_entry.destroy()
            self.btn_e_name.destroy()
            # destroy game canvas
            for unit in self.gameUnits:
                unit.cv.destroy()
            self.show_ranking(callfrom='endscreen', level=self.level)

    def read_rank(self):
        '''read rank file'''
        if os.path.exists("data/rank.pickle"):
            try:
                with open("data/rank.pickle", 'rb') as f:
                    self.ranks = pickle.load(f)
            except BaseException:
                self.ranks = {'normal': [], 'hard': []}
        else:
            self.ranks = {'normal': [], 'hard': []}

    def show_ranking(self, callfrom, level='normal'):
        '''show ranking page with difficulty "level".
        If called from endscreen, show play again button.'''
        # create end canvas for showing leaderboard and finalized things
        self.endCV = Canvas(
            self.window,
            width=self.window_width,
            height=self.window_height,
            cursor=self.default_cursor,
            highlightthickness=0)

        # load background
        '''background image was downloaded from
        (https://www.kenney.nl/assets/background-elements-redux)'''
        img_choice = 'ColorForest' if level == 'normal' else 'ColorFall'
        self.image_end_bg = PhotoImage(
            file='images/backgrounds/' + img_choice + '_HD.png')
        self.endCV.create_image(0, 0, image=self.image_end_bg, anchor='nw')

        if callfrom == 'endscreen' and level == self.level:
            # show current ranking
            self.endCV.create_text(
                1300,
                655,
                anchor='ne',
                text=self.ranks[self.level][self.rank - 1]['name'] +
                ', your current ranking is No.' + str(self.rank),
                font=self.titleFont,
                fill='black',
                activefill='yellow')

        self.read_rank()
        # show leaderboard
        self.endCV.create_text(self.window_width /
                               2, 60,
                               anchor='center',
                               text='Top 10  Leaderboard - ' +
                               level[0].upper() + level[1:],
                               font=self.titleFont,
                               fill='red')
        base_pos = 410
        self.endCV.create_text(
            base_pos,
            120,
            anchor='center',
            text='Rank',
            font=self.menuFont,
            fill='black',
            tag='rank0')
        self.endCV.create_text(
            base_pos + 200,
            120,
            anchor='center',
            text='Name',
            font=self.menuFont,
            fill='black',
            tag='rank0')
        self.endCV.create_text(
            base_pos + 420,
            120,
            anchor='center',
            text='Distance',
            font=self.menuFont,
            fill='black',
            tag='rank0')
        self.endCV.create_text(
            base_pos + 680,
            120,
            anchor='center',
            text='Time',
            font=self.menuFont,
            fill='black',
            tag='rank0')
        # show top 10
        for i in range(min(10, len(self.ranks[level]))):
            info = self.ranks[level][i]
            name = info['name']
            distance = str(int(info['distance']))
            ti = info['time']
            self.endCV.create_text(base_pos,
                                   180 + 50 * i,
                                   anchor='center',
                                   text=str(i + 1),
                                   font=self.menuFont,
                                   fill='black',
                                   tag='rank' + str(i + 1))
            self.endCV.create_text(base_pos + 200,
                                   180 + 50 * i,
                                   anchor='center',
                                   text=name,
                                   font=self.menuFont,
                                   fill='black',
                                   tag='rank' + str(i + 1))
            self.endCV.create_text(base_pos + 420,
                                   180 + 50 * i,
                                   anchor='center',
                                   text=distance,
                                   font=self.menuFont,
                                   fill='black',
                                   tag='rank' + str(i + 1))
            self.endCV.create_text(base_pos + 680,
                                   180 + 50 * i,
                                   anchor='center',
                                   text=ti,
                                   font=self.menuFont,
                                   fill='black',
                                   tag='rank' + str(i + 1))

        self.endCV.place(x=0, y=0)

        # highlight row mouse pointed
        def highlight_rank(event):
            if event.y >= 100 and event.y <= 140:
                self.endCV.itemconfig('rank0', fill='red')
            else:
                self.endCV.itemconfig('rank0', fill='black')
            for i in range(10):
                if event.y >= 160 + 50 * i and event.y <= 200 + 50 * i:
                    self.endCV.itemconfig('rank' + str(i + 1), fill='red')
                else:
                    self.endCV.itemconfig('rank' + str(i + 1), fill='black')
        self.bind_highlight = self.endCV.bind(
            '<Motion>', lambda e: highlight_rank(e))

        # place button that show the other difficulty
        next_page = 'hard' if level == 'normal' else 'normal'
        self.btn_l_level = HoverButton(self.window,
                                       anchor='center',
                                       text="<" +
                                       next_page[0].upper() + next_page[1:],
                                       width=8,
                                       font=self.menuFont,
                                       command=lambda: clear_to_next(
                                           next_page),
                                       background='lightblue',
                                       activebackground='lightgrey',
                                       foreground='black',
                                       cursor=self.active_cursor)
        self.btn_l_level.place(x=100, y=780)
        # place button that give restart option
        if callfrom == 'endscreen':
            self.btn_l_play = HoverButton(
                self.window,
                anchor='center',
                text="Play again",
                font=self.menuFont,
                command=lambda: clear_to_next('play'),
                background='lightblue',
                activebackground='lightgrey',
                foreground='black',
                cursor=self.active_cursor)
            self.btn_l_play.place(x=1100, y=780)
        self.btn_l_menu = HoverButton(
            self.window,
            anchor='center',
            text="Back to Menu",
            font=self.menuFont,
            command=lambda: clear_to_next('menu'),
            background='lightgreen',
            activebackground='lightgrey',
            foreground='black',
            cursor=self.active_cursor)
        self.btn_l_menu.place(x=1300, y=780)

        def clear_to_next(point):
            '''clear the rank screen and to the next'''
            self.endCV.unbind('<Motion>', self.bind_highlight)
            if callfrom == 'endscreen':
                self.btn_l_play.destroy()
            self.btn_l_menu.destroy()
            self.btn_l_level.destroy()
            self.endCV.destroy()

            if point == 'normal' or point == 'hard':
                # show the other difficulty
                self.show_ranking(callfrom=callfrom, level=next_page)
            elif callfrom == 'endscreen':
                if point == 'play':
                    # play again
                    self.game_start()
                elif point == 'menu':
                    # return to main menu
                    self.display_menu()


class HoverButton(Button):
    '''rewrite button class to add hover visual effect'''

    def __init__(self, *arg, **kw):
        super().__init__(*arg, **kw)
        self.bind_enter = self.bind("<Enter>", self.on_enter)
        self.bind_leave = self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.configure(foreground='red')

    def on_leave(self, e):
        self.configure(foreground='black')

    def destroy(self):
        self.unbind("<Enter>", self.bind_enter)
        self.unbind("<Leave>", self.bind_leave)
        super().destroy()
