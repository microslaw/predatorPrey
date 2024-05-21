from entity import Entity
import globals
from brain import Brain


class Grass(Entity):
    grassCount = 0

    def __init__(self, parent_pos=(0, 0), size=20):
        super().__init__(
            name=f"Grass{Grass.grassCount}",
            hp=10,
            damage=5,
            speed=0,
            size=size,
            model=Brain(0),
            color=(0, 255, 0),
            position=parent_pos,
        )

        Grass.grassCount += 1

    def decide(self, entities):
        self.age += 1
        self.size += 0.1 + self.size / 200 - self.size**2 / 20000

    def is_alive(self):
        return self.size > globals.min_grass_size

    def take_damage(self, damage):
        self.size -= globals.grass_eating_speed
