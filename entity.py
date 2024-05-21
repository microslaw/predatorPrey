from utils import *
import random
import globals
import numpy as np
from brain import Brain
from timer import timer_predict, timer_state


class Entity:
    def __init__(
        self,
        name,
        hp,
        damage,
        speed,
        size,
        model,
        color=(255, 255, 255),
        position=(100, 100),
        food=0,
        movement_states=None,
        reward=0,
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
        self.model: Brain = model
        self.movement_states = movement_states
        self.reward = reward
        self.last_action = 0
        self.previous_state = 0
        self.current_state = 0

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

        timer_state.tic()
        self.get_state(**entitiesDict)
        timer_state.toc()

        timer_predict.tic()
        movementId = self.model.decide(state=self.get_state(**entitiesDict))  # type: ignore
        # movementId = self.model.decide(state=[0, 434, 403, 5.05, 20, 185, 4.154198871677794, 124, 174, 6], verbose = 0)
        timer_predict.toc()
        movement = self.movement_states[movementId]  # type: ignore
        self.last_action = movementId
        self.previous_state = self.get_state(**entitiesDict)
        # movement = (
        #     random.randint(-self.speed, self.speed),
        #     random.randint(-self.speed, self.speed),
        # )

        self.move_by(*movement)
        self.current_state = self.get_state(**entitiesDict)

    def penalize_getting_killed(self):
        self.reward += globals.penalty_death

    def reward_reproducing(self):
        self.reward += globals.reward_reproduce

    def reward_eating(self):
        self.reward += globals.reward_eating

    def reward_high_hp(self):
        if self.hp > globals.high_hp_treshold:
            self.reward += globals.reward_high_hp

    def set_rewards(self, value):
        self.reward = value

    def fit(self):
        if "Grass" in self.name:
            return
        action = self.last_action
        state = np.array([self.previous_state])
        next_state = np.array([self.current_state])
        self.reward_high_hp()
        reward = self.reward
        print(
            f"Name: {self.name}, current hp: {self.hp}, current food: {self.food}, self reward: {self.reward}, reward: {reward}"
        )
        self.model.fit(state, action, reward, next_state, False)  # type: ignore

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
        self.x
        self.y
        """
        toReturn = [
            *proximity_entities(self, wolfes, max_sight=100),
            *proximity_entities(self, sheeps, max_sight=100),
            *proximity_entities(self, grass, max_sight=100),
            self.hp,
            self.position[0],
            self.position[1],
        ]

        return toReturn

    def get_hp(self):
        return self.hp

    def get_food(self):
        return self.food

    def __str__(self):
        return f"{self.name} has {self.hp} HP and {self.damage} damage"
