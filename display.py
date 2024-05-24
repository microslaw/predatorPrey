import pygame
from game import Game
from grass import Grass
import globals
from timer import timer_predict, timer_state, timer_total
import cv2
import numpy as np


class Display:

    def __init__(self, scale):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (globals.window_width, globals.window_height)
        )
        self.scale = scale
        self.clock = pygame.time.Clock()
        self.running = True
        self.entities = []
        self.game = Game(randomStart=True)

    def start(self):
        pygame.display.set_caption("predatorPrey")
        cv2.namedWindow('Animation', cv2.WINDOW_NORMAL)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            self.screen.fill((0, 0, 0))
            self.game.turn()
            for entity in self.game.entities:
                x, y = entity.position
                pygame.draw.circle(
                    self.screen,
                    entity.color,
                    (x / self.scale, y / self.scale),
                    max(1, entity.size / self.scale),
                )


                if entity.chosen:
                    entity.position = (x + 1, y + 1)

                    outlook = self.game.get_outlook(entity.position, 100, 20)
                    print(outlook.shape)
                    outlook = np.transpose(outlook, (1, 2, 0))
                    outlook = outlook.astype(np.float32)
                    outlook = cv2.cvtColor(outlook, cv2.COLOR_BGR2RGB)
                    cv2.imshow('Animation', cv2.resize(outlook, (800, 800)))

            if (
                sum([isinstance(entity, Grass) for entity in self.game.entities])
                >= len(self.game.entities) - 1
                or self.game.turnNo > 1000
                or self.game.get_sheeps_count() == 0
                or self.game.get_wolfes_count() == 0
            ):
                globals.game_no += 1
                print(f"Game {globals.game_no}")
                self.game = Game(randomStart=True)

            pygame.display.flip()
            self.clock.tick(globals.tickrate)

        pygame.quit()
        cv2.destroyAllWindows()

