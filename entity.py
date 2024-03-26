from utils import *
import random


class Entity:
    def __init__(
        self, name, hp, damage, speed, size, color=(255, 255, 255), position=(100, 100), food=0
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

    def attack(self, target):
        if distance(self.position, target.position) <= 1:
            target.hp -= self.damage

    def move(self, x, y):
        self.position = (x, y)

    def moveBy(self, dx, dy):
        x, y = self.position
        self.position = (x + dx, y + dy)

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage

    def decide(self, entities):
        self.age += 1
        # movement = self.model.predict(entities)
        movement = (
            random.randint(-self.speed, self.speed),
            random.randint(-self.speed, self.speed),
        )

        self.moveBy(*movement)

    def __str__(self):
        return f"{self.name} has {self.hp} HP and {self.damage} damage"
