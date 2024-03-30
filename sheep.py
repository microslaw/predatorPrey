from entity import Entity
from model import Model
from utils import generateStates
import globals


class Sheep(Entity):
    sheepCount = 0
    movementStates = generateStates(3)
    model = Model(
        input_shape=globals.modelParams.input_shape,
        output_shape=len(movementStates),
        learning_rate=0.001,
    )

    def __init__(self, parentPos=(0, 0)):
        super().__init__(
            name=f"Sheep{Sheep.sheepCount}",
            hp=6,
            damage=2,
            speed=3,
            size=5,
            color=(0, 0, 255),
            position=parentPos,
            food=50,
            model=Sheep.model,
            movementStates=Sheep.movementStates,
        )
        Sheep.sheepCount += 1
