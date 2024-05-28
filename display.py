import pygame
import globals
import cv2
import numpy as np
from utils import generate_outputs


class Display:

    def __init__(self, scale=1):

        self.scale = scale
        self.clock = pygame.time.Clock()
        self.running = True
        self.entities = []
        self.setup()

    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (globals.window_width, globals.window_height)
        )
        pygame.display.set_caption("predatorPrey")
        cv2.namedWindow("White wiew", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Predicted rewards", cv2.WINDOW_NORMAL)

    def update(self, entities, game):
        if not self.running:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        self.screen.fill((0, 0, 0))
        for entity in entities:
            x, y = entity.position
            if entity.chosen:
                self.handle_chosen(entity, game)

            else:
                pygame.draw.circle(
                    self.screen,
                    entity.color,
                    (x / self.scale, y / self.scale),
                    max(1, entity.size / self.scale),
                )
        pygame.display.flip()
        self.clock.tick(globals.tickrate)

    def handle_chosen(self, entity, game):
        x, y = entity.position
        # print(entity.food)

        pygame.draw.circle(
            self.screen,
            (255, 255, 255),
            (x / self.scale, y / self.scale),
            max(1, entity.size / self.scale),
        )

        outlook = game.get_outlook(entity)

        outlook = outlook.astype(np.float32)
        outlook = cv2.cvtColor(outlook, cv2.COLOR_BGR2RGB)
        cv2.imshow(
            "White wiew",
            cv2.resize(outlook, (outlook.shape[0], outlook.shape[1])),
        )

        map = np.array(generate_outputs(entity.speed)) + entity.speed
        reward_list = entity.previous_estimates

        size = int(entity.speed * 2 + 1)
        predicted_rewards = np.zeros((size, size))
        for i in range(len(map)):
            predicted_rewards[map[i][0], map[i][1]] = reward_list[i].astype(np.float32)
        # to rgb for display
        predicted_rewards = predicted_rewards + np.abs(np.min(predicted_rewards))
        predicted_rewards = (predicted_rewards / np.max(predicted_rewards)) * 255

        predicted_rewards = np.dstack(
            (
                predicted_rewards,
                np.zeros(predicted_rewards.shape),
                np.zeros(predicted_rewards.shape),
            )
        )

        best_x, best_y, best_z = np.unravel_index(
            np.argmax(predicted_rewards, axis=None), predicted_rewards.shape
        )

        predicted_rewards[best_x, best_y] = [0, 255, 0]

        a,b = entity.last_move
        a += entity.speed
        b += entity.speed

        predicted_rewards[a, b] += [0, 0, 255]
        predicted_rewards[best_x, best_y] += [0, 255, 0]
        predicted_rewards = predicted_rewards.transpose(1, 0, 2)
        # predicted_rewards = np.flip(predicted_rewards, 1)
        predicted_rewards = cv2.resize(
            predicted_rewards, predicted_rewards.shape[0:2]
        ).astype(np.uint8)
        cv2.imshow("Predicted rewards", predicted_rewards)

    def cleanup(self):
        pygame.quit()
        cv2.destroyAllWindows()
