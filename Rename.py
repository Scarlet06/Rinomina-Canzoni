import pygame
from eyed3 import load as eyeload
from os import listdir as oslistdir, chdir as oschdir, getenv as osgetenv, system as ossystem, environ
from os.path import isfile as osisfile, isdir as osisdir, join as osjoin,\
    exists as osexists, abspath as osabspath, dirname as osdirname
from sys import exit as sysexit, executable as sysexecutable
from re import match, findall

#to add into hidden imports label in py2exe
# from string import Formatter
# from ctypes import windll
# from random import choice,choices
# from pyperclip import copy,paste
# from requests import get as rget
# from io import BytesIO
# from google_images_search import GoogleImagesSearch
# from threading import Thread
#---------------------------------------------------------------

class Colors:
    #This class is used to have a a nice set of colors to used based on
    # the night_mode

    __slots__ = (
        '__colors',      #dict[str:pygame.Color] -> has the colors
        '__colors_dark'  #dict[str:pygame.Color] -> has the colors for dark mode
        )

    white = pygame.Color(255, 255, 255)         # that's pure white
    black = pygame.Color(0, 0, 0)               # that's pure black
    green= pygame.Color(0, 255, 0)              # that's pure green
    transparent = pygame.Color(255,255,255,0)   # that's invisible
    alphed = pygame.Color(0,0,0,5)

    def __init__(self) -> None:
        self.__colors = {
            'background': pygame.Color(239, 239, 239),
            'white': pygame.Color(255, 255, 255),
            'gray': pygame.Color(196, 196, 196),
            'dark_gray': pygame.Color(70,70,70),
            'light_blue': pygame.Color(0, 255, 255),
            'dark_blue': pygame.Color(0, 77, 255),
            'yellow': pygame.Color(255, 255, 0),
            'orange': pygame.Color(230, 100, 0),
            'pink': pygame.Color(255, 0, 255),
            'black': pygame.Color(0, 0, 0),
            'violet': pygame.Color(143, 0, 255),
            'dark_green': pygame.Color(0, 103, 0),
            'green': pygame.Color(0, 200, 0),
            'red': pygame.Color(230, 56, 56)
            }

        self.__colors_dark = {
            'background': pygame.Color(37,29,58),
            'white': pygame.Color(0, 0, 0),
            'gray': pygame.Color(70,70,70),
            'dark_gray': pygame.Color(196, 196, 196),
            'light_blue': pygame.Color(60,0,204),
            'dark_blue':pygame.Color(138,0,230),
            'yellow': pygame.Color(255, 255, 0),
            'orange': pygame.Color(230, 100, 0),
            'pink': pygame.Color(255, 0, 255),
            'black': pygame.Color(255, 255, 255),
            'violet': pygame.Color(143, 0, 255),
            'dark_green': pygame.Color(0, 103, 0),
            'green': pygame.Color(0, 200, 0),
            'red': pygame.Color(230, 56, 56)
            }

    def __getitem__(self, __color:str) -> pygame.color.Color:
        """
        This function returns the given referenced colour.
        If a secondo element is passed by, it has to be a number
        and it will return the alhped color

        INPUT:
        - [str]     -> the referenced color
        (- [int]    -> the alphed value of the color)   
        """

        if type(__color) is tuple:
            return self.__colors[__color[0]]-pygame.Color(0,0,0,255-__color[1])
        return self.__colors[__color]
        
    def reverse(self) -> None:
        """
        reverse the colors for the night theme
        """

        self.__colors, self.__colors_dark = self.__colors_dark, self.__colors

class ENV(dict):
    #this object simulates the dotenv package to work with .env file
    
    __slots__ = ()      # []    -> there is no need to use more attributes

    def __init__(self) -> None:
        """
        It creates the dict with some useful information.
        It will have some secrets
        """

        # it initialize the dict object
        
        _name = ".env"
        if osexists(_name):
            #it reads the file
            with open(_name,"r") as env:
                env=env.read()
        else:
            #it creates the file
            with open(_name,"w") as newenv:
                env = 'decode = "utf-8"\nyour_dev_api_key =\nyour_project_cx ='
                newenv.write(env)
            from ctypes import windll
            windll.kernel32.SetFileAttributesW(_name, 0x02)

        # for each row it splits between "=" and uses the left as key
        # and the right as value
        super().__init__(map(lambda x: x.strip().strip('"'),e.split("=")) for e in env.split("\n"))

    def __missing__(self, __k:str) -> None:
        """
        when using __getitem__ if the given key __k element is not in dict,
        it returns None

        INPUT:
        - __k [str]     -> is the key of the dict
        """

        return

class INI(dict):
    #this object simulates the configparser package to work with .ini file
    
    __slots__ = ("_decoder")    # [str]                 -> decoding/encoding
                                #                           text special char
    __name = "Options.ini"      # [str]                 -> this is the name of
                                #                           the file
    __key = (                   # [tuple[str]]          -> tuple of key for
        "pos",                  #                           the dict
        "resolution",
        "full_screen",
        "night_mode",
        "drop",
        "rename",
        "check_None",
        "del_pics",
        "directory"
        ) 
    __val = (                   # [tuple[str|float]]    -> tuple of value for
        '30,45',                #                           the dict with the
        "858,480",              #                           corresponding key
        0,                      #                           in the same index
        0,
        '000000',
        '{title} - {artist} - {album}',
        0,
        0,
        '.'
        )
    __dim = '{},{}'             # [str]                 -> place to put pos and
                                #                           ersolution in the 
                                #                           correct place
    def __init__(self, decoder:str) -> None:
        """
        It creates the dict with the program settings. 
        If the file is broken, it will be entiraly replaced

        INPUT:
        - decoder [str]     -> is the encoding/decoding format type 
                                to save in file special characters
        """
        
        self._decoder = decoder

        # it tries to read the file, if it can, it tries to get all the 
        # informations; else it resets all the settings
        if osexists(self.__name):
            try:
                #reading the file
                with open(self.__name, "r", encoding=decoder) as ini:
                    ini=ini.read()

                # if a value is broken, it will be correctly replaced and tt
                # becomes True. If so the new dict (which is correct) will 
                # be overwritten in the file
                tt=False
                t=dict(
                    map(lambda w:w.strip(), i.split("="))
                    for i in ini.split("\n")
                    if "=" in i and not i.startswith(";")
                )

                for i in range(-1,len(self.__key)-1):
                    
                    if self.__key[i] in t:

                        # if key is directory, its value (path) has to exists
                        if i==-1:
                            if osexists(osabspath(t[self.__key[i]])):
                                t[self.__key[i]] = osabspath(t[self.__key[i]])
                            else:
                                t[self.__key[i]] = osabspath(self.__val[i])
                                tt=True
                            continue

                        # if key is pos / resolution, its value has to be "x,y"
                        elif i<2:
                            k = t[self.__key[i]].split(",",1)
                            if len(k)<2 or not all(map(lambda z:z.isdecimal(),k)):
                                t[self.__key[i]] = self.__val[i]
                                tt=True
                            continue

                        # if the value has to be an int, so it will be checked
                        elif type(self.__val[i]) is int:
                            if t[self.__key[i]].isnumeric():
                                t[self.__key[i]] = int(t[self.__key[i]])
                            else:
                                t[self.__key[i]] = self.__val[i]
                                tt=True
                            continue

                    else:
                        #if any key is missing the original value is choosed
                        t[self.__key[i]] = self.__val[i]
                        tt=True

                # it initializes the dict
                super().__init__(t)

                #if tt becomed True, it overwrites the file
                if tt:
                    self.__write()

            except:
                #if there is any kind of error it resets any setting
                self.__correct()

        else:
            #if the file doesn't exists it sets the base settigns
            self.__correct()

    def __write(self) -> None:
        """
        It writes into the SettingsOne.ini file the dict in the .ini format
        """
                                                            
        # is the looking-like .ini file for the settings
        __settings = '[Screen]\npos = {pos}\nresolution = {resolution}\n'\
            'full_screen = {full_screen}\nnight_mode = {night_mode}\n'\
            ';la posizione dello schermo rappresenta le coordinate x,y dell\'angolo in alto a destra della finestra sullo schermo\n'\
            ';la risoluzione dello schermo rappresenta le dimensioni w,h della finestra\n'\
            ';il full screen con bordi è attivo se fissato a 1\n;la modalità notte è attiva se fissato a 1\n\n'\
            '[Folder]\ndirectory = {directory}\n;directory è la cartella in cui il programma cerca le informazioni\n\n'\
            '[Options]\nrename = {rename}\ncheck_None = {check_None}\ndrop = {drop}\ndel_pics = {del_pics}\n'\
            ';rename è la stringa utilizzata per rinominare i file sostituendo le parole contenute tra le parentesi graffe con l\'informazione presente nell\'audio\n'\
            ';check_None se è 1, allora i file non vengono rinominati nel caso almento un metadato risultasse mancante\n'\
            ';drop è un numero che rappresenta (in forma binaria) quali informazioni verranno salvate in un documento apposito\n'\
            ';del_pics è un\'impostazione che permette l\'eliminazione automatica di tutte le immagini salvate nel file mp3'

        
        with open(self.__name,"w",encoding=self._decoder) as ini:
            ini.write(__settings.format(**self))

    def __correct(self) -> None:
        """
        It pairs __key with __val and initializes the dict with it.
        This way there will be a brand new full working .ini file
        """
        
        super().__init__(dict(zip(self.__key,self.__val)))
        self.__setitem__(
            self.__key[-1],
            osabspath(self.__getitem__(self.__key[-1])) # the path has to exists
            )

    def __setitem__(self, __k:str, __v:str) -> None:
        """
        It adds the given value at the given key. 
        If language, it also updates _language and overwrites the .ini file

        INPUT:
        - __k [str]             -> key used to refear at the value
        - __v [str|int|float]   -> value of the key
        """
        
        super().__setitem__(__k,__v)
        self.__write()

    def __missing__(self, __k:str) -> int:
        """
        when using dict.__getitem__ if the given key __k element is not in dict
        it returns None.
        It should be used only for language...

        INPUT:
        - __k [str]     -> is the key of the dict
        """

        return 0

    def set_pos(self, x:int, y:int) -> None:
        """
        it will save the position of the window in the form of x,y

        INPUT:
        - x [int]     -> is the horizontal distance 
                         for the upper left corner of the window
        - y [int]     -> is the vertical distance 
                         for the upper left corner of the window
        """

        self.__setitem__(self.__key[0],self.__dim.format(x,y))

    def set_res(self, w:int, h:int) -> None:
        """
        it will save the dimensions of the window in the form of w,h

        INPUT:
        - w [int]     -> is the width of the window
        - h [int]     -> is the height of the window
        """

        self.__setitem__(self.__key[1],self.__dim.format(w,h))

    def reset_pos(self) -> None:
        """
        it will reset dimensions and position of the window
        """

        self.__setitem__(self.__key[0], self.__val[0])
        self.__setitem__(self.__key[1], self.__val[1])

class Screen:
    # This object is used to contain the screen surface in a mutable object 
    # and it has some function to it related that I uses very often
    
    __slots__ = (
        '__clock',       # [pygame.time.Clock]   -> this pygame object is used
                        #                           just to limit the fps
        '__screen',      # [pygame.Surface]      -> this Surface is the one 
                        #                           taken as reference by
                        #                           pygame.display
        '__settings',    # [INI]                 -> it contains all the settings
        '__len',         # [int]                 -> is is the number of displays
                        #                           attached to the pc
        '__win1_x',      # [int]                 -> it is the width of the first
                        #                           display
        '__win1_y',      # [int]                 -> it is the height of the
                        #                           first display
        '__wintot_x',    # [int]                 -> it is the width of the
                        #                           full complex of displays
        '__wintot_y',    # [int]                 -> it is the height of the 
                        #                           full complex of displays
        )

    minx = 480          # [int]                 -> minimum width of the screen
                        #                           the program can take
    miny = 360          # [int]                 -> minimum height of the screen
                        #                           the program can take
    _mins = (minx,miny) # [tuple[int,int]]      -> minimum dimension of the
                        #                           screen the program can take

    def __init__(self, settings:INI) -> None:
        """
        This funcuntion will initialize the screen object with some function
        taken by ctypes
        """

        self.__settings = settings

        # the get_desktop_sizes returns a list of the siszes for each dispaly,
        # but the overall taken screen display is different. idkw tho
        self.__len = len(pygame.display.get_desktop_sizes()) 

        from ctypes import windll
        #getting the screen sizes
        GetSystemMetrics = windll.user32.GetSystemMetrics
        self.__win1_x =  GetSystemMetrics(0)
        self.__win1_y =  GetSystemMetrics(1)
        self.__wintot_x = GetSystemMetrics(78)
        self.__wintot_y = GetSystemMetrics(79)

        #it creates the screen for the first time
        self.position_screen()

        if settings["full_screen"]:
            windll.user32.ShowWindow(pygame.display.get_wm_info()['window'], 3)

        self.__screen.fill(pygame.Color("black"))
        pygame.display.flip()

        # setting the clock
        self.__clock = pygame.time.Clock()

    def position_screen(self) -> None:
        """
        This function creates a new screen with the correct settings
        
        INPUT:
        - full [bool]   -> if True, the screen will be fullscreen, otherways a
                            new screen will be created with the right 
                            dimensions and positions
        """

        #getting the setting values
        pos = list(map(int,self.__settings["pos"].split(",")))
        width,height = map(int,self.__settings["resolution"].split(","))
        
        #checking every setting is right
        #width and height have to be greater than the minimum values
        if width<=self.minx:

            if height<=self.miny:
                width, height = self.minx,self.miny
            else:
                width = self.minx

            self.__settings.set_res(width,height)

        elif height<=self.miny:
            height = self.miny
            self.__settings.set_res(width,height)

        # The positioning of the window on the screen has at least to be
        # with the upper left corner in on of the displays
        if pos[0]>self.__wintot_x or pos[1]>self.__wintot_y or \
            (self.__len>1 and (\
                (pos[0]>self.__win1_x*2 and self.__win1_x*2==self.__wintot_x)\
                    or\
                (pos[1]>self.__win1_y*2 and self.__win1_y*2==self.__wintot_y)
            )):

            self.__settings.reset_pos()
            width,height = map(int,self.__settings["resolution"].split(","))

        #setting the window position (suposing it is changed)
        environ['SDL_VIDEO_WINDOW_POS'] = self.__settings["pos"]

        #creating a dummy window 
        #(it is used for solve some random bug when resizing)
        pygame.display.set_mode((width, height),pygame.RESIZABLE)

        #saving the new window
        self.__screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)

    def get_rect(self, *args, **kwargs) -> pygame.Rect:
        '''
        Standard function for pygame.Surface, it return the sizes of the screen
        It is possible to pass get_rect arguments, but isn't recomanded
        
        OUTPUT:
        - pygame.Rect -> is the rect of the object
        '''
        
        return self.__screen.get_rect(*args, **kwargs)

    def copy(self):
        return self.__screen.copy()

    def draw(self, ob:object, *_others) -> None:
        """
        This function will use the draw function of one,
        or for each object, on the screen

        INPUT:
        - object(s) to be drawn
        """
        
        ob.draw(self.__screen)
        for _o in _others:
            _o.draw(self.__screen)
    
    def blit(
        self,
        surfpos:tuple[pygame.Surface,tuple[float,float]|pygame.Rect],
        *_others
        ) -> None:
        """
        This function will use the blit function of the screen to one, or more,
        Surface by the given position

        INPUT:
        - [tuple[pygame.Surface,tuple[int,int]] -> the Surface wil be blitted
                                                    on the screen on the 
                                                    tuple[int, int] position
        """
        
        self.__screen.blit(*surfpos)
        for _o in _others:
            self.__screen.blit(*_o)

    def fill(self, color:pygame.Color) -> None:
        """
        This function will use the fill function of the screen surface
        to fill it by the given color

        INPUT:
        - [pygame.Color]    -> color used to fill the screen
        """
        
        self.__screen.fill(color)

    def tick(self, fps:int=60) -> None:
        """
        This function is used to make shure the program runs at 60 fps!
        It is possible to edit the fps counter but isn't recomended
        """
        
        self.__clock.tick(fps)

    def quit(self) -> None:
        """
        This function saves the current achievemnt and quits
        """

        pygame.quit()
        sysexit(0)

class Music:

    @staticmethod
    def returnNone(*args,**kwargs):
        return None
    
    @staticmethod
    def __check(func):

            def checker(self,*args,**kwargs):
                try:
                    return func(self,*args,**kwargs)
                except:
                    self.breaker()
            
            return checker

    @__check
    def __init__(self) -> None:
        self.__channel=None
        import pygame._sdl2 as sdl2
        sdl2.get_audio_device_names(False)
        pygame.mixer.set_num_channels(1)
        self.__channel = pygame.mixer.Channel(0)
        self.__volume=0.1
        self.__channel.set_volume(self.__volume)
        self.__works=True

    def __bool__(self)->bool:
        return self.__works

    def breaker(self):
        if self.__channel and self.__channel.get_busy():
            self.__channel.stop()
        self.__channel = None
        self.__works = False
        self.start = self.returnNone
        self.stop = self.returnNone
        self.up = self.returnNone
        self.down = self.returnNone
    
    @__check
    def start(self,sound:pygame.mixer.Sound):
        self.__channel.play(sound)
    
    @__check
    def stop(self):
        if self.__channel and self.__channel.get_busy():
            self.__channel.stop()
    
    @__check
    def up(self):
        self.__volume=min(self.__volume+0.05,1)
        self.__channel.set_volume(self.__volume)
    
    @__check
    def down(self):
        self.__volume=max(self.__volume-0.05,0)
        self.__channel.set_volume(self.__volume)

class Booleans(list):
    #It will be used to check that every screen format is right & working well

    __slots__ = (
        '__screen',     # [Screen]          -> it is the screen object
        '__settings',   # [INI]             -> it is the settings object
        )

    def __init__(self, screen:Screen, settings:INI) -> None:
        """
        It initializes the object so that its elements are:
         - loop             [bool]          -> it is used to check the main
                                                (event-list/billting) loop
         - visualrestart    [bool]          -> it is used to check the screen
                                                sizes changed (refresh) loop
         - windowmoving     [bool]          -> it is used to check the screen
                                                may has being moved
                                                It is True if it is
         - windowsizing     [bool]          -> it is used to check the screen
                                                may has being maximized
                                                It is True if it is NOT
         - list to restart  [tuple[int]]    -> it is used to remembers if in
                                                another page the 
                                                sizes/languages changed: 
                                                False if not; 
                                                True if visualrestart

        INPUT:
        - screen            [Screen]        -> screen object
        - settigns          [INI]           -> settings object
        """
        
        self.__screen = screen
        self.__settings = settings

        super().__init__((True,True,False,False,[]))

    def add(self) -> None:
        """
        This function is called to cad a 0 to booleans[-2].
        If this number is changed, the window has to be refreshed:
        1 -> every object,
        2 -> texts + 1
        """
        
        self[-1].append(False)
        self[0]=False

    def replace(self) -> None:
        """
        This function is called to change the number
        for each element in booleans[-1] if smaller

        INPUT:
        - reset [int]   -> 1 will be interpreted as 
                            "every object has to be refreshed"
                        -> 2 will be interpreted as 
                            "every used text has to be uptated + 1
        """

        for i in range(len(self[-1])):
            if not self[-1][i]:
                self[-1][i]=True

    def end(self) -> None:
        """
        This function is called to remove the last element of booleans[-2]
        """

        self[-1].pop()
        self[0] = True

    def breaker(self) -> None:
        """
        This function is called to stop the actual cycle
        """

        self[0] = False

    def update_changing(self, event_list:list[pygame.event.Event]) -> None:
        """
        It is called before everythingelse to the type of window modification

        INPUT:
        - event_list [list[pygame.event.Event]] -> it contains every event
        """

        if self.check_1(pygame.WINDOWMAXIMIZED, event_list):
            self[3] = self[2] = False
            self.__settings['full_screen']=1
            return
        elif self.check_1(pygame.WINDOWRESTORED, event_list):
            self.__settings['full_screen']=0


        if self.check_1(pygame.WINDOWSIZECHANGED, event_list):
            if self.check_1(pygame.WINDOWRESIZED, event_list) and self.check_1(pygame.VIDEORESIZE, event_list):
                self[3] = self[2] = True
                return
            self[3] = self[2] = False
            return
        self[3] = False
        self[2] = True

    def update_start(
        self,
        event_list:list[pygame.event.Event],
        esc:bool=False
        ) -> None:
        """
        It is called before everythingelse to check if the close button is pressed 

        INPUT:
        - event_list [list[pygame.event.Event]] -> it contains every event
        """

        if self.check_1(pygame.QUIT, event_list):
            self.__screen.quit()
        elif esc and self.check_k(pygame.K_ESCAPE, event_list):
            pygame.mouse.set_cursor(*pygame.cursors.Cursor(0))
            self.breaker()
        self.update_changing(event_list)

    def update_resizing(self, event:pygame.event.Event) -> None:
        """
        It is called to check if the window has being resized

        INPUT:
        - event [pygame.event.Event] -> event of the for loop
        """

        #it checks the position of the window has changed
        if self[2] and event.type == pygame.WINDOWMOVED:
              self.__settings.set_pos(event.x,event.y)

        #it checks the size of the window has changed
        elif event.type == pygame.WINDOWSIZECHANGED:
            self[1] = True
            if self[3]:
                self.__settings.set_res(
                    max(event.x,self.__screen.minx),
                    max(event.y,self.__screen.miny)
                    )
            if event.x<self.__screen.minx or event.y<self.__screen.miny:
                self.__screen.position_screen()
            self.replace()

    def update_booleans(self) -> None:
        """
        This function is used to handle the resources of the booleans variables
        """
        
        if self[-1][-1]:
            self[1] = True
            self[-1][-1] = False

    @staticmethod
    def check_1(to_what:int, event_list:list[pygame.event.Event])->bool:
        """
        it will check that in the event_list if to_what event is present

        INPUT:
        - to_what [int]                         -> event it is wanted to check
        - event_list [list[pygame.event.Event]] -> it contains every event
        """

        return any(el.type==to_what for el in event_list)
        
    @staticmethod
    def check_s(to_what:tuple[int], event_list:list[pygame.event.Event])->bool:
        """
        it will check that in the event_list if one of to_what event is present

        INPUT:
        - to_what [tuple[int]]                  -> events are wanted to check
        - event_list [list[pygame.event.Event]] -> it contains every event
        """
        
        return any(el.type in to_what for el in event_list)

    @staticmethod
    def check_k(to_what:int, event_list:list[pygame.event.Event])->bool:
        """
        it will check if to_what keyword is in the event_list

        INPUT:
        - to_what [int]                         -> event key is wanted to check
        - event_list [list[pygame.event.Event]] -> it contains every event
        """

        return any(
            event.key == to_what for event in event_list
            if event.type == pygame.KEYDOWN
            )

    @staticmethod
    def check_g(
        to_what:int, 
        what:str,
        tp:int,
        event_list:list[pygame.event.Event]
        ) -> bool:
        """
        it will check generic statuses for events

        INPUT:
        - to_what [int]                         -> event key is wanted to check
        - what [str]                            -> event attribute is wanted to
                                                    check with to_what
        - tp [int]                              -> type of event that has the
                                                    given what attribute
        - event_list [list[pygame.event.Event]] -> it contains every event
        """
        
        tt = lambda event: event.type == tp
        t = lambda event: getattr(event,what)==to_what
        return any(t(event) for event in event_list if tt(event))

class Utilities:
    magic = "./Font/KazukiReiwa - Regular.ttf"
    corbel = 'Corbel'

    __slots__ = (
        'decoder',
        'your_project_cx',
        'your_dev_api_key',
        'colors',
        'settings',
        'screen',
        'booleans',
        'showError',
        'music'
        )

    def __init__(self) -> None:
        # getting some things someway
        standard = ENV()
        # setting the settings
        self.decoder = standard["decode"]
        self.your_project_cx = standard["your_project_cx"]
        self.your_dev_api_key = standard["your_dev_api_key"]
        self.colors = Colors()
        self.settings = INI(self.decoder)
        if self.settings["night_mode"]:
            self.colors.reverse()
        self.screen:Screen = None
        self.booleans:Booleans = None
        self.showError:ErrorScreen.showError = None
        self.music:Music= None

    def init(self)->None:
        pygame.init()
        pygame.fastevent.init()

        # maybe it's not the best name for the window, I'll go with it for now
        pygame.display.set_caption("Rinomina Canzoni","RC")

        # Selecting the icon img
        pygame.display.set_icon(pygame.image.load('.\Images\Rinomina.png'))

        # creating the window and the booleans list
        self.screen = Screen(self.settings)
        self.booleans = Booleans(self.screen, self.settings)
        self.showError = ErrorScreen(self).showError
        self.music = Music()

        # Just to allow to ctrl-c/v/x in Textbox
        pygame.scrap.init()

    def color_reverse(self)->None:
        self.settings["night_mode"]=int(not self.settings["night_mode"])
        self.colors.reverse()
        self.booleans[1]=True
        self.booleans[0]=False

    @staticmethod
    def filename(name:str) -> str:
        for c in '/\\"?*:<>|':
            if c in name:
                name = name.replace(c,"")
        return name

    @staticmethod
    def superfunc(func:callable, args:tuple) -> callable:
        """
        This function returns a new function with the arguments in itself.
        It will be possible to pass more arguments if needed
        
        INPUT:
        - func [callable]       -> function to call
        - args [tuple]          -> the needed arguments for the given
                                    function func to work 
        
        OUTPUT:
        - midfunc [callable]    -> this is a function that when called,
                                    passes to func all the args
        """

        def midfunc(*arg):
            midfunc.func(*midfunc.args,*arg)
        midfunc.func = func
        midfunc.args = args
        return midfunc

