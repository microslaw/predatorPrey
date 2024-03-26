from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import Adam

class Model:
    def __init__(self, config):
        self.config = config
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(64, input_dim=self.config.input_dim, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model

    def train(self, X, y):
        self.model.fit(X, y, epochs=self.config.epochs, batch_size=self.config.batch_size)

    def predict(self, X):
        return self.model.predict(X)
