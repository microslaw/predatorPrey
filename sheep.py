from entity import Entity
from utils import generate_input_from_sight
import globals
import neuralNetwork as nn


class Sheep(Entity):
    sheep_count = 0
    brain = nn.NeuralNetwork()

    def __init__(self, parentPos=(0, 0)):
        super().__init__(
            name=f"Sheep{Sheep.sheep_count}",
            hp=globals.entityParams_sheep_hp,
            damage=globals.entityParams_sheep_damage,
            speed=globals.entityParams_sheep_speed,
            size=globals.entityParams_sheep_size,
            color=globals.entityParams_sheep_color,
            position=parentPos,
            food=globals.entityParams_sheep_food,
            brain=Sheep.brain,
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
                    10,
                    4,
                ],
                activationFunctions=[nn.leakyRelu, nn.leakyRelu, nn.leakyRelu],
            )
