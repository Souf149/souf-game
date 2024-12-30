from souf_game.clients.repos.db_client import DbClient
import pygame
import random


class Player:
    def __init__(self, name: str, color: tuple, x: int, y: int):
        self.name = name
        self.color = color
        self.size = 50
        self.x = x
        self.y = y
        self.timer = 0
        self.lifetime = 0
        self.walko = False
        self.walkw = False
        self.stil = False

    def update(self, screen_width: int, screen_height: int) -> None:
        self.lifetime += 1
        self.timer += 1

        if self.timer >= random.randint(100, 200):
            r = random.randint(1, 3)
            if r == 1 and not self.x >= screen_width * 0.8:
                self.walko = True
            else:
                self.walko = False
            if r == 2 and not self.x <= screen_width * 0.1:
                self.walkw = True
            else:
                self.walkw = False
            if r == 3:
                self.stil = True
            else:
                self.stil = False

            self.timer = 0

        x = screen_height - self.size
        if self.y != x:
            self.y += 1

        if self.y == screen_height - self.size:
            if self.walko:
                self.x += 1

            if self.walkw:
                self.x -= 1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))


class Game:
    players: list[Player]

    def __init__(self):
        self.db_client = DbClient()

        self.WIDTH = 1500
        self.HEIGHT = 300
        self.FPS = 60
        self.COLORS = [
            (255, 84, 0, 255),
            (0, 255, 12, 255),
            (255, 246, 0, 255),
            (0, 255, 187, 255),
            (0, 255, 246, 255),
            (0, 33, 255, 255),
            (0, 255, 178, 255),
            (144, 255, 0, 255),
            (255, 136, 0, 255),
        ]

        self.players = []

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("inkfree", 30, italic=True, bold=True)
        self.font.set_underline(True)

        self.frame_count = 0

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self._chat_message("Aashir")

            self.screen.fill((202, 42, 202, 255))

            if self.frame_count % 60 == 0:
                self._update_players()

            for i, player in enumerate(self.players):
                text = self.font.render(player.name, True, (255, 255, 255))
                textrect = text.get_rect()
                textrect.center = (player.x + 10, player.y - 25)
                self.screen.blit(text, textrect)

                if player.lifetime >= 200:  # 18000
                    self.players.pop(i)

                player.update(self.WIDTH, self.HEIGHT)
                player.draw(self.screen)

            pygame.display.flip()
            self.frame_count += 1
            self.clock.tick(self.FPS)

    def _chat_message(self, player_name: str) -> None:
        print("Message from: " + player_name)
        potential_players = [x for x in self.players if x.name == player_name]

        if len(potential_players) == 0:
            self.players.append(
                Player(
                    player_name,
                    self._get_random_hsv(),
                    random.randint(self.WIDTH * 0.1, self.WIDTH * 0.9),
                    self.HEIGHT // 2,
                )
            )
        else:
            potential_players[0].lifetime = 0

    def _get_random_hsv(self) -> tuple[int, int, int, int]:
        return random.choice(self.COLORS)

    def _update_players(self) -> None:
        print("Updating players")
        names = self.db_client.get_last_minute_users()
        print(names)
        for name in names:
            self._chat_message(name)
