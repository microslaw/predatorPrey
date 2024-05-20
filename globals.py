version_no = 0

min_wolf_age = 100
min_wolf_food = 100
min_sheep_age = 100
min_sheep_food = 100
min_grass_size = 10

grass_eating_speed = 1
grass_eating_efficiency = 10

attack_range = 1

food_cost = 0.5

starving_damage = 1

window_height = 500
window_width = 800
game_height = 500
game_width = 800

tickrate = 30

sheep_grass_size = 15
wolf_grass_size = 20
sheep_speed = 2
wolf_speed = 3

reward_eating = 1
reward_reproduce = 20
reward_high_hp = 1
high_hp_treshold = 4.5
penalty_death = -100


class modelParams:
    pass
modelParams.gamma = 0.95
modelParams.epsilon = 0.0
modelParams.epsilon_min = 0.0
modelParams.epsilon_decay = 0.995
modelParams.input_shape = 10
modelParams.learning_rate = 0.001

class modelRewards:
    pass
modelRewards.sheep_food_modifier=1
modelRewards.wolf_food_modifier=1
modelRewards.sheep_reproduce=100
modelRewards.wolf_reproduce=100
modelRewards.sheep_death=-100
modelRewards.wolf_death=-100

class entityParams:
    pass
entityParams.sheep_speed = 2
entityParams.wolf_speed = 3
