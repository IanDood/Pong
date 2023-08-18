import os
import pickle
import time

import smbus
import neat
import pygame

from Pong import Game
from Pong import button

NUNCHUCK_DEVICE = 0x52
bus = smbus.SMBus(1)


class PongGame:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball

    def read_nunchuck_data(self):
        bus.write_byte_data(NUNCHUCK_DEVICE, 0x40, 0x00)
        time.sleep(0.1)

        bus.write_byte(NUNCHUCK_DEVICE, 0x00)
        time.sleep(0.1)

        bytes = [bus.read_byte(NUNCHUCK_DEVICE) for _ in range(6)]

        joyY = bytes[1]
        return joyY

    def test_game(self):
        playing = True
        clock = pygame.time.Clock()
        while playing:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        main_menu()

            keys = pygame.key.get_pressed()
            if joyY > 160:
                self.game.move_paddle(left=True, up=True)
            if joyY < 50:
                self.game.move_paddle(left=True, up=False)
            # if keys[pygame.K_w]:
            #     self.game.move_paddle(left=True, up=True)
            # if keys[pygame.K_s]:
            #     self.game.move_paddle(left=True, up=False)

            if keys[pygame.K_i]:
                self.game.move_paddle(left=False, up=True)
            if keys[pygame.K_k]:
                self.game.move_paddle(left=False, up=False)

            game_info = self.game.loop()
            self.game.draw(True, False)
            pygame.display.update()

        pygame.quit()

    def test_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        playing = True
        clock = pygame.time.Clock()
        while playing:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        main_menu()

            keys = pygame.key.get_pressed()
            if joyY > 160:
                self.game.move_paddle(left=True, up=True)
            if joyY < 50:
                self.game.move_paddle(left=True, up=False)
            # if keys[pygame.K_w]:
            #     self.game.move_paddle(left=True, up=True)
            # if keys[pygame.K_s]:
            #     self.game.move_paddle(left=True, up=False)

            output = net.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            decision = output.index(max(output))

            if decision == 0:
                pass
            elif decision == 1:
                self.game.move_paddle(left=False, up=True)
            else:
                self.game.move_paddle(left=False, up=False)

            game_info = self.game.loop()
            self.game.draw(True, False)
            pygame.display.update()

        pygame.quit()

    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        playing = True
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            output1 = net1.activate((self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
            decision1 = output1.index(max(output1))

            if decision1 == 0:
                pass
            elif decision1 == 1:
                self.game.move_paddle(left=True, up=True)
            else:
                self.game.move_paddle(left=True, up=False)

            output2 = net2.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            decision2 = output2.index(max(output2))

            if decision2 == 0:
                pass
            elif decision2 == 1:
                self.game.move_paddle(left=False, up=True)
            else:
                self.game.move_paddle(left=False, up=False)

            game_info = self.game.loop()

            self.game.draw(draw_score=False, draw_hits=True)
            pygame.display.update()

            if game_info.left_score >= 1 or game_info.right_score >= 1 or game_info.left_hits > 50:
                self.calculate_fitness(genome1, genome2, game_info)
                break

    def calculate_fitness(self, genome1, genome2, game_info):
        genome1.fitness += game_info.left_hits
        genome2.fitness += game_info.right_hits


def eval_genomes(genomes, config):
    width, height = 700, 500
    window = pygame.display.set_mode((width, height))

    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness is None else genome2.fitness
            game = PongGame(window, width, height)
            game.train_ai(genome1, genome2, config)


def run_neat(config):
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-11')
    # p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 1)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


def one_player(config):
    width, height = 700, 500
    window = pygame.display.set_mode((width, height))

    pygame.display.set_caption("P1 vs CPU")

    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)

    game = PongGame(window, width, height)
    game.test_ai(winner, config)


def two_player():
    width, height = 700, 500
    window = pygame.display.set_mode((width, height))

    pygame.display.set_caption("P1 vs P2")

    game = PongGame(window, width, height)
    game.test_game()


def main_menu():
    width, height = 700, 500

    window = pygame.display.set_mode((width, height))

    pygame.display.set_caption("Main Menu")
    playing = True

    while playing:

        # Load Images
        one_img = pygame.image.load("images/button_one.png").convert_alpha()
        two_img = pygame.image.load("images/button_two.png").convert_alpha()
        quit_img = pygame.image.load("images/button_quit.png").convert_alpha()

        # Create button instances
        one_button = button.Button(196, 85, one_img, 1)
        two_button = button.Button(196, 209, two_img, 1)
        quit_button = button.Button(286, 333, quit_img, 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if one_button.find(window):
                    one_player(config)
                if two_button.find(window):
                    two_player()
                if quit_button.find(window):
                    pygame.quit()
                    break

        pygame.display.update()


if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()
    pygame.display.init()

    local_directory = os.path.dirname(__file__)
    config_path = os.path.join(local_directory, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    # run_neat(config)

    main_menu()

    pygame.quit()
