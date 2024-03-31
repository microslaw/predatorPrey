from entity import Entity
from model import Model
from utils import generate_states
import globals


class Sheep(Entity):
    sheep_count = 0
    movement_states = generate_states(globals.entityParams.sheep_speed)
    # model = Model(
    #     input_shape=globals.modelParams.input_shape,
    #     output_shape=len(movement_states),
    # )
    model = Model.load(f"v{globals.version_no}\sheep.h5", len(movement_states))
    print(model)

    def __init__(self, parentPos=(0, 0)):
        super().__init__(
            name=f"Sheep{Sheep.sheep_count}",
            hp=6,
            damage=2,
            speed=globals.entityParams.sheep_speed,
            size=5,
            color=(0, 0, 255),
            position=parentPos,
            food=50,
            model=Sheep.model,
            movement_states=Sheep.movement_states,
        )
        Sheep.sheep_count += 1
