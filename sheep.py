from entity import Entity
from brain import Brain
from utils import generate_states
import globals


class Sheep(Entity):
    sheep_count = 0
    movement_states = generate_states(globals.entityParams_sheep_speed) # type: ignore
    # model = Model(
    #     input_shape=globals.modelParams.input_shape,
    #     output_shape=len(movement_states),
    # )
    model = Brain.load(f".\\v{globals.version_no}\\sheepInitial.keras", len(movement_states))

    def __init__(self, parentPos=(0, 0)):
        super().__init__(
            name=f"Sheep{Sheep.sheep_count}",
            hp=6,
            damage=2,
            speed=globals.entityParams_sheep_speed, # type: ignore
            size=5,
            color=(0, 0, 255),
            position=parentPos,
            food=50,
            model=Sheep.model,
            movement_states=Sheep.movement_states,
        )
        Sheep.sheep_count += 1
