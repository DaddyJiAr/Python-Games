import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Laro ko")

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_SPEED = 10

# Spatial partitioning cell size
CELL_SIZE = 200

window = pygame.display.set_mode((WIDTH, HEIGHT))

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_spritesheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path,f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        sprites = []
        for i in range (sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0,0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size,size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96,0,size,size)
    surface.blit(image,(0,0), rect)
    return pygame.transform.scale2x(surface)


class SpatialHash:
    """Spatial partitioning system for efficient collision detection"""
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.grid = {}
    
    def clear(self):
        self.grid.clear()
    
    def _get_cell_key(self, x, y):
        return (int(x // self.cell_size), int(y // self.cell_size))
    
    def _get_cells_for_rect(self, rect):
        """Get all cells that a rectangle overlaps"""
        min_x, min_y = self._get_cell_key(rect.left, rect.top)
        max_x, max_y = self._get_cell_key(rect.right - 1, rect.bottom - 1)
        
        cells = []
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                cells.append((x, y))
        return cells
    
    def insert(self, obj):
        """Insert an object into the spatial hash"""
        cells = self._get_cells_for_rect(obj.rect)
        for cell in cells:
            if cell not in self.grid:
                self.grid[cell] = []
            self.grid[cell].append(obj)
    
    def get_nearby_objects(self, rect):
        """Get all objects that could potentially collide with the given rect"""
        nearby = set()
        cells = self._get_cells_for_rect(rect)
        
        for cell in cells:
            if cell in self.grid:
                nearby.update(self.grid[cell])
        
        return list(nearby)


class Player(pygame.sprite.Sprite):
    COLOR = (255,0,0)
    GRAVITY = 1
    SPRITES = load_spritesheets("MainCharacters", "NinjaFrog", 32, 32, True)
    ANIMATION_DELAY = 3
    
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.last_sprite_sheet = None
        self.invulnerable = False  # Add invulnerability period after being hit

    def jump(self):
        self.y_vel = -self.GRAVITY * 10
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        if not self.invulnerable:  # Only allow hit if not invulnerable
            self.hit = True
            self.hit_count = 0
            self.invulnerable = True
            self.bounce()
    
    def bounce(self):
        """Upward-only bounce effect when hitting an obstacle"""
        # Only upward bounce, no horizontal movement
        self.y_vel = -self.GRAVITY * 5  # Strong upward bounce only
        self.x_vel = 0  # Stop horizontal movement

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, self.fall_count / (fps * self.GRAVITY))
        self.move(self.x_vel, self.y_vel)

        # Handle hit state
        if self.hit:
            self.hit_count += 1
            # End hit state after 0.5 seconds
            if self.hit_count > fps * 0.5:
                self.hit = False
                self.hit_count = 0
        
        # Handle invulnerability period - separate counter
        if self.invulnerable:
            # Use a separate counter for invulnerability
            if hasattr(self, 'invulnerable_count'):
                self.invulnerable_count += 1
            else:
                self.invulnerable_count = 0
            
            # End invulnerability after 1.5 seconds
            if self.invulnerable_count > fps * 1.5:
                self.invulnerable = False
                self.invulnerable_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        
        # Don't reverse velocity, just stop upward movement and start falling
        if self.y_vel < 0:
            self.y_vel = 0

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        
        # Only update sprite if it changed
        if sprite_sheet_name != self.last_sprite_sheet:
            self.last_sprite_sheet = sprite_sheet_name
            self.animation_count = 0
        
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        # Add visual feedback during invulnerability (flashing effect)
        if self.invulnerable and hasattr(self, 'invulnerable_count') and (self.invulnerable_count // 10) % 2:
            # Create a slightly transparent version for flashing effect
            temp_surface = self.sprite.copy()
            temp_surface.set_alpha(128)
            win.blit(temp_surface, (self.rect.x - offset_x, self.rect.y))
        else:
            win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0,0))
        self.mask = pygame.mask.from_surface(self.image)


