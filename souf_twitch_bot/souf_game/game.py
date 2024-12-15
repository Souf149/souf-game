import sched
import sys
import time
import pygame
import random

background = pygame.Surface((800, 600))
background.fill(pygame.Color("#05D810FF"))


class Game:
    def run(self):
        print("Game is running")

        self.x = random.randint(0, 50)
        self.y = random.randint(0, 50)
        
        
        
        pygame.init()
        pygame.display.set_caption("Quick Start")
        self.window_surface = pygame.display.set_mode((800, 600))
        pygame.display.update()
        self.my_scheduler = sched.scheduler(time.time, time.sleep)
        self.my_scheduler.enter(
            1,
            1,
            self.draw,
        )
        self.my_scheduler.run()

    def new_message(self, message: str, username: str):
        self.x = random.randint(0, 50)
        self.y = random.randint(0, 50)
        
        
        
        

    def draw(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
        print("HELLO")
        self.window_surface.blit(background, (0, 0))
        pygame.draw.rect(background, "#FF0000", pygame.Rect(self.x, self.y, 50, 50))

        pygame.display.update()

        self.my_scheduler.enter(
            0.1,
            1,
            self.draw,
        )
game = Game()
game.run()
game.draw()
while True:
    time.sleep(1)    
    game.new_message("hello there","souf")
    
    
    