import pygame
class Pig:
    def __init__(self):
        self.sprite = pygame.image.load('data/gfx/pig.png')
        self.position = pygame.Vector2()
        self.position.xy