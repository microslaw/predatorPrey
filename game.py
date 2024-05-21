from wolf import Wolf
from sheep import Sheep
from grass import Grass
from utils import distance
import globals
import random
from timer import timer_fit


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
            return Game.reproduce(
                entity1, entity2, globals.min_wolf_age, globals.min_wolf_food
            )

        if isinstance(entity1, Sheep) and isinstance(entity2, Sheep):
            return Game.reproduce(
                entity1, entity2, globals.min_sheep_age, globals.min_sheep_food
            )

    @staticmethod
    def fight(wolf, sheep):
        sheep.take_damage(wolf.damage)
        wolf.take_damage(sheep.damage)

        if not sheep.is_alive():
            print(f"{wolf.name} killed {sheep.name}")
            sheep.penalize_getting_killed()
            wolf.reward_eating()
            return sheep

        if not wolf.is_alive():
            # print(f"{sheep.name} killed {wolf.name}")
            return wolf

    @staticmethod
    def reproduce(entity1, entity2, minAge, minFood):
        if entity1.age > minAge and entity2.age > minAge:
            if entity1.food > minFood and entity2.food > minFood:
                entity1.reward_reproducing()
                entity2.reward_reproducing()
                return entity1.__class__(entity1.position)

    @staticmethod
    def eat(grass, sheep):
        sheep.food += globals.grass_eating_efficiency
        grass.take_damage(sheep.damage)
        sheep.reward_eating()
        if not grass.is_alive():
            # print(f"{sheep.name} ate {grass.name}")
            return grass

    def __init__(self, randomStart, sheepCount=10, wolfCount=5, grassCount=3):
        self.entities = []
        self.turnNo = 0

        if randomStart:
            for _ in range(sheepCount):
                self.entities.append(
                    Sheep(
                        (
                            random.randint(0, globals.game_width),
                            random.randint(0, globals.game_height),
                        )
                    )
                )
            for _ in range(wolfCount):
                self.entities.append(
                    Wolf(
                        (
                            random.randint(0, globals.game_width),
                            random.randint(0, globals.game_height),
                        )
                    )
                )
            for _ in range(grassCount):
                self.entities.append(
                    Grass(
                        (
                            random.randint(0, globals.game_width),
                            random.randint(0, globals.game_height),
                        )
                    )
                )

    def turn(self):
        self.turnNo += 1
        for entity in self.entities:
            entityDict = {
                "wolfes": [e for e in self.entities if isinstance(e, Wolf)],
                "sheeps": [e for e in self.entities if isinstance(e, Sheep)],
                "grass": [e for e in self.entities if isinstance(e, Grass)],
            }
            print(f"Name: {entity.name}, current hp: {entity.hp}, current food: {entity.food}")
            entity.decide(entityDict)
        self.check_collisions()

        for entity in self.entities:
            timer_fit.tic()
            entity.fit()
            entity.set_rewards(0)
            timer_fit.toc()

        self.clean_dead()

    def get_wolfes_count(self):
        return sum([isinstance(entity, Wolf) for entity in self.entities])

    def get_sheeps_count(self):
        return sum([isinstance(entity, Sheep) for entity in self.entities])

    def check_collisions(self):
        for i, entity in enumerate(self.entities):
            for j, other in enumerate(self.entities):
                if i<j:
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
