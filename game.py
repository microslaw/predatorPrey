from wolf import Wolf
from sheep import Sheep
from grass import Grass
from utils import distance_kartesian, distance_manhattan
import cv2
import globals
import random
from timer import (
    timer_fit,
    timer_predict,
    timer_outlook,
    timer_collisions,
    timer_outlook_global,
)
import numpy as np
from entity import Entity


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

    def __init__(
        self,
        display=None,
        height=globals.game_height,
        width=globals.game_width,
        learning=True,
    ):
        self.entities = []
        self.turnNo = 0
        self.height = height
        self.width = width
        self.global_outlook = np.zeros((height, width, 3))
        self.outlook_padding = 0
        if display is not None:
            self.display = display
        else:
            self.display = None
        self.learning = learning

    def setup(
        self,
        randomStart=True,
        sheepCount=10,
        wolfCount=5,
        grassCount=3,
    ):
        self.entities = []
        self.turnNo = 0


        whiteWolf = Wolf(
            (
                self.width // 2,
                self.height // 2,
            ),
            learning=self.learning,

        )
        whiteWolf.chosen = True
        whiteWolf.color = (255, 255, 255)
        # whiteWolf.food = 2 * globals.min_wolf_food
        self.entities.append(whiteWolf)

        if randomStart:
            for _ in range(sheepCount):
                self.entities.append(
                    Sheep(
                        (
                            random.randint(self.width * 3 // 8, self.width * 5 // 8),
                            random.randint(self.height * 3 // 8, self.height * 5 // 8),
                        ),
                        learning=self.learning,
                    )
                )
            for _ in range(wolfCount):
                self.entities.append(
                    Wolf(
                        (
                            random.randint(self.width * 3 // 8, self.width * 5 // 8),
                            random.randint(self.height * 3 // 8, self.height * 5 // 8),
                        ),
                        learning=self.learning,
                    )
                )
            for _ in range(grassCount):
                self.entities.append(
                    Grass(
                        (
                            random.randint(self.width * 3 // 8, self.width * 5 // 8),
                            random.randint(self.height * 3 // 8, self.height * 5 // 8),
                        ),
                    )
                )

    def turn(self):

        for entity in self.entities:
            # print(f"Name: {entity.name}, current hp: {entity.hp}, current food: {entity.food}")

            if type(entity) is Grass:
                continue

            timer_outlook.tic()
            # self.global_outlook = self.get_global_outlook()
            outlook = self.get_outlook(entity)
            entity.act(outlook, self.get_entity_dict())
            timer_outlook.toc()


        timer_collisions.tic()
        self.check_collisions()
        timer_collisions.toc()

        self.clean_dead()
        if self.learning:
            globals.modelParams_epsilon = max(
                globals.modelParams_epsilon * globals.modelParams_epsilon_decay,
                globals.modelParams_epsilon_min,
            )

    def play(self, turns_max=200):
        # self.display.setup()
        while turns_max != self.turnNo:
            self.turn()
            self.turnNo += 1

            if self.display is not None:
                self.display.update(self.entities, self)
                if self.display.running == False:
                    break

            if self.get_sheeps_count() == 0 or self.get_wolfes_count() == 0:
                break
        globals.game_no += 1
        # print(f"game {globals.game_no} finished")

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


    def get_entity_dict(self):
        entityDict = {
            "wolfes": [e for e in self.entities if isinstance(e, Wolf)],
            "sheeps": [e for e in self.entities if isinstance(e, Sheep)],
            "grass": [e for e in self.entities if isinstance(e, Grass)],
        }
        return entityDict

    def clean_dead(self):
        bodies = [entity for entity in self.entities if not entity.is_alive()]

        for body in bodies:
            if self.learning and type(body) is not Grass:
                timer_fit.tic()
                entityDict = self.get_entity_dict()
                body.fit(done=True, entityDict=entityDict)
                timer_fit.toc()

            self.entities.remove(body)
            if isinstance(body, Wolf):
                self.entities.append(Grass(body.position, globals.wolf_grass_size))
            if isinstance(body, Sheep):
                self.entities.append(Grass(body.position, globals.sheep_grass_size))

        self.entities = [entity for entity in self.entities if entity.is_alive()]

    # def get_outlook_from_global(self, position, sight):
    #     # Initialize a numpy array of zeros
    #     x, y = position

    #     x_start = int(x - sight + self.outlook_padding)
    #     x_end = int(x + sight + self.outlook_padding + 1)

    #     y_start = int(y - sight + self.outlook_padding)
    #     y_end = int(y + sight + 1 + self.outlook_padding)

    #     a = self.global_outlook[
    #         x_start:x_end,
    #         y_start:y_end,
    #     ]

    #     if a.shape[0] != 2 * sight + 1 or a.shape[1] != 2 * sight + 1:
    #         print("invalid shape")
    #         # a = np.zeros((2 * sight + 1, 2 * sight + 1, 3))

    #     a = np.transpose(a, (1, 0, 2))
    #     return a

    def get_outlook(self, looker: Entity):
        # Initialize a numpy array of zeros
        # looker.sight = 1
        outlook = np.zeros((looker.sight * 2 + 1, looker.sight * 2 + 1, 3))

        # Iterate over the array of tuples
        looker_x, looker_y = looker.position

        for other_entity in self.entities:
            if other_entity.is_alive() == False:
                continue
            # if other_entity == entity:
            #     continue
            distance = distance_manhattan(looker.position, other_entity.position)
            # if distance > looker.sight - other_entity.size - 2:
            #     continue

            # if distance == looker.sight - other_entity.size - 2:
            #     print("A")

            x, y = other_entity.position
            x_vector = looker_x - x
            y_vector = looker_y - y
            size = int(other_entity.size)
            sight = looker.sight

            # x_seen = x_vector + looker.sight
            # y_seen = y_vector + looker.sight

            X_grid, Y_grid = np.ogrid[
                x_vector - sight : x_vector + sight + 1,
                y_vector - sight : y_vector + sight + 1,
            ]

            # Calculate the coordinates of the circle
            # Y, X = np.ogrid[:sight, :sight]

            dist_from_center = (X_grid) ** 2 + (Y_grid) ** 2
            mask = dist_from_center <= size**2

            outlook[mask] += other_entity.color

            x = 1

            # cv2.imwrite("outlook.png", outlook)
        outlook = np.where(outlook > 0, 1, 0).astype(np.float64)
        # outlook = np.flip(outlook, axis=1)
        outlook = np.transpose(outlook, (1, 0, 2))
        return outlook

    def get_global_outlook(self, scale=1):
        # Initialize a numpy array of zeros
        self.outlook_padding = (
            int(
                max(
                    globals.entityParams_sheep_sight,
                    globals.entityParams_wolf_sight,
                    max([entity.size for entity in self.entities]),
                )
            )
            + 1
        )
        # max(globals.entityParams_wolf_sight, globals.entityParams_sheep_sight)

        h = globals.game_height
        w = globals.game_width
        outlook = np.zeros(
            (w + 2 * self.outlook_padding, h + 2 * self.outlook_padding, 3)
        )

        for entity in self.entities:
            size = int(entity.size)
            # Calculate the coordinates of the circle
            x, y = entity.position

            padded_x = int(x + self.outlook_padding)
            padded_y = int(y + self.outlook_padding)
            X, Y = np.ogrid[
                padded_x
                - size : min(padded_x + size, w + 2 * self.outlook_padding - 1),
                padded_y
                - size : min(padded_y + size, h + 2 * self.outlook_padding - 1),
            ]

            dist_from_center = (X - padded_x + 0.5) ** 2 + (Y - padded_y + 0.5) ** 2
            mask = dist_from_center <= size**2

            # Use the mask to set the corresponding values in the numpy array to 1
            # mask = cv2.resize(mask.astype(np.uint8), (size, size))
            colored_mask = np.zeros((2 * size, 2 * size, 3))
            colored_mask[mask] = entity.color

            outlook[
                padded_x - size : padded_x + size,
                padded_y - size : padded_y + size,
            ] += colored_mask

            outlook = np.where(outlook > 0, 1, 0).astype(np.float64)

        return outlook