#checking where the program is starting from 
if not sysexecutable.endswith("python.exe"):

    k = osdirname(sysexecutable)
    if osabspath(".") != k:
        oschdir(k)
    
    from sys import path as syspath
    if not k in syspath:
        syspath.append(k)
    
utilities = Utilities()


class ScrollingSurface(pygame.sprite.Sprite):
    # pygame sprite to handle a text that should be scrolling on the screen

    __slots__ = (
        "__surf",    # [pygame.Surf]     -> full text
        "__rect",       # [pygame.Rect]     -> of "__surf"
        "__rect_x",     # [int]             -> init  x position of the image rect
        "__surf_x",     # [int]             -> x position where to extract the
                        #                       subsurface from "__surf"
        "__mod_x",      # [int]             -> x position where to place the
                        #                       extracted subsurface on the
                        #                       screen
        "__frame",      # [int]             -> counts the frames the surface is
                        #                       in stopped
        "__width",      # [float|int]       -> is the lenght of the space
                        #                       __surf is suppose to be
                        #                       scrolled
        "__pause",      # [int]             -> the number of __frame __surf
                        #                       is in pause
        '__need_sub',   # [bool]            -> is True if __surf is longer
                        #                       than __width
        '__length',     # [int]             -> is the lenght of the subsurface
                        #                       is wanted to be extracted from
                        #                       __surf
        'image',        # [pygame.Surf]     -> the resulted image is wanted to
                        #                       be blit on the screen
        'rect'          # [pygame.Rect]     -> rect of the dimensions of the
                        #                       text is showed
        )

    def __init__(self, pause:int=105, *args, **kwargs) -> None:
        '''
        Initializating the class to have a the scrolling text.
        After, init_rect() has to be called
        
        INPUT:
        - w [float|int]                 -> int the width of the space we want
                                            to show the string
        - text_surf [pygame.Surface]    -> the rendered text is wanted to be
                                            shown (could be anything)
        - pause [int]                   -> is the amount of frames is wanted
                                            to wait until starting scrolling 
        '''

        # initialising basic stuff
        super().__init__(*args, **kwargs)
        self.__pause = pause
        
        self.__surf_x = self.__mod_x = self.__frame = 0
        self.__rect_x = self.__length = self.__width = 0
        self.__need_sub = True

        self.__surf:pygame.Surface = None
        self.__rect: pygame.Rect = None

        self.image:pygame.Surface = None
        self.rect: pygame.Rect = None

    def get_rect(self) -> pygame.Rect:
        '''
        Standard function for pygame.Surface,
        but in the right position in the screen
        
        OUTPUT:
        - pygame.Rect -> is the rect of the object
        '''

        return self.rect

    def init_rect(self,**kwargs) -> pygame.Rect:
        '''
        it calls the standard function for pygame.Surface
        and passes to it all the arguments
        
        INPUT:
        - **kwargs    -> syntax for pygame.Surf().get_rect()
        
        OUTPUT:
        - pygame.Rect -> is the rect of the object
        '''

        self.rect = self.image.get_rect(**kwargs)
        self.__rect_x = self.rect.x
        return self.rect

    def update(self, *_) -> None:
        '''
        it update the state of the object
        
        INPUT:
        - *_    -> nothing is needed
        '''

        #it change nothing if the text doesn't change
        if self.__need_sub:

            if self.__surf_x == 0 and self.__length < self.__width:
                # PHASE 4
                # the text is showing from the right, not \w the full lenght __width
                self.__length += 1
                self.__mod_x -= 1

            elif self.__length == self.__width and self.__frame <= self.__pause:
                # PHASE 0
                # the start point text is on the left and it is in pause
                self.__frame += 1

            elif self.__length == self.__width\
                and\
                self.__surf_x+self.__length < self.__rect.w:
                # PHASE 1
                # the text is scrolling outide to the left until
                # it is possible to keep __length equals to __width
                self.__surf_x += 1

            elif self.__length < 1:
                # PHASE 3
                # it happens only once per cycle:
                # it reset the position all the way on the right for 1 pixel
                self.__surf_x = 0
                self.__mod_x = self.__width-1

            else:
                # PHASE 2
                # the text complitely fiding away on the left
                self.__surf_x += 1
                self.__length -= 1
                if self.__frame != 0:
                    self.__frame = 0

            # just setting the image and its position
            self.image = self.__surf.subsurface(
                self.__surf_x,
                0,
                self.__length,
                self.__rect.h
                )

            # updates the position and sizes of the rect
            self.rect.x = self.__rect_x + self.__mod_x
            # self.rect.w=self.__length

    def draw(self, screen:pygame.Surface) -> None:
        """
        It draws the buttons on the given surface with its
        corresponding rect position

        INPUT: 
         - screen [pygame.Surface]  -> surface where to blit the button
        """

        screen.blit(self.image, self.rect)

    def restart(self) -> None:
        """
        This function is used to restart the animation if needed
        """

        self.__surf_x = self.__mod_x = self.__frame = 0
        self.__length = self.__width

    def refresh(self, w:float|int, text_surf:pygame.Surface) -> None:
        '''
        This function let re-use the same object
        without creating a new one when resizing the screen
        After, init_rect() has to be called
        
        INPUT:
        - w [float|int]                 -> int the width of the space we want
                                            to show the string
        - text_surf [pygame.Surface]    -> the rendered text is wanted to be
                                            shown (could be anything)
        '''
        
        #setting these variables
        self.__surf = text_surf
        self.__rect = text_surf.get_rect()
        self.__surf_x = self.__mod_x = self.__frame = 0 
        self.__width = w

        # want to compute the scrolling only if the text_surf is longer that the w
        if self.__rect.w>w:
            self.__need_sub = True
            self.__length = w
            self.image = self.__surf.subsurface((self.__frame, self.__frame, w, self.__rect.h))
        else:

            self.__need_sub = False
            self.image = self.__surf

class NormalButton(pygame.sprite.Sprite):
    # pygame sprite to handle how a button should behave
    
    __slots__ = (
        '_surf',       # [pygame.Surf]         -> text to blit on the
                            #                           button
        '_normal',    # [pygame.Surf]         -> shape of the button
                            #                           in normal state
        '_hovered',     # [pygame.Surf]         -> shape od the button
                            #                           in hover state
        '_clicked',   # [pygame.Surf]         -> shape of the button
                            #                           in clicked state
        '_colors',          # [tuple[str,str,str]]  -> the choosed colors as
                            #                           (bt_normal_color,
                            #                           bt_hover_color,
                            #                           bt_pressed_color)
        '_is_clicked',         # [bool]                -> says if the button is
                            #                           clicked
        'func',             # [callable]            -> the function that is
                            #                           called when the button
                            #                           is released after
                            #                           clicked
        '_is_hovered',         # [bool]                -> says if the mouse is
                            #                           hovering over the
                            #                           button
        'image',            # [pygame.Surf]         -> image shown after the
                            #                           button state is updated
        'rect',             # [pygame.Rect]         -> rect of the dimensions
                            #                           of the button
        '_scrolls'        # [None|ScrollingSurface]  -> if ScrollingSurface, is
                            #                           replaced by Group and
                            #                           it will be updated
        )

    button_space = 4        # [int]                 -> total space around the
                            #                           plain text
                            #                           (to apllay the border)

    def __init__(
        self,
        bt_normal_color:str='gray',
        bt_hover_color:str='light_blue',
        bt_pressed_color:str='dark_blue',
        func:callable=None,
        func_args:tuple=(),
        utilities: Utilities=utilities,
        *args,
        **kwargs
        ) -> None:
        '''
        Initializating the class to have a button with text.
        After init_rect() has to be called,
        and, to positionate accordingly the text_surf,
        also text_rect() has to be called
        
        INPUT:
        - w_min [float|int]             -> value to get the min lenght of the
                                            button; its height would be the
                                            surface
        - text_surf [pygame.Surface]    -> the rendered text is wanted to be
                                            shown (could be anything)
        - w_max [float|int]             -> value of lenght max of the button:
                                            if greater than 0 and
                                            less than text_surf's lenght,
                                            the text_surf will be replaced by
                                            scrollingtext
        - h_min [float|int]             -> value to get the min height of the
                                            button
        - bt_normal_color [str]         -> color of the button in normal state
        - bt_hover_color [str]          -> color of the button in hovered state
        - bt_pressed_color [str]        -> color of the button in clicked state
                                            and as border in hovered state
        - func [callable|None]          -> function called when the button is
                                            clicked (the click has to uppered
                                            while hovering)
        - args [tuple]                  -> the args the function needs
        - booleans [Boleans]            -> the Booleans variable used for one
                                            little check
        - colors [Colors]               -> the Colors used for the image
        '''

        # initializing the sprite class
        super().__init__(*args, **kwargs)

        #setting the function
        if func is None:
            self.func = func
        else:
            self.func = utilities.superfunc(func,func_args)

        self._colors = (bt_normal_color, bt_hover_color, bt_pressed_color)

        self._scrolls:ScrollingSurface = None
        self._surf:pygame.Surface = None
        self._normal:pygame.Surface = None
        self._hovered:pygame.Surface= None
        self._clicked:pygame.Surface = None

        self._is_clicked = self._is_hovered = False

        self.image:pygame.Surface = None
        self.rect:pygame.Rect = None

    def refresh(
        self,
        surf:pygame.Surface,
        w_min:float=0,
        w_max:float=0,
        h_min:float=0,
        colors: Colors=utilities.colors
        ) -> None:
        '''
        This function let re-use the same button without creating a new one
        when resizing the screen. After init_rect() has to be called,
        and, to positionate accordingly the text_surf,
        also text_rect() has to be called
        
        INPUT:
        - w_min [float|int]             -> value to get the min lenght of
                                            the button; its height would be the
                                            surface 
        - text_surf [pygame.Surface]    -> the rendered text is wanted to be
                                            shown (could be anything)
        - w_max [float|int]             -> value to get the max lenght of the
                                            button, if greater than 0 and less
                                            than text_surf's lenght, 
                                            the text_surf will be replaced by 
                                            scrollingtext
        - h_min [float|int]             -> value to get the min height of the
                                            button
        - colors [Colors]               -> the Colors used for the image
        '''

        # setting the size of the button based on the given rendered text
        # options, I think it's pretty clear... isn't it?
        self._surf = surf
        surf_w,surf_h = surf.get_size()

        #getting the height of the button
        w = max(w_min, surf_w+self.button_space)
        h = max(h_min, surf_h+self.button_space)

        if w_max and w>w_max:
            if self._scrolls is None:
                self._scrolls = ScrollingSurface()
            self._scrolls.refresh(w_max-self.button_space, surf)
            t_size = (w_max, h)
        else:
            self._scrolls = None
            t_size = (w, h)

        # we prepare the sprite of the button if in normal state
        self._normal = pygame.Surface(t_size)
        self._normal.fill(colors[self._colors[0]])

        # we prepare the sprite of the button if in 'hover' state
        self._hovered = pygame.Surface(t_size)
        self._hovered.fill(colors[self._colors[1]])
        pygame.draw.rect(
            self._hovered,
            colors[self._colors[2]],
            self._hovered.get_rect(),
            self.button_space//4*3
            )

        # we prepare the sprite of the button if in clicked state
        self._clicked = pygame.Surface(t_size)
        self._clicked.fill(colors[self._colors[2]])
            
        # These are infos property needed to make the Sprite class work 
        # as expected
        self.image = self._normal.copy()
        self.rect = None

    def __bool__(self) -> bool:
        """
        Returns the value of 'clicked' -> is True if the mouse has clicked on
        the button but isn't released yet

        OUTPUT:
         - [bool] -> True if the button is in the clicked state
        """

        return self._is_clicked

    def get_rect(self) -> pygame.Rect:
        '''
        Standard function for pygame.Surface,
        but in the right position in the screen
        
        OUTPUT:
        - [pygame.Rect] -> is the rect of the object
        '''

        return self.rect

    def _set_image(self, hover:bool, *_) -> None:
        """
        This function is called from the update function update the image
        of the button

        INPUT: 
         - hover [bool] -> True if the mouse hovers the button.
                            If it's True for the first time, a sound is played.
        """

        # if the button is clicked, sets its image is in clicked state and
        # calls the function
        if self._is_clicked:
            self.image = self._clicked.copy()

        # if the button is only hovered, its image is in hover state
        elif hover:
            self.image = self._hovered.copy()

            # it plays a sound if it is the first time the button is overed
            if not self._is_hovered:
                self._is_hovered = True

        # it could've be eampty, but this way we set the hovered setting
        # to false only one time
        elif self._is_hovered:
            self._is_hovered = False

    def _set(self) -> None:
        """
        Initialize the image of the button in normal state
        """

        self.image = self._normal.copy()

    def update(
        self,
        event_list:list[pygame.event.Event],
        pos:tuple[int,int],
        hover:bool=True
        ) -> None:
        """
        It checks every event to update the button 

        INPUT: 
         - event_list [list[pygame.event.Event]]    -> list of all the events
                                                        from the program.
         - pos [tuple[int,int]]                     -> position of the mouse
        """

        # It checks the collision of the mouse with the button
        hover &= self.rect.collidepoint(pos)

        # It checks every event given from the pc
        for event in event_list:
            # It checks if the button is clicked
            if hover and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._is_clicked = True

            # It checks if the clicked is released
            elif self._is_clicked and event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if hover and self.func is not None:
                        self.func()
                    self._is_clicked = False
            
        # It checks if the button is clicked
        if self._scrolls is not None:
            self._scrolls.update(event_list)
                    
        # initialize the image of the button as in normal state
        self._set()
        self._set_image(hover,pos)

        # drawing the _scrolls text on the buttons if is needed
        if not self._scrolls is None:
            self._scrolls.draw(self.image)

    def draw(self, screen:pygame.Surface) -> None:
        """
        It draws the buttons on the given surface with its corresponding
        rect position

        INPUT: 
         - screen [pygame.Surface]  -> surface where to blit the button
        """

        screen.blit(self.image, self.rect)

    def init_rect(self, **kwargs) -> pygame.Rect:
        '''
        it calls the standard function for pygame.Surface and passes to it
        all the arguments
        
        INPUT:
        - **kwargs      -> syntax for pygame.Surf().get_rect()
        
        OUTPUT:
        - [pygame.Rect] -> is the rect of the object
        '''

        self.rect = self.image.get_rect(**kwargs)
        return self.rect

    def text_rect(self, position:str='center') -> None:
        '''
        it calls the standard function for pygame.Surface using the given key
        as argument. It will place the text as requested on the button
        
        INPUT:
        - position [str]    -> key for get_rect() in standard pygame.Surface
        '''
        
        t = self._normal.get_rect().inflate(-self.button_space,-self.button_space)
        
        if self._scrolls is None:
            #placing the text on the button
            
            r = self._surf.get_rect(**{position:t.__getattribute__(position)})
            self._normal.blit(self._surf, r)
            self._hovered.blit(self._surf, r)
            self._clicked.blit(self._surf, r)

        else:
            #setting the scrolling text on the button
            self._scrolls.init_rect(**{position:t.__getattribute__(position)})

        self.image = self._normal

    def copy(self) -> pygame.Surface:
        '''
        Standard function for pygame.Surface
        
        OUTPUT:
        - [pygame.Surface]  -> is the copy image of the button in normal state
        '''

        return self._normal.convert()

    def copy_alpha(self) -> pygame.Surface:
        '''
        Standard function for pygame.Surface
        
        OUTPUT:
        - [pygame.Surface]  -> is the alphed copy image of the button
                                in normal state
        '''

        return self._normal.convert_alpha()

    def copy_deactivated(self,alpha=150) -> pygame.Surface:
        '''
        It uses the Standard function for pygame.Surface
        
        OUTPUT:
        - [pygame.Surface]  -> is the copy image of the button in normal state,
                                but a little fogged (?)
        '''

        t = self.copy_alpha()
        t.set_alpha(alpha)
        return t

    def displayer(self) -> pygame.Rect:
        """
        It returns the rect of this object but inflated, by 2 px for each line
        
        OUTPUT:
        - [pygame.Rect] -> is the inflated rect of the object
        """
        
        return self.rect.inflate(self.button_space,self.button_space)

class CheckButton(NormalButton):
    # pygame sprite to handle how a checkbutton should behave

    __slots__ = ("_state")  # [bool]    -> True if is clicked,
                            #               False if unclicked

    def __init__(
        self,
        state:bool=False,
        bt_normal_color:str='gray',
        bt_hover_color:str='light_blue',
        bt_pressed_color:str='dark_blue',
        func:callable=None,
        func_args:tuple=(),
        utilities: Utilities=utilities,
        *args,
        **kwargs
        ) -> None:
        '''
        Initializating the class to have a check button. 
        After init_rect() has to be called
        
        INPUT:
        - w [float|int]             -> value to get the square dimensions of
                                        the button
        - state [bool]              -> value to decide if the button is
                                        clicked or not from start
        - bt_normal_color [str]     -> color of the button in normal state
        - bt_hover_color [str]      -> color of the button in hovered state
        - bt_pressed_color [str]    -> color of the button in clicked state 
                                        and as border in hovered state
        - func [callable|None]      -> function called when the button is
                                        clicked (the click has to uppered
                                        while hovering)
        - args [tuple]              -> the args the function needs
        - booleans [Boleans]        -> the Booleans variable used for one
                                        little check
        - colors [Colors]           -> the Colors used for the image
        '''

        # initializing the NormalButton class. It will be a little box:
        # there is no need for text
        if func is None:
            super().__init__(
                bt_normal_color,
                bt_hover_color,
                bt_pressed_color,
                self._select,
                utilities= utilities,
                *args,
                **kwargs
                )
        else:
            super().__init__(
                bt_normal_color,
                bt_hover_color,
                bt_pressed_color,
                lambda *x:self._both(func,*x),
                func_args,
                utilities,
                *args,
                **kwargs
                )

        # This is info property of the button used to make the
        # animation happen with "update"
        self._state = state

    def text_rect(self) -> None:
        """
        THIS FUNCTION IS USELESS
        """

        return

    def refresh(self, w:int, colors: Colors=utilities.colors) -> None:
        '''
        This function let re-use the same button without creating a new one
        when resizing the screen. After init_rect() has to be called
        
        INPUT:
        - w [float|int]             -> value of the width and height of the
                                        button
        - bt_normal_color [str]     -> color of the button in normal state
        - bt_hover_color [str]      -> color of the button in hovered state
        - bt_pressed_color [str]    -> color of the button in clicked state
                                        and as border in hovered state
        - colors [Colors]           -> the Colors used for the image
        '''

        super().refresh(
            pygame.Surface((1,1)),
            w+self.button_space,
            0,
            w+self.button_space,
            colors=colors
            )

    def __bool__(self) -> bool:
        """
        It overwrites Normalbutton's and returns the value of 'state'
        """

        return self._state

    def _both(self, func:callable, *args:tuple) -> None:
        '''
        It let call both the given function and also _select
        
        INPUT:
        - func [callable|None]      -> function called when the button is
                                        clicked (the click has to uppered
                                        while hovering)
        - args [tuple]              -> the args the function needs
        '''

        func(*args)
        self._select()

    def _select(self) -> None:
        """
        This function will reverse the state of the button.
        It is called from the update function in self.func
        """

        self._state = not self._state

    def _set(self) -> None:
        """
        Initialize the image of the button in normal state
        """

        if self._state:
            self.image = self._clicked
        else:
            self.image = self._normal

class RadioButton(CheckButton):
    # pygame sprite to handle how a radiobutton should behave

    __slots__ = (
        "_value",   # [str]                 -> is what the state's button
                    #                           refears to
        "_buttons"  # [list[RadioButtons]]  -> contains all the radiobuttons
                    #                           of the group
        )

    def __init__(
        self,
        value:str,
        state:bool=False,
        bt_normal_color:str='gray',
        bt_hover_color:str='light_blue',
        bt_pressed_color:str='dark_blue',
        func:callable=None,
        func_args:tuple=(),
        utilities: Utilities=utilities,
        *args,
        **kwargs
        ) -> None:
        '''
        Initializating the class to have a radio button. 
        After init_rect() has to be called
        
        INPUT:
        - w [float|int]             -> value to get the square dimensions
                                        of the button
        - value [str]               -> value that is what the state's button
                                        refears to
        - state [bool]              -> value to decide if the button is clicked
                                        or not from start
        - bt_normal_color [str]     -> color of the button in normal state
        - bt_hover_color [str]      -> color of the button in hovered state
        - bt_pressed_color [str]    -> color of the button in clicked state
                                        and as border in hovered state
        - func [callable|None]      -> function called when the button is
                                        clicked (the click has to uppered
                                        while hovering)
        - args [tuple]              -> the args the function needs
        - booleans [Boleans]        -> the Booleans variable used for one
                                        little check
        - colors [Colors]           -> the Colors used for the image
        '''

        # initializing the NormalButton class. It will be a little box:
        # there is no need for thext
        if func is None:
            super().__init__(
                state,
                bt_normal_color,
                bt_hover_color,
                bt_pressed_color,
                func,
                utilities= utilities,
                *args,
                **kwargs
                )
        else:
            super().__init__(
                state,
                bt_normal_color,
                bt_hover_color,
                bt_pressed_color,
                lambda *x:func(self._value,*x),
                func_args,
                utilities,
                *args,
                **kwargs
                )
        
        # This is info property of the button used to make the animation
        # happen with "update"
        self._value = value
        self._buttons:list[RadioButton] = None

    def __str__(self) -> str:
        """
        It returns the value
        """

        return self._value

    def _select(self) -> None:
        """
        It overwrite Checkbuton's to update the state of all the button group.
        It is called from the update function in self.func
        """

        if not (self._buttons is None):
            for i in self._buttons:
                i._state = i==self

    def setRadioButtons(self, buttons:list) -> None:
        """
        This function sets the given buttons as the radiobuttons group

        INPUT: 
         - buttons [list[RadioButton,...]]  -> list of all the buttons I want to
                                                have the "radio" meaning
        """

        self._buttons= buttons

    def getValueStateRB(self) -> dict[str,bool]:
        """
        It returns the state of each radiobutton in buttons if given,
        else return the value-state dict of this button

        OUTPUT:
         - [dict[str,bool]] -> dictonary of value:state for each button,
                                if present
        """

        if self._buttons is None:
            return {self._value:self._state}

        return dict((bb._value, bb._state) for bb in self._buttons)

    def setValueStateRB(self, value_state:dict[str,bool]) -> None:
        """
        This function is called to set the state for each button in self.button
        with each respective value

        INPUT:
         - value_state [dict[str,bool]] -> dictonary of value:state
        """

        if not (self._buttons is None):
            for i in self._buttons:
                i._state = value_state[i._value]

