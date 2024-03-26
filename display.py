import pygame
from game import Game
from wolf import Wolf
from sheep import Sheep
from grass import Grass
import globals

class Display:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((globals.window_width, globals.window_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.entities = []
        self.game = Game()

    def start(self):
        pygame.display.set_caption("predatorPrey")

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))
            self.game.turn()
            for entity in self.game.entities:
                pygame.draw.circle(self.screen, entity.color, entity.position, entity.size)

            pygame.display.flip()
            self.clock.tick(globals.tickrate)

        pygame.quit()

if __name__ == "__main__":
    display = Display()
    display.game.entities.append(Wolf((100, 100)))
    for i in range(2):
        display.game.entities.append(Sheep((250, 300)))
    display.game.entities.append(Grass((300, 300)))
    display.game.entities.append(Grass((500, 500)))
    display.start()
