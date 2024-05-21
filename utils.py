import numpy as np


def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def proximity_entities(center_entity, entities, max_sight=100):
    proximity = 0
    nearestDist = distance(center_entity.position, entities[0].position)
    nearest_x, nearest_y = entities[0].position

    for entity in entities:
        dist = distance(center_entity.position, entity.position) - entity.size
        if dist < max_sight:
            proximity += 5 - dist / max_sight
        if dist < nearestDist:
            nearestDist = dist
            nearest_x, nearest_y = entity.position

    return (proximity, nearest_x, nearest_y)


def generate_states(speed):
    return [(x, y) for x in range(-speed, speed + 1) for y in range(-speed, speed + 1)]


def mse(y_true, y_pred):
    return np.mean(np.square(y_pred - y_true))
