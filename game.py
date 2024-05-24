from wolf import Wolf
from sheep import Sheep
from grass import Grass
from utils import distance_kartesian, distance_manhattan
import globals
import random
from timer import timer_fit, timer_predict
import numpy as np
import cv2
from neuralNetwork import NeuralNetwork as nn


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
            # print(f"{wolf.name} killed {sheep.name}")
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
        self.neural = nn([5_000, 20, 20, 3], [nn.leakyRelu, nn.leakyRelu, nn.leakyRelu])

        pinkSheep = Sheep(
            (
                globals.game_width / 2,
                globals.game_height / 2,
            )
        )
        pinkSheep.color = (255, 0, 255)
        pinkSheep.chosen = True

        self.entities.append(pinkSheep)

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
            # print(f"Name: {entity.name}, current hp: {entity.hp}, current food: {entity.food}")

            timer_predict.tic()
            self.get_outlook(entity.position, 50, 20)
            self.neural.loadInput(np.random.uniform(0, 1, 5000))
            self.neural.forward()
            x = self.neural.readOutput()
            timer_predict.toc()

            entity.decide(entityDict)
        self.check_collisions()

        for entity in self.entities:

            timer_fit.tic()
            self.neural.loadInput(np.random.uniform(0, 1, 5000))
            self.neural.forward()
            self.neural.backpropagation(np.random.randint(3), 0.0001, nn.mseLoss)
            timer_fit.toc()

            entity.fit()
            entity.set_rewards(0)

        self.clean_dead()

    def get_wolfes_count(self):
        return sum([isinstance(entity, Wolf) for entity in self.entities])

    def get_sheeps_count(self):
        return sum([isinstance(entity, Sheep) for entity in self.entities])

    def check_collisions(self):
        for i, entity in enumerate(self.entities):
            for j, other in enumerate(self.entities):
                if i < j:
                    if (
                        distance_kartesian(entity.position, other.position)
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

    # sight is the number of bins. Scale is the size of the bin
    def get_outlook2(self, position, sight, scale=1):
        nearby_entities = []
        for entity in self.entities:
            if distance_manhattan(position, entity.position) < sight * scale:
                nearby_entities.append(entity)

        outlook = np.zeros((sight, sight, 3), dtype=np.uint8)
        for entity in nearby_entities:
            x, y = entity.position
            x -= position[0]
            y -= position[1]

            x = int((x + sight * scale * 0.5) // scale)
            y = int((y + sight * scale * 0.5) // scale)

            Y, X = np.ogrid[: entity.size, : entity.size]
            dist_from_center = distance_kartesian(
                (X, Y), (entity.size // 2, entity.size // 2)
            )
            mask = dist_from_center <= entity.size // 2

            x = min(max(0, x), sight - 1)
            y = min(max(0, y), sight - 1)

            # outlook[y, x] = entity.color if mask else (0, 0, 0)
            outlook[y, x] = entity.color

        return outlook.T

    def get_outlook(self, position, sight, scale=1):
        # Initialize a numpy array of zeros
        outlook = np.zeros((sight, sight, 3))

        # Iterate over the array of tuples
        for entity in self.entities:
            # Calculate the coordinates of the circle
            Y, X = np.ogrid[:sight, :sight]
            x, y = entity.position
            x -= position[0]
            y -= position[1]

            dist_from_center = np.sqrt(
                (X - sight / 2 - x) ** 2 + (Y - sight / 2 - y) ** 2
            )

            # Create a mask for the circle
            mask = dist_from_center <= entity.size

            # Use the mask to set the corresponding values in the numpy array to 1
            # mask = cv2.resize(mask.astype(np.uint8), (sight, sight))
            outlook[mask] += entity.color

        return outlook.T
