import pygame
import random
import math

# --- CONFIGURATION ---
WIDTH, HEIGHT = 1024, 768
FPS = 60
COLORS = {
    "WHITE": (255, 255, 255),
    "ORANGE_GOLD": (255, 215, 0), # Trelvyn
    "BLACK": (20, 20, 20),        # Isis/Tuxedos
    "FLOOR": (245, 245, 220),
    "RED": (255, 50, 50)
}

# --- SETUP ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trelvyn's Feast")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# --- CLASSES ---

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Placeholder for customizable sprite
        self.image = pygame.Surface((32, 32))
        self.image.fill((0, 100, 255)) 
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 4
        self.has_opener = False
        self.has_food = False
        self.facing = pygame.math.Vector2(0, 1) # Facing down

    def update(self, keys):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]: dx = -1
        if keys[pygame.K_RIGHT]: dx = 1
        if keys[pygame.K_UP]: dy = -1
        if keys[pygame.K_DOWN]: dy = 1
        
        if dx != 0 or dy != 0:
            move = pygame.math.Vector2(dx, dy)
            move.normalize_ip()
            self.rect.x += move.x * self.speed
            self.rect.y += move.y * self.speed
            self.facing = move # Update facing direction for Rorschach logic

class Cat(pygame.sprite.Sprite):
    def __init__(self, name, color, x, y, cat_type="Standard"):
        super().__init__()
        self.name = name
        self.image = pygame.Surface((40, 40)) if name == "Trelvyn" else pygame.Surface((28, 28))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.type = cat_type
        self.state = "SLEEP" if name == "Trelvyn" else "WANDER"
        self.speed = 2

    def update(self, player, bowl_pos, food_ready):
        # TRELVYN LOGIC
        if self.name == "Trelvyn":
            if not food_ready:
                self.state = "SLEEP"
                # He just sleeps
            else:
                self.state = "EAT"
                # Move to bowl
                dir_vector = pygame.math.Vector2(bowl_pos[0] - self.rect.centerx, bowl_pos[1] - self.rect.centery)
                if dir_vector.length() > 5:
                    dir_vector.normalize_ip()
                    self.rect.centerx += dir_vector.x * self.speed
                    self.rect.centery += dir_vector.y * self.speed
                else:
                    # After eating, rub against player (Win Condition Logic)
                    pass

        # RORSCHACH LOGIC
        elif self.name == "Rorschach":
            # Check angle between player facing vector and vector to cat
            to_cat = pygame.math.Vector2(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)
            angle = player.facing.angle_to(to_cat)
            
            # If player is looking away (angle > 90 or < -90) AND close enough
            if (abs(angle) > 90) and to_cat.length() < 300:
                # JUMP!
                to_player = -to_cat
                if to_player.length() > 0:
                    to_player.normalize_ip()
                    self.rect.centerx += to_player.x * (self.speed * 2.5) # Fast!
                    self.rect.centery += to_player.y * (self.speed * 2.5)
        
        # STANDARD CAT LOGIC (Wander)
        else:
            if random.randint(0, 50) == 0:
                self.rect.x += random.choice([-5, 5])
                self.rect.y += random.choice([-5, 5])

# --- GAME MANAGER ---

class GameManager:
    def __init__(self):
        self.level = 1
        self.reset_level()

    def reset_level(self):
        self.player = Player(100, 100)
        self.cats = pygame.sprite.Group()
        self.items = [] # Store rects for Opener, Can, Bowl
        
        # Determine Theme (Placeholder for 1000s of themes)
        themes = ["60s Mod", "Edo Castle", "Sci-Fi", "Pacific Northwest"]
        self.current_theme = random.choice(themes)
        
        # Always add Trelvyn
        self.trelvyn = Cat("Trelvyn", COLORS["ORANGE_GOLD"], WIDTH//2, HEIGHT//2, "BOSS")
        self.cats.add(self.trelvyn)

        # Add Isis (Level 2+)
        if self.level >= 2:
            self.cats.add(Cat("Isis", COLORS["BLACK"], random.randint(200,800), random.randint(200,600)))

        # Add Twins (Level 3+)
        if self.level >= 3:
            self.cats.add(Cat("Rorschach", (50, 50, 50), random.randint(200,800), random.randint(200,600)))
            self.cats.add(Cat("Enkidu", (50, 50, 50), random.randint(200,800), random.randint(200,600)))

        # Add Random Cats (Level 4+ -> +1 per level)
        if self.level >= 4:
            extra_cats = self.level - 3
            for i in range(extra_cats):
                self.cats.add(Cat(f"Cat_{i}", (random.randint(0,255), random.randint(0,255), random.randint(0,255)), random.randint(200,800), random.randint(200,600)))

        # Place Items
        self.opener_rect = pygame.Rect(random.randint(50, 900), random.randint(50, 700), 20, 20)
        self.food_rect = pygame.Rect(random.randint(50, 900), random.randint(50, 700), 20, 20)
        self.bowl_rect = pygame.Rect(random.randint(50, 900), random.randint(50, 700), 30, 30)
        
        self.food_in_bowl = False

    def run(self):
        running = True
        while running:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Updates
            self.player.update(keys)
            self.cats.update(self.player, self.bowl_rect.center, self.food_in_bowl)

            # Item Interactions
            player_rect = self.player.rect
            if player_rect.colliderect(self.opener_rect):
                self.player.has_opener = True
                self.opener_rect.x = -100 # Hide it
            
            if player_rect.colliderect(self.food_rect) and self.player.has_opener:
                self.player.has_food = True
                self.food_rect.x = -100 # Hide it

            if player_rect.colliderect(self.bowl_rect) and self.player.has_food:
                self.food_in_bowl = True

            # Collision with Cats (Loss Condition)
            # (In Level 1, Trelvyn doesn't hurt you if he's happy)
            for cat in self.cats:
                if cat.rect.colliderect(player_rect):
                    if cat.name == "Trelvyn" and self.food_in_bowl:
                        # WIN LEVEL
                        self.level += 1
                        print(f"Level {self.level} Start!")
                        self.reset_level()
                        pygame.time.delay(1000)
                    elif cat.name == "Trelvyn" and not self.food_in_bowl:
                        # In level 1, sleeping Trelvyn is safe? Or obstacle?
                        pass 
                    else:
                        print("GAME OVER - Touched a cat!")
                        running = False

            # Drawing
            screen.fill(COLORS["FLOOR"])
            
            # Draw Items
            if not self.player.has_opener: pygame.draw.rect(screen, (100, 100, 100), self.opener_rect) # Opener
            if not self.player.has_food: pygame.draw.rect(screen, (0, 100, 0), self.food_rect)     # Food Can
            color_bowl = (255, 0, 0) if not self.food_in_bowl else (0, 255, 0)
            pygame.draw.rect(screen, color_bowl, self.bowl_rect) # Bowl

            # Draw Sprites
            screen.blit(self.player.image, self.player.rect)
            self.cats.draw(screen)
            
            # UI
            ui_text = f"Level: {self.level} | Theme: {self.current_theme}"
            screen.blit(font.render(ui_text, True, (0,0,0)), (10, 10))
            
            items_text = f"Opener: {self.player.has_opener} | Food: {self.player.has_food}"
            screen.blit(font.render(items_text, True, (0,0,0)), (10, 30))

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = GameManager()
    game.run()