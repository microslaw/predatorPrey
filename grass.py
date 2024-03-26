from entity import Entity


class Grass(Entity):
    grassCount = 0

    def __init__(self, parentPos=(0, 0), size=20):
        super().__init__(
            name=f"Grass{Grass.grassCount}",
            hp=10,
            damage=5,
            speed=0,
            size=size,
            color=(0, 255, 0),
            position=parentPos,
        )

        Grass.grassCount += 1

    def decide(self, entities):
        self.age += 1
        self.size += 0.1
        pass

    def is_alive(self):
        return self.size > 3

    def take_damage(self, damage):
        self.size -= damage/10
