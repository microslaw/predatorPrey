from entity import Entity
from model import Model
from utils import generate_states
import globals


class Wolf(Entity):
    wolfCount = 0
    movement_states = generate_states(globals.entityParams_wolf_speed) # type: ignore
    # model = Model(
    #     input_shape=globals.modelParams.input_shape,
    #     output_shape=len(movement_states),
    # )
    model = Model.load(f".\\v{globals.version_no}\\wolfInitial.keras", len(movement_states))

    def __init__(self, parent_pos=(0, 0)):
        super().__init__(
            name=f"Wolf{Wolf.wolfCount}",
            hp=10,
            damage=5,
            speed=globals.entityParams_wolf_speed, # type: ignore
            size=10,
            color=(255, 0, 0),
            position=parent_pos,
            food=100,
            model=Wolf.model,
            movement_states=Wolf.movement_states,
        )
        Wolf.wolfCount += 1
