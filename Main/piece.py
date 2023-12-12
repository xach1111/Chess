import pygame
from constants import *
# class Piece():
#     def __init__(self, name):
#         self.name = name
#         self.colour = self.name[:5]
#         if self.name == WKING or self.name == BKING:
#             self.value = 200.0
#         elif self.name == WQUEEN or self.name == BQUEEN:
#             self.value = 9.5
#         elif self.name == WROOK or self.name == BROOK:
#             self.value = 5.63
#         elif self.name == WBISHOP or self.name == BBISHOP:
#             self.value = 3.33
#         elif self.name == WKNIGHT or self.name == BKNIGHT:
#             self.value = 3.05
#         elif self.name == WPAWN or self.name == BPAWN:
#             self.value = 1.0
#         self.image = pygame.image.load("Assets/" + self.name + ".png").convert_alpha()
#         self.moved = False
    
class Piece():
    def __init__(self, colour):
        self.colour = colour
        self.moved = False
    
class Pawn(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.value = 1 
        self.name = self.colour + "Pawn"
        self.image = pygame.image.load(f"Assets/{self.colour}Pawn.png").convert_alpha()
        
        self.whitePawnScores = [
            [8, 8, 8, 8, 8, 8, 8, 8],
            [7, 7, 7, 7, 7, 7, 7, 7],
            [3, 3, 4, 5, 5, 4, 3, 3],
            [2.5, 2.5, 3, 4.5, 4.5, 3, 2.5, 2.5],
            [2, 2, 2, 4, 4, 2, 2, 2],
            [2.5, 1.5, 1, 2, 2, 1, 1.5, 2.5],
            [2.5, 3, 3, 0, 0, 3, 3, 25],
            [2, 2, 2, 2, 2, 2, 2, 2]
            ]
    
        self.blackPawnScores = [
            [2, 2, 2, 2, 2, 2, 2, 2],
            [2.5, 3, 3, 0, 0, 3, 3, 2.5],
            [2.5, 1.5, 1, 2, 2, 1, 1.5, 2.5],
            [2, 2, 2, 4, 4, 2, 2, 2],
            [2.5, 2.5, 3, 4.5, 4.5, 3, 2.5, 2.5],
            [3, 3, 4, 5, 5, 4, 3, 3],
            [7, 7, 7, 7, 7, 7, 7, 7],
            [8, 8, 8, 8, 8, 8, 8, 8]
            ]
    def positionValue(self, row, col):
        if self.colour == "White":
            return self.whitePawnScores[row][col]
        else:
            return self.blackPawnScores[row][col]
        
class Knight(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.value = 3.05
        self.name = self.colour + "Knight"
        self.image = pygame.image.load(f"Assets/{self.colour}Knight.png").convert_alpha()
        
        self.knightScores = [
            [0, 1, 2, 2, 2, 2, 1, 0],
            [1, 3, 5, 5, 5, 5, 3, 1],
            [2, 5, 6, 6.5, 6.5, 6, 5, 2],
            [2, 5.5, 6.5, 7, 7, 6.5, 5.5, 2],
            [2, 5, 6.5, 7, 7, 6.5, 5, 2],
            [2, 5.5, 6, 6.5, 6.5, 6, 5.5, 2],
            [1, 3, 5, 5.5, 5.5, 5, 3, 1],
            [0, 1, 2, 2, 2, 2, 1, 0]
            ]
        
    def positionValue(self, row, col):   
        return self.knightScores[row][col]
    
class Bishop(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.value = 3.33
        self.name = self.colour + "Bishop"
        self.image = pygame.image.load(f"Assets/{self.colour}Bishop.png").convert_alpha()
        
        self.bishopScores = [
            [0, 2, 2, 2, 2, 2, 2, 0],
            [2, 4, 4, 4, 4, 4, 4, 2],
            [2, 4, 5, 6, 6, 5, 4, 2],
            [2, 5, 5, 6, 6, 5, 5, 2],
            [2, 4, 6, 6, 6, 6, 4, 2],
            [2, 6, 6, 6, 6, 6, 6, 2],
            [2, 5, 4, 4, 4, 4, 5, 2],
            [0, 2, 2, 2, 2, 2, 2, 0]
            ]
        
    def positionValue(self, row, col):   
        return self.bishopScores[row][col]

class Rook(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.value = 5.63
        self.name = self.colour + "Rook"
        self.image = pygame.image.load(f"Assets/{self.colour}Rook.png").convert_alpha()

        self.rookScores = [
            [2.5, 2.5, 2.5, 5, 5, 2.5, 2.5, 2.5],
            [5, 7.5, 7.5, 7.5, 7.5, 7.5, 7.5, 5],
            [0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 0],
            [0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 0],
            [0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 0],
            [0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 0],
            [0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 0],
            [2.5, 2.5, 2.5, 5, 5, 2.5, 2.5, 2.5]
            ]
        
    def positionValue(self, row, col):   
        return self.rookScores[row][col]
    
class Queen(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.value = 9.5
        self.name = self.colour + "Queen"
        self.image = pygame.image.load(f"Assets/{self.colour}Queen.png").convert_alpha()

        self.queenScores = [
            [0, 2, 2, 3, 3, 2, 2, 0],
            [2, 4, 4, 4, 4, 4, 4, 2],
            [2, 4, 5, 5, 5, 5, 4, 2],
            [3, 4, 5, 5, 5, 5, 4, 3],
            [4, 4, 5, 5, 5, 5, 4, 3],
            [2, 5, 5, 5, 5, 5, 4, 2],
            [2, 4, 5, 4, 4, 4, 4, 2],
            [0, 2, 2, 3, 3, 2, 2, 0]]
        
    def positionValue(self, row, col):   
        return self.queenScores[row][col]
    
class King(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.value = 200
        self.name = self.colour + "King"
        self.image = pygame.image.load(f"Assets/{self.colour}King.png").convert_alpha()