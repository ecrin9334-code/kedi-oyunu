
import pygame
import random
import sys

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 105, 180)
DARK_PINK = (255, 20, 147)
LIGHT_PINK = (255, 182, 193)
BLUE = (80, 160, 255)
YELLOW = (255, 220, 80)

WIDTH = 600
HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kedi Oyunu - Python")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 35)
small_font = pygame.font.SysFont("Arial", 20)

class Cat:
  def __init__(self):
    self.reset()
  def reset(self):
    self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
    self.grow_to = 3
    self.score = 0
    self.body_color = PINK
    self.head_color = DARK_PINK
  def get_head_position(self):
    return self.positions[0]
  def turn(self, direction):
    if len(self.positions) > 1:
      opposite = (direction[0] * -1, direction[1] * -1)
      if opposite == self.direction:
        return
    self.direction = direction
  def move(self):
    head = self.get_head_position()
    x = self.direction[0]
    y = self.direction[1]
    new_x = (head[0] + x) % GRID_WIDTH
    new_y = (head[1] + y) % GRID_HEIGHT
    new_position = (new_x, new_y)
    if new_position in self.positions[1:]:
      return False
    self.positions.insert(0, new_position)
    if len(self.positions) > self.grow_to:
      self.positions.pop()
    return True
  def draw(self, surface):
    for i, position in enumerate(self.positions):
      x = position[0] * GRID_SIZE
      y = position[1] * GRID_SIZE
      rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
      if i == 0:
        self.draw_head(surface, rect)
      else:
        pygame.draw.circle(surface, self.body_color, rect.center, GRID_SIZE // 2 - 2)
  def draw_head(self, surface, rect):
    pygame.draw.circle(surface, self.head_color, rect.center, GRID_SIZE // 2 - 1)
    left_ear = [(rect.left + 4, rect.top + 10), (rect.left + 10, rect.top - 2), (rect.left + 16, rect.top + 10)]
    right_ear = [(rect.right - 4, rect.top + 10), (rect.right - 10, rect.top - 2), (rect.right - 16, rect.top + 10)]
    pygame.draw.polygon(surface, self.head_color, left_ear)
    pygame.draw.polygon(surface, self.head_color, right_ear)
    eye_y = rect.centery - 3
    pygame.draw.circle(surface, WHITE, (rect.centerx - 6, eye_y), 4)
    pygame.draw.circle(surface, WHITE, (rect.centerx + 6, eye_y), 4)
    pygame.draw.circle(surface, BLACK, (rect.centerx - 6, eye_y), 2)
    pygame.draw.circle(surface, BLACK, (rect.centerx + 6, eye_y), 2)
    pygame.draw.polygon(surface, LIGHT_PINK, [(rect.centerx, rect.centery + 3), (rect.centerx - 3, rect.centery), (rect.centerx + 3, rect.centery)])
    pygame.draw.line(surface, WHITE, (rect.centerx - 3, rect.centery + 5), (rect.left + 2, rect.centery + 2), 1)
    pygame.draw.line(surface, WHITE, (rect.centerx - 3, rect.centery + 7), (rect.left + 2, rect.centery + 8), 1)
    pygame.draw.line(surface, WHITE, (rect.centerx + 3, rect.centery + 5), (rect.right - 2, rect.centery + 2), 1)
    pygame.draw.line(surface, WHITE, (rect.centerx + 3, rect.centery + 7), (rect.right - 2, rect.centery + 8), 1)

class Fish:
  def __init__(self):
    self.position = (0, 0)
    self.randomize_position()
  def randomize_position(self):
    self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
  def draw(self, surface):
    x = self.position[0] * GRID_SIZE
    y = self.position[1] * GRID_SIZE
    pygame.draw.ellipse(surface, BLUE, (x + 5, y + 8, 20, 14))
    pygame.draw.polygon(surface, BLUE, [(x + 5, y + 15), (x - 2, y + 8), (x - 2, y + 22)])
    pygame.draw.circle(surface, WHITE, (x + 20, y + 13), 3)
    pygame.draw.circle(surface, BLACK, (x + 20, y + 13), 1)

def draw_grid(surface):
  for y in range(0, HEIGHT, GRID_SIZE):
    for x in range(0, WIDTH, GRID_SIZE):
      rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
      pygame.draw.rect(surface, BLACK, rect, 1)

def show_score(surface, score, high_score):
  score_text = small_font.render("Balık: " + str(score), True, WHITE)
  high_score_text = small_font.render("En Yüksek: " + str(high_score), True, YELLOW)
  surface.blit(score_text, (10, 10))
  surface.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))

def show_game_over(surface, score):
  surface.fill(BLACK)
  game_over_text = font.render("OYUN BİTTİ!", True, PINK)
  score_text = font.render("Balık: " + str(score), True, WHITE)
  restart_text = small_font.render("Yeniden başlamak için SPACE", True, WHITE)
  quit_text = small_font.render("Çıkmak için ESC", True, WHITE)
  surface.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 70))
  surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 20))
  surface.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 30))
  surface.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 60))
  pygame.display.update()

def main():
  cat = Cat()
  fish = Fish()
  high_score = 0
  game_over = False
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if game_over:
          if event.key == pygame.K_SPACE:
            cat.reset()
            fish.randomize_position()
            game_over = False
          elif event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        else:
          if event.key == pygame.K_UP:
            cat.turn((0, -1))
          elif event.key == pygame.K_DOWN:
            cat.turn((0, 1))
          elif event.key == pygame.K_LEFT:
            cat.turn((-1, 0))
          elif event.key == pygame.K_RIGHT:
            cat.turn((1, 0))
    if game_over == False:
      if cat.move() == False:
        game_over = True
        if cat.score > high_score:
          high_score = cat.score
      if cat.get_head_position() == fish.position:
        cat.grow_to = cat.grow_to + 1
        cat.score = cat.score + 10
        fish.randomize_position()
        while fish.position in cat.positions:
          fish.randomize_position()
      screen.fill(BLACK)
      draw_grid(screen)
      cat.draw(screen)
      fish.draw(screen)
      show_score(screen, cat.score, high_score)
    else:
      show_game_over(screen, cat.score)
    pygame.display.update()
    clock.tick(FPS)

if __name__ == "__main__":
  main()