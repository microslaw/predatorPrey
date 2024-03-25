import pygame
import entity

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.entities = []

    def start(self):
        pygame.display.set_caption("predatorPrey")

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))

            self.turn()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def turn(self):
        for entity in self.entities:
            entity.moveBy(1, 1)
            pygame.draw.circle(self.screen, entity.color, entity.position, entity.size)
            print(entity.position)


if __name__ == "__main__":
    game = Game()
    game.entities.append(entity.Entity("Wolf", 10, 3))
    game.start()
