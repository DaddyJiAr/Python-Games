import pygame
from random import randint, choice
import sys
from sys import exit
import os



def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Example usage in Pygame
image = pygame.image.load(resource_path("graphics/Player/player_walk_1.png"))





start_time = 0
score = 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load(resource_path("graphics/Player/player_walk_1.png")).convert_alpha()
        player_walk2 = pygame.image.load(resource_path("graphics/Player/player_walk_2.png")).convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load(resource_path("graphics/Player/jump.png")).convert_alpha()
        
        self.image = self.player_walk[int(self.player_index)]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound(resource_path("audio/jump.mp3"))
        self.jump_sound.set_volume(0.05)  # Set volume to 50% kasi maingay
    
    
    def user_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity -= 20
            self.jump_sound.play()
        
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update(self):
        self.user_input()
        self.apply_gravity()
        self.animation_state()
        
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
            
        else:
            self.gravity = 0 # kasi walang reset
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'snail':
            snail_frame1 = pygame.image.load(resource_path("graphics/snail/snail1.png")).convert_alpha()
            snail_frame2 = pygame.image.load(resource_path("graphics/snail/snail2.png")).convert_alpha()
            self.frames = [snail_frame1, snail_frame2]
            # self.animation_timer = pygame.USEREVENT + 1
            # pygame.time.set_timer(self.animation_timer, 350)
            y_pos = 300
        elif type == 'fly':
            fly_frame1 = pygame.image.load(resource_path("graphics/Fly/Fly1.png")).convert_alpha()
            fly_frame2 = pygame.image.load(resource_path("graphics/Fly/Fly2.png")).convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos = randint(120, 200)
            
        self.type = type
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))
        
    def animation_state(self):
        # for event in pygame.event.get():
        #     if event == self.animation_timer:
        #         if self.animation_index == 0:
        #             self.animation_index = 1
        #         else:
        #             self.animation_index = 0
        # gawa ko nung una pero ginaya nya nalang yung kay player
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
        
    def destroy(self):
        if self.rect.right <= -10:
            self.kill()
            
            
def get_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    
    score_surface = test_font.render(f"Your Score: {current_time}", False, (64,64,64)) #True if not pixelated
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return current_time
    
# def obstacle_move(obstacle_list):
#     if obstacle_list:
#         for obstacle_rect in obstacle_list:
#             obstacle_rect.x -= 5
#             if obstacle_rect.bottom == 300:
#                 screen.blit(snail_surface, obstacle_rect)
#             else:
#                 screen.blit(fly_surface, obstacle_rect)
#             # if obstacle_rect.right <= 0:
#             #     obstacle_list.remove(obstacle_rect)
#         obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.right > 10]
#         return obstacle_list
    
#     else:
#         return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.groupcollide(player, obstacle_group, False, False):
        obstacle_group.empty()
        return False # collision
    return True

# def player_animation():
#     global player_index, player_surface
#     if player_rect.bottom < 300:
#         player_surface = player_jump
#     else:
#         player_index += 0.1
        
#         if player_index >= len(player_walk): #reset index
#             player_index = 0
#         player_surface = player_walk[int(player_index)]
        



pygame.init()



screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Game ni DaddyJiAr")
FPS = 60
clock = pygame.time.Clock()


player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()




test_font = pygame.font.Font(resource_path("font/Pixeltype.ttf"), 50)

run = True

sky_surface = pygame.image.load(resource_path("graphics/Sky.png")).convert()  # Convert for faster blitting
ground_surface = pygame.image.load(resource_path("graphics/Ground.png")).convert()
bg_music = pygame.mixer.Sound(resource_path("audio/music.wav"))
bg_music.set_volume(0.05)
bg_music.play(loops = -1) # infinite


# snail_frame1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
# snail_frame2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
# snail_frame = [snail_frame1, snail_frame2]
# snail_index = 0
# snail_surface = snail_frame[snail_index]

# fly_frame1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
# fly_frame2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
# fly_frame = [fly_frame1, fly_frame2]
# fly_index = 0
# fly_surface = fly_frame[fly_index]

# obstacle_rect_list = []

# player_walk1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
# player_walk2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
# player_walk = [player_walk1, player_walk2]
# player_index = 0
# player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

# player_surface = player_walk[player_index]
# player_rect = player_surface.get_rect(midbottom=(80, 300))
# player_gravity = 0


# intro screen
player_stand = pygame.image.load(resource_path("graphics/Player/player_stand.png")).convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2) # surface, angle, scale
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render("Talon ka lang", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render("Press Enter to start", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 330))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# snail_animation_timer = pygame.USEREVENT + 2
# pygame.time.set_timer(snail_animation_timer, 350)

# fly_animation_timer = pygame.USEREVENT + 3
# pygame.time.set_timer(fly_animation_timer, 100)

in_game = False

while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            exit()
        # if event.type == pygame.MOUSEBUTTONDOWN :
        #     if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300 and in_game:
        #         player_gravity = -20
        
        if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE and player_rect.bottom >= 300 and in_game:
        #         player_gravity = -20
        #     if event.key == pygame.K_ESCAPE:
        #         run = False
        #         pygame.quit()
        #         exit()
            if (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN) and not in_game:
                start_time = pygame.time.get_ticks() # Reset the timer
                in_game = True
                
        if event.type == obstacle_timer and in_game:
            obstacle_group.add(Obstacle(choice(["fly","snail","snail","snail","snail"])))    # obstacle_rect_list.append(fly_surface.get_rect(midbottom=(randint(900, 1100), randint(120, 200))))
        
        # if event.type == snail_animation_timer and in_game:
        #     if snail_index == 0:
        #         snail_index = 1
        #     else:
        #         snail_index = 0.
        #     snail_surface = snail_frame[int(snail_index)]
        # if event.type == fly_animation_timer and in_game:
        #     if fly_index == 0:
        #         fly_index = 1
        #     else:
        #         fly_index = 0.
        #     fly_surface = fly_frame[int(fly_index)]
                
        
    if in_game:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        
        
        
        
        
        
            
            
            
        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 300:
        #     player_rect.bottom = 300
        # player_animation()
        # screen.blit(player_surface, player_rect)
        # player_rect.left += 3
        
        # if player_rect.colliderect(snail_rect):
        #     print("Game Over")
        
        # mouse_pos = pygame.mouse.get_pos()
        # mouse_pos = pygame.mouse.get_pressed ()
        
        
        
        # obstacle_rect_list = obstacle_move(obstacle_rect_list)    
        
        
        in_game = collision_sprite()
        score = get_score()
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        
        if score > 0:
            game_name = test_font.render(f"Your score: {score}", False, (111, 196, 169))
            game_name_rect = game_name.get_rect(center=(400, 80))
            
        screen.blit(game_name, game_name_rect)
        screen.blit(game_message, game_message_rect)
        
    
    pygame.display.update()
    clock.tick(FPS)

