import pygame
from constants import *
    
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
            [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
            [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
            [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
            [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
            [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
            [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
            [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
            [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
            ]
    
        self.blackPawnScores = list(reversed(self.whitePawnScores))

    def positionValue(self, row, col):
        return self.whitePawnScores[row][col] if self.colour == "White" else self.blackPawnScores[row][col]
        
class Knight(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.value = 3.05
        self.name = self.colour + "Knight"
        self.image = pygame.image.load(f"Assets/{self.colour}Knight.png").convert_alpha()
        
        self.whiteKnightScores = [
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
            [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
            [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
            [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
            [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
            [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
            [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
            ]

        self.blackKnightScores = list(reversed(self.whiteKnightScores))
        
    def positionValue(self, row, col):
        return self.whiteKnightScores[row][col] if self.colour == "White" else self.blackKnightScores[row][col]
    
class Bishop(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.value = 3.33
        self.name = self.colour + "Bishop"
        self.image = pygame.image.load(f"Assets/{self.colour}Bishop.png").convert_alpha()
        
        self.whiteBishopScores = [
            [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
            [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
            [ -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
            [ -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
            [ -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
            [ -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
            [ -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
            [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
            ]
        
        self.blackBishopScores = list(reversed(self.whiteBishopScores))
        
    def positionValue(self, row, col):
        return self.whiteBishopScores[row][col] if self.colour == "White" else self.blackBishopScores[row][col]

class Rook(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.value = 5.63
        self.name = self.colour + "Rook"
        self.image = pygame.image.load(f"Assets/{self.colour}Rook.png").convert_alpha()

        self.whiteRookScores = [
            [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
            [  0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
            [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [  0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
            ]
        
        self.blackRookScores = list(reversed(self.whiteRookScores))
        
    def positionValue(self, row, col):
        return self.whiteRookScores[row][col] if self.colour == "White" else self.blackRookScores[row][col]
    
class Queen(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.value = 9.5
        self.name = self.colour + "Queen"
        self.image = pygame.image.load(f"Assets/{self.colour}Queen.png").convert_alpha()

        self.whiteQueenScores = [
            [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
            [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
            [ -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
            [ -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
            [  0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
            [ -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
            [ -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
            [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
            ]
        
        self.blackQueenScores = list(reversed(self.whiteQueenScores))
        
    def positionValue(self, row, col):
        return self.whiteQueenScores[row][col] if self.colour == "White" else self.blackQueenScores[row][col]
    
class King(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.value = 200
        self.name = self.colour + "King"
        self.image = pygame.image.load(f"Assets/{self.colour}King.png").convert_alpha()