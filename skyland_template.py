import pygame
from random import randint

# Game Constants
WIDTH, HEIGHT = 600, 400
CLOCK_RATE = 30
START_X, START_Y = 20, 350
END_X, END_Y = 400, 350
OBSTACLE_WIDTH = 50
OBSTACLE_GAP = 150
OBSTACLE_SPEED = 5
SCORE_INCREMENT = 10
MAX_LIVES = 3

# Colors
WHITE = (255, 255, 255)
LIGHTBLUE = (173, 216, 230)
LIMEGREEN = (50, 205, 50)
RED = (255, 0, 0)
ORCHID = (218, 112, 214)
SANDYBROWN = (244, 164, 96)
LIME = (0, 255, 0)

class Skyland:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Skyland Game")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Helvetica", 20, bold=True)
        self.high_score = 0
        self.settings = {
            "difficulty": "Easy",
            "sound": True
        }
        self.lives = MAX_LIVES
        self.paused = False

    def start(self):
        self.avatar = Avatar(self.screen, self)
        self.land = Land(self.screen)
        self.trophy = Trophy(self.screen)
        self.enemy = Enemy(self.screen, self.avatar)
        self.score = 0
        self.running = True

        while self.running:
            self.clock.tick(CLOCK_RATE)
            self.handle_events()
            if not self.paused:
                self.update()
            self.draw()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pause()
                elif event.key == pygame.K_r:
                    self.restart()
                elif event.key == pygame.K_UP:
                    self.avatar.move_up()
                elif event.key == pygame.K_DOWN:
                    self.avatar.move_down()

    def update(self):
     self.avatar.update(self.land, self.trophy, self.enemy)
     self.enemy.update()
     self.trophy.update()
     self.trophy.create_trophy()  # Create new trophy
     self.score += 1


    def draw(self):
        self.screen.fill(LIGHTBLUE)
        self.land.draw_clouds()
        self.land.draw_land()
        self.trophy.draw()
        self.enemy.draw()
        self.avatar.draw()

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))

        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_text, (20, 50))

        if self.paused:
            pause_text = self.font.render("Paused", True, WHITE)
            self.screen.blit(pause_text, (WIDTH / 2 - 30, HEIGHT / 2))

        pygame.display.flip()

    def restart(self):
     self.avatar.reset()
     self.trophy.reset()
     self.enemy.reset()
     self.score = 0
     self.lives = MAX_LIVES  # Reset lives to MAX_LIVES


    def pause(self):
        self.paused = not self.paused

    def game_over(self):
     if self.score > self.high_score:
        self.high_score = self.score

     self.screen.fill(LIGHTBLUE)
     game_over_text = self.font.render("Game Over", True, WHITE)
     score_text = self.font.render(f"Score: {self.score}", True, WHITE)
     lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)  # Added line
     high_score_text = self.font.render(f"High Score: {self.high_score}", True, WHITE)
     self.screen.blit(game_over_text, (WIDTH / 2 - 60, HEIGHT / 2 - 50))
     self.screen.blit(score_text, (WIDTH / 2 - 50, HEIGHT / 2))
     self.screen.blit(lives_text, (WIDTH / 2 - 50, HEIGHT / 2 + 25))  # Added line
     self.screen.blit(high_score_text, (WIDTH / 2 - 70, HEIGHT / 2 + 50))
     pygame.display.flip()
     pygame.time.wait(3000)
     self.restart()

class Land:
    def __init__(self, screen):
        self.screen = screen
        self.clouds = []
        self.make_cloud(50, 50)
        self.make_cloud(250, 100)
        self.make_cloud(450, 80)
        self.make_cloud(150, 200)
        self.make_cloud(350, 150)

    def make_cloud(self, x, y):
        cloud = pygame.Rect(x, y, 60, 30)
        self.clouds.append(cloud)

    def draw_clouds(self):
        for cloud in self.clouds:
            pygame.draw.ellipse(self.screen, WHITE, cloud)

    def draw_land(self):
        pygame.draw.rect(self.screen, SANDYBROWN, (0, START_Y - 100, WIDTH, 100))
        pygame.draw.rect(self.screen, LIMEGREEN, (0, START_Y - 120, WIDTH, START_Y))

