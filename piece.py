import pygame
from constants import *
class Piece():
    def __init__(self, name):
        self.name = name
        self.colour = self.name[:5]
        if self.name == WKING or self.name == BKING:
            self.value = 200.0
        elif self.name == WQUEEN or self.name == BQUEEN:
            self.value = 9.5
        elif self.name == WROOK or self.name == BROOK:
            self.value = 5.63
        elif self.name == WBISHOP or self.name == BBISHOP:
            self.value = 3.33
        elif self.name == WKNGIHT or self.name == BKNIGHT:
            self.value = 3.05
        elif self.name == WPAWN or self.name == BPAWN:
            self.value = 1.0
        self.image = pygame.image.load("Assets/" + self.name + ".png").convert_alpha()