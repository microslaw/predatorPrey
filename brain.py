print("Starting tensorflow imports...")
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import Adam
from keras.losses import MeanSquaredError

print("... Imports done")
import numpy as np
import random
import globals
from utils import mse


class Brain:

    @staticmethod
    def init_model(input_shape, output_shape, learning_rate):
        print(f"Model.init_model({input_shape}, {output_shape}, {learning_rate})")
        model = Sequential()
        model.add(Dense(input_shape, input_dim=input_shape, activation="relu"))
        model.add(Dense(10, activation="relu"))
        model.add(Dense(output_shape, activation="softmax"))
        model.compile(
            loss=MeanSquaredError(), optimizer=Adam(learning_rate=learning_rate)
        )
        return model

    @staticmethod
    def load(filename, output_shape):
        loaded_model = Brain(output_shape, model=load_model(filename))
        return loaded_model

    def __init__(
        self,
        output_shape,
        input_shape=globals.modelParams_input_shape,
        learning_rate=globals.modelParams_learning_rate,
        epsilon=globals.modelParams_epsilon,
        epsilon_min=globals.modelParams_epsilon_min,
        epsilon_decay=globals.modelParams_epsilon_decay,
        model=None,
    ):

        self.model = (
            model
            if model is not None
            else Brain.init_model(input_shape, output_shape, learning_rate)
        )
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.output_shape = output_shape

    def save(self, filename):
        self.model.save(filename)

    def fit(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = reward + globals.modelParams_gamma * np.max(  # type: ignore
                self.model.predict(np.array(next_state), verbose=0)[0]
            )
        target_f = self.model.predict(np.array(state), verbose=0)
        target_f[0][action] = target
        self.model.fit(state, target_f, epochs=1, verbose=0)

    def decide(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.output_shape)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        result = self.model.predict(np.array([state]), verbose=0)
        if globals.logging:
            print(f"    Model.decide({state}) -> {np.argmax(result[0])}")
            print(result)
        return np.argmax(result[0])