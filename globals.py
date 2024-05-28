from utils import generate_input_from_sight

version_no = 7
logging = False

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

tickrate = 10

sheep_grass_size = 15
wolf_grass_size = 20
sheep_speed = 2
wolf_speed = 3

reward_eating = 1
reward_reproduce = 20
reward_high_hp = 1
high_hp_treshold = 4.5
penalty_death = -100


modelParams_gamma = 0.95
modelParams_epsilon = 0.1
modelParams_epsilon_min = 0.00001
modelParams_epsilon_decay = 0.995
modelParams_learning_rate = 0.000001
# modelParams_learning_rate = 0.01
modelParams_output_shape = 3

modelRewards_sheep_food_modifier=1
modelRewards_wolf_food_modifier=1
modelRewards_sheep_reproduce=100
modelRewards_wolf_reproduce=100
modelRewards_sheep_death=-100
modelRewards_wolf_death=-100



entityParams_sheep_size = 2
entityParams_sheep_speed = entityParams_sheep_size * 2
entityParams_sheep_sight = entityParams_sheep_speed * 5
entityParams_sheep_color = (0, 0, 255)
entityParams_sheep_food = 50
entityParams_sheep_hp = 5
entityParams_sheep_damage = 2
entityParams_sheep_input = generate_input_from_sight(entityParams_sheep_sight)

entityParams_wolf_size = 3
entityParams_wolf_speed = entityParams_wolf_size * 2
entityParams_wolf_sight = entityParams_wolf_speed * 5
entityParams_wolf_color = (255, 0, 0)
entityParams_wolf_food = 100
entityParams_wolf_hp = 10
entityParams_wolf_damage = 6
entityParams_wolf_input = generate_input_from_sight(entityParams_wolf_sight)


game_no = 0
