from entity import Entity

class Wolf(Entity):
    wolfCount = 0
    def __init__(self, hp, damage, parentPos=(0,0)):
        super().__init__(hp, damage)
        self.name = f"Wolf{Wolf.wolfCount}"
        self.hp = 10
        self.damage = 5
        self.position = parentPos
        self.attackRange = 2
        self.size = 10
        self.color = (255, 0, 0)

