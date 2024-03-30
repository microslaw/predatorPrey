from entity import Entity
from model import Model
from utils import generateStates
import globals


class Wolf(Entity):
    wolfCount = 0
    movementStates = generateStates(3)
    model = Model(
        input_shape=globals.modelParams.input_shape,
        output_shape=len(movementStates),
        learning_rate=0.001,
    )

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
            model=Wolf.model,
            movementStates=Wolf.movementStates,
        )
        Wolf.wolfCount += 1
