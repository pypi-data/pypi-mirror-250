import pygame
import sys

class Game:
    def __init__(self, height: int = 1, width: int = 0, engine=pygame):  # supports only PyGame for now
        """
        Defines the game
        :param height: Optional, the height of the game window, starts at 1 to stop (0, 0) with width, but also allowing you to run the game
        :param width: Optional, the width of the game window, starts at 0
        :param engine: Optional, the game engine, only change if you want custom settings really, set to a module. If there is another game module for python, I will consider adding it, but for now it's just custom properties
        """
        self.width = width
        self.height = height
        self.engine = engine

        if self.engine == pygame:
            self.c = self.engine.time.Clock()
            self.d = self.engine.display
            self.s = self.d.set_mode((self.width, self.height))
        self.init = False

    def initEngine(self):
        """
        Initialises the current engine
        """
        if self.engine == pygame:
            self.engine.init()
            self.init = True

    def keyPressed(self, key: str):
        """
        Tests if a key is pressed
        :param key: The name of the key
        :return: If it is pressed
        """
        if self.engine == pygame and self.init:
            k = self.engine.key.get_pressed()
            k = k[self.engine.key.key_code(key.lower())]
            return k

    def runAtFPS(self, fps: int):
        """
        Ticks the game at a certain rate of frames per second
        :param fps: The frames per second to refresh on
        """
        if self.engine == pygame and self.init:
            self.d.flip()
            self.c.tick(fps)

    def getEvents(self):
        """
        Get the events of the game
        :return: The events since last tick
        """
        if self.engine == pygame and self.init:
            e = []
            for event in pygame.event.get():
                e.append(event)
            return e

    def run(self, gameFunction, fps: int, bgcol: tuple, **kwargs): #kw... kwaaaaargs... uwu(what the fuck is wrong with me)
        """
        Runs the game with specified code. Once called, loops until quit.
        :param gameFunction: The function to be run once per tick, renders/updates the game
        :param fps: The frames per second max to run the game at
        """
        if self.engine == pygame and self.init:
            running = True
            while running:
                e = self.getEvents()
                for event in e:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                
                self.s.fill(bgcol)

                gameFunction(**kwargs)

                self.runAtFPS(fps)