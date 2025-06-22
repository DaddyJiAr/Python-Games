import pygame
import math
from random import randint, choice
from sys import exit

pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Game ko")
FPS = 60
clock = pygame.time.Clock()

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, player_number=1):
        super().__init__()
        self.player_number = player_number
        self.image = pygame.Surface((width, height))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self):
        keys = pygame.key.get_pressed()
        if self.player_number == 2:
            if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= 7
            if keys[pygame.K_DOWN] and self.rect.bottom < 400:
                self.rect.y += 7
        elif self.player_number == 1:
            if keys[pygame.K_w] and self.rect.top > 0:
                self.rect.y -= 7
            if keys[pygame.K_s] and self.rect.bottom < 400:
                self.rect.y += 7
    
    def drawAt(self, x, y, surface):
        surface.blit(self.image, self.image.get_rect(center=(x, y)))
        
    def setColor(self, color):
        self.color = color
        self.image.fill(self.color)
        

class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, color):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(400, randint(50, 350)))
        self.mask = pygame.mask.from_surface(self.image)
        self.color = color
        self.radius = radius
        self.speed = 5
        self.speed_x = choice([-self.speed, self.speed])
        self.speed_y = choice([-self.speed, self.speed])
        self.max_speed_x = 10
        self.max_speed_y = 15

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top <= 0:
            self.speed_y = abs(self.speed_y)
        elif self.rect.bottom >= 400:
            self.speed_y = -1 * self.speed_y
    
    def reset(self):
        self.rect.center = (400, randint(50, 350))
        self.speed_x = choice([-self.speed, self.speed])
        self.speed_y = choice([-self.speed, self.speed])
        pause(500)
    
    def drawAt(self, x, y, surface):
        radius = self.rect.width // 2
        pygame.draw.circle(surface, self.color, (x, y), radius)
    
    def setColor(self, color):
        self.color = color
        # self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        # self.image.fill(self.color)
        # self.mask = pygame.mask.from_surface(self.image)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(400, randint(50, 350)))
        self.mask = pygame.mask.from_surface(self.image)
    


def pause(milliseconds):
    global player1, player2, ball, player1_score_text, player2_score_text, player1_score_text_rect, player2_score_text_rect
    ball.draw(screen)
    player1.draw(screen)
    player2.draw(screen)
    screen.blit(player1_score_text, player1_score_text_rect)
    screen.blit(player2_score_text, player2_score_text_rect)
    pygame.display.update()
    pygame.time.delay(milliseconds)

def collide_masks(paddle, ball):
    return pygame.sprite.collide_mask(paddle, ball)
    


# player1_paddle = pygame.Surface((20, 120))
# player1_paddle.fill((255,0,0))

# player2_paddle = pygame.Surface((20, 120))
# player2_paddle.fill((0,0,255))

# circle_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
# pygame.draw.circle(circle_surface, (0, 255, 0), (30, 30), 10)


# circle_mask = pygame.mask.from_surface(circle_surface)
# paddle_mask = pygame.mask.from_surface(player1_paddle)



test_font = pygame.font.Font("font/Pixeltype.ttf", 50)
bigger_font = pygame.font.Font("font/Pixeltype.ttf", 70)

player1_score = 0
player2_score = 0

player1_score_text = test_font.render(str(player1_score), True, (255, 255, 255))
player2_score_text = test_font.render(str(player2_score), True, (255, 255, 255))

player1_score_text_rect = player1_score_text.get_rect(center=(200, 50))
player2_score_text_rect = player2_score_text.get_rect(center=(600, 50))


player1_colors = ["Red", "Green", "Blue", "Yellow", "Purple", "Orange", "Pink", "Cyan", "Magenta", "Brown", "Gold"]
player2_colors = player1_colors.copy()
ball_colors = player1_colors.copy()

player1_color_index = 0
ball_color_index = 1
player2_color_index = 2

player1_color = test_font.render(str(player1_colors[player1_color_index]), True, (255, 255, 255))
ball_color = test_font.render(str(ball_colors[ball_color_index]), True, (255, 255, 255))
player2_color = test_font.render(str(player2_colors[player2_color_index]), True, (255, 255, 255))
player1_color_rect = player1_color.get_rect(center=(150, 280))
ball_color_rect = ball_color.get_rect(center=(400, 280))
player2_color_rect = player2_color.get_rect(center=(650, 280))

player1_left = test_font.render("<", True, (255, 255, 255))
player1_right = test_font.render(">", True, (255, 255, 255))
player1_left_rect = player1_left.get_rect(center=(50, 280))
player1_right_rect = player1_right.get_rect(center=(250, 280))

