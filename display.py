import pygame
from entity import Entity
from wolf import Wolf
from sheep import Sheep
from grass import Grass
from utils import distance

class Game:
    @staticmethod
    def collide(entity1, entity2):
        if isinstance(entity1, Wolf) and isinstance(entity2, Sheep):
            Game.fight(entity1, entity2)
        if isinstance(entity1, Sheep) and isinstance(entity2, Wolf):
            Game.fight(entity2, entity1)

        if isinstance(entity1, Sheep) and isinstance(entity2, Grass):
            Game.eat(entity2, entity1)
        if isinstance(entity1, Grass) and isinstance(entity2, Sheep):
            Game.eat(entity1, entity2)

        if isinstance(entity1, Wolf) and isinstance(entity2, Wolf):
            return Game.reproduce(entity1, entity2, 100, 100)

        if isinstance(entity1, Sheep) and isinstance(entity2, Sheep):
            return Game.reproduce(entity1, entity2, 100, 100)

    @staticmethod
    def fight(wolf, sheep):
        sheep.take_damage(wolf.damage)
        wolf.take_damage(sheep.damage)

        if not sheep.is_alive():
            print(f"{wolf.name} killed {sheep.name}")
            return sheep

        if not wolf.is_alive():
            print(f"{sheep.name} killed {wolf.name}")
            return wolf

    @staticmethod
    def reproduce(entity1, entity2, minAge, minFood):
        if entity1.age > 100 and entity2.age > 100:
            if entity1.food > minFood and entity2.food > minFood:
                return entity1.__class__(entity1.position)

    @staticmethod
    def eat(grass, sheep):
        sheep.food += 1
        grass.take_damage(sheep.damage)

        if not grass.is_alive():
            print(f"{sheep.name} ate {grass.name}")
            return grass


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
            self.clock.tick(30)

        pygame.quit()

    def turn(self):
        for entity in self.entities:
            entity.decide(self.entities)
            pygame.draw.circle(self.screen, entity.color, entity.position, entity.size)
        self.check_collisions()
        self.clean_dead()

    def check_collisions(self):
        for entity in self.entities:
            for other in self.entities:
                if entity != other:
                    if distance(entity.position, other.position) < entity.size + other.size:
                        # print(f"{entity.name} collided with {other.name}")
                        result = Game.collide(entity, other)
                        if result is not None:
                            self.entities.append(result)

    def clean_dead(self):
        bodies = [entity for entity in self.entities if not entity.is_alive()]
        for body in bodies:
            self.entities.remove(body)
            if isinstance(body, Wolf):
                self.entities.append(Grass(body.position,50))


        self.entities = [entity for entity in self.entities if entity.is_alive()]
if __name__ == "__main__":
    game = Game()
    # game.entities.append(Wolf((100, 100)))
    # for i in range(2):
    #     game.entities.append(Sheep((250, 300)))
    game.entities.append(Grass((300, 300)))
    game.entities.append(Grass((500, 500)))
    game.start()
