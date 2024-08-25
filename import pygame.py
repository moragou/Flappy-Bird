import pygame
import random

#inisialisasi
pygame.init()

#spesifikasi
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
PIPE_WIDTH = 70
PIPE_HEIGHT = 500
PIPE_GAP = 150
BIRD_GRAVITY = 0.5
BIRD_JUMP = -10
PIPE_SPEED = 5
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (135, 206, 250)
BLACK = (0, 0, 0)

#pembuatan layar display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

#gambar burung/kotak kuning
def draw_bird(bird_rect):
    pygame.draw.rect(screen, (255, 255, 0), bird_rect)

#menggambar pipa random
def draw_pipe(pipe_rect):
    pygame.draw.rect(screen, GREEN, pipe_rect)

#mengecek tabrakan (collide)
def check_collision(bird_rect, pipes):
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return True
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    return False

#Game over dan score
def show_game_over(score):
    font = pygame.font.Font(None, 74)
    game_over_surface = font.render('GAME OVER', True, GREEN)
    score_surface = font.render(f'SCORE: {score}', True, GREEN)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill(BLUE)
        screen.blit(game_over_surface, (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(score_surface, (SCREEN_WIDTH // 2 - score_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()
        pygame.time.wait(3000)  #tampilkan Game Over selama 3 detik

def game_loop():
    clock = pygame.time.Clock()
    bird_rect = pygame.Rect(50, SCREEN_HEIGHT // 2, BIRD_WIDTH, BIRD_HEIGHT)
    bird_velocity = 0
    pipes = []
    pipe_timer = 0
    score = 0
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = BIRD_JUMP

        #burung
        bird_velocity += BIRD_GRAVITY
        bird_rect.y += int(bird_velocity)

        #pipa
        pipe_timer += 1
        if pipe_timer > 90:
            pipe_timer = 0
            pipe_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
            pipes.append(pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, pipe_height))
            pipes.append(pygame.Rect(SCREEN_WIDTH, pipe_height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - pipe_height - PIPE_GAP))
            score += 1  # Tambahkan skor setiap kali pipa baru muncul

        #posisi pipa 
        pipes = [pipe.move(-PIPE_SPEED, 0) for pipe in pipes if pipe.right > 0]

        #collide check
        if check_collision(bird_rect, pipes):
            show_game_over(score)
            return

        #draw
        screen.fill(BLUE)
        draw_bird(bird_rect)
        for pipe in pipes:
            draw_pipe(pipe)
        score_surface = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surface, (10, 10))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    game_loop()
