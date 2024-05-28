from utils import *
import globals
import numpy as np
import neuralNetwork as nn
from timer import timer_predict, timer_fit


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
        sight=0,
        learning=True,
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
        self.previous_estimates = np.zeros(4)
        self.sight = sight
        self.action_space = generate_outputs(self.speed)
        self.learner = learning
        self.chosen = False

    def attack(self, target):
        if distance_kartesian(self.position, target.position) <= globals.attack_range:
            target.hp -= self.damage

    def move_to(self, x, y):
        if x > globals.game_width:
            x -= globals.game_width

        if y > globals.game_height:
            y -= globals.game_height

        if x < 0:
            x += globals.game_width

        if y < 0:
            y += globals.game_height

        self.position = (x, y)

    def move_by(self, dx, dy):
        # if self.chosen:
        #     print(f"Moving by {dx}, {dy}")
        x, y = self.position
        self.move_to(x + dx, y + dy)

    def perform_move(self, estimates):
        movement_id = np.argmax(estimates)

        if np.random.rand() < globals.modelParams_epsilon:
            x, y = self.action_space[np.random.randint(0, len(self.action_space))]
        else:
            x, y = self.action_space[movement_id]
        if self.chosen:
            # x, y = 0, 0
            # print(x,y)
            self.set_last_move((x, y))
        self.move_by(x, y)

    def set_last_move(self, move):
        self.last_move = move


    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage

    def act(self, outlook, entityDict):
        self.age += 1
        self.food -= globals.food_cost
        if self.food < 0:
            self.hp -= globals.starving_damage
        move = self.decide(outlook)
        self.perform_move(move)
        if self.learner:
            timer_fit.tic()
            self.fit(outlook, entityDict=entityDict)
            timer_fit.toc()

    def decide(self, outlook):
        timer_predict.tic()
        state = self.get_state(outlook)
        self.previous_state = state
        move = self.brain.predict(state)
        self.previous_estimates = move
        timer_predict.toc()

        return move

    def get_state(self, outlook):
        state = np.reshape(outlook, (-1,))
        state = np.concatenate((state, np.array([self.hp, self.food])))
        return state

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

    def fit(self, outlook=None, done=False, entityDict=None):
        if "Grass" in self.name:
            return

        self.reward_high_hp()
        # self.reward_close_proximity(entityDict)
        self.brain.qlearn_cyclic(
            reward=self.reward,
            previous_estimates=self.previous_estimates,
            previous_state=self.previous_state,
            current_state=self.get_state(outlook) if outlook is not None else None,
            done=done,
        )
        self.reward = 0

    def get_hp(self):
        return self.hp

    def get_food(self):
        return self.food

    def find_closest_wolf(self, entityDict):
        closest_dist = 1000000000
        if "Wolf" in self.name:
            return 0
        for category, objects in entityDict.items():
            for entity in objects:
                if "Wolf" in entity.name:
                    dist_to_wolf = distance_kartesian(self.position, entity.position)
                    if dist_to_wolf < closest_dist:
                        closest_dist = dist_to_wolf
        return closest_dist

    def find_closest_sheep(self, entityDict):
        closest_dist = 1000000000
        if "Sheep" in self.name:
            return 0
        for category, objects in entityDict.items():
            for entity in objects:
                if "Sheep" in entity.name:
                    dist_to_sheep = distance_kartesian(self.position, entity.position)
                    if dist_to_sheep < closest_dist:
                        closest_dist = dist_to_sheep
        return closest_dist

    def find_closest_grass(self, entityDict):
        closest_dist = 1000000000
        if "Wolf" in self.name:
            return 0
        for category, objects in entityDict.items():
            for entity in objects:
                if "Grass" in entity.name:
                    dist_to_grass = distance_kartesian(self.position, entity.position)
                    if dist_to_grass < closest_dist:
                        closest_dist = dist_to_grass
        return closest_dist

    def reward_close_proximity(self, entityDict):
        wolf_distance = self.find_closest_wolf(entityDict)
        sheep_distance = self.find_closest_sheep(entityDict)
        grass_distance = self.find_closest_grass(entityDict)
        if wolf_distance != 0:
            self.reward -= 10 / wolf_distance
        if sheep_distance != 0:
            self.reward += 10 / sheep_distance
        if grass_distance != 0:
            self.reward += 10 / grass_distance

    def __str__(self):
        return f"{self.name} has {self.hp} HP and {self.damage} damage"
