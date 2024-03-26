from entity import Entity


class Wolf(Entity):
    wolfCount = 0

    def __init__(self, parentPos=(0, 0)):
        super().__init__(
            name=f"Wolf{Wolf.wolfCount}",
            hp=10,
            damage=5,
            speed=5,
            size=10,
            color=(255, 0, 0),
            position=parentPos,
            food=100,
        )
        Wolf.wolfCount += 1
