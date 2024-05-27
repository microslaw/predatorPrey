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
        self.position = (
            min(max(0, x), globals.game_width),
            min(max(0, y), globals.game_height),
        )

    def move_by(self, dx, dy):
        x, y = self.position
        self.move_to(x + dx, y + dy)

    def perform_move(self, estimates):
        movement_id = np.argmax(estimates)

        if np.random.rand() < globals.modelParams_epsilon:
            x, y = self.action_space[np.random.randint(0, len(self.action_space))]
        else:
            x, y = self.action_space[movement_id]
        self.move_by(x, y)

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage

    def act(self, outlook):
        move = self.decide(outlook)
        self.perform_move(move)
        if self.learner:
            timer_fit.tic()
            self.fit(outlook)
            timer_fit.toc()

    def decide(self, outlook):
        self.age += 1
        self.food -= globals.food_cost
        if self.food < 0:
            self.hp -= globals.starving_damage



        timer_predict.tic()
        state = self.get_state(outlook)
        self.previous_state = state
        move = self.brain.predict(state)
        self.previous_estimates = move
        timer_predict.toc()

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

    def fit(self, outlook=None, done=False):
        if "Grass" in self.name:
            return

        self.reward_high_hp()
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

    def __str__(self):
        return f"{self.name} has {self.hp} HP and {self.damage} damage"