class ImageButton(NormalButton):
    # pygame sprite to handle any shape of button

    __slots__ = ()

    def __init__(
        self,
        bt_hover_color:str='light_blue',
        bt_clicked_color:str='dark_blue',
        func:callable=None,
        func_args:tuple=(),
        utilities: Utilities=utilities,
        *args,
        **kwargs
        ) -> None:
        '''
        Initializating the class to have a button with an image. 
        After init_rect() has to be called
        
        INPUT:
        - image [pygame.Surface]    -> any surface that will become a button
        - bt_hover_color [str]      -> color of the button in hovered state 
                                        with whuch covered the given image
        - bt_clicked_color [str]    -> color of the button in clicked state
                                        with whuch covered the given image
        - func [callable|None]      -> function called when the button is
                                        clicked (the click has to uppered
                                        while hovering)
        - args [tuple]              -> the args the function needs
        - booleans [Boleans]        -> the Booleans variable used for one
                                        little check
        - colors [Colors]           -> the Colors used for the image
        '''

        # initializing the NormalButton class.
        # It will be a little box: there is no need for thext
        super().__init__(
            func=func,
            func_args=func_args,
            utilities=utilities,
            *args,
            **kwargs
            )

        self._colors = (bt_hover_color, bt_clicked_color)

    def text_rect(self) -> None:
        """
        THIS FUNCTION IS USELESS
        """

        return

    def refresh(self, image:pygame.Surface, colors: Colors=utilities.colors):
        '''
        This function let re-use the same button without creating a new one
        when resizing the screen. After init_rect() has to be called
        
        INPUT:
        - image [pygame.Surface]    -> any surface that will become a button
        - colors [Colors]           -> the Colors used for the image
        '''

        #setting the actual images of the button
        bt_sizes=image.get_size()
        self._normal = image.copy()

        mask = pygame.mask.from_surface(image).to_surface().convert_alpha()
        mask.set_colorkey((0,0,0))
        sc = pygame.Surface(bt_sizes,pygame.SRCALPHA)
        t = (0,0)

        tem = mask.copy()
        sc.fill(colors[self._colors[0],50])
        tem.blit(sc,t,None,pygame.BLEND_RGBA_MULT)

        # transparent color to blit over the image
        self._hovered = image.copy()
        self._hovered.blit(tem,t)

        tem = mask.copy()
        sc.fill(colors[self._colors[1],50])
        tem.blit(sc,t,None,pygame.BLEND_RGBA_MULT)
    
        # transparent color to blit over the image, but it is different
        self._clicked = image.copy()
        self._clicked.blit(tem,t)

        # These are infos property needed to make the Sprite class work as expecter
        self.image = self._normal
        self.rect = None

    @classmethod
    def allImages(
        cls,
        func:callable=None,
        func_args:tuple=(),
        utilities: Utilities=utilities,
        *args,
        **kwargs
        ) -> None:
        '''
        Initializating the class to have a button with an image for each state.
        After init_rect() has to be called
        
        INPUT:
        - normal_image [pygame.Surface]     -> any surface for the button
                                                in normal state
        - hovered_image [pygame.Surface]    -> any surface for the button
                                                in hover state
        - clicked_image [pygame.Surface]    -> any surface for the button
                                                in clicked state
        - func [callable|None]              -> function called when the button
                                                is clicked (the click has to
                                                uppered while hovering)
        - args [tuple]                      -> the args the function needs
        - booleans [Boleans]                -> the Booleans variable used for
                                                onelittle check
        - colors [Colors]                   -> the Colors used for the image
        '''

        t = cls(
            func=func,
            func_args=func_args,
            utilities=utilities,
            *args,
            **kwargs
            )
        t.refresh = t.__refresh
        return t
    
    def __refresh(
        self,
        normal_image:pygame.Surface,
        hovered_image:pygame.Surface,
        clicked_image:pygame.Surface
        ) -> None:
        '''
        This function let re-use the same button without creating a new one
        when resizing the screen. After init_rect() has to be called
        
        INPUT:
        - normal_image [pygame.Surface]     -> any surface for the button
                                                in normal state
        - hovered_image [pygame.Surface]    -> any surface for the button
                                                in hover state
        - clicked_image [pygame.Surface]    -> any surface for the button
                                                in clicked state
        '''

        #setting the image for the button in normal state
        self._normal = normal_image

        #setting the image for the button in hover state
        self._hovered = hovered_image

        #setting the image for the button in clicked state
        self._clicked = clicked_image

        # These are infos property needed to make the Sprite class work as expecter
        self.image = self._normal
        self.rect = None
    
    
class LittleMenu(pygame.sprite.Sprite):
    # pygame sprite to handle the menu for the textBox object
    
    __slots__ = (
        '_active',      # [bool]        -> if True it is be used, becomes False
                        #                   when a menu's function is called
        '_copy',        # [callable]    -> function that applay copy of the
                        #                   linked textbox
        '_cut',         # [callable]    -> function that applay cut of the
                        #                   linked textbox
        '_paste',       # [callable]    -> function that applay paste of the
                        #                   linked textbox
        '_activeCopy',  # [ImageButton] -> button which uses the copy function
        '_activeCut',   # [ImageButton] -> button which uses the cut function
        '_activePaste', # [ImageButton] -> button which uses the paste function
        'image',        # [pygame.Surf] -> image shown after the button state
                        #                   is updated
        'rect',         # [pygame.Rect] -> rect of the dimensions of the button
        )

    def __init__(
        self,
        bt_hover_color:str='gray',
        bt_clicked_color:str='white',
        utilities: Utilities=utilities,
        *args,
        **kwargs
        ) -> None:
        '''
        Initializating the class to have a right-mouse-click menu.
        To use it, init() has to be called.
        
        INPUT:
        - font [pygame.font.SysFont]    -> font which how to render
                                            the strings of the littlemenu
        - bt_hover_color [str]          -> color of the button in hovered state
                                            with whuch covered the given image
        - bt_clicked_color [str]        -> color of the button in clicked state
                                            with whuch covered the given image
        - length_min [in]               -> minimum lenght of the little menu
        - booleans [Boleans]            -> the Booleans variable used for one
                                            little check
        - colors [Colors]               -> the Colors used for the image
        '''

        # initializing the sprite class
        super().__init__(*args, **kwargs)

        #setting initial value of the object
        self._active = False
        self._copy = self._cut = self._paste = None

        #defining each button for the little menu
        self._activeCopy = ImageButton(
            bt_hover_color,
            bt_clicked_color,
            self.copy_func,
            utilities=utilities
            )

        self._activeCut = ImageButton(
            bt_hover_color,
            bt_clicked_color,
            self.cut_func,
            utilities=utilities
            )

        self._activePaste = ImageButton(
            bt_hover_color,
            bt_clicked_color,
            self.paste_func,
            utilities=utilities
            )
        
        self.image:pygame.Surface = None
        self.rect:pygame.Rect = None

    def __bool__(self) -> bool:
        """
        Returns the value of _active -> is True if it is showed
        (right-mouse-click on the mouse on a TextBox)

        OUTPUT:
         - [bool] -> True if it is active
        """

        return self._active

    def refresh(
        self,
        font:pygame.font.Font,
        length_min:int=0,
        colors: Colors=utilities.colors
        ) -> None:
        '''
        This function let re-use the same button without creating a new one
        when resizing the screen
        
        INPUT:
        - font [pygame.font.Font]   -> font which how to render the strings
                                        of the littlemenu
        - length_min [int]          -> minimum lenght to get a nice little menu
        - colors [Colors]           -> the Colors used for the image
        '''
        
        #getting the text surfaces
        copy_text = font.render(
            "Copia",
            True,
            colors["black"]
            )
        cut_text = font.render(
            "Taglia",
            True,
            colors["black"]
            )
        paste_text = font.render(
            "Incolla",
            True,
            colors["black"]
            )
       
        #the max lenght to get a nice-looking little menu
        w=max(
            copy_text.get_width(),
            cut_text.get_width(),
            paste_text.get_width(),
            length_min
            )
        
        #adding some space upper for the text
        h=copy_text.get_height()+NormalButton.button_space

        #settign the image for each option of the menu
        rectangle = pygame.surface.Surface((w, h))
        sz = (w/2,h/2)
        rectangle.fill(colors["background"])
        inactiveCopy = rectangle.copy()
        inactiveCopy.blit(copy_text, copy_text.get_rect(center=sz))
        inactiveCut = rectangle.copy()
        inactiveCut.blit(cut_text, cut_text.get_rect(center=sz))
        inactivePaste = rectangle.copy()
        inactivePaste.blit(paste_text, paste_text.get_rect(center=sz))

        #defining each button for the little menu
        self._activeCopy.refresh(inactiveCopy,colors=colors)
        self._activeCopy.init_rect(x=0, y=0)
        self._activeCut.refresh(inactiveCut,colors=colors)
        self._activeCut.init_rect(x=0, y=h)
        self._activePaste.refresh(inactivePaste,colors=colors)
        self._activePaste.init_rect(x=0, y=h*2)

        self._active = False
        self._copy = self._cut = self._paste = None
        
        self.image = pygame.surface.Surface((w, h*3))
        self.rect = self.image.get_rect()

    def get_rect(self) -> pygame.Rect:
        '''
        Standard function for pygame.Surface,
        but in the right position in the screen
        
        OUTPUT:
        - [pygame.Rect] -> is the rect of the object
        '''

        return self.rect

    def init(
        self, 
        x:float,
        y:float,
        screen_rect:pygame.Rect,
        /, *,
        copy:callable=None,
        cut:callable=None,
        paste:callable=None
        ) -> None:
        '''
        Initializating the LittleMenu to place it in the right place
        with the right func.
        
        INPUT:
        - x [float|int]             -> orizontal position of the mouse
                                        when right-clicked on the textbox
        - y [float|int]             -> vertical position of the mouse
                                        when right-clicked on the textbox
        - screen_rect [pygame.Rect] -> Rect object of the full window
        - copy [callable]           -> function given by textBox for copy
                                        (put text on the "note")
        - cut [callable]            -> function given by textBox for cut
                                        (put text on the "note")
        - paste [callable]          -> function given by textBox for paste
                                        (take text from the "note")
        '''

        #restoring the mouse icon as ->
        pygame.mouse.set_cursor(*pygame.cursors.Cursor(0))

        #setting the position of the little menu
        self.rect.x=x-self.rect.w*(x+self.rect.w>screen_rect.w)
        self.rect.y=y-self.rect.h*(y+self.rect.h>screen_rect.h)

        #saving the given function
        self._copy = copy
        self._cut = cut
        self._paste = paste
            
        #setting the littlebutton to be active
        self._active = True

    def copy_func(self) -> None:
        '''
        This function is called from the copy button
        '''

        self._active=False
        self._copy()
        self._copy = self._cut = self._paste = None

    def cut_func(self) -> None:
        '''
        This function is called from the cut button
        '''

        self._active=False
        self._cut()
        self._copy = self._cut = self._paste = None

    def paste_func(self) -> None:
        '''
        This function is called from the paste button
        '''

        self._active=False
        self._paste()
        self._copy = self._cut = self._paste = None

    def update(
        self,
        event_list:list[pygame.event.Event],
        pos:tuple[int,int]
        ) -> None:
        """
        It checks every event to update all the buttons of the little menu

        INPUT: 
         - event_list [list[pygame.event.Event]]    -> list of all the events
                                                        from the program.
         - pos [tuple[int,int]]                     -> position of the mouse
        """

        #check if the mouse clicked elsewhere or the esc button is presed
        # -> it quits from the littlemenu
        if Booleans.check_g(1,'button',pygame.MOUSEBUTTONDOWN,event_list):
        # if any(event.button == 1 for event in event_list\
        #         if event.type == pygame.MOUSEBUTTONDOWN):
            if not self.rect.collidepoint(pos):
                self._active = False
                return
        elif Booleans.check_k(pygame.K_ESCAPE,event_list):
            self._active = False
            return

        # Update the buttons in the right position
        # (couse even if the little menu is on (x,y),
        # each button is in it's own palace ((0,0), (0,h) and (0,2h)))
        self._activeCopy.update(
            event_list,
            (pos[0]-self.rect.x, pos[1]-self.rect.y)
            )
        self._activeCut.update(
            event_list,
            (pos[0]-self.rect.x, pos[1]-self.rect.y)
            )
        self._activePaste.update(
            event_list,
            (pos[0]-self.rect.x, pos[1]-self.rect.y)
            )

        #updating the image
        self._activeCopy.draw(self.image)
        self._activeCut.draw(self.image)
        self._activePaste.draw(self.image)

    def draw(self, screen:pygame.Surface) -> None:
        """
        It draws the buttons on the given surface
        with its corresponding rect position

        INPUT: 
         - screen [pygame.Surface]  -> surface where to blit the button
        """

        #drawing the image surface on the given screen
        screen.blit(self.image, self.rect)
       
    def displayer(self) -> pygame.Rect:
        """
        It returns the rect of this object but inflated, by 2 px for each line
        
        OUTPUT:
        - [pygame.Rect] -> is the inflated rect of the object
        """
        
        return self.rect.inflate(4,4)

