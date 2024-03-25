from entity import Entity

class Sheep(Entity):
    sheepCount = 0
    def __init__(self, hp, damage, parentPos=(0,0)):
        super().__init__(hp, damage)
        self.name = f"Sheep{Sheep.sheepCount}"
        self.hp = 6
        self.damage = 2
        self.position = parentPos
        self.attackRange = 1
        self.size = 5
        self.color = (255, 0, 0)