ball_left = test_font.render("<", True, (255, 255, 255))
ball_right = test_font.render(">", True, (255, 255, 255))
ball_left_rect = ball_left.get_rect(center=(300, 280))
ball_right_rect = ball_right.get_rect(center=(500, 280))

player2_left = test_font.render("<", True, (255, 255, 255))
player2_right = test_font.render(">", True, (255, 255, 255))
player2_left_rect = player2_left.get_rect(center=(550, 280))
player2_right_rect = player2_right.get_rect(center=(750, 280))




player1 = pygame.sprite.GroupSingle()
player1.add(Paddle(20, 20, 20, 120, player1_colors[player1_color_index], 1))
player2 = pygame.sprite.GroupSingle()
player2.add(Paddle(760, 20, 20, 120, player2_colors[player2_color_index], 2))
ball = pygame.sprite.GroupSingle()
ball.add(Ball(10, (0, 255, 0)))



#main menu
game_title = bigger_font.render("Ping Ponginamo", False, (255, 255, 255))
game_title_rect = game_title.get_rect(center=(400, 100))

start_game = test_font.render("Start Game", False, (255, 255, 255))
start_game_rect = start_game.get_rect(center=(400, 300))

customize = test_font.render("Customize", False, (255, 255, 255))
customize_rect = customize.get_rect(center=(400, 330))
hit_sound = pygame.mixer.Sound("audio/pong_hit.mp3")
hit_sound.set_volume(0.2)

WIN_SCORE = 3


in_game = False
in_customize = False
start_screen = True
win_lose_screen = False

