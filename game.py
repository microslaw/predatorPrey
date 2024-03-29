from wolf import Wolf
from sheep import Sheep
from grass import Grass
from utils import distance
import globals
import random


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
            return Game.reproduce(entity1, entity2, globals.min_wolf_age, globals.min_wolf_food)

        if isinstance(entity1, Sheep) and isinstance(entity2, Sheep):
            return Game.reproduce(entity1, entity2, globals.min_sheep_age, globals.min_sheep_food)

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
        if entity1.age > minAge and entity2.age > minAge:
            if entity1.food > minFood and entity2.food > minFood:
                return entity1.__class__(entity1.position)

    @staticmethod
    def eat(grass, sheep):
        sheep.food += globals.grass_eating_efficiency
        grass.take_damage(sheep.damage)

        if not grass.is_alive():
            print(f"{sheep.name} ate {grass.name}")
            return grass


    def __init__(self, randomStart, sheepCount = 5, wolfCount = 2, grassCount = 5):
        self.entities = []
        self.turnNo = 0

        if randomStart:
            for i in range(sheepCount):
                self.entities.append(Sheep((random.randint(0, globals.game_width), random.randint(0, globals.game_height))))
            for i in range(wolfCount):
                self.entities.append(Wolf((random.randint(0, globals.game_width), random.randint(0, globals.game_height))))
            for i in range(grassCount):
                self.entities.append(Grass((random.randint(0, globals.game_width), random.randint(0, globals.game_height))))

    def turn(self):
        self.turnNo += 1
        for entity in self.entities:
            entity.decide(self.entities)
        self.check_collisions()

        # for entity in self.entities:
        #     entity.reward()

        self.clean_dead()



    def check_collisions(self):
        for entity in self.entities:
            for other in self.entities:
                if entity != other:
                    if (
                        distance(entity.position, other.position)
                        < entity.size + other.size
                    ):
                        # print(f"{entity.name} collided with {other.name}")
                        result = Game.collide(entity, other)
                        if result is not None:
                            self.entities.append(result)

    def clean_dead(self):
        bodies = [entity for entity in self.entities if not entity.is_alive()]
        for body in bodies:
            self.entities.remove(body)
            if isinstance(body, Wolf):
                self.entities.append(Grass(body.position, globals.wolf_grass_size))
            if isinstance(body, Sheep):
                self.entities.append(Grass(body.position, globals.sheep_grass_size))

        self.entities = [entity for entity in self.entities if entity.is_alive()]
