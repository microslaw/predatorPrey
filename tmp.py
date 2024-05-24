import random
import numpy as np
from matplotlib import pyplot as plt
from collections import defaultdict
from sklearn.model_selection import train_test_split, KFold
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Input
from tensorflow.keras.models import Model

class GeneticAlgorithm:
    def __init__(self, population_size, generations, crossover_probability, mutation_probability):
        self.population_size = population_size
        self.generations = generations
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability

    def initialize_population(self, search_space):
        population = []
        for _ in range(self.population_size):
            individual = {}
            for parameter, values in search_space.items():
                individual[parameter] = random.choice(values)
            population.append(individual)
        return population

    def fitness_function(self, individual, trainX, trainY, testX, testY):
        # Create and train the neural network with the given hyperparameters
        model = create_model(**individual)
        #fold_accuracy, histories, trained_models = evaluate_model(trainX, trainY, testX, testY, **individual)
        model.fit(trainX, trainY, epochs=10, batch_size=32, verbose=0)  # Training the model

        # Predict labels for test data
        predicted_labels = model.predict(testX)
        predicted_classes = np.argmax(predicted_labels, axis=1)

        # Map predicted labels to corresponding persons
        person_mapping = {}  # Dictionary to map labels to persons
        for i, label in enumerate(np.argmax(testY, axis=1)):
            person_mapping[label] = i

        # Compute accuracy per person
        correct_predictions_per_person = defaultdict(int)
        total_predictions_per_person = defaultdict(int)

        for predicted_classes, true_label in zip(predicted_classes, np.argmax(testY, axis=1)):
            if predicted_classes == np.argmax(true_label):
                person = np.argmax(true_label)  # Assume true label corresponds to person ID
                correct_predictions_per_person[person] += 1
            person = np.argmax(true_label)
            total_predictions_per_person[person] += 1

        # Compute accuracy per person
        accuracies_per_person = {}
        for person in total_predictions_per_person:
            if total_predictions_per_person[person] != 0:
                accuracies_per_person[person] = correct_predictions_per_person[person] / total_predictions_per_person[person]
            else:
                accuracies_per_person[person] = 0

        # Compute mean accuracy per person
        mean_accuracy_per_person = np.mean(list(accuracies_per_person.values()))

        # Return the mean accuracy per person as the fitness score
        return mean_accuracy_per_person

    def crossover(self, parent1, parent2):
        child = {}
        for parameter in parent1:
            if random.random() < 0.5:
                child[parameter] = parent1[parameter]
            else:
                child[parameter] = parent2[parameter]
        return child

    def mutate(self, individual, search_space):
        mutated_individual = individual.copy()
        for parameter, values in search_space.items():
            if random.random() < self.mutation_probability:
                mutated_individual[parameter] = random.choice(values)
        return mutated_individual

    def select_parents(self, population, trainX, trainY, testX, testY):
        return random.choices(population, k=2, weights=[self.fitness_function(individual, trainX, trainY, testX, testY) for individual in population])

    def run(self, search_space, trainX, trainY, testX, testY):
        population = self.initialize_population(search_space)

        for generation in range(self.generations):
            print(f"Generation {generation + 1}/{self.generations}")

            new_population = []

            for _ in range(self.population_size):
                parent1, parent2 = self.select_parents(population, trainX, trainY, testX, testY)
                child = self.crossover(parent1, parent2)
                if random.random() < self.crossover_probability:
                    child = self.mutate(child, search_space)
                new_population.append(child)

            population = new_population

            best_individual = max(population, key=lambda x: self.fitness_function(x, trainX, trainY, testX, testY))
            best_fitness = self.fitness_function(best_individual, trainX, trainY, testX, testY)
            print("Best Fitness:", best_fitness)

        best_individual = max(population, key=lambda x: self.fitness_function(x, trainX, trainY, testX, testY))
        best_fitness = self.fitness_function(best_individual, trainX, trainY, testX, testY)
        print("\nBest Individual:", best_individual)
        print("Best Fitness Score:", best_fitness)

        return best_individual, best_fitness


def load_pixels_and_attributes_from_file(files_arr):
    pixels = []
    attributes = []

    for filename in files_arr:
        with open(filename, 'r') as file:
            next(file)
            next(file)

            for line in file:
                values = list(map(float, line.strip().split()))
                pixels.append(values[:-8])
                attributes.append(values[-8:])

    pixels_array = np.array(pixels)
    attributes_array = np.array(attributes)
    return pixels_array, attributes_array


def load_data (pixels, attributes):
    labels = attributes[:, 2]  # Extract the labels from the attributes array

    # Split your dataset into training and testing sets
    train_pixels, test_pixels, train_labels, test_labels = train_test_split(pixels, labels, test_size=0.2, random_state=42)

    trainX = train_pixels.reshape((train_pixels.shape[0], 24, 24, 1))
    testX = test_pixels.reshape((test_pixels.shape[0], 24, 24, 1))

    trainY = to_categorical(train_labels)
    testY = to_categorical(test_labels)

    return trainX, trainY, testX, testY


def create_model(hidden_layers, units_per_layer):
    inputs = Input(shape=(24, 24, 1))
    x = Conv2D(32, (3, 3), activation='relu')(inputs)
    x = MaxPooling2D((2, 2))(x)
    x = Flatten()(x)
    for _ in range(hidden_layers):
        x = Dense(units_per_layer, activation='relu')(x)
    outputs = Dense(48, activation='softmax')(x)
    model = Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def evaluate_model(pixels, attr, n_folds=48, **hyperparameters):
    fold_accuracy, histories, trained_models = [], [], []
    kfold = KFold(n_folds, shuffle=True)
    for train_indices, val_indices in kfold.split(pixels):
        model = create_model(**hyperparameters)
        train_pixels, train_attributes = pixels[train_indices], attr[train_indices]
        val_pixels, val_attributes = pixels[val_indices], attr[val_indices]
        history = model.fit(train_pixels, train_attributes, epochs=10, batch_size=32, validation_data=(val_pixels, val_attributes))
        _, accuracy = model.evaluate(val_pixels, val_attributes)
        fold_accuracy.append(accuracy)
        histories.append(history)
        trained_models.append(model)
    return fold_accuracy, histories, trained_models


def run_proc():
    file_to_read = ['famous48\\x24x24.txt','famous48\\y24x24.txt','famous48\\z24x24.txt']
    pixels, attributes = load_pixels_and_attributes_from_file(file_to_read)

    trainX, trainY, testX, testY = load_data(pixels, attributes)

    # Define the search space for genetic algorithm
    search_space = {
        'hidden_layers': [1, 2, 3],
        'units_per_layer': [64, 128, 256]
    }

    # Initialize and run the genetic algorithm
    ga = GeneticAlgorithm(population_size=10, generations=5, crossover_probability=0.8, mutation_probability=0.1)
    best_hyperparameters, best_fitness = ga.run(search_space, trainX, trainY, testX, testY)

    final_model = create_model(**best_hyperparameters)
    final_model.fit(trainX, trainY, epochs=10, batch_size=32, validation_data=(testX, testY))

    # Evaluate the final model
    final_loss, final_accuracy = final_model.evaluate(testX, testY)
    print("Final Accuracy:", final_accuracy, final_loss)

run_proc()
