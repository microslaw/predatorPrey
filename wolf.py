from entity import Entity
from utils import generate_input_from_sight
import globals
import neuralNetwork as nn


class Wolf(Entity):
    wolfCount = 0
    brain = nn.NeuralNetwork()

    def __init__(self, parent_pos=(0, 0)):
        super().__init__(
            name=f"Wolf{Wolf.wolfCount}",
            hp=globals.entityParams_wolf_hp,
            damage=globals.entityParams_wolf_damage,
            speed=globals.entityParams_wolf_speed,
            size=globals.entityParams_wolf_size,
            color=globals.entityParams_wolf_color,
            position=parent_pos,
            food=globals.entityParams_wolf_food,
            brain=Wolf.brain,
            sight=globals.entityParams_wolf_sight,
        )
        Wolf.wolfCount += 1

    @staticmethod
    def add_brain(brain=None):
        if isinstance(brain, nn.NeuralNetwork):
            Wolf.brain = brain
        else:
            Wolf.brain = nn.NeuralNetwork(
                layerSizes=[
                    generate_input_from_sight(globals.entityParams_wolf_sight),
                    10,
                    10,
                    globals.modelParams_output_shape,
                ],
                activationFunctions=[nn.leakyRelu, nn.leakyRelu, nn.leakyRelu],
            )
