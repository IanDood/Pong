import pygame
import math
import random


class Ball:
    RADIUS = 7
    MAX_VELOCITY = 5

    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y

        angle = self.get_random_angle(-30, 30, [0])
        position = 1 if random.random() < 0.5 else -1

        self.x_velocity = position * abs(math.cos(angle) * self.MAX_VELOCITY)
        self.y_velocity = math.sin(angle) * self.MAX_VELOCITY

    def get_random_angle(self, min_angle, max_angle, excluded):
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))

        return angle

    def draw(self, window):
        pygame.draw.circle(window, (60, 255, 116), (self.x, self.y), self.RADIUS)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

        angle = self.get_random_angle(-30, 30, [0])
        x_vel = abs(math.cos(angle) * self.MAX_VELOCITY)
        y_vel = math.sin(angle) * self.MAX_VELOCITY

        self.y_velocity *= y_vel
        self.x_velocity *= -1
