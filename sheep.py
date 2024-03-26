from entity import Entity


class Sheep(Entity):
    sheepCount = 0

    def __init__(self, parentPos=(0, 0)):
        super().__init__(
            name=f"Sheep{Sheep.sheepCount}",
            hp=6,
            damage=2,
            speed=5,
            size=5,
            color=(0, 0, 255),
            position=parentPos,
            food=50,
        )
        Sheep.sheepCount += 1
