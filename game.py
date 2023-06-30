import pygame
from constants import *
from piece import Piece

class Game():
    def __init__(self, screen):
        self.board = [
            [Piece(BROOK), Piece(BKNIGHT), Piece(BBISHOP), Piece(BQUEEN), Piece(BKING), Piece(BBISHOP), Piece(BKNIGHT), Piece(BROOK)],
            [Piece(BPAWN)] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [Piece(WPAWN)] * 8,
            [Piece(WROOK), Piece(WKNGIHT), Piece(WBISHOP), Piece(WQUEEN), Piece(WKING), Piece(WBISHOP), Piece(WKNGIHT), Piece(WROOK)],
        ]
        self.screen = screen
        self.flipped = False
        self.turn = "White"
        self.startPos = None
        self.endPos = None
        
    def drawBoard(self, x, y, d, l ,h):
        self.x = x
        self.y = y
        self.dark = d
        self.light = l
        self.highlight = h
        for row in range(8):
            for col in range(8):
                if (row % 2 == 0 and col % 2 != 0) or (row % 2 != 0 and col % 2 == 0) :
                    pygame.draw.rect(self.screen, l, pygame.rect.Rect(x + col * SQUARESIZE, y + row * SQUARESIZE, SQUARESIZE, SQUARESIZE))
                else:
                    pygame.draw.rect(self.screen, d, pygame.rect.Rect(x + col * SQUARESIZE, y + row * SQUARESIZE, SQUARESIZE, SQUARESIZE))
    
        for row in range(8):
            for col in range(8):
                if self.board[row][col] != EMPTY:
                    self.screen.blit(self.board[row][col].image, (x + col * SQUARESIZE, y + row * SQUARESIZE)) if not self.flipped else self.screen.blit(self.board[row][col].image, (WIDTH - (x + col * SQUARESIZE) - SQUARESIZE, HEIGHT - (y + row * SQUARESIZE) - SQUARESIZE))



    def action(self):
        col = pygame.mouse.get_pos()[0]//SQUARESIZE - self.x // SQUARESIZE if not self.flipped else 7 - (pygame.mouse.get_pos()[0]//SQUARESIZE - self.x // SQUARESIZE)
        row = pygame.mouse.get_pos()[1]//SQUARESIZE - self.y // SQUARESIZE if not self.flipped else 7 - (pygame.mouse.get_pos()[1]//SQUARESIZE - self.y // SQUARESIZE)
        if not self.startPos:
            self.startPos = [row,col]
        elif not self.endPos:
            self.endPos = [row,col]

        if self.startPos and self.endPos:
            if self.endPos in self.validMoves(self.startPos):
                self.board[self.startPos[0]][self.startPos[1]], self.board[self.endPos[0]][self.endPos[1]] = EMPTY, self.board[self.startPos[0]][self.startPos[1]]
                self.startPos = self.endPos = None
                self.turn = "White" if self.turn == "Black" else "Black"
        
    
    def validMoves(self, startPos):
        all = []
        for row in range(8):
            for col in range(8):
                all.append([row,col])
        return all