class Trophy:
    def __init__(self, screen):
        self.screen = screen
        self.trophies = []
        self.score = 0
        self.delay = 0

    def create_trophy(self):
        if self.delay == 0:  # Check if delay time has elapsed
            x = randint(0, WIDTH - 20)
            y = randint(0, START_Y - 10)
            trophy = pygame.Rect(x, y, 20, 10)
            self.trophies.append(trophy)
            self.delay = 50  # Set the delay time to 50 frames (adjust as needed)

    def draw(self):
        for trophy in self.trophies:
            pygame.draw.ellipse(self.screen, WHITE, trophy)

    def reset(self):
        self.trophies = []
        self.score = 0

    def increase_score(self):
        self.score += SCORE_INCREMENT

    def update(self):
        for trophy in self.trophies:
            trophy.x -= OBSTACLE_SPEED

        if self.delay > 0:
            self.delay -= 1


class Enemy:
    def __init__(self, screen, avatar):
        self.screen = screen
        self.avatar = avatar
        self.obstacles = []
        self.create_obstacle()

    def create_obstacle(self):
        top_height = randint(50, 250)
        bottom_height = HEIGHT - OBSTACLE_GAP - top_height
        top_obstacle = pygame.Rect(WIDTH, 0, OBSTACLE_WIDTH, top_height)
        bottom_obstacle = pygame.Rect(WIDTH, HEIGHT - bottom_height, OBSTACLE_WIDTH, bottom_height)
        self.obstacles.append((top_obstacle, bottom_obstacle))

    def draw(self):
        for pair in self.obstacles:
            pygame.draw.rect(self.screen, RED, pair[0])
            pygame.draw.rect(self.screen, RED, pair[1])

    def reset(self):
        self.obstacles = []

    def update(self):
        for pair in self.obstacles:
            pair[0].x -= OBSTACLE_SPEED
            pair[1].x -= OBSTACLE_SPEED
            if pair[0].right < 0:
                self.obstacles.remove(pair)
                self.create_obstacle()

class Avatar:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.head = pygame.Rect(0, 0, 10, 10)
        self.torso = pygame.Rect(0, 10, 10, 20)
        self.legs = pygame.Rect(0, 30, 10, 10)
        self.reset()

    def reset(self):
        self.head.topleft = (START_X, START_Y)
        self.torso.topleft = (START_X - 5, START_Y + 10)
        self.legs.topleft = (START_X, START_Y + 30)

    def move_up(self):
        self.head.y -= 10
        self.torso.y -= 10
        self.legs.y -= 10

    def move_down(self):
        self.head.y += 10
        self.torso.y += 10
        self.legs.y += 10

    def draw(self):
        pygame.draw.rect(self.screen, LIME, self.head)
        pygame.draw.rect(self.screen, LIME, self.torso)
        pygame.draw.rect(self.screen, LIME, self.legs)

    def update(self, land, trophy, enemy):
     if self.head.top <= 0 or self.legs.bottom >= HEIGHT or self.check_collision(enemy.obstacles):
        self.game.lives -= 1
        if self.game.lives == 0:
            self.game.game_over()
        else:
            self.reset()

     if self.check_collision(land.clouds):
        self.reset()

     collided_trophies = [trophy for trophy in trophy.trophies if self.check_collision(trophy)]
     for collided_trophy in collided_trophies:
         trophy.trophies.remove(collided_trophy)
         trophy.increase_score()
         self.game.lives += 1


    def check_collision(self, rects):
     for rect in rects:
        if isinstance(rect, pygame.Rect):
            if self.head.colliderect(rect) or self.torso.colliderect(rect) or self.legs.colliderect(rect):
                return True
        elif isinstance(rect, tuple):
            top_rect, bottom_rect = rect
            if (self.head.colliderect(top_rect) or self.torso.colliderect(top_rect) or self.legs.colliderect(top_rect) or
                self.head.colliderect(bottom_rect) or self.torso.colliderect(bottom_rect) or self.legs.colliderect(bottom_rect)):
                return True
     return False


game = Skyland()
game.start()
