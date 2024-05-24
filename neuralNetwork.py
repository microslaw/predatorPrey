import numpy as np
from timer import Timer
import pickle


neuronMax = 1
neuronMin = -1
neuronDtype = np.float32


class NeuralNetwork:
    @staticmethod
    def sigmoid(x, derivative=False):
        if derivative:
            return x * (1 - x)
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def relu(x, derivative=False):
        if derivative:
            return 1.0 * (x > 0)
        return np.maximum(0, x)

    @staticmethod
    def leakyRelu(x, derivative=False):
        if derivative:
            return 1.0 * (x > 0) + 0.01 * (x <= 0)
        return np.maximum(0.01 * x, x)

    @staticmethod
    def absolute(x, derivative=False):
        if derivative:
            return 1 if x > 0 else -1
        return np.abs(x)


    # @staticmethod
    # def softmax(x):
    #     exps = np.exp(x - np.max(x))
    #     return exps / np.sum(exps, axis=1, keepdims=True)

    # @staticmethod
    # def softmaxDerivative(x):
    #     return x * (1 - x)
    @staticmethod
    def mseLoss(errorVector, derivative=False):
        if derivative:
            return errorVector
        return np.mean(np.square(errorVector))*0.5

    def __init__(self, layerSizes, activationFunctions):
        self.layerSizes = layerSizes
        self.activationFunctions = activationFunctions
        self.layers = [
            np.random.uniform(low=neuronMin, high=neuronMax, size=layerSizes[i]).astype(neuronDtype)
            for i in range(len(layerSizes))
        ]
        self.weights = [
            np.random.uniform(
                low=neuronMin, high=neuronMax, size=layerSizes[i] * layerSizes[i + 1]
            ).astype(neuronDtype).reshape(layerSizes[i], layerSizes[i + 1])
            for i in range(len(layerSizes) - 1)
        ]
        self.biases = [
            np.random.uniform(low=neuronMin, high=neuronMax, size=layerSizes[i + 1]).astype(
                neuronDtype
            )
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
            # Calculate the derivative of the activation function
            derivative = self.activationFunctions[i](self.layers[i + 1], derivative=True)

            # Calculate the error of the current layer
            layer_error = np.dot(output_error * derivative, self.weights[i].T) * learning_rate

            # Calculate the adjustments for the weights and biases
            weight_adjustments = np.outer(self.layers[i], output_error)
            bias_adjustments = output_error

            # Update the weights and biases
            self.weights[i] += weight_adjustments * learning_rate
            self.biases[i] += bias_adjustments * learning_rate

            # Set the output error for the next iteration
            # np.normalize(layer_error)
            output_error = layer_error



