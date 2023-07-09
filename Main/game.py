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
        self.gameOver = False
        self.winner = ""
        self.enpassent = False
        self.enpassentPosition = None
    def drawBoard(self, x, y, d, l ,h):
        self.x = x
        self.y = y
        self.dark = d
        self.light = l
        self.highlight = h

        # Board
        for row in range(8):
            for col in range(8):
                if (row % 2 == 0 and col % 2 != 0) or (row % 2 != 0 and col % 2 == 0) :
                    pygame.draw.rect(self.screen, l, pygame.rect.Rect(x + col * SQUARESIZE, y + row * SQUARESIZE, SQUARESIZE, SQUARESIZE))
                else:
                    pygame.draw.rect(self.screen, d, pygame.rect.Rect(x + col * SQUARESIZE, y + row * SQUARESIZE, SQUARESIZE, SQUARESIZE))

        # Pieces
        for row in range(8):
            for col in range(8):
                if self.board[row][col] != EMPTY:
                    self.screen.blit(self.board[row][col].image, (x + col * SQUARESIZE, y + row * SQUARESIZE)) if not self.flipped else self.screen.blit(self.board[row][col].image, (WIDTH - (x + col * SQUARESIZE) - SQUARESIZE, HEIGHT - (y + row * SQUARESIZE) - SQUARESIZE))

        # Highlights
        if self.startPos:
            pygame.draw.rect(self.screen, h, pygame.rect.Rect((self.startPos[1] * SQUARESIZE) + self.x, (self.startPos[0] * SQUARESIZE) + self.y, SQUARESIZE, SQUARESIZE), 5) if not self.flipped else pygame.draw.rect(self.screen, h, pygame.rect.Rect(7 * SQUARESIZE - (self.startPos[1] * SQUARESIZE) + self.x, 7 * SQUARESIZE - ((self.startPos[0] * SQUARESIZE) + self.y), SQUARESIZE, SQUARESIZE), 5)
            moves = self.validMoves(self.startPos)
            if len(moves) > 0:
                for move in moves:
                    pygame.draw.rect(self.screen, h, pygame.rect.Rect((move[1] * SQUARESIZE) + self.x, (move[0] * SQUARESIZE) + self.y, SQUARESIZE, SQUARESIZE), 5) if not self.flipped else pygame.draw.rect(self.screen, h, pygame.rect.Rect(7 * SQUARESIZE - (move[1] * SQUARESIZE) + self.x, 7 * SQUARESIZE - ((move[0] * SQUARESIZE) + self.y), SQUARESIZE, SQUARESIZE), 5)

    def action(self):
        col = (pygame.mouse.get_pos()[0] - self.x) // SQUARESIZE if not self.flipped else 7 - ((pygame.mouse.get_pos()[0] - self.x) // SQUARESIZE)
        row = (pygame.mouse.get_pos()[1] - self.y) // SQUARESIZE if not self.flipped else 7 - ((pygame.mouse.get_pos()[1] - self.y) // SQUARESIZE)
        if row > 7 or col > 7 or row < 0  or col < 0:
            return
        if not self.startPos and self.board[row][col] != EMPTY and self.board[row][col].colour == self.turn:
            self.startPos = [row,col]
        elif not self.endPos and self.startPos:
            self.endPos = [row,col]

        if self.startPos and self.endPos:
            if self.endPos in self.validMoves(self.startPos):
                self.makeMove()
            else:
                self.startPos = self.endPos = None
                if self.board[row][col] != EMPTY and self.board[row][col].colour == self.turn:
                    self.startPos = [row,col]
    
    def makeMove(self):
        if self.board[self.startPos[0]][self.startPos[1]].name == BPAWN and self.startPos[0] == 1 and self.endPos[0] == 3:
            self.enpassent = True
            self.enpassentPosition = self.endPos
        elif self.board[self.startPos[0]][self.startPos[1]].name == WPAWN and self.startPos[0] == 6 and self.endPos[0] == 4:
            self.enpassent = True
            self.enpassentPosition = self.endPos
        else:
            self.enpassent = False
            self.enpassentPosition = None
        if self.board[self.startPos[0]][self.startPos[1]].name == WPAWN and self.board[self.endPos[0]][self.endPos[1]] == EMPTY and self.endPos[0] == self.startPos[0] - 1:
            if self.endPos[1] == self.startPos[1] - 1 or self.endPos[1] == self.startPos[1] + 1:
                self.board[self.endPos[0] + 1][self.endPos[1]] = EMPTY           
        elif self.board[self.startPos[0]][self.startPos[1]].name == BPAWN and self.board[self.endPos[0]][self.endPos[1]] == EMPTY and self.endPos[0] == self.startPos[0] + 1:
            if self.endPos[1] == self.startPos[1] - 1 or self.endPos[1] == self.startPos[1] + 1:
                self.board[self.endPos[0] - 1][self.endPos[1]] = EMPTY
        
        if self.board[self.startPos[0]][self.startPos[1]].name == WKING or self.board[self.startPos[0]][self.startPos[1]].name == BKING:
            if self.startPos[1] == 4 and self.endPos[1] == 6:
                self.board[self.startPos[0]][7].moved = True
                self.board[self.startPos[0]][5], self.board[self.startPos[0]][7] = self.board[self.startPos[0]][7], EMPTY
            if self.startPos[1] == 4 and self.endPos[1] == 2:
                self.board[self.startPos[0]][0].moved = True
                self.board[self.startPos[0]][3], self.board[self.startPos[0]][0] = self.board[self.startPos[0]][0], EMPTY
        
        self.board[self.startPos[0]][self.startPos[1]].moved = True
        self.board[self.endPos[0]][self.endPos[1]], self.board[self.startPos[0]][self.startPos[1]] =  self.board[self.startPos[0]][self.startPos[1]], EMPTY
        if self.turn == "White":
            if self.checkForMate("Black"):
                self.gameOver = True
                self.winner = self.turn
        else:
            if self.checkForMate("White"):
                self.gameOver = True
                self.winner = self.turn
        self.startPos = self.endPos = None
        self.turn = "White" if self.turn == "Black" else "Black"

    def validMoves(self, startPos):
        colour = self.board[startPos[0]][startPos[1]].colour
        moves = self.fetchMoves(startPos)
        illiegalMoves = []
        for move in moves:
            temp = self.board[move[0]][move[1]]
            self.board[move[0]][move[1]], self.board[startPos[0]][startPos[1]] =  self.board[startPos[0]][startPos[1]], EMPTY
            if self.checkForCheck(colour):
                illiegalMoves.append(move)
            self.board[move[0]][move[1]], self.board[startPos[0]][startPos[1]] =  temp, self.board[move[0]][move[1]]
        for move in illiegalMoves:
            moves.remove(move)
        
        if (self.board[startPos[0]][startPos[1]].name == WKING or self.board[startPos[0]][startPos[1]].name == BKING) and [startPos[0],startPos[1] + 2] in moves:
            if self.checkForCheck(colour):
                moves.remove([startPos[0],startPos[1] + 2])
            elif [startPos[0],startPos[1] + 1] not in moves:
                moves.remove([startPos[0],startPos[1] + 2])

        if (self.board[startPos[0]][startPos[1]].name == WKING or self.board[startPos[0]][startPos[1]].name == BKING) and [startPos[0],startPos[1] - 2] in moves:
            if self.checkForCheck(colour):
                moves.remove([startPos[0],startPos[1] - 2])
            elif [startPos[0],startPos[1] - 1] not in moves:
                moves.remove([startPos[0],startPos[1] - 2])
        return moves
  
    def checkForCheck(self, kingColour):
        position = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] != EMPTY and self.board[row][col].name == kingColour + "King":
                    position = [row,col]
        allMoves = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] != EMPTY and self.board[row][col].colour != kingColour:
                    moves = self.fetchMoves([row,col])
                    for move in moves:
                        allMoves.append([[row, col],move])
        for move in allMoves:
            if move[1][0] == position[0] and move[1][1] == position[1]:
                return True
        return False

    def fetchMoves(self, startPos):
        moves = []
        if self.board[startPos[0]][startPos[1]] != EMPTY:
            colour = self.board[startPos[0]][startPos[1]].colour

            if self.board[startPos[0]][startPos[1]].name == BPAWN:
                if startPos[0] + 1 < 8:
                    if self.board[startPos[0] + 1][startPos[1]] == EMPTY:
                        moves.append([startPos[0] + 1, startPos[1]])
                        if startPos[0] == 1 and self.board[startPos[0] + 2][startPos[1]] == EMPTY:
                            moves.append([startPos[0] + 2, startPos[1]])
                    
                    if startPos[1] + 1 < 8 and (self.board[startPos[0] + 1][startPos[1] + 1] != EMPTY and self.board[startPos[0] + 1][startPos[1] + 1].colour != colour):
                        moves.append([startPos[0] + 1, startPos[1] + 1])
                    
                    if startPos[1] - 1 > -1 and (self.board[startPos[0] + 1][startPos[1] - 1] != EMPTY and self.board[startPos[0] + 1][startPos[1] - 1].colour != colour):
                        moves.append([startPos[0] + 1, startPos[1] - 1])

                    if self.enpassent and startPos[1] + 1 < 8 and self.board[startPos[0] + 1][startPos[1] + 1] == EMPTY and self.enpassentPosition == [startPos[0], startPos[1] + 1] and self.board[startPos[0]][startPos[1] + 1].colour != colour:
                        moves.append([startPos[0] + 1, startPos[1] + 1])
                    
                    if self.enpassent and startPos[1] - 1 > -1 and self.board[startPos[0] + 1][startPos[1] - 1] == EMPTY and self.enpassentPosition == [startPos[0], startPos[1] - 1] and self.board[startPos[0]][startPos[1] - 1].colour != colour:
                        moves.append([startPos[0] + 1, startPos[1] - 1])

            elif self.board[startPos[0]][startPos[1]].name == WPAWN:
                if startPos[0] - 1  > -1:
                    if self.board[startPos[0] - 1][startPos[1]] == EMPTY:
                        moves.append([startPos[0] - 1, startPos[1]])
                        if startPos[0] == 6 and self.board[startPos[0] - 2][startPos[1]] == EMPTY:
                            moves.append([startPos[0] - 2, startPos[1]])
                    
                    if startPos[1] + 1 < 8 and (self.board[startPos[0] - 1][startPos[1] + 1] != EMPTY and self.board[startPos[0] - 1][startPos[1] + 1].colour != colour):
                        moves.append([startPos[0] - 1, startPos[1] + 1])
                    
                    if startPos[1] - 1 > -1 and (self.board[startPos[0] - 1][startPos[1] - 1] != EMPTY and self.board[startPos[0] - 1][startPos[1] - 1].colour != colour):
                        moves.append([startPos[0] - 1, startPos[1] - 1])
                    
                    if self.enpassent and startPos[1] + 1 < 8 and self.board[startPos[0] - 1][startPos[1] + 1] == EMPTY and self.enpassentPosition == [startPos[0], startPos[1] + 1] and self.board[startPos[0]][startPos[1] + 1].colour != colour:
                        moves.append([startPos[0] - 1, startPos[1] + 1])
                    
                    if self.enpassent and startPos[1] - 1 > -1 and self.board[startPos[0] - 1][startPos[1] - 1] == EMPTY and self.enpassentPosition == [startPos[0], startPos[1] - 1] and self.board[startPos[0]][startPos[1] - 1].colour != colour:
                        moves.append([startPos[0] - 1, startPos[1] - 1])

            elif self.board[startPos[0]][startPos[1]].name == WKNGIHT or self.board[startPos[0]][startPos[1]].name == BKNIGHT:
                twoUp = startPos[0] + 2
                twoDown = startPos[0] - 2
                oneRight = startPos[1] + 1
                oneleft = startPos[1] - 1

                twoRight = startPos[1] + 2
                twoLeft = startPos[1] - 2
                oneUp = startPos[0] + 1
                oneDown = startPos[0] - 1

                if twoUp < 8:
                    if oneRight < 8:
                        if self.board[twoUp][oneRight] == EMPTY or self.board[twoUp][oneRight].colour != colour:
                            moves.append([twoUp, oneRight])
                
                    if oneleft > -1:
                        if self.board[twoUp][oneleft] == EMPTY or self.board[twoUp][oneleft].colour != colour:
                            moves.append([twoUp, oneleft])
                
                if twoDown > -1:
                    if oneRight < 8:
                        if self.board[twoDown][oneRight] == EMPTY or self.board[twoDown][oneRight].colour != colour:
                            moves.append([twoDown, oneRight])

                    if oneleft > -1:
                        if self.board[twoDown][oneleft] == EMPTY or self.board[twoDown][oneleft].colour != colour:
                            moves.append([twoDown, oneleft])


                if oneUp < 8:
                    if twoRight < 8:
                        if self.board[oneUp][twoRight] == EMPTY or self.board[oneUp][twoRight].colour != colour:
                            moves.append([oneUp, twoRight])
                
                    if twoLeft > -1:
                        if self.board[oneUp][twoLeft] == EMPTY or self.board[oneUp][twoLeft].colour != colour:
                            moves.append([oneUp, twoLeft])
                
                if oneDown > -1:
                    if twoRight < 8:
                        if self.board[oneDown][twoRight] == EMPTY or self.board[oneDown][twoRight].colour != colour:
                            moves.append([oneDown, twoRight])

                    if twoLeft > -1:
                        if self.board[oneDown][twoLeft] == EMPTY or self.board[oneDown][twoLeft].colour != colour:
                            moves.append([oneDown, twoLeft])

            elif self.board[startPos[0]][startPos[1]].name == WKING or self.board[startPos[0]][startPos[1]].name == BKING:
                oneUp = startPos[0] + 1
                oneDown = startPos[0] - 1
                oneRight = startPos[1] + 1
                oneleft = startPos[1] - 1
                if oneUp < 8:
                    if self.board[oneUp][startPos[1]] == EMPTY or self.board[oneUp][startPos[1]].colour != colour:
                            moves.append([oneUp, startPos[1]])
                    if oneRight < 8 and (self.board[oneUp][oneRight] == EMPTY or self.board[oneUp][oneRight].colour != colour):
                        moves.append([oneUp, oneRight])
                    if oneleft > -1 and (self.board[oneUp][oneleft] == EMPTY or self.board[oneUp][oneleft].colour != colour):
                        moves.append([oneUp, oneleft])

                if oneDown > -1:
                    if self.board[oneDown][startPos[1]] == EMPTY or self.board[oneDown][startPos[1]].colour != colour:
                            moves.append([oneDown, startPos[1]])
                    if oneRight < 8 and (self.board[oneDown][oneRight] == EMPTY or self.board[oneDown][oneRight].colour != colour):
                        moves.append([oneDown, oneRight])
                    if oneleft > -1 and (self.board[oneDown][oneleft] == EMPTY or self.board[oneDown][oneleft].colour != colour):
                        moves.append([oneDown, oneleft])
                
                if oneRight < 8:
                    if self.board[startPos[0]][oneRight] == EMPTY or self.board[startPos[0]][oneRight].colour != colour:
                        moves.append([startPos[0], oneRight])
                
                if oneleft > -1:
                    if self.board[startPos[0]][oneleft] == EMPTY or self.board[startPos[0]][oneleft].colour != colour:
                        moves.append([startPos[0], oneleft])
                    
                if not self.board[startPos[0]][startPos[1]].moved and self.board[startPos[0]][startPos[1] + 1] == EMPTY and self.board[startPos[0]][startPos[1] + 2] == EMPTY and self.board[startPos[0]][startPos[1] + 3] != EMPTY and (self.board[startPos[0]][startPos[1] + 3].name == WROOK or self.board[startPos[0]][startPos[1] + 3].name == BROOK) and not self.board[startPos[0]][startPos[1] + 3].moved:
                    moves.append([startPos[0], startPos[1] + 2])
                
                if not self.board[startPos[0]][startPos[1]].moved and self.board[startPos[0]][startPos[1] - 1] == EMPTY and self.board[startPos[0]][startPos[1] - 2] == EMPTY and self.board[startPos[0]][startPos[1] - 3] == EMPTY and self.board[startPos[0]][startPos[1] - 4] != EMPTY and (self.board[startPos[0]][startPos[1] - 4].name == WROOK or self.board[startPos[0]][startPos[1] - 4].name == BROOK) and not self.board[startPos[0]][startPos[1] - 4].moved:
                    moves.append([startPos[0], startPos[1] - 2])


            elif self.board[startPos[0]][startPos[1]].name == WROOK or self.board[startPos[0]][startPos[1]].name == BROOK:
                row = startPos[0] + 1
                blocked = False
                while not blocked and row < 8:
                    if self.board[row][startPos[1]] == EMPTY:
                        moves.append([row, startPos[1]])
                    elif self.board[row][startPos[1]].colour != colour:
                        moves.append([row, startPos[1]])
                        blocked = True
                    else:
                        blocked = True
                    row += 1
                
                row = startPos[0] - 1
                blocked = False
                while not blocked and row > -1:
                    if self.board[row][startPos[1]] == EMPTY:
                        moves.append([row, startPos[1]])
                    elif self.board[row][startPos[1]].colour != colour:
                        moves.append([row, startPos[1]])
                        blocked = True
                    else:
                        blocked = True
                    row -= 1

                col = startPos[1] + 1
                blocked = False
                while not blocked and col < 8:
                    if self.board[startPos[0]][col] == EMPTY:
                        moves.append([startPos[0], col])
                    elif self.board[startPos[0]][col].colour != colour:
                        moves.append([startPos[0], col])
                        blocked = True
                    else:
                        blocked = True
                    col += 1
                
                col = startPos[1] - 1
                blocked = False
                while not blocked and col > -1:
                    if self.board[startPos[0]][col] == EMPTY:
                        moves.append([startPos[0], col])
                    elif self.board[startPos[0]][col].colour != colour:
                        moves.append([startPos[0], col])
                        blocked = True
                    else:
                        blocked = True
                    col -= 1
        
            elif self.board[startPos[0]][startPos[1]].name == WBISHOP or self.board[startPos[0]][startPos[1]].name == BBISHOP:
                row = startPos[0] + 1
                col = startPos[1] + 1
                blocked = False
                while not blocked and row < 8 and col < 8:
                    if self.board[row][col] == EMPTY:
                        moves.append([row, col])
                    elif self.board[row][col].colour != colour:
                        moves.append([row, col])
                        blocked = True
                    else:
                        blocked = True
                    row += 1
                    col += 1
                
                row = startPos[0] - 1
                col = startPos[1] - 1
                blocked = False
                while not blocked and row > -1 and col > -1:
                    if self.board[row][col] == EMPTY:
                        moves.append([row, col])
                    elif self.board[row][col].colour != colour:
                        moves.append([row, col])
                        blocked = True
                    else:
                        blocked = True
                    row -= 1
                    col -= 1

                row = startPos[0] + 1
                col = startPos[1] - 1
                blocked = False
                while not blocked and row < 8 and col > -1:
                    if self.board[row][col] == EMPTY:
                        moves.append([row, col])
                    elif self.board[row][col].colour != colour:
                        moves.append([row, col])
                        blocked = True
                    else:
                        blocked = True
                    row += 1
                    col -= 1
                
                row = startPos[0] - 1
                col = startPos[1] + 1
                blocked = False
                while not blocked and row > -1 and col < 8:
                    if self.board[row][col] == EMPTY:
                        moves.append([row, col])
                    elif self.board[row][col].colour != colour:
                        moves.append([row, col])
                        blocked = True
                    else:
                        blocked = True
                    row -= 1
                    col += 1
        
            elif self.board[startPos[0]][startPos[1]].name == WQUEEN or self.board[startPos[0]][startPos[1]].name == BQUEEN:
                row = startPos[0] + 1
                blocked = False
                while not blocked and row < 8:
                    if self.board[row][startPos[1]] == EMPTY:
                        moves.append([row, startPos[1]])
                    elif self.board[row][startPos[1]].colour != colour:
                        moves.append([row, startPos[1]])
                        blocked = True
                    else:
                        blocked = True
                    row += 1
                
                row = startPos[0] - 1
                blocked = False
                while not blocked and row > -1:
                    if self.board[row][startPos[1]] == EMPTY:
                        moves.append([row, startPos[1]])
                    elif self.board[row][startPos[1]].colour != colour:
                        moves.append([row, startPos[1]])
                        blocked = True
                    else:
                        blocked = True
                    row -= 1

                col = startPos[1] + 1
                blocked = False
                while not blocked and col < 8:
                    if self.board[startPos[0]][col] == EMPTY:
                        moves.append([startPos[0], col])
                    elif self.board[startPos[0]][col].colour != colour:
                        moves.append([startPos[0], col])
                        blocked = True
                    else:
                        blocked = True
                    col += 1
                
                col = startPos[1] - 1
                blocked = False
                while not blocked and col > -1:
                    if self.board[startPos[0]][col] == EMPTY:
                        moves.append([startPos[0], col])
                    elif self.board[startPos[0]][col].colour != colour:
                        moves.append([startPos[0], col])
                        blocked = True
                    else:
                        blocked = True
                    col -= 1
                
                row = startPos[0] + 1
                col = startPos[1] + 1
                blocked = False
                while not blocked and row < 8 and col < 8:
                    if self.board[row][col] == EMPTY:
                        moves.append([row, col])
                    elif self.board[row][col].colour != colour:
                        moves.append([row, col])
                        blocked = True
                    else:
                        blocked = True
                    row += 1
                    col += 1
                
                row = startPos[0] - 1
                col = startPos[1] - 1
                blocked = False
                while not blocked and row > -1 and col > -1:
                    if self.board[row][col] == EMPTY:
                        moves.append([row, col])
                    elif self.board[row][col].colour != colour:
                        moves.append([row, col])
                        blocked = True
                    else:
                        blocked = True
                    row -= 1
                    col -= 1

                row = startPos[0] + 1
                col = startPos[1] - 1
                blocked = False
                while not blocked and row < 8 and col > -1:
                    if self.board[row][col] == EMPTY:
                        moves.append([row, col])
                    elif self.board[row][col].colour != colour:
                        moves.append([row, col])
                        blocked = True
                    else:
                        blocked = True
                    row += 1
                    col -= 1
                
                row = startPos[0] - 1
                col = startPos[1] + 1
                blocked = False
                while not blocked and row > -1 and col < 8:
                    if self.board[row][col] == EMPTY:
                        moves.append([row, col])
                    elif self.board[row][col].colour != colour:
                        moves.append([row, col])
                        blocked = True
                    else:
                        blocked = True
                    row -= 1
                    col += 1

        return moves

    def checkForMate(self, colour):
        allMoves = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] != EMPTY and self.board[row][col].colour == colour:
                    moves = self.validMoves([row,col])
                    for move in moves:
                        allMoves.append([[row, col],move])

        if self.checkForCheck(colour) and len(allMoves) == 0:
            return True
        
        return False