import pygame
from .paddle import Paddle
from .ball import Ball
from .brick import Brick

# Game Engine

WHITE  = (255, 255, 255)
YELLOW = (255, 220, 50)
BG     = (15, 15, 25)
BRICK_COLORS = [
    (200, 60, 60),
    (200, 140, 60),
    (200, 200, 60),
    (80, 180, 80),
    (80, 140, 200),
]

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.paddle = Paddle(width // 2 - 50, height - 30, 100, 14)

        self.ball = Ball(width // 2, height - 50, radius=8)
        self.ball.vx, self.ball.vy = 4, -4

        self.rows, self.cols = 5, 8
        self.bricks = self._build_bricks(self.rows, self.cols)

        self.lives = 3
        self.score = 0
        self.font      = pygame.font.SysFont("Arial", 28)
        self.big_font  = pygame.font.SysFont("Arial", 56, bold=True)
        self.game_over = False
        self.result    = None  # "win" or "lose"

    def _build_bricks(self, rows, cols):
        bricks = []
        margin, gap, top = 30, 6, 60
        brick_w = (self.width - margin * 2 - gap * (cols - 1)) // cols
        brick_h = 22
        for r in range(rows):
            for c in range(cols):
                x = margin + c * (brick_w + gap)
                y = top + r * (brick_h + gap)
                bricks.append(Brick(x, y, brick_w, brick_h))
        return bricks

    def handle_event(self, event):
        # Task 2: press R to restart after game-over
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self._restart()

    def handle_input(self):
        if self.game_over:
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.paddle.move(-self.paddle.speed, self.width)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.paddle.move(self.paddle.speed, self.width)

    def update(self):
        if self.game_over:
            return

        self.ball.move()

        if self.ball.x - self.ball.radius <= 0 or self.ball.x + self.ball.radius >= self.width:
            self.ball.vx *= -1
        if self.ball.y - self.ball.radius <= 0:
            self.ball.vy *= -1

        if self.ball.rect().colliderect(self.paddle.rect()):
            self._resolve_collision(self.paddle.rect())

        for brick in self.bricks:
            if brick.alive and self.ball.rect().colliderect(brick.rect()):
                brick.alive = False
                self.score += 1
                self._resolve_collision(brick.rect())
                break

        if self.ball.y - self.ball.radius > self.height:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
                self.result = "lose"
            else:
                self._reset_ball()

        if all(not b.alive for b in self.bricks):
            self.game_over = True
            self.result = "win"

    def _resolve_collision(self, rect):
        """Determine which side of *rect* the ball hit and flip the
        appropriate velocity component.

        Strategy: compute how far the ball centre has penetrated the
        rectangle along each axis.  Whichever axis has the *smaller*
        overlap is the one the ball entered from, so that is the axis
        whose velocity we flip.  This correctly handles side-hits
        (left/right → flip vx) vs. top/bottom hits (flip vy).
        """
        ball_rect = self.ball.rect()

        # Penetration depths along each axis
        overlap_x = min(ball_rect.right, rect.right) - max(ball_rect.left, rect.left)
        overlap_y = min(ball_rect.bottom, rect.bottom) - max(ball_rect.top, rect.top)

        if overlap_x < overlap_y:
            # Ball entered from the left or right side
            self.ball.vx *= -1
        else:
            # Ball entered from the top or bottom
            self.ball.vy *= -1

    def _reset_ball(self):
        self.ball.x, self.ball.y = self.width // 2, self.height - 50
        self.ball.vx, self.ball.vy = 4, -4

    def _restart(self):
        """Task 2: full game restart."""
        self.bricks    = self._build_bricks(self.rows, self.cols)
        self.lives     = 3
        self.score     = 0
        self.game_over = False
        self.result    = None
        self._reset_ball()

    def render(self, screen):
        screen.fill(BG)

        pygame.draw.rect(screen, WHITE, self.paddle.rect())
        pygame.draw.circle(screen, WHITE, (int(self.ball.x), int(self.ball.y)), self.ball.radius)

        for i, brick in enumerate(self.bricks):
            if brick.alive:
                row = i // self.cols
                color = BRICK_COLORS[row % len(BRICK_COLORS)]
                pygame.draw.rect(screen, color, brick.rect())

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        screen.blit(lives_text, (self.width - 130, 10))

        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            if self.result == "win":
                msg   = "YOU WIN!"
                color = YELLOW
            else:
                msg   = "GAME OVER"
                color = (220, 60, 60)

            title = self.big_font.render(msg, True, color)
            screen.blit(title, (self.width // 2 - title.get_width() // 2,
                                self.height // 2 - 60))

            score_msg = self.font.render(f"Final Score: {self.score}", True, WHITE)
            screen.blit(score_msg, (self.width // 2 - score_msg.get_width() // 2,
                                    self.height // 2 + 10))

            restart_msg = self.font.render("Press R to Restart", True, WHITE)
            screen.blit(restart_msg, (self.width // 2 - restart_msg.get_width() // 2,
                                      self.height // 2 + 55))
