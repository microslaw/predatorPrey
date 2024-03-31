import pygame
from game import Game
from grass import Grass
import globals
from timer import timer_predict, timer_state, timer_total

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

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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

            if (
                sum([isinstance(entity, Grass) for entity in self.game.entities])
                >= len(self.game.entities) - 1
                or self.game.turnNo > 1000
            ):
                self.game = Game(randomStart=True)

            pygame.display.flip()
            self.clock.tick(globals.tickrate)

        pygame.quit()




if __name__ == "__main__":

    timer_total.tic()
    display = Display(scale=1)
    display.start()
    timer_total.toc()


    print("Predict:")
    timer_predict.stats()

    print("State:")
    timer_state.stats()

    print("Total:")
    timer_total.stats()