# pause(1000)  # Pause for 1 second before starting the game
def check_score():
    global player1_score, player2_score, player1_score_text, player2_score_text
    if ball.sprite.rect.right <= 0:
        player2_score += 1
        player2_score_text = test_font.render(str(player2_score), True, (255, 255, 255))
        ball.sprite.reset() 
    elif ball.sprite.rect.left >= 800:
        player1_score += 1
        player1_score_text = test_font.render(str(player1_score), True, (255, 255, 255))
        ball.sprite.reset()
        
       
    if player1_score >= WIN_SCORE or player2_score >= WIN_SCORE:
        print(f"Player 1: {player1_score}, Player 2: {player2_score}")
        return False
    return True
        
        
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and start_screen:
                exit()
            if event.key == pygame.K_ESCAPE and win_lose_screen:
                start_screen = True
                win_lose_screen = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_screen:
                if start_game_rect.collidepoint(event.pos):
                    in_game = True
                    start_screen = False
                    player1_score = 0
                    player2_score = 0
                    player1_score_text = test_font.render(str(player1_score), True, (255, 255, 255))
                    player2_score_text = test_font.render(str(player2_score), True, (255, 255, 255))
                elif customize_rect.collidepoint(event.pos):
                    in_customize = True
            elif in_customize:
                if player1_left_rect.collidepoint(event.pos):
                    player1_color_index = (player1_color_index - 1) % len(player1_colors)
                    player1.sprite.setColor(player1_colors[player1_color_index])
                    player1_color = test_font.render(str(player1_colors[player1_color_index]), True, (255, 255, 255))
                    player1_color_rect = player1_color.get_rect(center=(150, 280))
                elif player1_right_rect.collidepoint(event.pos):
                    player1_color_index = (player1_color_index + 1) % len(player1_colors)
                    player1.sprite.setColor(player1_colors[player1_color_index])
                    player1_color = test_font.render(str(player1_colors[player1_color_index]), True, (255, 255, 255))
                    player1_color_rect = player1_color.get_rect(center=(150, 280))
                elif player2_left_rect.collidepoint(event.pos):
                    player2_color_index = (player2_color_index - 1) % len(player2_colors)
                    player2.sprite.setColor(player2_colors[player2_color_index])
                    player2_color = test_font.render(str(player2_colors[player2_color_index]), True, (255, 255, 255))
                    player2_color_rect = player2_color.get_rect(center=(650, 280))
                elif player2_right_rect.collidepoint(event.pos):
                    player2_color_index = (player2_color_index + 1) % len(player2_colors)
                    player2.sprite.setColor(player2_colors[player2_color_index]) 
                    player2_color = test_font.render(str(player2_colors[player2_color_index]), True, (255, 255, 255))
                    player2_color_rect = player2_color.get_rect(center=(650, 280))
                elif ball_left_rect.collidepoint(event.pos):
                    ball_color_index = (ball_color_index - 1) % len(ball_colors)
                    ball.sprite.setColor(ball_colors[ball_color_index])
                    ball_color = test_font.render(str(ball_colors[ball_color_index]), True, (255, 255, 255))
                    ball_color_rect = ball_color.get_rect(center=(400, 280))
                elif ball_right_rect.collidepoint(event.pos):
                    ball_color_index = (ball_color_index + 1) % len(ball_colors)
                    ball.sprite.setColor(ball_colors[ball_color_index])
                    ball_color = test_font.render(str(ball_colors[ball_color_index]), True, (255, 255, 255))
                    ball_color_rect = ball_color.get_rect(center=(400, 280))
                else:
                    in_customize = False
            elif win_lose_screen:
                screen.fill((0, 0, 0))
                player1_score = 0
                player2_score = 0
                player1_score_text = test_font.render(str(player1_score), True, (255, 255, 255))
                player2_score_text = test_font.render(str(player2_score), True, (255, 255, 255))
                in_game = True
                win_lose_screen = False
                ball.sprite.reset()
    if in_game:
        
        # screen.blit(player1_paddle, (20,20))
        # screen.blit(player2_paddle, (760,20)) # 740 = 800 (width) - 20 (paddle width) - 20 (gap)
        # screen.blit(circle_surface, (400, 50))
        
        screen.fill((0, 0, 0))
        
        player1.update()
        player1.draw(screen)
        player2.update()
        player2.draw(screen)
        ball.update()
        ball.draw(screen)
        check_score()
        
        if collide_masks(player1.sprite, ball.sprite):
            hit_sound.play()
            deltaY = ball.sprite.rect.centery-((player1.sprite.rect.top+player1.sprite.rect.bottom)/2)
            ball.sprite.speed_x = abs(ball.sprite.speed_x)  
            ball.sprite.speed_y += deltaY * 0.1  
            ball.sprite.speed_y = max(min(ball.sprite.speed_y, ball.sprite.max_speed_y), -ball.sprite.max_speed_y)

        if collide_masks(player2.sprite, ball.sprite):
            hit_sound.play()
            deltaY = ball.sprite.rect.centery-((player2.sprite.rect.top+player2.sprite.rect.bottom)/2)
            ball.sprite.speed_x = -abs(ball.sprite.speed_x)
            ball.sprite.speed_y += deltaY * 0.1
            ball.sprite.speed_y = max(min(ball.sprite.speed_y, ball.sprite.max_speed_y), -ball.sprite.max_speed_y)

        screen.blit(player1_score_text, player1_score_text_rect)
        screen.blit(player2_score_text, player2_score_text_rect)

        in_game = check_score()
        if not in_game:
            win_lose_screen = True
        
    
    elif in_customize:
        screen.fill((0, 0, 0))
        player1.sprite.drawAt(150, 150, screen)
        player2.sprite.drawAt(650, 150, screen)
        ball.sprite.drawAt(400, 150, screen)
        screen.blit(player1_color, player1_color_rect)
        screen.blit(ball_color, ball_color_rect)
        screen.blit(player2_color, player2_color_rect)
        screen.blit(player1_left, player1_left_rect)
        screen.blit(player1_right, player1_right_rect)
        screen.blit(ball_left, ball_left_rect)
        screen.blit(ball_right, ball_right_rect)
        screen.blit(player2_left, player2_left_rect)
        screen.blit(player2_right, player2_right_rect)
        
        
    elif start_screen: 
        screen.fill((0, 0, 0))
        screen.blit(game_title, game_title_rect)
        screen.blit(start_game, start_game_rect)
        screen.blit(customize, customize_rect)
    
    elif win_lose_screen:
        screen.fill((0, 0, 0))
        player1_score_text = test_font.render("WIN", True, (255, 255, 255))
        player2_score_text = test_font.render("LOSE", True, (255, 255, 255))
        
        if player2_score >= WIN_SCORE:
            player1_score_text = test_font.render("LOSE", True, (255, 255, 255))
            player2_score_text = test_font.render("WIN", True, (255, 255, 255))

        player1_score_text_rect = player1_score_text.get_rect(center=(200, 50))
        player2_score_text_rect = player2_score_text.get_rect(center=(600, 50))
        screen.blit(player1_score_text, player1_score_text_rect)
        screen.blit(player2_score_text, player2_score_text_rect)
        
        message1 = test_font.render("Click to play again", True, (255, 255, 255))
        message1_rect = message1.get_rect(center=(400, 300))
        message2 = test_font.render("Esc to menu", True, (255, 255, 255))
        message2_rect = message2.get_rect(center=(400, 350))
        screen.blit(message1, message1_rect)
        screen.blit(message2, message2_rect)
        
    pygame.display.update()
    clock.tick(FPS)