class TextBox(pygame.sprite.Sprite):
    # pygame sprite to handle a box where to write
    
    __slots__ = (
        "_colors",      # [Colors]                  -> colors object
        "_font",        # [pygame.font.SysFont]     -> font to rendere the
                        #                               typed in text
        "_text",        # [str]                     -> typed in text
        "_text_surf",   # [list[pygame.Surface]]    -> list of rendered text
                        #                               with the given font
        "_max_char",    # [int]                     -> max lenght of both text
                        #                               and text_surf
        "_clicked",     # [bool]                    -> if True, when the mouse
                        #                               left button is up the
                        #                               object will be writable
        "_writable",    # [bool]                    -> if True, it is possible
                        #                               to type in text
        "_hovered",     # [bool]                    -> if True (when the mouse
                        #                               hovers over it), the
                        #                               mouse will change it's
                        #                               icon
        "image",        # [pygame.Surface]          -> surface is blitted on
                        #                               the given surface
        "rect",         # [pygame.Rect]             -> rect of the postion of
                        #                               image where to blit on
                        #                               the given surface
        "_bar",         # [pygame.Surface]          -> is the '|' char rendered
                        #                               with the given font to
                        #                               show wheere it is going
                        #                               to be written if the
                        #                               object is writable
        "_i",           # [int]                     -> frame counter to make
                        #                               the blinking animation
                        #                               for the bar, over
                        #                               _wait_b
        "_j",           # [int]                     -> frame counter to use the
                        #                               "keep pressing" LRdc,
                        #                               over _wait_w
        "_k",           # [int]                     -> it counts the characters
                        #                               of text where to put
                        #                               the bar
        "_kk",          # [int]                     -> thats the second index
                        #                               whene the text is
                        #                               selected or selectable
        "_sel_rect",    # [pygame.Surface]          -> transparent surface to
                        #                               use over the selected
                        #                               text
        "_text_rect",   # [pygame.Surface]          -> rectangle where
                        #                               text_surf is blitted
                        #                               and that is blitted
                        #                               over image
        "_selectable",  # [bool]                    -> it is True when the left
                        #                               mouse is downand the
                        #                               cursor it is moving
                        #                               left or right without
                        #                               being released. _kk is
                        #                               moved. The self_rect
                        #                               will be showed
        "_selected",    # [bool]                    -> it is True when the left
                        #                               mouse is released in a
                        #                               position different than
                        #                               earlier or by shifr+R/L
                        #                               -> _kk is moved.
                        #                               The self_rect will be
                        #                               showed
        "_rule",        # [callable]                -> given function that
                        #                               returns the text is
                        #                               want to ba axcepted by
                        #                               the textbox
        "_pos_x",       # [int|float]               -> if text_rect is longer
                        #                               than image, pos_x is
                        #                               the translater when
                        #                               blitting
                        # [str]                     -> color for the box
        "_box_normal_color",
                        # [str]                     -> color for the border
                        #                               when writable
        "_box_writable_color",
        "_text_color",  # [str]                     -> color when rendering the
                        #                               text
        "_bar_color",   # [str]                     -> color of the "|" bar
        "_empty_text",  # [str]                     -> text to render when the
                        #                               text is empty   
        "_empty_surf",  # [pygame.Surface|bool]     -> text showed when the
                        #                               text is empty. If
                        #                               False, doesn't saw
                        #                               anything
        "_control",     # [list[bool,bool]]         -> keeps track when a ctrl
                        #                               button is pressed or
                        #                               not
        "_shift",       # [list[bool,bool]]         -> keeps track when a shift
                        #                               button is pressed or
                        #                               not
        "_littlemenu",  # [bool]                    -> becomes True when the
                        #                               right mouse is clicked
                        #                               on the object while is
                        #                               writable. It is used to
                        #                               keep track and activate
                        #                               the LittleMenu
        "_counter",     # [int]                     -> frame counter to let 
                        #                               double left mouse click
                        #                               and select all the
                        #                               text, if the object is
                        #                               writable, over _wait_c1
                        #                               and over _wait_c2
        "_LRdc",        # [list[bool]*4]            -> keeps track when
                        #                               "Left arrow",
                        #                               "Right arrow",
                        #                               "delete" or "canc"
                        #                               button are pressed or
                        #                               not
        "_changed",
        '_prev',
        '_next'
        )

    button_space = 4    # [int]                     -> total space around the
                        #                               plain text
                        #                               (to apllay the border)
                        # [tuple[int,int]]          -> button's code to update
    _mod_C = (pygame.K_LCTRL, pygame.K_RCTRL)       #   "control"
                        # [tuple[int,int]]          -> button's code to update
    _mod_S = (pygame.K_LSHIFT, pygame.K_RSHIFT)     #   "shift"
                        # [tuple[int,int]]          -> button's code to check
    _enters = (pygame.K_RETURN, pygame.K_KP_ENTER)  #   "enter" buttons
                        # [tuple[str]]                  -> special chr to avoid
    _specials = ('a','c','v','x')                   #   if any ctrl is pressed
    _wait_w = 10        # [int]                     -> int over which 'i'
                        #                               cicle through
    _wait_b = 60        # [int]                     -> int over which 'j'
                        #                               cicle through
    _wait_c1 = 15       # [int]                     -> int over which 'counter'
                        #                               cicle through
    _wait_c2 = 25       # [int]                     -> int over which 'counter'
                        #                               cicle through
    
    from pyperclip import copy,paste
    __copy=staticmethod(copy)
    __paste=staticmethod(paste)
    del copy,paste

    def __init__(
        self,
        initial_text:str="",
        empty_text:str="",
        max_char:int=256,
        writable:bool=False,
        bar_color:str="dark_blue",
        box_normal_color:str='gray',
        box_writable_color:str='orange',
        selected_text_color:str='orange',
        text_color:str="black",
        rule=None,
        func=None,
        func_args=(),
        utilities: Utilities=utilities,
        *args,
        **kwargs
        ) -> None:
        '''
        Initializating the class to have a the Box where the user can type text
        After init_rect() has to be called
        
        INPUT:
        - w [float|int]                 -> value of the lenght of the box
        - font [pygame.font.SysFont]    -> font to render the text of the 
        - initial_text [str]            -> initial text to render and show
                                            in the box
        - empty_text [str]              -> text to render which will be shown
                                            when there's no text on hte box
        - max_char [int]                -> max number of char tu put in the box
        - writable [bool]               -> if True, when the box is defined and
                                            showed, it will be already possible
                                            to write
        - bar_color [str]               -> color of the "|" bar
        - box_normal_color [str]        -> color of the box in normal state
        - box_writable_color [str]      -> color of the border of the box when
                                            writable
        - selected_text_color [str]     -> color of the rectangle shown when
                                            text is selected or selectable
        - text_color [str]              -> color of the text that will be
                                            rendered with font
        - rule [callable|None]          -> function that selects the kind of
                                            text will be accepted. MUST receive
                                            any string and return the wanted
                                            string
        - func [callable|None]          -> function to call if wanted when
                                            pressing the Enter key
        - args [tuple]                  -> the args the function needs
        - colors [Colors]               -> the Colors used for the image
        '''

        # initializing the sprite class
        super().__init__(*args,**kwargs)
        self._colors = utilities.colors

        # setting all the variables which will be used 
        self._font:pygame.font.Font = None
        self._max_char = max_char
        self._empty_text = empty_text
        self._empty_surf:pygame.Surface = None
        self._bar:pygame.Surface = None
        self._rule = rule

        #the dimensione of thesel_rect isn't important
        # -> it will be streached anyway
        self._sel_rect = pygame.Surface((1,1),pygame.SRCALPHA)
        self._sel_rect.fill(utilities.colors[selected_text_color,50])

        #This Surface has to be long enought to keep all the text
        self._text_rect = pygame.Surface((1,1), pygame.SRCALPHA)
        self._text_rect.fill(utilities.colors.transparent)

        #these are value that I use much
        self._pos_x = self._k = self._kk = self._i = self._j = self._counter =0
        self._box_normal_color = box_normal_color
        self._box_writable_color = box_writable_color
        self._text_color = text_color
        self._bar_color = bar_color
        self._shift = [False, False]
        self._control = [False, False]
        self._LRdc = [False, False, False, False]
        self._selectable = self._selected = self._hovered = self._clicked = \
            self._littlemenu = False 
        self._writable = writable

        #setting the function
        if func is None:
            self.func = None
        else:
            self.func=utilities.superfunc(func, func_args)
        
        #setting the text of the box
        self._text = initial_text
        self._text_surf:list[pygame.Surface] = []
        self._changed = False
        
        self._next=None
        self._prev=None

        # These are infos property needed to make the Sprite class work
        # as expecter
        self.image:pygame.Surface = None
        self.rect=pygame.Rect(0,0,1,1)

    def refresh(
        self,
        w:int,
        font:pygame.font.Font
        ) -> None:
        '''
        This function let re-use the same button without creating a
        new one when resizing the screen. After init_rect() has to be called
        
        INPUT:
        - w [float|int]                 -> value of the lenght of the box
        - font [pygame.font.SysFont]    -> font to render the text of the 
        - colors [Colors]               -> the Colors used for the image
        '''

        #getting the height of the box
        ww,h = font.size("LM")

        # setting all the variables which will be used 
        if self._empty_text:
            self._empty_surf = font.render(
                self._empty_text,
                True,
                self._colors[self._text_color]
                )
            self._empty_surf.set_alpha(90)
        self._bar = font.render("|", True, self._colors[self._bar_color])

        #the dimensione of thesel_rect isn't important
        # -> it will be streached anyway
        self._sel_rect = pygame.transform.scale(self._sel_rect,(5, h))

        #This Surface has to be long enought to keep all the text
        self._text_rect = pygame.transform.scale(
            self._text_rect,
            ((ww+3)*self._max_char,h+self.button_space)
            )

        #these are the previous and nextsizes for all teh rendered text
        now_l,_ = font.size(self._text)
        pre_l,_ = self._font.size(self._text) if self._font else font.size(self._text)
        
        #setting the text of the box
        #k would be set to 0 when the whole text is replaced
        #_pos_x is set to scale right? That was involving some math
        k = self._k
        self._font = font
        self.replaceText(self._text)
        self._pos_x= min(
            0,
            (pre_l+self._pos_x)*w/self.rect.w-now_l
        )
        self._k = k

        # These are infos property needed to make the
        # Sprite class work as expecter
        self.image = pygame.Surface((w, h+self.button_space))
        self.rect = None

    def __bool__(self) -> bool:
        """
        Returns the value of 'littlemenu' -> is True if the mouse
        has rightclicked on the box

        OUTPUT:
         - [bool] -> True to open the littlemenu
        """

        return self._littlemenu

    def is_writable(self):
        return self._writable

    def __str__(self) -> str:
        """
        Returns the value of 'text'

        OUTPUT:
         - [str] -> the text contained in the textBox
        """

        return self._text

    def opened_little_menu(self) -> None:
        """
        it has to be called when the littlemenu is opened.
        It restore littlemenu tu False
        """

        self._littlemenu = False

    def init_rect(self, **kwargs) -> pygame.Rect:
        '''
        it calls the standard function for pygame.Surface
        and passes to it all the arguments
        
        INPUT:
        - **kwargs      -> syntax for pygame.Surf().get_rect()
        
        OUTPUT:
        - [pygame.Rect] -> is the rect of the object
        '''

        self.rect = self.image.get_rect(**kwargs)
        return self.rect
        
    def get_rect(self) -> pygame.Rect:
        '''
        Standard function for pygame.Surface,
        but in the right position in the screen
        
        OUTPUT:
        - [pygame.Rect] -> is the rect of the object
        '''

        return self.rect

    def update(
        self,
        event_list:list[pygame.event.Event],
        pos:tuple[int,int],
        hover:bool=True
        ) -> None:
        """
        It checks every event to update the button 

        INPUT: 
        - event_list [list[pygame.event.Event]]     -> list of all the events
                                                        from the program.
        - pos [tuple[int,int]]                      -> position of the mouse
        """

        # It checks the collision of the mouse with the button
        hover &= self.rect.collidepoint(pos)

        # It checks every event given from the pc
        remove = None
        for event in event_list:
            
            # it checks if a mouse button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:

                # it checks the left mouse button
                if event.button == 1:
                    

                    if self._writable and hover and self._text:

                        # This chunk will checks for double click and,
                        # if it succeeds, do a ctrl+A
                        self._selectable = True
                        if self._counter:
                            self._selected=True
                            self._selectable=False
                            self._k = 0
                            self._kk = len(self._text)
                            self._counter=0
                            continue

                        else:
                            self._counter=1
                        
                        # This chunk will understand the position of
                        # the mouse within the text
                        xx = self._pos_x + self.rect.x + self.button_space/2 +\
                            self._text_surf[0].get_width()/2
                        if pos[0]<=xx:
                            self._kk = self._k = 0
                            self._i=0
                            continue

                        j=-1
                        for j in range(len(self._text)-1):
                            t = (self._text_surf[j].get_width() +\
                                self._text_surf[j+1].get_width()
                                )/2

                            xx+=t
                            if pos[0]<=xx:
                                self._kk = self._k = j+1
                                self._i=0
                                break
                         
                        #if it's not found, it will be all the way on the right
                        else: 
                            self._i=0
                            self._kk = self._k = j+2
                    
                    # The mouse has to be released hovering the box before
                    # getting writable
                    elif not self._writable:
                        self._clicked = hover

                        if self._selected or self._selectable:

                            self._k = self._kk
                            self._selected = self._selectable = False

                    # This could be else, but it saves some iteration(?)
                    # I've to remember this in case of bugs
                    elif self._selected or self._selectable:
                        self._k = self._kk
                        self._selected = self._selectable = False
            
                # That's the right button, I coud do the same as for
                # the left and wait the button to be released...
                # this way is simpler and doeasn't matter much
                if event.button == 3:

                    if hover:

                        # it sets itself to let the littlemenu open if is _writable
                        if self._writable:
                            self._littlemenu = True
                            
                        #it just becomes right away writable
                        else:
                            self._writable = True

                    elif self._selected or self._selectable:
                        self._k = self._kk
                        self._selected = self._selectable = False

            # Only if selectable is True (meaning we have clicked the left
            # mouse button and moving around to select text), we update the
            # second _kk variable to underline the text
            elif event.type == pygame.MOUSEMOTION and self._selectable:
                
                #if the mouse x position is on he left of the box, the _kk
                #is changed by 1 position on the left if more characters
                #are aviable (at least 1)
                if pos[0]<self.rect.x and self._kk>0:
                    self._kk-=1

                #if the mouse x position is on the right of the box, the 
                #_kk is changed by one position on the right if more
                #characters are aviable (at least 1)
                elif pos[0]>self.rect.right and self._kk<len(self._text):
                    self._kk+=1

                # Else the place is searched inside the box between the
                # letters, counting also if the text is mooved left or
                # right.
                else:
                    
                    # This chunk will understand the position of
                    # the mouse within the text
                    xx = self._pos_x+self.rect.x+self.button_space//2 + \
                        self._text_surf[0].get_width() / 2

                    if pos[0]<=xx:
                        self._kk = 0
                        self._i=0
                        continue

                    j=-1
                    for j in range(len(self._text)-1):
                        t= (self._text_surf[j].get_width() + \
                            self._text_surf[j+1].get_width() \
                            )/2

                        xx+=t
                        if pos[0]<=xx:
                            self._kk=j+1
                            self._i=0
                            break

                    else:
                        self._i=0
                        self._kk = j+2

            # it checks if a mouse button is released
            elif event.type == pygame.MOUSEBUTTONUP:

                # it checks the left mouse button
                if event.button == 1:

                    #it checks if it is in time for the double click
                    if self._counter>self._wait_c1:
                        self._counter=0

                    # if the mouse is hovering it means the mouse has being
                    # clicked and unclicked over the box -> is writable 
                    # (was good use `if hover: self.writable = ... = True`)
                    if self._clicked:
                        self._writable = hover
                        self._clicked = False

                    # mouse is released, is selected only if the two indeces
                    # are different, ortherways it's just in place
                    elif self._selectable:
                        self._selectable = False
                        self._selected= self._k != self._kk

                    #saving some litle iteration by putting `and self.writable`
                    elif not hover and self._writable:
                        self._selectable = self._selected = self._writable = False
                        self._k = self._kk = min(self._kk,len(self._text))

                # it checks the right mouse button only it is _writable
                # and the mouse is hovering
                elif event.button == 3 and self._writable and not hover:

                    if self._selected or self._selectable:
                        self._k = self._kk
                        self._selected = self._selectable = False

                    self._writable = False

            # this skips every other check if the box isn't _writable, just put
            # some little checks... else it goes on!
            elif not self._writable:

                #it keeps _control/_shift lists updated if any is pressed ...
                if event.type == pygame.KEYDOWN:
                    if event.key in self._mod_C:
                        self._control[self._mod_C.index(event.key)] = True
                    elif event.key in self._mod_S:
                        self._shift[self._mod_S.index(event.key)] = True

                #... or just released
                elif event.type == pygame.KEYUP:
                    if event.key in self._mod_C:
                        self._control[self._mod_C.index(event.key)]=False
                    elif event.key in self._mod_S:
                        self._shift[self._mod_S.index(event.key)]=False

                #nothing more is requested
                continue

            #it has to be writable, we'll add text!
            elif event.type == pygame.TEXTINPUT:

                #it doesn't add the char if ctrl is pressed and any _special is
                #given
                if any(self._control) and event.text in self._specials:
                    continue

                self.addText(event.text)

                #if it was selected (or electable) it has to be setted as False
                if self._selectable or self._selected:
                    self._selectable = self._selected = False

            #if key has being pressed, it checks if any event has to be thrown
            elif event.type == pygame.KEYDOWN:
                
                # CTRL+V
                if event.key == pygame.K_v and any(self._control):
                    self.paste()

                # CTRL+C
                elif event.key == pygame.K_c and any(self._control):
                    self.copy()

                # CTRL+X
                elif event.key == pygame.K_x and any(self._control):
                    self.cut()

                # CTRL+A
                elif event.key == pygame.K_a and any(self._control) and \
                    self._text:

                    self._selected=True
                    self._k = 0
                    self._kk = len(self._text)
                
                # CTRL
                elif event.key in self._mod_C:
                    self._control[self._mod_C.index(event.key)] = True
                    
                # ALT
                elif event.key in self._mod_S:
                    self._shift[self._mod_S.index(event.key)] = True

                # ENTER and function is not None
                elif event.key in self._enters and not self.func is None:
                    #It resets to normal pointer the mouse
                    pygame.mouse.set_cursor(*pygame.cursors.Cursor(0))
                    self.func()

                # RIGHT
                elif event.key == pygame.K_RIGHT:
                    self._LRdc[1]=True
                    self._j=0

                # LEFT
                elif event.key == pygame.K_LEFT:
                    self._LRdc[0]=True
                    self._j=0

                # CANCEL
                elif event.key == pygame.K_BACKSPACE:
                    self._LRdc[2]=True
                    self._j=0

                # DELETE
                elif event.key == pygame.K_DELETE:
                    self._LRdc[3]=True
                    self._j=0

                elif event.key == 1073741925: #compose key
                    self._littlemenu = True

                elif event.key == pygame.K_TAB:
                    if any(self._shift) and self._prev is not None:
                        self._prev.keep_alive()
                        self._writable = self._selected = self._selectable = False
                        remove = event
                    elif self._next is not None:
                        self._next.keep_alive()
                        self._writable = self._selected = self._selectable = False
                        remove = event

            #if key has being released, it checks if any event has to be thrown
            elif event.type == pygame.KEYUP:
                
                # CTRL
                if event.key in self._mod_C:
                    self._control[self._mod_C.index(event.key)]=False
                
                # SHIFT
                elif event.key in self._mod_S:
                    self._shift[self._mod_S.index(event.key)]=False
                
                # RIGHT
                elif event.key == pygame.K_RIGHT:
                    self._LRdc[1]=False
                
                # LEFT
                elif event.key == pygame.K_LEFT:
                    self._LRdc[0]=False
                
                # CANCEL
                elif event.key == pygame.K_BACKSPACE:
                    self._LRdc[2]=False
                
                # DELETE
                elif event.key == pygame.K_DELETE:
                    self._LRdc[3]=False

        if remove is not None:
            event_list.remove(remove)

        # as reference to SMB3 -> R moovement boosted if both LR are pressed
        # as result dc are being ignored
        if all(self._LRdc[:2]) and self._j:
            self._j=0

        # R moovement of the bar in the text
        elif self._LRdc[1]:
            
            #The bar position is updated only if _j == 0
            if not self._j:

                # CTRL + SHIFT + RIGHT
                if any(self._control) and any(self._shift):

                    #If there is need to moove
                    if self._k<len(self._text):
                        self._selected = True
                        self._kk = len(self._text)

                # CTRL + RIGHT
                elif any(self._control):

                    # unselecting if selected
                    if self._selected or self._selectable:
                        self._selected = self._selectable = False

                    self._k = len(self._text)

                # SHIFT + RIGHT
                elif any(self._shift):

                    # add 1 right char if selected
                    if self._selected and self._kk<len(self._text):
                        self._kk +=1

                    # select 1 right char
                    elif not self._selected and self._k<len(self._text):
                        self._selected = True
                        self._kk=self._k+1

                # RIGHT
                else:
                    #moving on char right
                    self.r()

            #updating the _j counter to frame the movement
            self._j=(self._j+1)%self._wait_w

        # L moovement of the bar in the text
        elif self._LRdc[0]:
            
            #The bar position is updated only if _j == 0
            if not self._j:

                # CTRL + SHIFT + LEFT
                if any(self._control) and any(self._shift):

                    #If there is need to moove
                    if self._k>0:
                        self._selected = True
                        self._kk = 0

                # CTRL + LEFT
                elif any(self._control):

                    # unselecting if selected
                    if self._selected:
                        self._selected = False

                    self._k = 0

                # SHIFT + LEFT
                elif any(self._shift):

                    # add 1 left char if selected
                    if self._selected and self._kk>0:
                        self._kk -=1

                    # select 1 left char
                    elif not self._selected and self._k>0:
                        self._selected = True
                        self._kk=self._k-1

                # LEFT
                else:
                    #moving on char right
                    self.l()

            #updating the _j counter to frame the movement
            self._j=(self._j+1)%self._wait_w

        #it deletes one char to the left
        elif self._LRdc[2]:
            
            #it deletes it only if _j == 0
            if not self._j:
                self.removeTextL()

            #updating the _j counter to frame the movement
            self._j=(self._j+1)%self._wait_w

        #it deletes (cancels) one char to the right
        elif self._LRdc[3]:
            
            #it deletes it only if _j == 0
            if not self._j:
                self.removeTextR()

            #updating the _j counter to frame the movement
            self._j=(self._j+1)%self._wait_w

        #it updates the cursor image related to _writable
        #if hover is True the cursor will be for text,
        #whereas when hover is False the cursor will be in normal state
        if self._writable and self._hovered != hover:
            pygame.mouse.set_cursor(*pygame.cursors.Cursor(hover))
            self._hovered = hover

        #this updates the counter
        if self._counter:
            self._counter+=1
            if self._counter==self._wait_c2:
                self._counter=0
            
        #setting the surfaces
        self.image.fill(self._colors[self._box_normal_color])
        self._text_rect.fill(self._colors.transparent)

        #seting the initial positions
        y = self.button_space//2
        z = zz = x = 0

        # this is used to blit every rendered char (if any)
        # and the _sel_rect over _text_rect if is _selected or _selectable.
        # This which will be blitted over the image translated
        if self._text_surf:

            #it searches where to blit _sel_rect and how much big has to be
            if (self._selectable or self._selected) and self._k != self._kk:

                #_kk may be left or right to _k
                t_m = min(self._k,self._kk)
                t_M = max(self._k,self._kk)

                #it bilts every char
                for t_i, t_j in enumerate(self._text_surf):

                    self._text_rect.blit(t_j,(x,y))

                    if t_i==t_M:
                        zz=x
                    elif t_i==t_m:
                        z=x

                    x+=t_j.get_width()

                #zz is greater than z, if is still 0, it is in the end
                if not zz:
                    zz=x
                
                # finally it blits _sel_rect in the right position with
                # the right sizes
                self._text_rect.blit(
                    pygame.transform.scale(
                        self._sel_rect,
                        (zz-z,self.rect.h)
                        ),
                    (z,y)
                    )

            # it search where the _bar should be blitted
            # (just to get the positioning of the text right)
            else:

                #it bilts every char
                for t_i,t_j in enumerate(self._text_surf):

                    self._text_rect.blit(t_j,(x,y))

                    if t_i==self._k:
                        z=x

                    x+=t_j.get_width()

                #if _k>0 and z still is 0, than it has to be in the end
                if self._k and not z:
                    z=x
        
        #If there is no text but there is an _eampty_surf, it is blitted
        elif self._empty_surf:
            self._text_rect.blit(self._empty_surf,(x,y))

        #If is writtable and is not _selected or _selectable, it updates _i
        #and blits _bar if it is the right time
        if self._writable and not zz:
            if self._i<30:
                self._text_rect.blit(self._bar,(z-y,y))

            self._i=(self._i+1)%self._wait_b

        #It updates the positioning of the text related to _kk pos and _k:
        #it tries to show the needed text on .image thanks by _pos_x
        if x>self.rect.w-self.button_space:

            #if text is selected or selectable
            if zz:

                #if _kk is greater than _k
                if self._kk>self._k:

                    #it gets the lenght of the next char
                    kk=self._text_surf[
                        min(self._kk+1, len(self._text_surf)-1)
                        ].get_width()

                    # if _kk is max, than pos_x is the difference between 
                    # zz and rect.w moved by y (half buttonspace)
                    if self._kk == len(self._text_surf):
                        self._pos_x = self.rect.w-zz-y

                    # if zz is greater than the actual pos in the rect.w
                    # (if the mouse is outside the box on the right)
                    # than pos_x is the difference between
                    # zz and rect.w moved by kk
                    elif zz>self.rect.w-self._pos_x-kk:
                        self._pos_x = self.rect.w-zz-kk

                    # if zz is less than the actual pos in the rect.w
                    # (if the mouse is outside the box on the left)
                    # than pos_x is zz moved by kk and y
                    elif zz<-self._pos_x+kk:
                        self._pos_x = -zz+y+kk

                #if _kk is less than _k
                elif self._kk<self._k:

                    #it gets the lenght of the previous char
                    kk=self._text_surf[
                        max(self._kk-1, 0)
                        ].get_width()

                    # if _kk is min, than pos_x is just y (half buttonspace)
                    if self._kk == 0:
                        self._pos_x = y

                    # if z is less than the actual pos in the rect.w
                    # (if the mouse is outside the box on the left)
                    # than pos_x is z moved by kk and y
                    elif z<-self._pos_x+kk:
                        self._pos_x = -z+y+kk

                    # if z is greater than the actual pos in the rect.w
                    # (if the mouse is outside the box on the right)
                    # than pos_x is the difference between
                    # z and rect.w moved by kk
                    elif z>self.rect.w-self._pos_x-kk:
                        self._pos_x = self.rect.w-z-kk

            # if the text is not selected or selectable
            else:
                
                # if z is less than the actual pos in the rect.w
                # (if the mouse is outside the box on the left)
                # than pos_x is z moved by y
                if z<-self._pos_x:
                    self._pos_x = -z+y

                # if z is greater than the actual pos in the rect.w
                # (if the mouse is outside the box on the right)
                # than pos_x is the difference between
                # z and rect.w moved by self.button_space
                # (with just y the _bar is hidden)
                elif z>self.rect.w-self._pos_x:
                    self._pos_x = self.rect.w-z-self.button_space

        #If the total lenght is shorter than image's width, it gives a little
        #space to the left of button
        else:

            self._pos_x = y

        #It blits _text_rect on image translated by _pos_x, by actually
        #'cutting' _text_rect in the right way
        self.image.blit(self._text_rect, (self._pos_x,0))
        
        #Only if writable, the rect is drawn on image.
        #It is after to get a nicer look
        if self._writable:
            pygame.draw.rect(
                self.image,
                self._colors[self._box_writable_color],
                self.image.get_rect(),
                y
                )

    def draw(self, screen:pygame.Surface) -> None:
        """
        It draws the box on the given surface
        with its corresponding rect position

        INPUT: 
         - screen [pygame.Surface]  -> surface where to blit the button
        """

        #drawing the image surface on the given screen
        screen.blit(self.image, self.rect)

    def _insert(self, nt:str) -> None:
        '''
        This function adds a character in the current bar position.
        It has to be called from addText
        
        INPUT:
        - nt [str] -> the character to add
        '''

        self._text_surf.insert(
            self._k,
            self._font.render(nt,True,self._colors[self._text_color])
            )
        self._text = self._text[:self._k]+nt+self._text[self._k:]
        self._k+=1
        
        if not self._changed:
            self._changed = True

    def addText(self, new_text:str) -> None:
        '''
        This function adds a string in the current bar position.
        If text is selected, it will be deleted
        
        INPUT:
        - new_text [str] -> the string to add
        '''

        #if _selected, the text selected will be replaced by new_text.
        #so the selected text is deleted
        if self._selected:
            self._pops()

        #the given text is checked by the _rule, if one is present
        #next the text is added 
        if self._rule is not None:
            #check the rule if present and add every accepted char (until the limit is reached)
            for i,nt in enumerate(self._rule(new_text),len(self._text)):
                if i>=self._max_char:
                    break
                elif self._font.size(nt)[0]:
                    self._insert(nt)

        else:
            #adds every accepted char (until the limit is reached)
            for i,nt in enumerate(new_text,len(self._text)):
                if i>=self._max_char:
                    break
                elif self._font.size(nt)[0]:
                    self._insert(nt)
        self._i = 0

    def _pop(self, left:bool=True) -> None:
        '''
        This function deletes a char in text. 
        If left is True, the left char will be removed,
        otherways the right one
        
        INPUT:
        - left [str] -> the "direction" where to remove the char
        '''

        #backspace is used
        if left:
            self._text_surf.pop(self._k-1)
            self._text = self._text[:self._k-1]+self._text[self._k:]
            self._k-=1
        
        #delete is used
        else:
            self._text_surf.pop(self._k)
            self._text = self._text[:self._k]+self._text[self._k+1:]

        if not self._changed:
            self._changed = True

    def _pops(self) -> None:
        '''
        This function deletes every char in text between _k and _kk if selected
        '''

        #it sets the indices in the right places
        if self._k<self._kk:
            self._kk,self._k = self._k,self._kk

        #deletes the selected text
        for _ in range(self._kk,self._k):
            self._pop()

    def removeTextL(self) -> None:
        '''
        This function deletes chars from the Left (with backspace) in _k,
        if selected between _k and _kk
        '''

        #to remove manychars
        if self._selected:
            self._pops()
            self._selected=False
        
        #to remove only one char
        elif self._k>0:
            self._pop()

        #resetting the _bar animation
        self._i = 0

    def removeTextR(self) -> None:
        '''
        This function deletes chars from the Right (with canc) in _k,
        if selected between _k and _kk
        '''

        #to remove manychars
        if self._selected:
            self._pops()
            self._selected=False
        
        #to remove only one char
        elif self._k<len(self._text):
            self._pop(False)

        #resetting the _bar animation
        self._i = 0

    def removeAll(self) -> None:
        '''
        This function deletes the whole _text
        '''

        self._text=""
        self._text_surf.clear()
        self._k=self._kk=self._i=0

        if not self._changed:
            self._changed = True

    def replaceText(self, new_text:str) -> None:
        '''
        This function replaces the text with the given one
        
        INPUT:
        - new_text [str] -> the new text that will replace the current one
        '''

        self.removeAll()
        self.addText(new_text)

    def r(self) -> None:
        '''
        This function will move the bar one step right
        '''

        if self._selected:
            self._kk = self._k = max(self._kk,self._k)
            self._i = 0
            self._selectable = self._selected = False
        elif self._k<len(self._text):
            self._k+=1
            self._i = 0

    def l(self) -> None:
        '''
        This function will move the bar one step left
        '''

        if self._selected:
            self._kk = self._k = min(self._kk,self._k)
            self._i = 0
            self._selectable = self._selected = False
        elif self._k>0:
            self._k-=1
            self._i = 0
 
    def copy(self) -> None:
        '''
        This function puts the selected (or the whole text) on the scrap list
        '''

        # it 'copies' the selected text.
        # it justs checks which come first between _k and _kk
        if self._selected:

            if self._k<self._kk:
                self.__copy(self._text[self._k:self._kk])

            else:
                self.__copy(self._text[self._kk:self._k])

            #it un-selects the text
            self._selected = False

        # if text is not selected but there is text written in
        # it 'copies' the whole text
        elif self._text:
            self.__copy(self._text)

    def little_copy(self) -> None:
        '''
        Thinking about changing it...
        this function put the selected text (or the whole text)
        on the scrap list
        '''

        self.copy()

    def cut(self) -> None:
        '''
        This function put the selected text (or the whole text)
        on the scrap list and then deletes it
        '''

        # it 'copies' the selected text and next it is deleted
        # it justs checks which come first between _k and _kk
        if self._selected:

            if self._k<self._kk:
                self.__copy(self._text[self._k:self._kk])

            else:
                self.__copy(self._text[self._kk:self._k])

            #it deletes the selected text
            self.removeTextR()

        # if text is not selected but there is text written in
        # it 'copies' the whole text and then it deletes it
        elif self._text:
            self.__copy(self._text)
            self.removeAll()

    def little_cut(self) -> None:
        '''
        Thinking about changing it...
        this function put the selected text (or the whole text)
        on the scrap list and then deletes it
        '''

        self.cut()
    
    def paste(self) -> None:
        '''
        This function adds the text (or replacing if selected)
        from the scrap list
        '''

        #it get the text to 'paste'
        self.addText(self.__paste())
        
        self._selected = False

    def little_paste(self) -> None:
        '''
        Thinking about changing it...
        this function adds the text (or replacing if selected)
        from the scrap list
        '''

        self.paste()

    def displayer(self) -> pygame.Rect:
        """
        It returns the rect of this object but inflated, by 2 px for each line
        
        OUTPUT:
        - [pygame.Rect] -> is the inflated rect of the object
        """
        
        return self.rect.inflate(4,4)

    def has_changed(self) -> bool:
        if self._changed:
            self._changed = False
            return True
        return False

    def keep_alive(self) -> None:
        if not self._writable:
            self._writable = True
    
    def set_prev(self,__o) -> None:
        self._prev = __o
    def set_next(self,__o) -> None:
        self._next = __o

