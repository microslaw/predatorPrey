from utils import *
import random
import globals
from model import Model
from timer import timer_predict, timer_state


class Entity:
    def __init__(
        self,
        name,
        hp,
        damage,
        speed,
        size,
        color=(255, 255, 255),
        position=(100, 100),
        food=0,
        model=None,
        movement_states=None,
    ):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.position = position
        self.size = size
        self.age = 0
        self.speed = speed
        self.color = color
        self.food = food
        self.model = model
        self.movement_states = movement_states

    def attack(self, target):
        if distance(self.position, target.position) <= globals.attack_range:
            target.hp -= self.damage

    def move(self, x, y):
        self.position = (x, y)

    def move_by(self, dx, dy):
        x, y = self.position
        self.position = (x + dx, y + dy)

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage

    def decide(self, entitiesDict):
        self.age += 1
        self.food -= globals.food_cost
        if self.food < 0:
            self.hp -= globals.starving_damage

        # movement = self.model.decide(self, state=self.get_state(**entitiesDict))

        timer_state.tic()
        self.get_state(**entitiesDict)
        timer_state.toc()


        timer_predict.tic()
        movementId = self.model.decide(state=[0, 434, 403, 5.05, 20, 185, 4.154198871677794, 124, 174, 6], verbose = 0)
        timer_predict.toc()
        movement = self.movement_states[movementId]

        # movement = (
        #     random.randint(-self.speed, self.speed),
        #     random.randint(-self.speed, self.speed),
        # )

        self.move_by(*movement)

    def get_state(self, wolfes, sheeps, grass):
        """
        wolf nearest x
        wolf nearest y
        sheep nearest x
        sheep nearest y
        grass nearest x
        grass nearest y
        wolf proximity
        sheep proximity
        grass proximity
        self.hp
        """
        toReturn =  [
            *proximity_entities(self, wolfes, max_sight=100),
            *proximity_entities(self, sheeps, max_sight=100),
            *proximity_entities(self, grass, max_sight=100),
            self.hp,
        ]

        return toReturn

    def __str__(self):
        return f"{self.name} has {self.hp} HP and {self.damage} damage"
