import pygame
from grass import Grass
import globals
from timer import timer_predict, timer_outlook, timer_total
import cv2
import numpy as np


class Display:

    def __init__(self, scale=1):

        self.scale = scale
        self.clock = pygame.time.Clock()
        self.running = True
        self.entities = []
        self.setup()

    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (globals.window_width, globals.window_height)
        )
        pygame.display.set_caption("predatorPrey")
        cv2.namedWindow("Animation", cv2.WINDOW_NORMAL)

    def update(self, entities, game):
        if not self.running:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        self.screen.fill((0, 0, 0))
        for entity in entities:
            x, y = entity.position
            pygame.draw.circle(
                self.screen,
                entity.color,
                (x / self.scale, y / self.scale),
                max(1, entity.size / self.scale),
            )

            if entity.chosen:
                entity.position = (x + 1, y + 1)

                outlook = game.get_outlook(entity.position, 100, 20)
                print(outlook.shape)
                outlook = np.transpose(outlook, (1, 2, 0))
                outlook = outlook.astype(np.float32)
                outlook = cv2.cvtColor(outlook, cv2.COLOR_BGR2RGB)
                cv2.imshow("Animation", cv2.resize(outlook, (800, 800)))

        pygame.display.flip()
        self.clock.tick(globals.tickrate)

    def cleanup(self):
        pygame.quit()
        cv2.destroyAllWindows()