class Drop(pygame.sprite.Sprite):

    def __init__(self,
        box:TextBox,
        file:str,
        quantity:int = 5,
        txt_color:str = "white",
        bk_color:str = "gray",
        bt_hover_color:str='dark_gray',
        bt_clicked_color:str='black',
        utilities: Utilities=utilities
        ) -> None:

        super().__init__()

        self.active = False
        self.prev_status = False

        self.utilities = utilities
        self.quantity = quantity
        self.length = 0
        self.box = box
        self.font:pygame.font.Font = None
        self.colors = (txt_color, bk_color, bt_hover_color, bt_clicked_color)
        
        self.h = 0
        self.rect = None
        self.image = pygame.Surface((1,1),pygame.SRCALPHA)
        self.long_image = pygame.Surface((1,1),pygame.SRCALPHA)
        self.v_bar = VerticalBar(bar_color="dark_gray",utilities=utilities)
        self.bar = None
        self.g = pygame.sprite.Group()

        from ctypes import windll
        self._hidder = lambda x: windll.kernel32.SetFileAttributesW(x, 0x02)
        self._shower = lambda x: windll.kernel32.SetFileAttributesW(x, 0x80)
        from re import escape,IGNORECASE
        self._finder = lambda x,y: match(f".*{escape(x)}.*",y,IGNORECASE)

        self.file = file+".__"
        self.data = []
        self.buttons = []
        self.findet = []
        self.__read()

    def __bool__(self) -> bool:
        return self.active

    def refresh(
        self,
        font:pygame.font.Font,
        length:int,
        colors:pygame.Color=utilities.colors
        ) -> None:

        self.length = length
        self.font = font
        self.h = font.size("A")[1]

        self.image = pygame.transform.scale(self.image,(self.length,self.h*self.quantity))
        self.rect = self.image.get_rect()
        
        if self.box.has_changed():
            self.__find()
        else:

            x=y=0
            for button,text in zip(self.buttons,self.findet):
        
                button.refresh(
                    length-self.h//2,
                    font.render(text,True,self.utilities.colors[self.colors[0]]),
                    length-self.h//2,
                    colors=colors
                    )
                
                y+=button.init_rect(x=x,y=y).h
                button.text_rect(self.center)
            
            self.long_image = pygame.transform.scale(self.long_image, (length,y))

            if len(self.buttons)>1:
                self.v_bar.refresh(self.h//2,self.rect.h,y,self.h,colors=colors)
                self.v_bar.init_rect(right = self.length,y=0)
                self.bar = self.v_bar
            else:
                self.bar = None
        self.rect = None

    def __read(self):
        
        if osexists(self.file):
            self._shower(self.file)

            with open(self.file, "r", encoding=self.utilities.decoder) as file:
                self.data.extend(file.read().split("\n"))
                self.data.sort()
            
            self._hidder(self.file)
        else:
            with open(self.file, "w", encoding=self.utilities.decoder) as file:
                file.write("")
            
            self._hidder(self.file)
    
    def __write(self, data:str) -> None:

        self.data.append(data)
        self.data.sort()

        self._shower(self.file)
        
        with open(self.file, "w", encoding=self.utilities.decoder) as file:
            file.write("\n".join(self.data))
        
        self._hidder(self.file)
        
    def __find(self) -> None:
        findet = filter(lambda y:self._finder(str(self.box),y),self.data)
        if findet != self.findet:
            self.findet = findet
            self.buttons.clear()

            x=y=0
            for f in findet:
                t = NormalButton(
                        bt_normal_color=self.colors[2],
                        bt_hover_color=self.colors[3],
                        bt_pressed_color=self.colors[3],
                        func=self.box.replaceText,
                        func_args=(f,),
                        utilities=utilities
                )
                t.refresh(
                    self.font.render(f,True,self.utilities.colors[self.colors[0]]),
                    self.length-self.h//2,
                    self.length-self.h//2
                    )
                y+=t.init_rect(x=x,y=y).h
                t.text_rect()
                self.buttons.append(t)

            self.long_image = pygame.transform.scale(self.long_image, (self.length,y))
            
            if len(self.buttons)>1:
                self.v_bar.refresh(self.h//2,self.rect.h,y,self.h)
                self.v_bar.init_rect(right = self.length,y=0)
                self.bar = self.v_bar
            else:
                self.bar = None
            
            self.g.empty()
            self.g.add(self.buttons)

    def init_rect(self, **kwargs) -> pygame.Rect:
        '''
        it calls the standard function for pygame.Surface
        and passes to it all the arguments
        
        INPUT:
        - **kwargs      -> syntax for pygame.Surf().get_rect()
        
        OUTPUT:
        - [pygame.Rect] -> is the rect of the object
        '''

        self.rect = self.image.get_rect(**kwargs)
        return self.rect
        
    def get_rect(self) -> pygame.Rect:
        '''
        Standard function for pygame.Surface,
        but in the right position in the screen
        
        OUTPUT:
        - [pygame.Rect] -> is the rect of the object
        '''

        return self.rect

    def update(
        self,
        event_list:list[pygame.event.Event],
        pos:tuple[int,int],
        hover:bool=True
        ) -> None:
        """
        It checks every event to update the button 

        INPUT: 
        - event_list [list[pygame.event.Event]]     -> list of all the events
                                                        from the program.
        - pos [tuple[int,int]]                      -> position of the mouse
        - colors [Colors]                           -> the Colors used for
                                                        the image
        """

        hover &= self.rect.collidepoint(pos)
        clicked = self.utilities.booleans.check_g(1,'button',pygame.MOUSEBUTTONDOWN,event_list) or self.utilities.booleans.check_g(1,'button',pygame.MOUSEBUTTONUP,event_list)
        self.box.update(event_list,pos)
        if self.active and hover and clicked:
            self.box.keep_alive()

        if self.box.has_changed():
            self.__find()

        self.image.fill(self.utilities.colors[self.colors[1],100])

        if self.prev_status ^ self.box.is_writable():
            self.active = self.prev_status = self.box.is_writable()

        if not self.active:
            return
    
        if clicked:
            if not (hover or self.box.get_rect().collidepoint(pos)):
                self.active = False
                return
        elif self.utilities.booleans.check_k(pygame.K_RETURN,event_list):
            self.active = False
            return
        
        if self.bar:
            self.bar.update(event_list, (pos[0]-self.rect.x,pos[1]-self.rect.y))

            self.g.update(event_list, (pos[0]-self.rect.x,pos[1]-self.rect.y-float(self.bar)))
        
        else:
            self.g.update(event_list, (pos[0]-self.rect.x,pos[1]-self.rect.y))

        self.long_image.fill(self.utilities.colors.transparent)

        self.g.draw(self.long_image)
        if self.bar:
            self.image.blit(self.long_image,(0,float(self.bar)))
            self.bar.draw(self.image)
        else:
            self.image.blit(self.long_image,(0,0))

    def draw(self, screen:pygame.Surface) -> None:
        """
        It draws the box on the given surface
        with its corresponding rect position

        INPUT: 
         - screen [pygame.Surface]  -> surface where to blit the button
        """

        #drawing the image surface on the given screen
        screen.blit(self.image, self.rect)

    def displayer(self) -> pygame.Rect:
        """
        It returns the rect of this object but inflated, by 2 px for each line
        
        OUTPUT:
        - [pygame.Rect] -> is the inflated rect of the object
        """
        
        return self.rect.inflate(4,4)

    def exit(self) -> None:
        t = str(self.box).strip()
        if t not in self.data:
            self.__write(t)

class RectengleText(pygame.sprite.Sprite):
    #This object is used to display some text in a rectangular space with fixed
    #height

    __slots__ = (
        'colors',   # [tuple[str,int,str]]  -> colors to use to edit the text
        'text',     # [str]                 -> text to blit on the rect
        'image',    # [pygame.Surface]      -> image of the sprite
        'rect'      # [pygame.Rect]         -> rect of the sprite
        )

    space=4         # [int]                 -> space on the border
    
    from pyperclip import copy
    __copy=staticmethod(copy)
    del copy

    def __init__(
        self,
        rect_color:str,
        rect_alpha:int,
        text:str,
        text_color:str,
        *args,
        **kwargs
        ) -> None:
        """
        This function initializes the Rect by the refresh function
        """

        #initializes the sprite
        super().__init__(*args, **kwargs)

        #base information needed for colorizing
        self.colors = (rect_color,rect_alpha,text_color)
        self.text = text
        self.image:pygame.Surface = None 
        self.rect = pygame.Rect(0,0,0,0)

    def refresh(
        self,
        width:int|float,
        font:pygame.font.Font,
        colors:Colors=utilities.colors
        ):
        """
        This function is called to update the object without creating a new
        identical object
        """

        # taking the width of the space character
        sp = font.size(" ")[0]

        #getting each word and its width
        t=self.text.split()
        sizes = [font.size(tex)[0]+sp for tex in t]

        #deciding how to go in new line (depending on the width of each word
        #and the aviable space)
        summer=0
        texter=[""]
        for i,j in zip(sizes,t):
            summer+=i
            if summer<width:
                texter[-1]+=j+" "
            elif summer<width+sp:
                texter[-1]+=j
                summer=0
                texter.append("")
            else:
                summer=i
                texter.append(j+" ")

        #the last word is removed if eampty
        if not texter[-1]:
            del texter[-1]

        #setting the rectangular shape
        self.image = pygame.Surface(
            (width,(font.get_height()+self.space)*len(texter)),
            pygame.SRCALPHA
            )
        self.image.fill(colors[self.colors[:2]])
        self.rect.update(self.image.get_rect())
        
        #lbitting the text on the rect
        y=self.space//2
        for t in texter:
            h=font.render(t.strip(" "),True,colors[self.colors[-1]])
            self.image.blit(h,(0,y))
            y+=self.space+h.get_height()

    def init_rect(self, **kwargs) -> pygame.Rect:
        '''
        it calls the standard function for pygame.Surface and passes to it
        all the arguments
        
        INPUT:
        - **kwargs      -> syntax for pygame.Surf().get_rect()
        
        OUTPUT:
        - [pygame.Rect] -> is the rect of the object
        '''

        self.rect = self.image.get_rect(**kwargs)
        return self.rect

    def get_rect(self) -> pygame.Rect:
        '''
        Standard function for pygame.Surface,
        but in the right position in the screen
        
        OUTPUT:
        - [pygame.Rect] -> is the rect of the object
        '''

        return self.rect

    def update(
        self,
        event_list:list[pygame.event.Event],
        pos:tuple[int,int],
        hover:bool=True
        ) -> None:
        # It checks the collision of the mouse with the button
        hover &= self.rect.collidepoint(pos)

        # It checks every event given from the pc
        for event in event_list:
            # it checks if a mouse button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3 and hover:
                    try:
                        self.__copy(self.text)
                    except:
                        pass
                    break

    def draw(self, screen:pygame.Surface) -> None:
        """
        It draws the box on the given surface
        with its corresponding rect position

        INPUT: 
         - screen [pygame.Surface]  -> surface where to blit the rect
        """

        #drawing the image surface on the given screen
        screen.blit(self.image, self.rect)


class VerticalBar(pygame.sprite.Sprite):
    #pygame Sprite to handle vertical scroll bar object

    __slots__ = (
        "image",        # [pygame.Surf]         -> image shown after the object
                        #                           is updated
        "rect",         # [pygame.Rect]         -> rect of the dimensions of
                        #                           the object
        "_up",          # [ImageButton]         -> button to move the
                        #                           moving_button up
        "_down",        # [ImageButton]         -> button to move the
                        #                           moving_button down
        "_bar_len",     # [float]               -> the the lenght of
                        #                           the bar button
        "_len",         # [float]               -> the lenght where the button
                        #                           can move
        "_scroll_rate", # [float]               -> that's the ratio the get the
                        #                           crolling right
        "_start",       # [float]               -> 0-point for the bar to move
        "_translate",   # [float]               -> the translation for the bar
                        #                           from start
        "_bar_r",       # [pygame.Surf]         -> the image for teh bar
        "_bar",         # [ImageButton]         -> button that moves
        "_g",           # [pygame.sprite.Group] -> group of sprites
        "_key_clicked", # [tuple[bool,bool]]    -> it contains True when a key
                        #                           is pressed and not yet
                        #                           released.
                        #                           It stands for [Left, Right]
        "_bar_color",   # [str]                 -> color of the bar
        "_window_h",    # [float]               -> current height of the window
                        #                           (needed to calculate the
                        #                           fixed position)
        "_down_i",
        "_up_i"
        )
    
    button_length = 15  # [int]                 -> button size if
                        #                           VarticalBar.scroller
                        #                           is called
    modifier = 5        # [int]                 -> scroller value for buttons
                        #                           or mousewheel

    def __init__(
        self,
        bt_hover_color:str='light_blue',
        bt_clicked_color:str='dark_blue',
        bar_color:str="gray",
        utilities: Utilities=utilities,
        *args,
        **kwargs
        ) -> None:
        '''
        Initializating the class to have a vertical bar for scroll things.
        After init_rect() has to be called
        
        INPUT:
        - window_w [float|int]      -> value of the length of the image
        - window_h [float|int]      -> value of the height of the image
        - scroll_len [float|int]    -> lenght it it is wanted to scroll
        - real_len [float|int]      -> lenght visible wher the scrolled
                                        will be blitted
        - bt_hover_color [str]      -> color of the Imagebutton in
                                        hovered state
        - bt_pressed_color [str]    -> color of the Imagebutton in
                                        clicked state and as border in
                                        hovered state
        - bar_color [str]           -> color of the moving button
        - start_bar [float|int]     -> initial point where the scroller
                                        will be at
        - booleans [Boleans]        -> the Booleans variable used for one
                                        little check
        - colors [Colors]           -> the Colors used for the image
        '''

        # initializing the sprite class
        super().__init__(*args,**kwargs)
        self._down_i = pygame.image.load("./Images/down.png").convert()
                            # [pygame.Sprite]       -> sprite for the up button
        self._up_i = pygame.transform.rotate(self._down_i, 180)

        #setting the buttons
        self._up = ImageButton(
            bt_hover_color,
            bt_clicked_color,
            utilities=utilities
            )
        
        self._down = ImageButton(
            bt_hover_color,
            bt_clicked_color,
            utilities=utilities
            )

        #setting all the lenght values
        self._len = 10
        self._scroll_rate = 1

        #setting the values for the moving bar
        self._start = 0
        self._translate = 0

        #setting the moving button
        self._bar_r = pygame.Surface((1,1))
        self._bar = ImageButton(
            bt_hover_color,
            bt_clicked_color,
            utilities=utilities
            )
        self._g = pygame.sprite.Group(self._up, self._down, self._bar)

        #setting other values
        self._key_clicked = [False,False]
        self._bar_color = bar_color
        self._window_h = 10

        #setting the image
        self.image = pygame.Surface((1,1),pygame.SRCALPHA)
        self.rect:pygame.Rect = None

    def __float__(self) -> float:
        """
        It returns the value of pixels the wanted surface has to be translated
        accordingly

        OUTPUT:
        - [float] -> the to-scroll quantity
        """

        return -self._translate*self._scroll_rate

    def refresh(
        self,
        window_w:float,
        window_h:float,
        scroll_len:float,
        real_len:float,
        start_bar_init:bool=True,
        colors: Colors=utilities.colors
        ) -> None:
        '''
        This function let re-use the same button without creating a new one
        when resizing the screen. After init_rect() has to be called
        
        INPUT:
        - window_w [float|int]      -> value of the length of the image
        - window_h [float|int]      -> value of the height of the image
        - scroll_len [float|int]    -> lenght it it is wanted to scroll
        - real_len [float|int]      -> lenght visible wher the scrolled
                                        will be blitted
        - start_bar_init [bool|int] -> if True, the old height-point, resized,
                                        will be used, otherways it will be put
                                        at 0
        - colors [Colors]           -> the Colors used for the image
        '''
        
        #calculationg the position of the previous bar
        start_bar = self._translate*window_h/self._window_h*start_bar_init
        self._window_h = window_h

        #refreshing teh buttons
        self._up.refresh(
            pygame.transform.smoothscale(
                self._up_i,
                (window_w, window_w)
                ),
            colors = colors
            )
        t = self._up.init_rect(x=0, y=0)
        
        self._down.refresh(
            pygame.transform.smoothscale(
                self._down_i,
                (window_w, window_w)
                ),
            colors = colors
            )
        self._down.init_rect(x=0, bottom=window_h)

        #refreshing all the lenght values
        full_len = window_h- 2*t.w
        bar_len = full_len*real_len/scroll_len
        self._len = full_len-bar_len
        if self._len > int(self._len):
            self._len = int(self._len+1)
        self._scroll_rate = (scroll_len-real_len)/(self._len)

        #refreshing the values for the moving bar
        self._start = t.w
        self._translate = 0
        if 0<start_bar/self._scroll_rate<self._len:
            self.minus(start_bar/self._scroll_rate)
        else:
            self._modifier = 0

        #refreshing the moving button
        self._bar_r = pygame.transform.scale(self._bar_r, (window_w,bar_len))
        self._bar_r.fill(colors[self._bar_color])
        self._bar.refresh(self._bar_r,colors=colors)
        self._bar.init_rect(x=0,y=self._start+self._translate)

        #refreshing the image
        self.image = pygame.transform.scale(self.image, (window_w,window_h))

    def init_rect(self, **kwargs) -> pygame.Rect:
        '''
        it calls the standard function for pygame.Surface and
        passes to it all the arguments
        
        INPUT:
        - **kwargs      -> syntax for pygame.Surf.get_rect()
        
        OUTPUT:
        - [pygame.Rect] -> is the rect of the object
        '''

        self.rect = self.image.get_rect(**kwargs)
        return self.rect
        
    def get_rect(self) -> pygame.Rect:
        '''
        Standard function for pygame.Surface,
        but in the right position in the screen
        
        OUTPUT:
        - [pygame.Rect] -> is the rect of the object
        '''

        return self.rect

    def draw(self, screen:pygame.Surface) -> None:
        """
        It draws the buttons on the given surface
        with its corresponding rect position

        INPUT: 
         - screen [pygame.Surface]  -> surface where to blit the button
        """

        #drawing the image surface on the given screen
        screen.blit(self.image, self.rect)

    def plus(self, modifier:float = modifier) -> None:
        """
        This function changes the position bar by the given quantity

        INPUT:
        - modifier [float|int]  -> it is used to move up the bar, if it is
                                    not given, the class.value will be used
        """

        if self._translate> modifier:
            self._translate -= modifier
        elif self._translate>0:
            self._translate = 0
    
    def minus(self, modifier:float = modifier) -> None:
        """
        This function changes the position bar by the given quantity

        INPUT:
        - modifier [float|int]  -> it is used to move down the bar, if it is
                                    not given, the class.value will be used
        """

        if self._translate<self._len-modifier:
            self._translate += modifier
        elif self._translate <self._len:
            self._translate = self._len

    def update(
        self,
        event_list:list[pygame.event.Event],
        pos:tuple[int,int],
        hover:bool=True,
        colors: Colors=utilities.colors
        ) -> None:
        """
        It checks every event to update all the buttons of the little menu

        INPUT: 
         - event_list [list[pygame.event.Event]]    -> list of all the events
                                                        from the program.
         - pos [tuple[int,int]]                     -> position of the mouse
         - colors [Colors]                          -> the Colors used for
                                                        the image
        """

        pos = (pos[0]-self.rect.x, pos[1]-self.rect.y)
        self._g.update(event_list, pos, hover)
        
        if self._bar:
            cy = self._bar.get_rect().centery
            if pos[1]<cy and self._translate>0:
                self.plus(cy-pos[1])
            elif pos[1]>cy and self._translate<self._len:
                self.minus(pos[1]-cy)
        elif self._up and self._up.get_rect().collidepoint(pos):
            self.plus()
        elif self._down and self._down.get_rect().collidepoint(pos):
            self.minus()

        for event in event_list:
            if event.type == pygame.MOUSEWHEEL:
                self.modifier=5
                if event.x > 0 or event.y > 0:
                    self.plus()
                if event.x < 0 or event.y < 0:
                    self.minus()

            elif event.type == pygame.KEYDOWN:
                # if an arrow key is pressed it moves the bar by 5 in
                # the corrisponding direction
                if event.key == pygame.K_UP:
                    self._key_clicked[0]=True
                elif event.key == pygame.K_DOWN:
                    self._key_clicked[1]=True

            elif event.type == pygame.KEYUP:
                # if an arrow key is un-pressed it stops moving the bar
                if event.key == pygame.K_UP:
                    self._key_clicked[0]=False
                elif event.key == pygame.K_DOWN:
                    self._key_clicked[1]=False
            
        if self._key_clicked[0] ^ self._key_clicked[1]:
            if self._key_clicked[0]:
                self.plus()
            elif self._key_clicked[1]:
                self.minus()

        self._bar.init_rect(x=0, y=self._start+self._translate)

        self.image.fill(colors.transparent)
        self._g.draw(self.image)

    @classmethod
    def scroller(
        cls,
        utilities: Utilities=utilities,
        *args,
        **kwargs
        ) -> None:
        """
        This class type will create a scrollbar all the way to the left,
        in such a way that it fills all the screen
        (except for the optional values)

        INPUT: 
        - screen_rect [pygame.Rect] -> dimensions of the screen
        - scroll_len [float|int]    -> lenght it it is wanted to scroll
        - window_y [float|int]      -> value of where in its height,
                                        put the VerticalBar
        - window_h [float|int]      -> value of the height of the image
        - booleans [Boleans]        -> the Booleans variable used for one
                                        little check
        - colors [Colors]           -> the Colors used for the image
        """

        t = cls(
            utilities=utilities,
            *args,
            **kwargs
            )
        t.refresh, t._refresh = t._refresh, t.refresh
        return t

    def _refresh(
        self,
        screen_rect:pygame.Rect,
        scroll_len:float,
        window_y:float=0,
        window_h:float=0,
        start_bar_init:bool=True,
        colors: Colors=utilities.colors
        ) -> None:
        '''
        This function let re-use the same object without creating a new one
        when resizing the screen. It is used for VarticalBar.scroller()
        
        INPUT:
        - screen_rect [pygame.Rect] -> dimensions of the screen
        - scroll_len [float|int]    -> lenght it it is wanted to scroll
        - window_y [float|int]      -> value of where in its height,
                                        put the VerticalBar
        - window_h [float|int]      -> value of the height of the image
        - start_bar_init [bool|int] -> if True, the old height-point, resized,
                                        will be used,
                                        otherways it will be put at 0
        - colors [Colors]           -> the Colors used for the image
        '''

        if window_h==0:
            window_h=screen_rect.h

        self._refresh(
            self.button_length,
            window_h,
            scroll_len,
            screen_rect.h,
            start_bar_init,
            colors = colors
            )
        self.init_rect(right=screen_rect.w, y=window_y)

    def displayer(self) -> pygame.Rect:
        """
        It returns the rect of this object but inflated, by 2 px for each line
        
        OUTPUT:
        - [pygame.Rect] -> is the inflated rect of the object
        """
        
        return self.rect.inflate(4,4)
    
if __name__ == "__main__":
    class Song:
        ID3_V24 = (2,4,0)

        @staticmethod
        def droppable():
            return {
                "title":"Titolo",
                "album":"Album",
                "artist":"Artista",
                "album_artist":"Artista album",
                "composer":"Compositore",
                "genre":"Genere"
            }
        @staticmethod
        def non_droppable():
            return {
                "track_num": "Numero traccia",
                "disc_num": "Numero disco",
                "recording_date":"Data",
                "comments":"Commenti",
                "images":"Immagini"
            }
        @staticmethod
        def info():
            return {
                'time_secs':'Minuti: {}',
                'size_bytes':'Dimensioni: {}',
                'file':'Nome: {}'
            }
        @staticmethod
        def order():
            return (
                "title",
                "album",
                "artist",
                "album_artist",
                "artist_origin",
                "composer",
                "genre",
                "track_num",
                "disc_num",
                "recording_date",
                "images",
                "comments"
                )

        def __init__(self, path:str, file:str) -> None:
            self.path = path
            self.file = file
            self.__mp3 = None
            self.__comments = None
            self.__mp3__comments = None
        
        def get_Sound(self) -> pygame.mixer.Sound:
            return pygame.mixer.Sound(osjoin(self.path,self.file))

        @staticmethod
        def __check(func):

            def checker(self,*args,**kwargs):

                if not self.__mp3:
                    self.__mp3 = eyeload(osjoin(self.path,self.file))
                    if self.__mp3.tag.version<self.ID3_V24:
                        self.__mp3.tag.version=self.ID3_V24

                return func(self,*args,**kwargs)
            
            return checker

        @property
        @__check
        def title(self) -> str:
            return self.__mp3.tag.title

        @title.setter
        @__check
        def title(self,title:str) -> None:
            self.__mp3.tag.title = title

        @property
        @__check
        def album(self) -> str:
            return self.__mp3.tag.album

        @album.setter
        @__check
        def album(self,album:str) -> None:
            self.__mp3.tag.album = album

        @property
        @__check
        def album_artist(self) -> str:
            return self.__mp3.tag.album_artist

        @album_artist.setter
        @__check
        def album_artist(self,album_artist:str) -> None:
            self.__mp3.tag.album_artist = album_artist

        @property
        @__check
        def artist(self) -> str:
            return self.__mp3.tag.artist

        @artist.setter
        @__check
        def artist(self,artist:str) -> None:
            self.__mp3.tag.artist = artist

        @property
        @__check
        def composer(self) -> str:
            return self.__mp3.tag.composer

        @composer.setter
        @__check
        def composer(self,composer:str) -> None:
            self.__mp3.tag.composer = composer

        @property
        @__check
        def genre(self) -> str:
            if self.__mp3.tag.genre:
                return self.__mp3.tag.genre.name
            else:
                return self.__mp3.tag.genre
            
        @genre.setter
        @__check
        def genre(self,genre:str) -> None:
            self.__mp3.tag.genre = genre

        @property
        @__check
        def track_num(self) -> tuple[int,int|None]:
            t = self.__mp3.tag.track_num
            return t[0],t[1]

        @track_num.setter
        @__check
        def track_num(self,data:tuple[int,int|None]|int) -> None:
            #this, total = data
            try:
                self.__mp3.tag.track_num = data#(this,total)
            except:
                ...

        @property
        @__check
        def disc_num(self) -> tuple[int,int|None]:
            t = self.__mp3.tag.disc_num
            return t[0],t[1]

        @disc_num.setter
        @__check
        def disc_num(self,data:tuple[int,int|None]|int) -> None:
            #this, total = data
            try:
                self.__mp3.tag.disc_num = data#(this,total)
            except:
                ...

        @property
        @__check
        def recording_date(self) -> None:
            t = self.__mp3.tag.recording_date
            try:
                if t is None:
                    return (None,None,None,None,None,None)
                
                elif "T" in (t:=str(t)):
                    t1,t2 = t.split("T")
                    t1=t1.split("-")
                    t2 = t2.split(":")
                    return tuple((*t1,*(t2[i] if i<len(t2) else None for i in range(3))))
                
                t1=t.split("-")
                return tuple((*(t1[i] if i<len(t1) else None for i in range(3)),None,None,None))

            except:
                return (None,None,None,None,None,None)

        @recording_date.setter
        @__check
        def recording_date(self,data:tuple[int,...]) -> None:
            year,*data = data
            if year is None:
                self.__mp3.tag.recording_date = None
                return
            date = str(year)
            mode = ("-{}","-{}","T{}",":{}",":{}")
            for d,m in zip(data,mode):
                if d is None:
                    break
                date+=m.format(d)
            self.__mp3.tag.recording_date = date

        @property
        @__check
        def comments(self) -> list[tuple[str,str,bytes]]:
            if self.__mp3__comments is None:
                self.__mp3__comments = self.__mp3.tag.comments
                self.__comments = [(i.description,i.text,i.lang) for i in self.__mp3__comments]
            return self.__comments
        
        @comments.deleter
        @__check
        def comments(self) -> None:
            for i in self.comments:
                self.__mp3__comments.remove(i[0],i[2])
            self.__comments.clear()

        @comments.setter
        @__check
        def comments(self, data:tuple[tuple[str,str],...]) -> None:
            "data is a tuple of description and text"
            self.comments
            for d in data:
                self.__mp3__comments.set(*d)

        @property
        @__check
        def images(self) -> list[tuple[str,str,bytes]]:
            return [(i.description,i.image_data,None) if i.image_data else (i.description,None,i.img_url) for i in self.__mp3.tag.images]

        @images.deleter
        @__check
        def images(self) -> None:
            try:
                for i in self.__mp3.tag.images:
                    self.__mp3.tag.images.remove(i.description)
            except:
                pass

        @images.setter
        @__check
        def images(self, data:tuple[str, bytes|None, str]) -> None:
            """
            data is description:str, img_data:bytes|None, mime_type:str
            mime_type has to be the type of the file image
            """
            description, img_data, mime_type = data
            self.__mp3.tag.images.set(3,img_data,f"image/{mime_type}", description, None)

        @__check
        def del_images(self, description:str):
            try:
                self.__mp3.tag.images.remove(description)
            except:
                ...

        @property
        @__check
        def time_secs(self) -> str:
            if self.__mp3.info:
                t = self.__mp3.info.time_secs
                return f"{int(t//60)}:{int(t%60)}"
            return ""
        
        @property
        @__check
        def size_bytes(self) -> str:
            if self.__mp3.info:
                return f"{self.__mp3.info.size_bytes/1024:.2f} Kb"
            return ""

        @__check
        def close(self, utilities:Utilities=utilities) -> None:
            self.__mp3.tag.save()

            if utilities.settings['rename']:
                t = self.newfile(utilities)
                k = f"{t}.mp3"
                if k.lower()!=self.file.lower():
                    if osexists(osjoin(self.path,k)):
                        self.quit()
                        raise NameError(f"Esiste già:{t}")
                    self.__mp3.rename(t)
                    self.file = k

            self.quit()

        def quit(self):
            if self.__mp3:
                self.__mp3= None
                self.__comments = None
                self.__mp3__comments = None

        @staticmethod
        def example() -> dict[str,str]:
            return {
                "title":"Sweet Dreams",
                "album":"Single",
                "artist":"We Are Magonia",
                "album_artist":None,
                "composer":"Annie Lennox, Dave Stewart",
                "genre":None,
                "track_num": (1,None),
                "disc_num":(None,None),
                "recording_date":"2020-03-10T00:00:00",
                "comments":[('source','https://www.youtube.com/watch?v=yOwA1yAbHSo')],
                "images":[],
                'time_secs':'3:48',
                'size_bytes':'8980.48 Kb',
                '__file__':'We are Magonia: sweet dreams'
            }
        
        @staticmethod
        def name() -> dict[str,str]:
            return {
                "title":"Titolo",
                "album":"Album",
                "artist":"Artista",
                "album_artist":"Artista album",
                "composer":"Compositore",
                "genre":"Genere",
                "track_num": "Numero traccia",
                "disc_num": "Numero disco",
                "recording_date":"Data",
                "comments":"Commenti",
                "images":"Immagini",
                'time_secs':'Minuti:',
                'size_bytes':'Dimensioni:'
            }

        def newfile(self,utilities:Utilities=utilities):
            if utilities.settings['check_None']:
                t = {}
                for tt in findall(r'{(.*?)}',utilities.settings['rename']):
                    k = getattr(self.__mp3.tag,tt)
                    if k is None:
                        break
                    t[tt] = k
                else:
                    #through the whole loop
                    return utilities.filename(utilities.settings['rename'].format(**t))
                #breaked:
                return self.file.rsplit(".",1)[0]
            
            return  utilities.filename(utilities.settings['rename'].format(**{t:getattr(self.__mp3.tag,t) for t in findall(r'{(.*?)}',utilities.settings['rename'])})) 
    
    class ErrorScreen:
        # This class is used to show any kind of error

        __slots__ = (
            'utilities',    #[Utilities]                   -> utilities object
            'magic_screen', #[list[pygame.Surface,tuple[int]]]
                            #                           -> it is the alphed screen
                            #                               with all the numbers
                            #                               and its position
            'big_rect',     #[pygame.Surface]           -> is the scree where the
                            #                               new numbers are blitted
            '_k',           #[int]                      -> is the number of numbers
                            #                               is wanted to blit
            '_yrange',      #[range]                    -> is the range of height
                            #                               is possible to blit all
                            #                               the numbers at the
                            #                               start
            '_xrange',      #[range]                    -> is the range of
                            #                               horizontal position
                            #                               where to blit all
                            #                               the numbers
            '_nn',          #[tuple[pygame.Surface]]    -> rendered numbers
            '_speeds',      #[tuple[int]]               -> random speeds
            'numbers',      #[tuple[pygame.Surface]]    -> choosed number to
                            #                               display on the
                            #                               screen each frames
            'positions',    #[tuple[list[int,int]]]     -> choosed random position
                            #                               for each number to
                            #                               display on the
                            #                               screen each frames
            'cncButton',    #[NormalButton]             -> button where to stop
                            #                               the download, used by 
                            #                               ed_showError()
            'bk',           #[bool]                     -> bool that handle bk
            '_choice',
            '_choices'
            )

        def __init__(self, utilities:Utilities=utilities) -> None:
            """
            It initializes the error screen, which will be shown as numbers of
            matrix, when something goes really wrong

            INPUT:
            - screen [Screen]       -> screen object
            - booleans [booleans]   -> booleans object
            """

            #base settings
            self.utilities = utilities
            
            from random import choice,choices
            self._choice = choice
            self._choices = choices

            #blitted screen
            self.magic_screen:pygame.Surface
            #rect used to draw the current set of numbers.
            #It is blitted on magic_screen
            self.big_rect:pygame.Surface

            #quantity of numbers to blit
            self._k:int
            #range for the positions
            self._yrange:range
            self._xrange:range
            
            #rendered numbers
            self._nn:tuple
            #random speeds
            self._speeds:tuple

            #positions and numbers to blit on bigrect
            self.numbers:list
            self.positions:tuple
            
        def _up(self) -> None:
            """
            it just updates the nambers with the respect position
            """
            
            h = self.utilities.screen.get_rect().h

            #for each number
            for i in range(self._k):

                #it takes a random number
                self.numbers[i] = self._choice(self._nn)

                #it lowers its position if it is still on the screen
                if self.positions[i][1]<h:
                    self.positions[i][1]+=self._speeds[i]

                #it resets the position if it is down outside the screen
                else:
                    self.positions[i][:] = \
                        self._choice(self._xrange),self._choice(self._yrange)

        def _res(self, width:int, height:int) -> None:
            """
            It sets the dimension for each object

            INPUT:
            - width [int]   -> the width of the screen
            - height [int]  -> the height of the screen
            """
            
            #it updates the size of the numbers
            ll_font = pygame.font.SysFont(self.utilities.corbel, height//30)
            self._nn = tuple(
                ll_font.render(str(i),True,self.utilities.colors.green) for i in range(10)
                )

            # it updates the surfaces
            self.magic_screen = [pygame.Surface((width,height)),(0,0)]
            self.magic_screen[0].fill(self.utilities.colors.black)
            self.big_rect = [
                pygame.Surface((width,height),pygame.SRCALPHA),
                (0,0)
                ]
            self.big_rect[0].fill(self.utilities.colors.alphed)

            #it updates each information
            self._k = width//4
            self._yrange = range(-height//2,0)
            self._xrange = range(0,width)
            self._speeds = self._choices(
                range(1,10),
                (1/18, 1/18, 1/9, 1/9, 1/3, 1/9, 1/9, 1/18, 1/18),
                k=self._k
                )
            
            #it updates numbers and positions
            self.numbers = self._choices(self._nn,k=self._k)
            self.positions = tuple(
                [self._choice(self._xrange),yy] for yy in self._choices(self._yrange,k=self._k)
                )
            
        def showError(self, exception:str) -> None:
            """
            This function is called to get the reading section working!
            It is awesome, but not!

            INPUT:
            - exception [str]  -> explanation of the error
            """

            self.utilities.booleans.add()

            #first it updates the screen sizes
            screen_rect = self.utilities.screen.get_rect()
            self._res(screen_rect.w,screen_rect.h)

            #and the font of the exception
            font = pygame.font.SysFont(self.utilities.corbel, screen_rect.h//6,True)
            text = ScrollingSurface()
            text.refresh(screen_rect.w,font.render(exception,True,self.utilities.colors["dark_green"]))
            text.init_rect(x = screen_rect.w/30, y = screen_rect.w/30)

            l_font = pygame.font.SysFont(self.utilities.corbel, screen_rect.h//12)
            l_text = l_font.render("Premi un pulsante qualunque per continuare...Premi un pulsante qualunque per continuare...",True, self.utilities.colors.white)
            l_text = (l_text,(screen_rect.w/30,screen_rect.h/6*5))

            self.utilities.booleans[0]=True
            for _ in range(360):
                self.utilities.screen.tick()

                # lets https://tic80.com/play?cart=3245 if some event is happening
                event_list = pygame.event.get()
                if self.utilities.booleans.check_1(pygame.QUIT, event_list):
                    self.utilities.screen.quit()

                for event in event_list:
                    self.utilities.booleans.update_resizing(event)

                #if any button is pressed by keyboard or mouse,
                #the error screen is stopper to be shown
                if self.utilities.booleans.check_s(
                    (pygame.MOUSEBUTTONDOWN,pygame.KEYDOWN),
                    event_list
                    ):
                    self.utilities.booleans.end()
                    return
                    
                #or also if the screen is changed
                self.utilities.booleans.update_booleans()
                if not self.utilities.booleans[0] or self.utilities.booleans[1]:
                    self.utilities.booleans.end()
                    return

                #it updates the scrolling exception
                text.update(event_list)
                
                #it updates the numbers animation 
                self.magic_screen[0].blit(*self.big_rect)
                for pair in zip(self.numbers,self.positions):
                    self.magic_screen[0].blit(*pair)
                
                #it uopdates the number new positions for the next round
                self._up()

                #it blits everything on the screen
                self.utilities.screen.blit(self.magic_screen)
                self.utilities.screen.blit(l_text)
                self.utilities.screen.draw(text)

                # just display everything done
                pygame.display.update()

            self.utilities.booleans.end()

    class Options:
        def __init__(self, utilities:Utilities=utilities) -> None:
            self.utilities = utilities

        def __call__(self) -> None:
            self.utilities.booleans.add()

            from string import Formatter

            class MissingFormatter(Formatter):
                def get_value(self, key, args, kwds):
                    if key in kwds:
                        # if isinstance(kwds[key],tuple)
                        if kwds[key] is None:
                            raise AttributeError()
                        return kwds[key]
                    return key
                
                def format(self,s:str,args,**kwargs):
                        result = ""
                        while "{" in s:
                            t = s.index("{")
                            result+=s[:t].replace("}","")
                            s = s[t:]
                            if "}" in s:
                                tt = s.index("}")
                                try:
                                    result+=super().format(s[:tt+1],args,**kwargs)
                                except AttributeError:
                                    if args:
                                        return kwargs["__file__"]
                                    else:
                                        result+="None"
                                        s = s[tt+1:]
                                except:
                                    s = s[1:]
                                else:
                                    s = s[tt+1:]
                            else:
                                result+=s[1:]
                                s=""

                        return result+s.replace("}","")
                        
            class ResultFormatter(MissingFormatter):
                def get_value(self, key, args, kwds):
                    if key in kwds:
                        return f"{{{key}}}"
                    return key
                
                def format(self, s: str, **kwargs):
                    return super().format(s, False, **kwargs)
                
            missing = MissingFormatter()
            result = ResultFormatter()

            font = pygame.font.SysFont("corbel",3)

            settings = "SETTINGS"
            settings_s = [None,None]
            explain_b = RectengleText("gray",0,"Seleziona quali di questi dati si vuole tenere la drop table","black")
            
            b = [i=="1" for i in self.utilities.settings["drop"]]
            
            def change(b,i):
                b[i]=not b[i]

            check_b = tuple(
                [CheckButton(j,func=change,func_args=(b,i),utilities=utilities),None,None]
                for i,j in enumerate(b)
            )
            
            __explain_t = "Scrivi come vuoi rinominare ciascun file .mp3. Inserisci tra parentesi graffe {} i metadati del file audio scelti tra: "
            for ar in Song.name():
                __explain_t+=f"'{ar}'; "
            __explain_t = __explain_t[:-2]+ ". Seleziona il box a fianco per non rinominare la canzone nel caso manchino dei metadati"
            explain_t = RectengleText("gray",0,__explain_t,"black")
            del __explain_t

            def invert():
                self.utilities.settings["del_pics"] = int(not self.utilities.settings["del_pics"])

            check_d = CheckButton(self.utilities.settings["del_pics"],func=invert,utilities=utilities)
            explain_d = RectengleText("gray",0,"Seleziona quest'opzione per eliminare le immagini in automatico","black")

            example = self.utilities.settings["rename"]
            
            def inv_res():
                self.utilities.booleans[1]=True
                self.utilities.settings['check_None'] = int(not self.utilities.settings['check_None'])

            check_t = CheckButton(self.utilities.settings["check_None"],func=inv_res,utilities=utilities)
            t = TextBox(example,"Lascia vuoto per non rinominare",writable=True,rule = self.utilities.filename)
            example_s = [None,None]

            q = "Torna indietro"
            q_b = NormalButton(func=self.utilities.booleans.breaker,utilities=utilities)

            little_menu = LittleMenu()
            g = pygame.sprite.Group(c[0] for c in check_b)
            g.add(check_t,t,q_b, explain_t,explain_b,explain_d,check_d)
            del ar

            self.utilities.booleans[1] = True
            while self.utilities.booleans[1]:
                self.utilities.booleans[1] = False
                
                screen_rect = self.utilities.screen.get_rect()
                centerx = screen_rect.w/2
                width = screen_rect.w/6*5

                button_heigh = min(screen_rect.w//20,screen_rect.h//10)
                bigger_font = pygame.font.SysFont(self.utilities.corbel,button_heigh,True)
                font = pygame.font.SysFont(self.utilities.corbel,button_heigh//2)
                little_font = pygame.font.SysFont(self.utilities.corbel,button_heigh//3)
                
                if bigger_font.size(settings)[0]>screen_rect.w:
                    button_heigh//=2
                    bigger_font,font = font, little_font
                    little_font = pygame.font.SysFont(self.utilities.corbel,button_heigh//2)
                
                button_heigh//=2
                settings_s[0] = bigger_font.render(settings,True,self.utilities.colors["black"])
                settings_s[1] = settings_s[0].get_rect(y=button_heigh//2,centerx = centerx)

                explain_t.refresh(width,font,colors=utilities.colors)
                r = explain_t.init_rect(centerx=centerx, y = settings_s[1].bottom+button_heigh)
                h = little_font.size("Pq")[1]
                if max(little_font.size(a)[0]+h*2 for a in Song.name().values())>centerx:
                    little_font = pygame.font.SysFont(self.utilities.corbel,button_heigh//6)
                    h = little_font.size("Pq")[1]
                check_t.refresh(h,colors=utilities.colors)
                r = check_t.init_rect(x = r.x,centery=r.bottom+button_heigh)
                t.refresh(width-(r.width+h/2),font)
                r = t.init_rect(x=r.right+h/2,centery=r.centery)

                example_s[0] = little_font.render(missing.format(example,self.utilities.settings['check_None'],**Song.example()),True,self.utilities.colors["black"])
                example_s[1] = example_s[0].get_rect(centerx=centerx, centery=r.bottom+button_heigh)

                explain_b.refresh(width,font,colors=utilities.colors)
                r = explain_b.init_rect(centerx=centerx, centery = example_s[1].bottom+button_heigh)
                
                bottom = r.bottom
                for i,drop in enumerate(Song.droppable().keys()):
                    if i%2:
                        x+= centerx
                    else:
                        x=centerx/2-button_heigh
                        y=bottom + h
                    check_b[i][0].refresh(h,colors=utilities.colors)
                    r = check_b[i][0].init_rect(x=x,centery=y)
                    check_b[i][1] = little_font.render(drop,True,self.utilities.colors["black"])
                    bottom = r.bottom
                    check_b[i][2] = check_b[i][1].get_rect(x = r.right+h/2, bottom=bottom)
                
                check_d.refresh(h,colors=utilities.colors)
                r = check_d.init_rect(x=centerx/6,y=bottom + h)
                explain_d.refresh(width-h/2*3,font,colors=utilities.colors)
                bottom = explain_d.init_rect(x=r.right+h/2,top=r.top).bottom

                q_b.refresh(font.render(q,True,self.utilities.colors["black"]),colors=utilities.colors)
                q_b.init_rect(centerx=centerx,y=bottom+button_heigh)
                q_b.text_rect("center")

                little_menu.refresh(little_font,colors=utilities.colors)

                del bottom,r,h,width, font, bigger_font

                self.utilities.booleans[0] = True
                while self.utilities.booleans[0]:
                    self.utilities.screen.tick()

                    # events for the action
                    pos = pygame.mouse.get_pos()
                    event_list = pygame.event.get()
                    self.utilities.booleans.update_start(event_list,True)

                    if not self.utilities.booleans[0]:
                        break

                    for event in event_list:
                        self.utilities.booleans.update_resizing(event)
                    self.utilities.booleans.update_booleans()

                    if not self.utilities.booleans[0] or self.utilities.booleans[1]:
                        break
                    
                    if t:
                        t.opened_little_menu()
                        little_menu.init(*pos, screen_rect, copy=t.little_copy, cut=t.little_cut, paste=t.little_paste)
                        little_menu.update(event_list,pos)

                    elif little_menu:
                        little_menu.update(event_list,pos)

                    else:
                        g.update(event_list,pos)
                    
                    if example != str(t):
                        example = str(t)
                        example_s[0] = little_font.render(missing.format(example,self.utilities.settings['check_None'],**Song.example()),True,self.utilities.colors["black"])
                        example_s[1] = example_s[0].get_rect(centerx=centerx, bottom=example_s[1].bottom)
                        
                    if little_menu:
                        self.utilities.screen.draw(little_menu)
                        pygame.display.update(little_menu.get_rect())
                    else:
                        #colore + titolo
                        self.utilities.screen.fill(self.utilities.colors['background'])
                        
                        self.utilities.screen.blit(*(c[1:] for c in check_b),example_s,settings_s)

                        self.utilities.screen.draw(g)
                        
                        # that's t oupdate every sprite
                        pygame.display.update()

            if self.utilities.settings["rename"] != example:
                self.utilities.settings["rename"] = result.format(example,**Song.example())
            self.utilities.settings["drop"] = "".join(str(int(i)) for i in b)
            
            self.utilities.booleans.end()

    class EditPic:

        def __init__(self, utilities:Utilities=utilities) -> None:
            self.utilities = utilities
            self.find=[]
            self.page=0
            if self.utilities.your_dev_api_key and self.utilities.your_project_cx:

                try:
                    from google_images_search import GoogleImagesSearch
                    self.gis=GoogleImagesSearch(self.utilities.your_dev_api_key,self.utilities.your_project_cx, validate_images=False)
                except:
                    self.gis=None
            else:
                self.gis = None

            from io import BytesIO
            self.ioBytesIO = BytesIO

        def del_image(self,song:Song, description:str, images:list):
            song.del_images(description)
            for i in range(len(images)):
                if images[i][0]==description:
                    images[i][-2].kill()
                    images[i][-1].kill()
                    images.pop(i)
                    break
            self.utilities.booleans[1]=True

        def add_image(self, song:Song, description:str, i:bytes, img:pygame.Surface, images:list, g:pygame.sprite.Group):
            song.images = (description,i,"jpeg")
            images.append((description,i,img,RectengleText("black",50,description,"black"),ImageButton(func=self.del_image,func_args=(song, description, images),utilities=utilities)))
            g.add(images[-1][-2:])
            self.utilities.booleans[1]=True

        def sel_image(self, song:Song, i:bytes, img:pygame.Surface, images:list, g:pygame.sprite.Group):
            self.add_image(song,str(self.find[0]),i,img,images,g)
            for f in self.find[1:]:
                f[1].kill()
            self.find[0].kill()
            self.find.clear()

        def search(self, song:Song, what:TextBox, images:list, g:pygame.sprite.Group, g_findet:pygame.sprite.Group):
            try:
                if osisfile(osabspath(str(what))):
                    image = pygame.image.load(osabspath(str(what)))
                    bts = open(osabspath(str(what)),"rb").read()
                    if not self.find:
                        self.find.append(TextBox("","Descrizione"))
                        self.find[0].init_rect()
                        g_findet.add(self.find[0])
                    self.find.append((image,ImageButton(pygame.Surface((1,1)),func = self.sel_image, func_args=(song,bts,image,images,g),utilities=utilities)))
                    g_findet.add(self.find[-1][1])
                    self.utilities.booleans[1]=True
                    return
            except:
                ...
            
            if self.gis is None:
                self.utilities.showError("No given API keys aviable")
                return

            from threading import Thread
            breaker = [False]
            event_list = list(pygame.event.get())
            wait = Thread(target=self.waiting, args=(breaker,event_list), daemon=True)
            wait.start()
            
            event_list.extend(pygame.event.get())

            try:
                self.gis.search({'q':str(what) if str(what) else " ", 'num':5})
            except Exception as e:
                breaker[0] = True
                event_list.extend(pygame.event.get())
                wait.join()
                self.utilities.showError(str(e))
                return
            
            event_list.extend(pygame.event.get())
            
            if not self.find:
                self.find.append(TextBox("","Descrizione"))
                g_findet.add(self.find[0])
            
            event_list.extend(pygame.event.get())

            for _ in range(self.page):
                self.gis.next_page()
                event_list.extend(pygame.event.get())
            self.page+=1
            
            s = pygame.Surface((1,1))
            for image in self.gis.results():
            
                event_list.extend(pygame.event.get())

                try:
                    image = image.get_raw_data()
                    self.find.append(((k:=pygame.image.load(self.ioBytesIO(image))),ImageButton(func = self.sel_image, func_args=(song,image,k,images,g),utilities=utilities)))
                except:
                    continue

                g_findet.add(self.find[-1][1])
                
            breaker[0] = True
            event_list.extend(pygame.event.get())
            wait.join()
            self.page+=1
            self.utilities.booleans[1]=True

        def waiting(self,breaker:list[bool], event_list = list[pygame.event.Event]):
            self.utilities.booleans.add()

            copied = self.utilities.screen.copy()
            transformed= [None,(0,0)]

            width = 64
            loading = pygame.Surface((width,width),pygame.SRCALPHA)
            loading_r:pygame.Rect = None
            r = width/16
            circle = pygame.Surface((r*2,r*2),pygame.SRCALPHA)

            from math import sin,cos
            n = 5
            for i in range(1,1+n):
                pygame.draw.circle(circle,self.utilities.colors["black",255//n*i],(r,r),r)
                loading.blit(circle,(cos(4/n*i)*width/4+width/2,sin(4/n*i)*width/4+width/2))

            i=0
            value = False

            self.utilities.booleans[1] = True
            while self.utilities.booleans[1]:
                self.utilities.booleans[1] = False

                screen_rect = self.utilities.screen.get_rect()
                transformed[0] = pygame.transform.scale(copied,screen_rect.size)
                loading_r = loading.get_rect(bottomright = screen_rect.bottomright)

                self.utilities.booleans[0] = True
                while self.utilities.booleans[0] and not breaker[0]:
                        self.utilities.screen.tick()

                        # events for the action
                        self.utilities.booleans.update_start(event_list,True)

                        if not self.utilities.booleans[0] or breaker[0]:
                            break

                        for event in event_list:
                            self.utilities.booleans.update_resizing(event)
                        self.utilities.booleans.update_booleans()
                        event_list.clear()

                        if not self.utilities.booleans[0] or self.utilities.booleans[1] or breaker[0]:
                            break

                        self.utilities.screen.blit(transformed)
                        t = pygame.transform.rotate(loading,-i**1.4)
                        self.utilities.screen.blit((t,t.get_rect(center = loading_r.center)))

                        i+=1-6*value
                        i%=500
                        if not i:
                            value = not value

                        pygame.display.update()

            self.utilities.booleans.end()

        def __call__(self, song:Song):
            self.utilities.booleans.add()

            try:
                from requests import get as rget

                f =pygame.font.SysFont("corbel",2)
                s = pygame.Surface((1,1))
                short = pygame.Surface((1,1),pygame.SRCALPHA)
                long=pygame.Surface((1,1),pygame.SRCALPHA)
                t = "black"
                search = "Cerca"
                back = "Torna indietro"
                
                little_menu = LittleMenu()

                whole_data = {(k,v):"" if (z:=getattr(song,k)) is None else z for k,v in song.name().items()}
                rectangles = {k:[None,None,RectengleText(t,50,v,t)] for (_,k),v in whole_data.items() if isinstance(v,str)}
                g = pygame.sprite.Group(r for *_,r in rectangles.values())
                g_findet = pygame.sprite.Group()

                v_bar = VerticalBar.scroller(utilities)
                bar =None
                
                for (kk,k),v in whole_data.items():

                    if kk=="images":
                        images = []
                        for (d,i,l) in v:
                            if l and not i:
                                try:
                                    i = rget(l).content
                                except:
                                    song.del_images(d)
                                    return
                            try:
                                img = pygame.image.load(self.ioBytesIO(i))
                            except:
                                song.del_images(d)
                                return
                            
                            images.append((d,i,img,RectengleText(t,50,d,t),ImageButton(func=self.del_image,func_args=(song, d, images),utilities=utilities)))
                            g.add(images[-1][-2:])
                            del d,i,l,img
                        del kk,k,v
                        break
                
                search_t = TextBox("",search)
                search_b = NormalButton(func=self.search,func_args=(song,search_t,images,g, g_findet),utilities=utilities)
                back_b = NormalButton(func=self.utilities.booleans.breaker,utilities=utilities)
                g.add(search_b,search_t)

                del f,s,t,whole_data

                self.utilities.booleans[1] = True
                while self.utilities.booleans[1]:
                    self.utilities.booleans[1] = False

                    screen_rect = self.utilities.screen.get_rect()
                    black = self.utilities.colors["black"]

                    button_heigh = min(screen_rect.w//25,screen_rect.h//10)
                    button_half = int(button_heigh/2)
                    font = pygame.font.Font(self.utilities.magic,button_heigh)
                    small_font = pygame.font.Font(self.utilities.magic,button_half)

                    little_menu.refresh(small_font,colors=utilities.colors)

                    x = y = button_heigh
                    for k,r in rectangles.items():
                        r[0] = font.render(k,True,black)
                        r[1]=r[0].get_rect(x=x,y=y)
                        xx=r[1].right+button_half
                        r[2].refresh(screen_rect.w-(xx+button_heigh),font,colors=utilities.colors)
                        t = r[2].init_rect(x=xx,y=y)
                        y=max(t.bottom,r[1].bottom)+button_half
                        del xx,t,k,r
                    
                    w = button_heigh*3
                    w=(w,w)
                    for img in images:
                        img[-1].refresh(pygame.transform.smoothscale(img[2],w),colors=utilities.colors)
                        t = img[-1].init_rect(x=x,y=y)
                        xx = t.right+button_half
                        img[-2].refresh(screen_rect.w-(xx+button_heigh),font,colors=utilities.colors)
                        img[-2].init_rect(x=xx, centery=t.centery)
                        y=t.bottom+button_half
                        del img,t,xx

                    search_b.refresh(font.render(search,True,black),colors=utilities.colors)
                    t = search_b.init_rect()
                    search_t.refresh(screen_rect.w-(t.w+button_half*5),font)
                    t = search_t.init_rect(x=x,y=y)
                    search_b.init_rect(x=t.right+button_half,centery=t.centery)
                    search_b.text_rect()
                    y=t.bottom+button_half

                    if self.find:
                        self.find[0].refresh(screen_rect.w-button_heigh*2,font)
                        y = self.find[0].init_rect(x=x,y=y).bottom+button_half
                        for img,ib in self.find[1:]:
                            try:
                                ib.refresh(pygame.transform.smoothscale(img,w),colors=utilities.colors)
                            except:
                                ib.refresh(pygame.transform.scale(img,w),colors=utilities.colors)
                            y = ib.init_rect(x=x,y=y).bottom+button_half

                    back_b.refresh(font.render(back,True,black),colors=utilities.colors)
                    t = back_b.init_rect(centerx=screen_rect.w/2,centery=screen_rect.h-button_heigh)
                    back_b.text_rect()

                    short = pygame.transform.scale(short,(screen_rect.w,t.top-button_half))
                    long = pygame.transform.scale(long,(screen_rect.w,y))
                    if long.get_height()>=short.get_height():
                        v_bar.refresh(screen_rect,y*2,window_h=short.get_height(),colors=utilities.colors)
                        bar = v_bar
                    else:
                        bar = None

                    self.utilities.booleans[0] = True
                    while self.utilities.booleans[0]:
                        self.utilities.screen.tick()

                        # events for the action
                        pos = pygame.mouse.get_pos()
                        event_list = pygame.event.get()
                        self.utilities.booleans.update_start(event_list,True)

                        if not self.utilities.booleans[0]:
                            break

                        for event in event_list:
                            self.utilities.booleans.update_resizing(event)
                        self.utilities.booleans.update_booleans()

                        if not self.utilities.booleans[0] or self.utilities.booleans[1]:
                            break
                        
                        if self.find and self.find[0]:
                            self.find[0].opened_little_menu()
                            little_menu.init(*pos, screen_rect, copy=self.find[0].little_copy, cut=self.find[0].little_cut, paste=self.find[0].little_paste)
                            little_menu.update(event_list,pos)
                        elif search_t:
                            search_t.opened_little_menu()
                            little_menu.init(*pos, screen_rect, copy=search_t.little_copy, cut=search_t.little_cut, paste=search_t.little_paste)
                            little_menu.update(event_list,pos)
                        elif little_menu:
                            little_menu.update(event_list,pos)
                        else:
                            back_b.update(event_list,pos)
                            if bar:
                                bar.update(event_list,pos)
                                if short.get_rect().collidepoint(pos):
                                    g_findet.update(event_list,(pos[0],pos[1]-float(bar)))
                                    if not self.utilities.booleans[0] or self.utilities.booleans[1]:
                                        break
                                    g.update(event_list,(pos[0],pos[1]-float(bar)))
                                else:
                                    g_findet.update(event_list,pos,False)
                                    if not self.utilities.booleans[0] or self.utilities.booleans[1]:
                                        break
                                    g.update(event_list,pos,False)
                            else:
                                g_findet.update(event_list,pos)
                                if not self.utilities.booleans[0] or self.utilities.booleans[1]:
                                    break
                                g.update(event_list,pos)
                            
                        if not self.utilities.booleans[0] or self.utilities.booleans[1]:
                            break

                        if little_menu:
                            self.utilities.screen.draw(little_menu)
                            pygame.display.update(little_menu.get_rect())
                        
                        else:
                            self.utilities.screen.fill(self.utilities.colors['background'])
                            short.fill(self.utilities.colors.transparent)
                            long.fill(self.utilities.colors.transparent)
                            g_findet.draw(long)
                            g.draw(long)
                            long.blits(r[:2] for r in rectangles.values())
                            if bar:
                                short.blit(long,(0,float(bar)))
                                self.utilities.screen.blit((short,(0,0)))
                                self.utilities.screen.draw(bar,back_b)
                            else:
                                short.blit(long,(0,0))
                                self.utilities.screen.blit((short,(0,0)))
                            
                            pygame.display.update()

            except Exception as e:
                self.utilities.showError(str(e))

            self.find.clear()
            self.page=0
            self.utilities.booleans.end()

    class EditSong:
        def __init__(self, utilities:Utilities=utilities) -> None:
            self.utilities = utilities
            self.list_mp3:list[Song] = []
            self.options = Options(self.utilities)
            self.edpics = EditPic(utilities)
            self.explorer = lambda x: ossystem(f'explorer.exe /select, "{x}"')

        def __call__(self, wait:bool = False):
            self.utilities.booleans.add()

            try:
                h_char = '日QpL`幽雅に咲墨桜石の国'
                extension= ".mp3"

                self.list_mp3.clear()
                self.list_mp3.extend(Song(self.utilities.settings["directory"],o) for o in oslistdir(self.utilities.settings["directory"]) if osisfile(osjoin(self.utilities.settings["directory"],o)) and o.endswith(extension))
                
                if not self.list_mp3:
                    raise NameError("Folder has no .mp3 files")
                
                title = "Choose a song"
                start = "Start"
                options = "Options"

                v_bar = VerticalBar(utilities= utilities)
                bar = None

                max_lenght = 20_000
                short_s = [pygame.Surface((0,0),pygame.SRCALPHA),None]
                title_s = [None,None]
                if wait:
                    start_b = NormalButton(func=self.run,utilities=utilities)
                else:
                    start_b = NormalButton(func=self.fastrun)
                options_b = NormalButton(func=self.options,utilities=utilities)
                g = pygame.sprite.Group(options_b,start_b)

                self.utilities.booleans[1]=True
                while self.utilities.booleans[1]:
                    self.utilities.booleans[1] = False

                    screen_rect = self.utilities.screen.get_rect()

                    title_heigh = min(screen_rect.w//20,screen_rect.h//10)*2
                    text_heigh = title_heigh//3
                    bigger_font = pygame.font.SysFont(self.utilities.corbel,title_heigh,True)
                    font = pygame.font.Font(self.utilities.magic,text_heigh)
                    text_heigh=max(text_heigh,font.size(h_char)[1],font.size(self.list_mp3[0].file)[1])

                    title_s[0] = bigger_font.render(title,True, self.utilities.colors["black"])
                    title_s[1] = title_s[0].get_rect(centerx = screen_rect.centerx,centery = title_heigh)

                    short_h = screen_rect.h-(text_heigh+title_heigh)*2
                    full_lenght = text_heigh*len(self.list_mp3)
                    if full_lenght>short_h:
                        short_s[0] = pygame.transform.scale(short_s[0],(screen_rect.w-v_bar.button_length,short_h))
                        short_s[1] = short_s[0].get_rect(x=0,y=title_heigh*2)
                        long_s = tuple(pygame.Surface((short_s[1].w,max_lenght if max_lenght*k<full_lenght else full_lenght%max_lenght),pygame.SRCALPHA) for k in range(int(full_lenght//max_lenght)+1))

                        v_bar.refresh(v_bar.button_length,short_s[1].h,full_lenght,short_s[1].h,colors=utilities.colors)
                        v_bar.init_rect(right=screen_rect.w,y=short_s[1].y)
                        bar = v_bar
                    else:
                        short_s[0] = pygame.transform.scale(short_s[0],(screen_rect.w,short_h))
                        short_s[1] = short_s[0].get_rect(x=0,y=title_heigh*2)
                        long_s = (pygame.Surface((short_s[1].w,full_lenght),pygame.SRCALPHA),)

                        bar = None
                        
                    y = 0
                    j=0
                    black = self.utilities.colors["black"]
                    for song in self.list_mp3:
                        t = y%max_lenght
                        long_s[j].blit(font.render(song.file,True,black),(0,t))

                        if t+text_heigh>=max_lenght:
                            j+=1
                            long_s[j].blit(font.render(song.file,True,black),(0,t-max_lenght))

                        y+=text_heigh

                    w = max(font.size(options)[0],font.size(start)[0])
                    options_b.refresh(font.render(options,True,black),w,colors=utilities.colors)
                    r = options_b.init_rect(centerx=screen_rect.w//3,centery=screen_rect.h-text_heigh)
                    options_b.text_rect()
                    start_b.refresh(font.render(start,True,black),w,colors=utilities.colors)
                    start_b.init_rect(centerx=screen_rect.w//3*2,centery=r.centery)
                    start_b.text_rect()

                    # del r,font,bigger_font
                    del r,bigger_font

                    self.utilities.booleans[0] = True
                    while self.utilities.booleans[0]:
                        self.utilities.screen.tick()

                        # events for the action
                        pos = pygame.mouse.get_pos()
                        event_list = pygame.event.get()
                        self.utilities.booleans.update_start(event_list,True)

                        if not self.utilities.booleans[0]:
                            break

                        for event in event_list:
                            self.utilities.booleans.update_resizing(event)

                            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1 and short_s[1].collidepoint(pos):
                                if bar:
                                    w = int((pos[1]-short_s[1].y-float(bar))//text_heigh)
                                else:
                                    w = int((pos[1]-short_s[1].y)//text_heigh)
                                if w>=len(self.list_mp3):
                                    w=-1

                            elif event.type==pygame.MOUSEBUTTONUP and event.button==1 and short_s[1].collidepoint(pos):
                                if bar and w==(pos[1]-short_s[1].y-float(bar))//text_heigh:
                                    start_b.func(w)
                                elif w==(pos[1]-short_s[1].y)//text_heigh:
                                    start_b.func(w)

                        self.utilities.booleans.update_booleans()

                        if not self.utilities.booleans[0] or self.utilities.booleans[1]:
                            break
                        
                        g.update(event_list,pos)
                        short_s[0].fill(self.utilities.colors.transparent)
                        if bar:
                            bar.update(event_list,pos)
                            j=int(-float(bar)//max_lenght)
                            y=float(bar)+max_lenght*j
                            short_s[0].blit(long_s[j],(0,y))
                            if y+max_lenght>0 and j+1<len(long_s):
                                short_s[0].blit(long_s[j+1],(0,y+max_lenght))
                        else:
                            short_s[0].blit(long_s[0],(0,0))

                        self.utilities.screen.fill(self.utilities.colors["background"])
                        self.utilities.screen.blit(title_s,short_s)
                        self.utilities.screen.draw(g)
                        if bar:
                            self.utilities.screen.draw(bar)

                        pygame.display.update()
                        
            except Exception as e:
                self.utilities.showError(str(e))

            self.utilities.booleans.end()
        
        def __prev(self):
            self.change_song=-1
            self.save=True
            self.utilities.booleans.breaker()
        def __follow(self):
            self.change_song=1
            self.save=True
            self.utilities.booleans.breaker()
        def __stop(self):
            self.change_song=0
            self.save=False
            self.utilities.booleans.breaker()
        def __refresh(self):
            self.change_song=0
            self.save=False
            self.utilities.booleans[1] = True
        
        @staticmethod
        def isdigit(x:str)->str:
            return "".join(y for y in x if y.isdigit())

        def fastrun(self,starting:int=0):
            self.utilities.booleans.add()

            if not utilities.settings['rename']:
                self.utilities.booleans.end()
                return 
            
            try:
                stop = "Interrompi"
                cont = "Continua"
                wait = "Aspetta"
                work = [True]
                wait_s = [None,None]
                num_s = [None,None]
                file_s = [None,pygame.Rect(0,0,0,0)]
                surfaces=(wait_s,num_s,file_s)
                name = ""
                black = self.utilities.colors["black"]

                error="Errore.txt"
                explaining = "\n\Convertendo: {}"
                breaked = False

                def s():
                    if s.work[0]:
                        s.work[0] = False
                        return
                    self.utilities.booleans.breaker()
                s.work = work

                def c():
                    c.work[0] = True
                c.work = work

                t = pygame.Surface((1,1))
                stop_b = NormalButton(func=s,utilities=utilities)
                cont_b = NormalButton(func=c,utilities=utilities)

                self.utilities.booleans[1] = True
                while self.utilities.booleans[1]:
                    self.utilities.booleans[1] = False

                    screen_rect = self.utilities.screen.get_rect()
                    
                    button_heigh = min(screen_rect.w//25,screen_rect.h//10)
                    bigger_font = pygame.font.SysFont(self.utilities.corbel,button_heigh*2,True)
                    font = pygame.font.Font(self.utilities.magic,button_heigh)
                    small_font = pygame.font.SysFont(self.utilities.corbel,int(button_heigh/2))

                    wait_s[0] = bigger_font.render(wait,True,black)
                    wait_s[1] = wait_s[0].get_rect(centerx=screen_rect.centerx,centery=button_heigh/2*3)
                    num_s[1] = (0,screen_rect.h-button_heigh/2)
                    file_s[1] = (0,screen_rect.centery)

                    w_min = min(small_font.size(stop)[0],small_font.size(cont)[0])
                    stop_b.refresh(small_font.render(stop,True,black),w_min,colors=utilities.colors)
                    stop_b.init_rect(centerx=screen_rect.w/3,centery=screen_rect.h/4*3)
                    stop_b.text_rect()
                    cont_b.refresh(small_font.render(cont,True,black),w_min,colors=utilities.colors)
                    cont_b.init_rect(centerx=screen_rect.w/3*2,centery=screen_rect.h/4*3)
                    cont_b.text_rect()

                    self.utilities.booleans[0] = True
                    for starting in range(starting,len(self.list_mp3)):
                        try:
                            name = self.list_mp3[starting].file
                            if self.utilities.settings['del_pics']:
                                del self.list_mp3[starting].images
                            
                            self.list_mp3[starting].close()

                        except:
                            try:
                                if breaked:
                                    with open(error,"a",encoding=self.utilities.decoder) as e:
                                        e.write(explaining.format(self.list_mp3[starting].file))
                                else:
                                    breaked=True
                                    with open(error,"w+",encoding=self.utilities.decoder) as e:
                                        e.write("Error while renaming the following files into")
                                        e.write(explaining.format(self.list_mp3[starting].file))
                            except Exception as e:
                                self.utilities.showError(str(e))
                            
                            self.list_mp3[starting].quit()

                        num_s[0] = small_font.render(str(starting),True,black)
                        file_s[0] = font.render(name,True,black)
                        
                        # events for the action
                        pos = pygame.mouse.get_pos()
                        event_list = pygame.event.get()
                        self.utilities.booleans.update_start(event_list,True)

                        if not self.utilities.booleans[0]:
                            break

                        for event in event_list:
                            self.utilities.booleans.update_resizing(event)
                        self.utilities.booleans.update_booleans()

                        stop_b.update(event_list,pos)
                        if work[0]:
                            cont_b.update(event_list,pos)

                        if not self.utilities.booleans[0] or self.utilities.booleans[1]:
                            break
                        
                        self.utilities.screen.fill(self.utilities.colors['background'])
                        self.utilities.screen.blit(*surfaces)
                        self.utilities.screen.draw(stop_b)
                        if work[0]:
                            self.utilities.screen.draw(cont_b)
                        
                        pygame.display.update()

            except Exception as e:
                self.utilities.showError(str(e))

            self.utilities.booleans.end()
            self.utilities.booleans[1]=True

        def run(self, starting:int=0):
            self.utilities.booleans.add()

            try:
                delete = "Rimuovi"
                add = "Aggiungi"
                stop = "Stop"
                prev = "Precedente"
                follow = "Prossima"
                refresh = "Ricarica"
                nr_tot = ("Nr","Tot")
                calendar = ("AAAA","MM","DD","HH","MM","SS")
                desc = "Descrizione"
                content = "Contenuto"
                edit = "Gestisci"

                g = pygame.sprite.Group()
                g_super = pygame.sprite.Group()
                g_diff = pygame.sprite.Group()
                little_menu = LittleMenu()
                all_boxes = []
                all_drops = []
                v_bar = VerticalBar.scroller(utilities)
                bar =None
                shorter = pygame.Surface((1,1),pygame.SRCALPHA)
                longer = pygame.Surface((1,1),pygame.SRCALPHA)

                player = pygame.Surface((32,32),pygame.SRCALPHA)
                pygame.draw.rect(player,self.utilities.colors['black'],pygame.Rect(4,4,8,24))
                pygame.draw.polygon(player,self.utilities.colors['black'],((16,4),(16,27),(27,16),(27,15)))
                stopper = pygame.Surface((32,32),pygame.SRCALPHA)
                pygame.draw.rect(stopper,self.utilities.colors['black'],pygame.Rect(8,8,16,16))
                downer = pygame.Surface((32,32),pygame.SRCALPHA)
                pygame.draw.rect(downer,self.utilities.colors['black'],pygame.Rect(4,12,24,8))
                upper = downer.copy()
                pygame.draw.rect(upper,self.utilities.colors['black'],pygame.Rect(12,4,8,24))
                folder = pygame.Surface((32,32),pygame.SRCALPHA)
                pygame.draw.polygon(folder,self.utilities.colors['black'],((4,24),(4,8),(12,8),(14,10),(24,10),(24,14),(8,14)),2)
                pygame.draw.polygon(folder,self.utilities.colors['black'],((4,24),(8,14),(28,14),(20,24)),2)

                player_b = ImageButton(func =lambda: self.utilities.music.start(self.list_mp3[starting].get_Sound()),utilities=utilities)
                stopper_b = ImageButton(func = self.utilities.music.stop,utilities=utilities)
                upper_b = ImageButton(func = self.utilities.music.up,utilities=utilities)
                downer_b = ImageButton(func = self.utilities.music.down,utilities=utilities)
                folder_b = ImageButton(func=lambda: self.explorer(osjoin(self.list_mp3[starting].path,self.list_mp3[starting].file)),utilities=utilities)

                prev_b = NormalButton(func=self.__prev,utilities=utilities)
                follow_b = NormalButton(func=self.__follow,utilities=utilities)
                stop_b = NormalButton(func=self.__stop,utilities=utilities)
                refresh_b = NormalButton(func=self.__refresh,utilities=utilities)
                g_diff.add(prev_b,follow_b,stop_b,refresh_b,player_b,stopper_b,upper_b,downer_b,folder_b)

                droppable:dict[str,tuple[Drop|None,TextBox,list[pygame.Surface,pygame.Rect]]] = {}
                boxes = {}
                infos = {'file':["",None,None]}

                for d,(k,v) in zip(self.utilities.settings["drop"],Song.droppable().items()):

                    b=TextBox(empty_text=v)
                    all_boxes.append(b)
                    if int(d):
                        droppable[k]=([v,None,None],Drop(b,k),b)
                        droppable[k][-2].init_rect()
                        g_super.add(droppable[k][1])
                        all_drops.append(droppable[k][1])
                    else:
                        droppable[k]=([v,None,None],None,b)
                        g.add(b)
                
                for k,v in Song.non_droppable().items():
                    
                    if "num" in k:
                        b = (TextBox(empty_text=nr_tot[0],max_char=6,rule=self.isdigit),TextBox(empty_text=nr_tot[1],max_char=6,rule=self.isdigit))
                        all_boxes.extend(b)
                        g.add(*b)
                        boxes[k]=([v,None,None],b)
                        
                    elif "date" in k:
                        b = (TextBox(empty_text=calendar[0],max_char=4,rule=self.isdigit),TextBox(empty_text=calendar[1],max_char=2,rule=self.isdigit),TextBox(empty_text=calendar[2],max_char=2,rule=self.isdigit),TextBox(empty_text=calendar[3],max_char=2,rule=self.isdigit),TextBox(empty_text=calendar[4],max_char=2,rule=self.isdigit),TextBox(empty_text=calendar[5],max_char=2,rule=self.isdigit))
                        all_boxes.extend(b)
                        g.add(*b)
                        boxes[k]=([v,None,None],b)
                    
                    elif "comments" == k:
                        def __del(list_boxes:list[pygame.sprite.Sprite],all_boxes:list = all_boxes):
                            
                            del self.list_mp3[starting].comments
                            for _ in range(len(list_boxes)):
                                x = list_boxes.pop()
                                all_boxes.remove(x)
                                x.kill()
                        
                        def __add(list_boxes:list[pygame.sprite.Sprite],x,y,space,w,ww,font,this_b,g:pygame.sprite.Group=g,all_boxes = all_boxes):
                            list_boxes.append(TextBox("",desc,64))
                            list_boxes[-1].refresh(w,font)
                            r = list_boxes[-1].init_rect(x=x,y=y)
                            list_boxes.append(TextBox("",content,1024))
                            list_boxes[-1].refresh(ww,font)
                            list_boxes[-1].init_rect(x=r.right+space,y=y)
                            g.add(list_boxes[-2:])
                            all_boxes.extend(list_boxes[-2:])
                            this_b.func.args=(*this_b.func.args[:2],r.bottom+space/2,*this_b.func.args[3:])
                            
                        c=[]
                        b = (NormalButton(func=__add, func_args=(c,),utilities=utilities),NormalButton(func=__del, func_args=(c,),utilities=utilities),c)
                        g.add(*b[:2])
                        boxes[k]=([v,None,None],b)
                        del __del,__add

                    elif "images" == k:
                        b = NormalButton(func=lambda:self.edpics(self.list_mp3[starting]),utilities=utilities)
                        g.add(b)
                        boxes[k]=([v,None,None],b)

                for k,v in Song.info().items():
                    infos[k] = [v,None,None]

                f:TextBox = None
                p:TextBox = None
                n:TextBox = None
                for k in Song.order():
                    if k in droppable:
                        if f is not None:
                            n = droppable[k][-1]
                            p.set_next(n)
                            n.set_prev(p)
                            p = n
                        else:
                            f = p = droppable[k][-1]

                    elif "num" in k or "date" in k:
                        for n in boxes[k][-1]:
                            p.set_next(n)
                            n.set_prev(p)
                            p = n
                p.set_next(f)
                f.set_prev(p)

                del b,k,v,d,p,n,f

                self.change_song = 0
                self.save=False
                self.utilities.booleans[1] = True
                while self.utilities.booleans[1]:
                    self.utilities.booleans[1] = False

                    screen_rect = self.utilities.screen.get_rect()
                    black = self.utilities.colors["black"]
                    try:
                        if self.utilities.settings['del_pics']:
                            del self.list_mp3[starting].images

                        button_heigh = min(screen_rect.w//25,screen_rect.h//10)//3*2
                        font = pygame.font.Font(self.utilities.magic,button_heigh)
                        small_font = pygame.font.Font(self.utilities.magic,int(button_heigh/2))

                        little_menu.refresh(small_font,colors=utilities.colors)

                        x = y = button_heigh
                        for k in Song.order():
                            if k in droppable:
                                drop = droppable[k]
                                drop[0][1] = font.render(drop[0][0],True,black)
                                drop[0][2] = drop[0][1].get_rect(x=x,y=y)
                                drop[-1].refresh(screen_rect.w-(drop[0][2].right+button_heigh*2),font)
                                drop[-1].replaceText(getattr(self.list_mp3[starting],k) if getattr(self.list_mp3[starting],k) else "")
                                r = drop[-1].init_rect(x=drop[0][2].right+button_heigh,bottom=drop[0][2].bottom)
                                if drop[-2] is not None:
                                    drop[-2].refresh(small_font,r.w)
                                    drop[-2].init_rect(topleft=r.bottomleft)
                                y = r.bottom+button_heigh/2

                            elif "num" in k:
                                drop = boxes[k]
                                drop[0][1] = font.render(drop[0][0],True,black)
                                r = drop[0][2] = drop[0][1].get_rect(x=x,y=y)
                                num = getattr(self.list_mp3[starting],k)
                                for i,b in zip(num,drop[-1]):
                                    b.refresh(screen_rect.w/4,font)
                                    b.replaceText(str(i) if i else "")
                                    r = b.init_rect(x=r.right+button_heigh,bottom=drop[0][2].bottom)

                                y = r.bottom+button_heigh/2
                                del num
                            
                            elif "date" in k:
                                drop = boxes[k]
                                drop[0][1] = font.render(drop[0][0],True,black)
                                r = drop[0][2] = drop[0][1].get_rect(x=x,y=y)
                                data = getattr(self.list_mp3[starting],k)
                                
                                for i,b in zip(data,drop[-1]):
                                    b.refresh(screen_rect.w/10,font)
                                    b.replaceText(str(i) if i else "")
                                    r = b.init_rect(x=r.right+button_heigh,bottom=drop[0][2].bottom)

                                y = r.bottom+button_heigh/2
                                del data

                            elif "comments" == k:
                                drop = boxes[k]
                                drop[0][1] = font.render(drop[0][0],True,black)
                                drop[0][2] = drop[0][1].get_rect(x=x,y=y)
                                drop[-1][0].refresh(font.render(add,True,black),colors=utilities.colors)
                                r = drop[-1][0].init_rect(x=drop[0][2].right+button_heigh,bottom=drop[0][2].bottom)
                                drop[-1][0].text_rect()
                                drop[-1][1].refresh(font.render(delete,True,black),colors=utilities.colors)
                                drop[-1][1].init_rect(x=r.right+button_heigh,bottom=drop[0][2].bottom)
                                drop[-1][1].text_rect()
                                comments = getattr(self.list_mp3[starting],k)
                                y=r.bottom+button_heigh/2
                                i=0
                                dr = drop[-1][-1]
                                for description,comment,*_ in comments:
                                    if i<len(dr):
                                        dr[i].refresh(screen_rect.w/4,font)
                                        dr[i].replaceText(description if description else "")
                                        r = dr[i].init_rect(x=x,y=y)
                                        i+=1
                                        dr[i].refresh(screen_rect.w/3*2,font)
                                        dr[i].replaceText(comment if comment else "")
                                        r = dr[i].init_rect(x=r.right+button_heigh,bottom=r.bottom)
                                        i+=1
                                        y=r.bottom+button_heigh/2
                                    else:
                                        dr.append(TextBox(description if description else "",desc,64))
                                        dr[-1].refresh(screen_rect.w/4,font)
                                        r = dr[-1].init_rect(x=x,y=y)
                                        dr.append(TextBox(comment if comment else "",content,1024))
                                        dr[-1].refresh(screen_rect.w/3*2-button_heigh,font)
                                        dr[-1].init_rect(x=r.right+button_heigh,bottom=r.bottom)
                                        i+=2
                                        y=r.bottom+button_heigh/2
                                        g.add(dr[-2:])
                                        all_boxes.extend(dr[-2:])
                                
                                drop[-1][0].func.args=(drop[-1][0].func.args[0],x,y,button_heigh,screen_rect.w/4,screen_rect.w/3*2-button_heigh,font,drop[-1][0])
                                
                                for ob in dr[i:]:
                                    ob.kill()
                                del dr[i:], comments
                                
                            elif "images" == k:
                                b = boxes[k]
                                b[0][1] = font.render(b[0][0],True,black)
                                b[0][2] = b[0][1].get_rect(x=x,y=y)
                                b[1].refresh(font.render(edit,True,black),colors=utilities.colors)
                                y=b[1].init_rect(x=b[0][2].right+button_heigh/2,centery=b[0][2].centery).bottom+button_heigh/2
                                b[1].text_rect()

                                del b

                        longer = pygame.transform.scale(longer,(screen_rect.w,y*2))

                        x=0
                        for information in infos:
                            infos[information][1] = small_font.render(infos[information][0].format(getattr(self.list_mp3[starting],information)),True,black)
                            infos[information][2] = infos[information][1].get_rect(x=x,bottom=screen_rect.bottom)
                            x=infos[information][2].right+button_heigh/2
                        y = infos[information][2].y
                        width = min(max(
                            font.size(stop)[0],
                            font.size(prev)[0],
                            font.size(follow)[0],
                            font.size(refresh)[0]
                        ),screen_rect.w/6)+NormalButton.button_space
                        w = screen_rect.w/5
                        x = w/2
                        prev_b.refresh(font.render(prev,True,black),width,width,colors=utilities.colors)
                        prev_b.init_rect(centerx=x,bottom=y)
                        prev_b.text_rect()
                        x+=w
                        follow_b.refresh(font.render(follow,True,black),width,width,colors=utilities.colors)
                        follow_b.init_rect(centerx=x,bottom=y)
                        follow_b.text_rect()
                        x+=w
                        stop_b.refresh(font.render(stop,True,black),width,width,colors=utilities.colors)
                        t = stop_b.init_rect(centerx=x,bottom=y)
                        stop_b.text_rect()
                        x+=w
                        refresh_b.refresh(font.render(refresh,True,black),width,width,colors=utilities.colors)
                        y = refresh_b.init_rect(centerx=x,bottom=y).top
                        refresh_b.text_rect()

                        x+=w
                        ww=(width//5,width//5)
                        stopper_b.refresh(pygame.transform.scale(stopper,ww),colors=utilities.colors)
                        t=tt = stopper_b.init_rect(centerx=x,centery=t.centery)
                        player_b.refresh(pygame.transform.scale(player,ww),colors=utilities.colors)
                        t = player_b.init_rect(right=t.left,centery=t.centery)
                        folder_b.refresh(pygame.transform.scale(folder,ww),colors=utilities.colors)
                        folder_b.init_rect(right=t.left,centery=t.centery)
                        downer_b.refresh(pygame.transform.scale(downer,ww),colors=utilities.colors)
                        tt = downer_b.init_rect(left=tt.right,centery=tt.centery)
                        upper_b.refresh(pygame.transform.scale(upper,ww),colors=utilities.colors)
                        upper_b.init_rect(left=tt.right,centery=tt.centery)

                        shorter = pygame.transform.scale(shorter,(screen_rect.w,y))
                        if longer.get_height()>=shorter.get_height():
                            v_bar.refresh(screen_rect,longer.get_height(),window_h=shorter.get_height(),colors=utilities.colors)
                            bar = v_bar
                        else:
                            bar = None

                        del width,w,x,y,information,t,ww

                        self.utilities.booleans[0] = True
                        while self.utilities.booleans[0]:
                            self.utilities.screen.tick()

                            # events for the action
                            pos = pygame.mouse.get_pos()
                            event_list = pygame.event.get()
                            self.utilities.booleans.update_start(event_list,True)

                            if not self.utilities.booleans[0]:
                                break

                            for event in event_list:
                                self.utilities.booleans.update_resizing(event)
                            self.utilities.booleans.update_booleans()

                            if not self.utilities.booleans[0] or self.utilities.booleans[1]:
                                break
                                
                            for box in all_boxes:
                                if box:
                                    box.opened_little_menu()
                                    little_menu.init(*pos, screen_rect, copy=box.little_copy, cut=box.little_cut, paste=box.little_paste)
                                    little_menu.update(event_list,pos)
                                    break
                            else:
                                if little_menu:
                                    little_menu.update(event_list,pos)
                                else:
                                    if any(all_drops):
                                        for drop in all_drops:
                                            if drop:
                                                if bar:
                                                    drop.update(event_list,(pos[0],pos[1]-float(bar)))
                                                else:
                                                    drop.update(event_list,pos)
                                            else:
                                                drop.box.update(event_list,pos,False)
                                        g.update(event_list,pos,False)
                                        g_diff.update(event_list,pos)

                                    else:
                                        if bar:
                                            bar.update(event_list,pos)
                                            if shorter.get_rect().collidepoint(pos):
                                                g_super.update(event_list,(pos[0],pos[1]-float(bar)))
                                                g.update(event_list,(pos[0],pos[1]-float(bar)))
                                            else:
                                                g_super.update(event_list,pos,False)
                                                g.update(event_list,pos,False)
                                        else:
                                            g_super.update(event_list,pos)
                                            g.update(event_list,pos)
                                        g_diff.update(event_list,pos)

                            if little_menu:
                                self.utilities.screen.draw(little_menu)
                                pygame.display.update(little_menu.get_rect())

                            else:
                                self.utilities.screen.fill(self.utilities.colors['background'])
                                shorter.fill(self.utilities.colors.transparent)
                                longer.fill(self.utilities.colors.transparent)
                                g.draw(longer)
                                drops = None
                                for drop in all_drops:
                                    drop.box.draw(longer)
                                    if drop:
                                        drops = drop
                                if drops:
                                    drops.draw(longer)
                                longer.blits((item[1:] for item,*_ in (droppable|boxes).values()))

                                if bar:
                                    shorter.blit(longer,(0,float(bar)))
                                else:
                                    shorter.blit(longer,(0,0))
                                self.utilities.screen.draw(g_diff)

                                self.utilities.screen.blit((shorter,(0,0)))
                                if bar:
                                    self.utilities.screen.draw(bar)
                                self.utilities.screen.blit(*(item[1:] for item in infos.values()))

                                pygame.display.update()
                        
                        if self.save:
                            try:
                                for k,v in droppable.items():
                                    setattr(self.list_mp3[starting],k,str(v[-1]) if str(v[-1]) else None)
                                for k,(_,v) in boxes.items():
                                    if "num" in k:
                                        setattr(self.list_mp3[starting],k,(str(v[0]) if str(v[0]) else None,str(v[1]) if str(v[1]) else None))
                                    elif "date" in k:
                                        setattr(self.list_mp3[starting],k,tuple(str(vv) if str(vv) else None for vv in v))
                                    elif "comments" == k:
                                        setattr(self.list_mp3[starting],k,tuple((str(v[-1][i*2+1]),str(v[-1][i*2])) for i in range(int(len(v[-1])/2))))


                                for drop in all_drops:
                                    drop.exit()
                                self.list_mp3[starting].close(self.utilities)
                                self.save=False
                            except Exception as e:
                                self.utilities.showError(str(e))
                                self.list_mp3[starting].quit()
                        else:
                            self.list_mp3[starting].quit()
                        
                        if self.change_song>0:
                            self.change_song=0
                            starting+=1
                            self.utilities.booleans[1] = starting<len(self.list_mp3)
                        elif self.change_song<0:
                            self.change_song=0
                            starting-=1
                            self.utilities.booleans[1] = starting>=0
                    except OSError as e:
                        try:
                            open(osjoin(self.list_mp3[starting].path,self.list_mp3[starting].file)).readline()
                            raise e
                        except:
                            self.list_mp3.pop(starting)
                            self.utilities.showError(str(e))
                            if starting>0:
                                starting-=1
                                self.utilities.booleans[1]=True
                            elif len(self.list_mp3):
                                self.utilities.booleans[1]=True

                    except Exception as e:
                        raise e
                      
            except Exception as e:
                self.utilities.showError(str(e))
        
            self.utilities.booleans.end()
            self.utilities.booleans[1]=True

    class Start:
        """
        This class is used to be able to change folder.
        """
        
        def __init__(self, utilities:Utilities=utilities) -> None:
            '''
            Function to initialize the starting parameters of Fexplorer.
            '''
            self.utilities = utilities
            self.path = osabspath(utilities.settings["directory"])
            self.directory_box:TextBox
            self.search = True
            self.song = EditSong(utilities)
            
            self.arr_back = pygame.image.load("./Images/arr_back.png").convert_alpha()
            self.circle = pygame.image.load("./Images/circle.png").convert_alpha()
            
        def walk_in(self, folder:str) -> str:
            '''
            Function to change the path of the directory
            '''
            self.search=True
            t = osjoin(self.path,folder)
            try:
                oslistdir(t)
                self.path = t
            except:
                ...
        
        def get_foldersfiles(self) -> tuple[list[str],int]:
            '''
            Function to separate items of a directory in folders and documents
            '''
            if not osisdir(self.path):
                t = osabspath(self.utilities.settings["directory"])
                if osisdir(t):
                    self.path = t
                else:
                    self.path = self.utilities.settings["directory"] = osabspath(".")

            l = oslistdir(self.path)
            folders = [x for x in l if osisdir(osjoin(self.path,x))]
            
            return folders, len(l)-len(folders)

        def walk_out(self) -> str:
            '''
            Function that emulates .. of command prompt
            '''
            self.search=True
            self.path = osabspath(osjoin(self.path,".."))
            
        def replace_folder(self) -> None:
            '''
            Function to get the directory in the TextBox
            '''
            self.search=True
            if osexists(str(self.directory_box)):
                self.path = str(self.directory_box)

        def rename(self, how=False) -> None:
            '''
            Function to update to current directory and start the reading
            '''
            
            self.utilities.settings["directory"]=self.path
            self.renameSong(how)
            self.search=True

        def run(self, func,*args):
            self.utilities.settings["directory"]=self.path
            func(*args)

        def __call__ (self):
            """
            This function is called to get the select folder menu working
            """

            self.utilities.booleans.add()

            title = "Rinomina Canzoni"
            sub_t = "Scegli cartella"
            new_songs = "Rinomina nuove"
            old_songs = "Rinomina vecchie"
            options = ("Notte","Giorno")
            empty_textBox = "Inserisci il percorso di una cartella"
            counter = "La cartella {} (con {} sotto-cartelle)"
            with_files = "contiene {} file"
            without_files = "non contiene file"
            close = "Esci"
            
            close_b = NormalButton(func=self.utilities.screen.quit,utilities=utilities)
            opt_b = NormalButton(func=self.utilities.color_reverse,utilities=utilities)
            new_b = NormalButton(func=self.run, func_args=(self.song,True),utilities=utilities)
            old_b = NormalButton(func=self.run, func_args=(self.song,),utilities=utilities)
            goback = ImageButton(func=self.walk_out,utilities=utilities)
            replace = ImageButton(func=self.replace_folder,utilities=utilities)
            self.directory_box = TextBox(initial_text=self.path, empty_text=empty_textBox, max_char=500, bar_color="black",func=self.replace_folder)

            # a group of sprites
            g = pygame.sprite.Group(self.directory_box, old_b, new_b, close_b, opt_b, goback, replace)
            
            little_menu = LittleMenu()
            title_s = [None,None]
            subt_s = [None,None]
            current_s = [None,None]
            little_surface = [pygame.Surface((2,2),pygame.SRCALPHA),None]
            bigger_surface = pygame.Surface((2,2),pygame.SRCALPHA)
            v_bar = VerticalBar(utilities=utilities)
            g2 = pygame.sprite.Group()

            bar:VerticalBar = None
            folders_b:list[NormalButton] = []
            folders:list[str] = []
            n_files:int = None

            #starting the initial while loop to update text & graphics
            self.utilities.booleans[1] = True
            while self.utilities.booleans[1] or self.search:
                #getting screen sizes
                screen_rect = self.utilities.screen.get_rect()

                if self.utilities.booleans[1]:
                    self.utilities.booleans[1] = False

                    #dimensions to use
                    little_width = screen_rect.w/10*9
                    button_heigh = min(screen_rect.w//25,screen_rect.h//10)
                    little_font = pygame.font.Font(self.utilities.magic,button_heigh)
                    fontone = pygame.font.Font(self.utilities.magic,button_heigh*3)
                    font = pygame.font.SysFont(self.utilities.corbel,button_heigh*2)
                    
                    if screen_rect.w <= little_font.size(counter.format(with_files,1))[0]+screen_rect.w/5+font.size(sub_t)[0]:
                        button_heigh = int(button_heigh*0.7)
                        little_font = pygame.font.Font(self.utilities.magic,button_heigh)
                        fontone = pygame.font.Font(self.utilities.magic,button_heigh*3)
                        font = pygame.font.SysFont(self.utilities.corbel,button_heigh*2)
                    space = button_heigh//2
                    
                    smallfont = pygame.font.SysFont(self.utilities.corbel,button_heigh)
                    button_w = max(
                        smallfont.size(old_songs)[0],
                        smallfont.size(new_songs)[0],
                        smallfont.size(options[self.utilities.settings["night_mode"]])[0],
                        smallfont.size(close)[0]
                        )
                    
                    if (button_w+NormalButton.button_space)*4>screen_rect.w:
                        smallfont = pygame.font.SysFont(self.utilities.corbel,int(button_heigh*(screen_rect.w/4-8)/button_w))
                    
                    little_menu.refresh(smallfont,colors=utilities.colors)

                    title_s[0] = fontone.render(title, True, self.utilities.colors["black"])
                    title_s[1] = title_s[0].get_rect(x=button_heigh,y=space)
                    subt_s[0] = font.render(sub_t,False,self.utilities.colors["black"])
                    subt_s[1] = subt_s[0].get_rect(x=button_heigh,y=title_s[1].bottom+button_heigh/3)

                    #create a textbox of directory
                    l = little_width-smallfont.size("a")[1]*2-TextBox.button_space
                    self.directory_box.refresh(little_width-smallfont.size("a")[1]*2-TextBox.button_space, little_font)
                    f = self.directory_box.init_rect(centerx=screen_rect.w/2,y = subt_s[1].bottom+button_heigh/2)
            
                    #Inizializzazione lista
                    little_surface[0] = pygame.transform.scale(little_surface[0],(little_width,screen_rect.h-subt_s[1].bottom-button_heigh*6))
                    little_surface[1] = little_surface[0].get_rect(centerx=screen_rect.w/2,top=f.bottom+button_heigh/2)
                    
                    self.directory_box.refresh(l*little_width/(l+f.h*2), little_font)
                    f = self.directory_box.init_rect(left = little_surface[1].left,y = subt_s[1].bottom+button_heigh/2)
                    subt_s[1].left = f.left

                    old_s = smallfont.render(old_songs,True,self.utilities.colors["black"])
                    new_s = smallfont.render(new_songs,True,self.utilities.colors["black"])
                    opt_s = smallfont.render(options[self.utilities.settings["night_mode"]],True,self.utilities.colors["black"])
                    close_s = smallfont.render(close,True,self.utilities.colors["black"])
                    button_w = max(screen_rect.w/6, button_w)
                    button_x = (screen_rect.w-(button_w+NormalButton.button_space)*4)/4
                    button_y = little_surface[1].bottom+button_heigh*2
                    x=button_x*0.5

                    close_b.refresh(close_s,button_w,colors=utilities.colors)
                    x += close_b.init_rect(x=x,centery=button_y).width+button_x
                    close_b.text_rect()

                    opt_b.refresh(opt_s,button_w,colors=utilities.colors)
                    x += opt_b.init_rect(x=x,centery=button_y).width+button_x
                    opt_b.text_rect()

                    new_b.refresh(new_s,button_w,colors=utilities.colors)
                    x += new_b.init_rect(x=x,centery=button_y).width+button_x
                    new_b.text_rect()

                    old_b.refresh(old_s,button_w,colors=utilities.colors)
                    old_b.init_rect(x=x,centery=button_y)
                    old_b.text_rect()

                    surf_t = (f.h,f.h)
                    surf = pygame.Surface(surf_t)
                    
                    #Bottone torna indietro
                    surf.fill(self.utilities.colors['gray'])
                    surf.blit(pygame.transform.scale(self.arr_back,surf_t),(0,0))
                    goback.refresh(surf.copy(),colors=utilities.colors)
                    temp = goback.init_rect(x=f.x+f.w,y=f.y)
                    
                    #Bottone vai avanti
                    surf.fill(self.utilities.colors['gray'])
                    surf.blit(pygame.transform.scale(self.circle,surf_t),(0,0))
                    replace.refresh(surf.copy(),colors=utilities.colors)
                    replace.init_rect(x=temp.x+temp.w,y=temp.y)
                    del f,temp,x

                    #resizing of trasparent items
                    if folders_b:
                        vw = little_surface[1].w-NormalButton.button_space
                        y = 1
                        for i in range(len(folders_b)):
                            folders_b[i].refresh(smallfont.render(folders[i],True,self.utilities.colors["black"]),vw,little_width,colors=utilities.colors)
                            y += folders_b[i].init_rect(x=0,y=y).h+1
                            folders_b[i].text_rect('midleft')

                        bigger_surface = pygame.transform.scale(bigger_surface,(little_width,y))

                        if y>little_surface[1].h:
                            try:
                                v_bar.refresh((screen_rect.w-little_surface[1].w)//6,little_surface[1].h,y,little_surface[1].h,colors=utilities.colors)
                            except:
                                v_bar.refresh((screen_rect.w-little_surface[1].w)//8,little_surface[1].h,y,little_surface[1].h,colors=utilities.colors)
                            v_bar.init_rect(left=little_surface[1].right,y=little_surface[1].y)
                            bar = v_bar
                        else:
                            bar = None
                        
                        del vw,y
                    
                    if n_files:
                        current_s[0] = little_font.render(counter.format(with_files.format(n_files),len(folders_b)), True, self.utilities.colors["black"])
                    else:
                        current_s[0] = little_font.render(counter.format(without_files,len(folders_b)), True, self.utilities.colors["red"])

                    current_s[1] = current_s[0].get_rect(right=little_surface[1].right,bottom=subt_s[1].bottom)

                #it search for items
                if self.search:
                    #generating directories buttons
                    self.search=False 

                    try:
                        folders,n_files = self.get_foldersfiles()
                    except Exception as e:
                        self.utilities.showError(str(e))
                        self.walk_out()
                        self.utilities.booleans[1]=True
                        break
                
                    #positionate the textbox of directory
                    self.directory_box.replaceText(self.path)

                    folders_b.clear()
                    g2.empty()
                    if folders:
                        vw = little_surface[1].w-NormalButton.button_space
                        y = 1
                        for directory in folders:
                            folders_b.append(NormalButton(func=self.walk_in,func_args=(directory,),utilities=utilities))
                            folders_b[-1].refresh(smallfont.render(directory,True,self.utilities.colors["black"]),vw,little_width,colors=utilities.colors)
                            y += folders_b[-1].init_rect(x=0,y=y).h+1
                            folders_b[-1].text_rect('midleft')

                        bigger_surface = pygame.transform.scale(bigger_surface,(little_width,y))

                        if y>little_surface[1].h:
                            try:
                                v_bar.refresh((screen_rect.w-little_surface[1].w)//6,little_surface[1].h,y,little_surface[1].h,False,colors=utilities.colors)
                            except:
                                v_bar.refresh((screen_rect.w-little_surface[1].w)//8,little_surface[1].h,y,little_surface[1].h,False,colors=utilities.colors)
                            v_bar.init_rect(left=little_surface[1].right,y=little_surface[1].y)
                            bar = v_bar
                        else:
                            bar = None

                        del vw,y
                    
                    if n_files:
                        current_s[0] = little_font.render(counter.format(with_files.format(n_files),len(folders)), True, self.utilities.colors["black"])
                    else:
                        current_s[0] = little_font.render(counter.format(without_files,len(folders)), True, self.utilities.colors["red"])

                    current_s[1] = current_s[0].get_rect(right=little_surface[1].right,bottom=subt_s[1].bottom)

                    # a group of sprites
                    g2.add(folders_b)

                #cylce for the animation with some clocking thing going on
                self.utilities.booleans[0] = True
                while self.utilities.booleans[0]:
                    self.utilities.screen.tick()

                    # events for the action
                    pos = pygame.mouse.get_pos()
                    event_list = pygame.event.get()
                    self.utilities.booleans.update_start(event_list)

                    if not self.utilities.booleans[0]:
                        break

                    for event in event_list:
                        self.utilities.booleans.update_resizing(event)
                    self.utilities.booleans.update_booleans()

                    if not self.utilities.booleans[0] or self.utilities.booleans[1] or self.search:
                        break
                    
                    if self.directory_box:
                        self.directory_box.opened_little_menu()
                        little_menu.init(*pos, screen_rect, copy=self.directory_box.little_copy, cut=self.directory_box.little_cut, paste=self.directory_box.little_paste)
                        little_menu.update(event_list,pos)

                    elif little_menu:
                        little_menu.update(event_list,pos)

                    else:
                        if bar:
                            bar.update(event_list,pos)
                            if little_surface[1].collidepoint(pos):
                                g2.update(event_list,(pos[0]-little_surface[1].x,pos[1]-little_surface[1].y-float(bar)))
                            else:
                                g2.update(event_list,(pos[0]-little_surface[1].x,pos[1]-little_surface[1].y-float(bar)),False)
                        else:
                            g2.update(event_list,(pos[0]-little_surface[1].x,pos[1]-little_surface[1].y))
                        
                        g.update(event_list,pos)
                        
                    if little_menu:
                        self.utilities.screen.draw(little_menu)
                        pygame.display.update(little_menu.displayer())
                    else:
                        #colore + titolo
                        self.utilities.screen.fill(self.utilities.colors['background'])
                        # self.utilities.screen.blit(background) 
                        self.utilities.screen.blit(title_s,current_s,subt_s)

                        self.utilities.screen.draw(g)

                        if folders:
                            bigger_surface.fill(self.utilities.colors.transparent)
                            g2.draw(bigger_surface)
                            little_surface[0].fill(self.utilities.colors.transparent)
                            
                            if bar is not None:
                                little_surface[0].blit(bigger_surface,(0,float(bar)))
                                self.utilities.screen.draw(bar)
                            else:
                                little_surface[0].blit(bigger_surface,(0,0))
                            self.utilities.screen.blit(little_surface)
            
                        # that's t oupdate every sprite
                        pygame.display.update()

            #reset of self.search
            self.search = True
            self.utilities.booleans.end()

    utilities.init()
    Start(utilities)()