import numpy as np
import pickle
import globals


neuronMax = 1
neuronMin = -1
neuronDtype = np.float32


def sigmoid(x, derivative=False):
    if derivative:
        return x * (1 - x)
    return 1 / (1 + np.exp(-x))


def relu(x, derivative=False):
    if derivative:
        return 1.0 * (x > 0)
    return np.maximum(0, x)


def leakyRelu(x, derivative=False):
    if derivative:
        return 1.0 * (x > 0) + 0.01 * (x <= 0)
    return np.maximum(0.01 * x, x)


def absolute(x, derivative=False):
    if derivative:
        return 1 if x > 0 else -1
    return np.abs(x)


def mseLoss(errorVector, derivative=False):
    if derivative:
        return errorVector
    return np.mean(np.square(errorVector)) * 0.5


class NeuralNetwork:

    def __init__(self, layerSizes=None, activationFunctions=None):
        if layerSizes is None or activationFunctions is None:
            return

        self.layerSizes = layerSizes
        self.activationFunctions = activationFunctions
        self.layers = [
            np.random.uniform(low=neuronMin, high=neuronMax, size=layerSizes[i]).astype(
                neuronDtype
            )
            for i in range(len(layerSizes))
        ]
        self.weights = [
            np.random.uniform(
                low=neuronMin, high=neuronMax, size=layerSizes[i] * layerSizes[i + 1]
            )
            .astype(neuronDtype)
            .reshape(layerSizes[i], layerSizes[i + 1])
            for i in range(len(layerSizes) - 1)
        ]
        self.biases = [
            np.random.uniform(
                low=neuronMin, high=neuronMax, size=layerSizes[i + 1]
            ).astype(neuronDtype)
            for i in range(len(layerSizes) - 1)
        ]

    def loadInput(self, input):
        self.layers[0] = input.astype(neuronDtype)

    def readOutput(self):
        return self.layers[-1]

    def forward(self):
        for i in range(len(self.weights)):
            self.layers[i + 1] = self.activationFunctions[i](
                np.dot(self.layers[i], self.weights[i]) + self.biases[i]
            )

    def backpropagation(self, target, learning_rate, lossFunction):
        output_error = lossFunction(target - self.layers[-1], derivative=True)

        for i in range(len(self.layers) - 2, -1, -1):
            derivative = self.activationFunctions[i](
                self.layers[i + 1], derivative=True
            )

            layer_error = (
                np.dot(output_error * derivative, self.weights[i].T) * learning_rate
            )

            weight_adjustments = np.outer(self.layers[i], output_error)
            bias_adjustments = output_error

            self.weights[i] += weight_adjustments * learning_rate
            self.biases[i] += bias_adjustments * learning_rate

            output_error = layer_error

    def predict(self, input):
        self.loadInput(input)
        self.forward()
        return self.readOutput()

    def train(self, input, target, learning_rate, lossFunction):
        self.loadInput(input)
        self.forward()
        self.backpropagation(target, learning_rate, lossFunction)


    def qlearn_cyclic(self, reward, previous_estimates, previous_state, current_state, done):

        previous_pick = np.argmax(previous_estimates)
        target = previous_estimates

        if done:
            target[previous_pick] = reward
        else:
            target[previous_pick] = reward + globals.modelParams_gamma * np.argmax(
                self.predict(current_state)
            )
        #epsilon greedy has been moved to entity.perform move for implementation reasons

        self.train(previous_state, target, globals.modelParams_learning_rate, mseLoss)


    def save(self, filename):
        with open(filename, "wb") as wfile:
            pickle.dump(self, wfile)


def load(filename) -> NeuralNetwork:
    with open(filename, "rb") as rfile:
        return pickle.load(rfile)
