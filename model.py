from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import Adam
import numpy as np
import random
import globals

print("Imports done")


class Model:

    @staticmethod
    def init_model(input_shape, output_shape, learning_rate):
        model = Sequential()
        model.add(Dense(64, input_dim=input_shape, activation="relu"))
        model.add(Dense(64, activation="relu"))
        model.add(
            Dense(output_shape, activation="linear")
        )  # Output is Q-value of each action
        model.compile(loss="mse", optimizer=Adam(learning_rate=learning_rate))
        return model

    @staticmethod
    def load(filename):
        return load_model(filename)

    def __init__(
        self,
        input_shape,
        output_shape,
        learning_rate,
        epsilon=globals.modelParams.epsilon,
        epsilon_min=globals.modelParams.epsilon_min,
        epsilon_decay=globals.modelParams.epsilon_decay,
    ):
        self.model = Model.init_model(input_shape, output_shape, learning_rate)
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

    def save(self, filename):
        model.save(filename)

    def reward(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = reward + globals.modelParams.gamma * np.max(
                self.model.predict(next_state)[0]
            )
        target_f = self.model.predict(state)
        target_f[0][action] = target
        self.model.fit(state, target_f, epochs=1, verbose=0)


    def decide(self, state, action_size):
        if np.random.rand() <= self.epsilon:
            return random.randrange(action_size)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        return np.argmax(model.predict(state)[0])


model = Model.init_model(10, 2, 0.001)
model.save("model.h5")
model2 = Model.load("model.h5")
