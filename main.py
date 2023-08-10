# # Pong Game Creation
# import pygame
# pygame.init()
#
# # Setting size of the window, and also the title
# WIDTH, HEIGHT = 700, 500
# WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Pong")
#
# # Frame Rate in which the clock updates the screen
# FPS = 60
#
# # Font to keep up the text that will be shown in screen and declaring constant for winning score
# SCORE_FONT = pygame.font.SysFont("Courier New", 50)
# WINNING_FONT = pygame.font.SysFont("Comic Sans", 56)
# WINNING_SCORE = 10
#
#
# def handle_paddle_mov(keys, left_paddle, right_paddle):
#     if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0:
#         left_paddle.move(up=True)
#     if keys[pygame.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= HEIGHT:
#         left_paddle.move(up=False)
#
#     if keys[pygame.K_i] and right_paddle.y - right_paddle.VELOCITY >= 0:
#         right_paddle.move(up=True)
#     if keys[pygame.K_k] and right_paddle.y + right_paddle.VELOCITY + right_paddle.height <= HEIGHT:
#         right_paddle.move(up=False)

#
# def main():
#     playing = True
#     clock = pygame.time.Clock()
#
#     left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
#     right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
#     ball = Ball(WIDTH / 2, HEIGHT // 2, BALL_RADIUS)
#
#     left_score = 0
#     right_score = 0
#
#     while playing:
#         clock.tick(FPS)
#         draw(WINDOW, [left_paddle, right_paddle], ball, left_score, right_score)
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 playing = False
#                 break
#
#         keys = pygame.key.get_pressed()
#         handle_paddle_mov(keys, left_paddle, right_paddle)
#
#         ball.move()
#         handle_collision(ball, left_paddle, right_paddle)
#
#         if ball.x < 0:
#             right_score += 1
#             ball.reset()
#         elif ball.x > WIDTH:
#             left_score += 1
#             ball.reset()
#
#         winner = False
#         if left_score > WINNING_SCORE:
#             winner = True
#             winning_text = "Left Player Won!"
#         elif right_score > WINNING_SCORE:
#             winner = True
#             winning_text = "Right Player Won!"
#
#         if winner:
#             text = WINNING_FONT.render(winning_text, 1, WIN_GREEN)
#             WINDOW.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
#             pygame.display.update()
#             pygame.time.delay(5000)
#             ball.reset()
#             left_paddle.reset()
#             right_paddle.reset()
#             left_score = 0
#             right_score = 0
#
#     pygame.quit()


# if __name__ == '__main__':
#     main()
