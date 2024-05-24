from utils import *
import random
import globals
import numpy as np
import neuralNetwork as nn
from timer import timer_predict, timer_state


class Entity:
    def __init__(
        self,
        name,
        hp,
        damage,
        speed,
        size,
        brain,
        color=(255, 255, 255),
        position=(100, 100),
        food=0,
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
        self.brain: nn.NeuralNetwork = brain
        self.reward = reward
        self.last_action = 0
        self.previous_state = 0
        self.current_state = 0

        self.chosen = False

    def attack(self, target):
        if distance_kartesian(self.position, target.position) <= globals.attack_range:
            target.hp -= self.damage

    def move_to(self, x, y):
        self.position = (x, y)

    def move_by(self, dx, dy):
        x, y = self.position
        self.position = (x + dx, y + dy)

    def perform_move(self, movement):
        x, y, distance = movement
        vector = x**2 + y**2
        norm_x = x / vector
        norm_y = y / vector

        norm_distance = min(abs(distance), self.speed)

        self.move_by(norm_x * norm_distance, norm_y * norm_distance)

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage

    def decide(self, outlook):
        self.age += 1
        self.food -= globals.food_cost
        if self.food < 0:
            self.hp -= globals.starving_damage

        timer_state.tic()
        state = np.reshape(outlook, (1, -1))
        #maybe add random to that
        state = np.concatenate((state, np.array([[self.hp, self.food]])), axis=1)
        move = self.brain.predict(state)
        timer_state.toc()

        # movementId = self.brain.predict(state=self.get_state(**entitiesDict))
        # # movementId = self.model.decide(state=[0, 434, 403, 5.05, 20, 185, 4.154198871677794, 124, 174, 6], verbose = 0)
        # movement = self.movement_states[movementId]  # type: ignore
        # self.last_action = movementId
        # self.previous_state = self.get_state(**entitiesDict)
        # movement = (
        #     random.randint(-self.speed, self.speed),
        #     random.randint(-self.speed, self.speed),
        # )
        # self.current_state = self.get_state(**entitiesDict)

        self.perform_move(move)

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
        return
        action = self.last_action
        state = np.array([self.previous_state])
        next_state = np.array([self.current_state])
        self.reward_high_hp()
        reward = self.reward
        # print(
        #     f"Name: {self.name}, current hp: {self.hp}, current food: {self.food}, self reward: {self.reward}, reward: {reward}"
        # )
        self.brain.fit(state, action, reward, next_state, False)  # type: ignore


    def get_hp(self):
        return self.hp

    def get_food(self):
        return self.food

    def __str__(self):
        return f"{self.name} has {self.hp} HP and {self.damage} damage"
