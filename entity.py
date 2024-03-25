from utils import *


class Entity:
    color = (255, 255, 255)

    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.position = (100, 100)
        self.attackRange = 1
        self.size = 10
        self.age = 0

    def attack(self, target):
        if distance(self.position, target.position) <= self.attackRange:
            target.hp -= self.damage

    def move(self, x, y):
        self.position = (x, y)

    def moveBy(self, dx, dy):
        x, y = self.position
        self.position = (x + dx, y + dy)

    def is_alive(self):
        return self.hp > 0

    def decide(self, entities):
        pass

    def speed(self):
        return

    def __str__(self):
        return f"{self.name} has {self.hp} HP and {self.damage} damage"
