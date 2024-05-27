from entity import Entity
from utils import generate_input_from_sight, generate_outputs
import globals
import numpy as np
import neuralNetwork as nn


class Sheep(Entity):
    sheep_count = 0
    brain = nn.NeuralNetwork()

    def __init__(self, parentPos=(0, 0), learning=True):
        super().__init__(
            name=f"Sheep{Sheep.sheep_count}",
            hp=globals.entityParams_sheep_hp,
            damage=globals.entityParams_sheep_damage,
            speed=globals.entityParams_sheep_speed,
            size=globals.entityParams_sheep_size,
            color=globals.entityParams_sheep_color,
            position=parentPos,
            # food=globals.entityParams_sheep_food,
            food=int(np.random.normal(globals.entityParams_sheep_food, 10)),
            brain=Sheep.brain,
            sight=globals.entityParams_sheep_sight,
            learning=learning,
        )
        Sheep.sheep_count += 1

    @staticmethod
    def add_brain(brain=None):
        if isinstance(brain, nn.NeuralNetwork):
            Sheep.brain = brain
        else:
            Sheep.brain = nn.NeuralNetwork(
                layerSizes=[
                    generate_input_from_sight(globals.entityParams_sheep_sight),
                    10,
                    len(generate_outputs(globals.entityParams_sheep_speed)),
                ],
                activationFunctions=[nn.leakyRelu, nn.leakyRelu],
            )