class Fire(Object):
    ANIMATION_DELAY = 3
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_spritesheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"
        
    def off(self):
        self.animation_name = "off"
        
    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0
        


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    # Only draw objects that are visible on screen
    screen_rect = pygame.Rect(offset_x - 100, -100, WIDTH + 200, HEIGHT + 200)
    
    for obj in objects:
        if obj.rect.colliderect(screen_rect):
            obj.draw(window, offset_x)

    player.draw(window, offset_x)
    pygame.display.update()


def handle_vertical_collision(player, nearby_objects, dy):
    """Optimized vertical collision using spatial partitioning"""
    collided_objects = []
    
    player.move(0, dy)
    player.update()
    for obj in nearby_objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:  # Falling down; landed on top of object
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:  # Moving up; hit head
                player.rect.top = obj.rect.bottom
                player.hit_head()
            collided_objects.append(obj)
    player.move(0, -dy)
    player.update()
    
    return collided_objects


def collide(player, nearby_objects, dx):
    """Optimized collision check using spatial partitioning"""
    player.move(dx, 0)
    player.update()
    collided_object = None
    
    for obj in nearby_objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, spatial_hash):
    """Optimized movement handling with spatial partitioning"""
    keys = pygame.key.get_pressed()
    
    # Get nearby objects for all collision checking
    check_rect = pygame.Rect(
        player.rect.x - PLAYER_SPEED - 50,
        player.rect.y - 50,
        player.rect.width + 2 * PLAYER_SPEED + 100,
        player.rect.height + abs(player.y_vel) + 100
    )
    nearby_objects = spatial_hash.get_nearby_objects(check_rect)
    
    # Handle player movement (normal control, no special hit state movement)
    player.x_vel = 0
    
    collide_left = collide(player, nearby_objects, -PLAYER_SPEED)
    collide_right = collide(player, nearby_objects, PLAYER_SPEED)
    
    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_SPEED)

    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_SPEED)
    
    # Handle vertical collisions (now includes fire for platform collision)
    vertical_collide = handle_vertical_collision(player, nearby_objects, player.y_vel)
    
    # Check for fire collision damage (separate from platform collision)
    for obj in nearby_objects:
        if obj.name == "fire":
            # Use rect collision for damage detection
            if player.rect.colliderect(obj.rect):
                if not player.hit and not player.invulnerable:
                    player.make_hit()


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Pink.png")

    BLOCK_SIZE = 96

    player = Player(100, 100, 50, 50)
    fire = Fire(300, HEIGHT - BLOCK_SIZE - 64, 16, 32)  # Moved fire for easier testing
    fire.on()
    
    # Add more fire traps for testing
    fire2 = Fire(500, HEIGHT - BLOCK_SIZE - 64, 16, 32)
    fire2.on()
    
    floor = [Block(i * BLOCK_SIZE, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
             for i in range(-WIDTH // BLOCK_SIZE, (WIDTH * 2) // BLOCK_SIZE)]
    
    left_wall = [Block(0, i * BLOCK_SIZE, BLOCK_SIZE) 
                 for i in range(-HEIGHT // BLOCK_SIZE, HEIGHT // BLOCK_SIZE)]

    objects = [*floor, Block(BLOCK_SIZE * 3, HEIGHT - BLOCK_SIZE * 4, BLOCK_SIZE), *left_wall, fire, fire2]
    
    # Initialize spatial hash
    spatial_hash = SpatialHash(CELL_SIZE)

    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        # Rebuild spatial hash each frame
        spatial_hash.clear()
        for obj in objects:
            spatial_hash.insert(obj)

        player.loop(FPS)
        fire.loop()
        fire2.loop()
        handle_move(player, spatial_hash)
        draw(window, background, bg_image, player, objects, offset_x)

        # Camera scrolling
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width and player.x_vel > 0) or 
            (player.rect.left - offset_x <= scroll_area_width and player.x_vel < 0)):
            offset_x += player.x_vel

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)