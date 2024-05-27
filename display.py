import pygame
import globals
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
                print(entity.previous_estimates)

                outlook = game.get_outlook(entity.position, entity.sight)
                outlook = outlook.astype(np.float32)
                outlook = cv2.cvtColor(outlook, cv2.COLOR_BGR2RGB)
                cv2.imshow(
                    "Animation",
                    cv2.resize(outlook, (outlook.shape[0], outlook.shape[1])),
                )

        pygame.display.flip()
        self.clock.tick(globals.tickrate)

    def cleanup(self):
        pygame.quit()
        cv2.destroyAllWindows()
