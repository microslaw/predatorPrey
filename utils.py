import math


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def proximityEntities(centerEntity, entities, maxSight=100):
    proximity = 0
    nearestDist = distance(centerEntity.position, entities[0].position)
    nearest_x, nearest_y = entities[0].position

    for entity in entities:
        dist = distance(centerEntity.position, entity.position) - entity.size
        if dist < maxSight:
            proximity += 5 - dist / maxSight
        if dist < nearestDist:
            nearestDist = dist
            nearest_x, nearest_y = entity.position

    return (proximity, nearest_x, nearest_y)


def generateStates(speed):
    return [(x, y) for x in range(-speed, speed + 1) for y in range(-speed, speed + 1)]


