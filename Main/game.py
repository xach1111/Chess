import pygame
from constants import *
from piece import Pawn, Knight, Bishop, Rook, Queen, King
from widgets import Button
import copy
pygame.init()


class Game():
    def __init__(self, screen):
        self.board = [
            [Rook("Black"), Knight("Black"), Bishop("Black"), Queen("Black"), King("Black"), Bishop("Black"), Knight("Black"), Rook("Black")],
            [Pawn("Black")] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [Pawn("White")] * 8,
            [Rook("White"), Knight("White"), Bishop("White"), Queen("White"), King("White"), Bishop("White"), Knight("White"), Rook("White")],
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
        self.needToPromote = False
        self.promoteToPiece = None
        self.knightButton = Button(screen, 500, 100, 400, 100, "Knight", BLACK)
        self.bishopButton = Button(screen, 500, 200, 400, 100, "Bishop", BLACK)
        self.rookButton = Button(screen, 500, 300, 400, 100, "Rook", BLACK)
        self.queenButton = Button(screen, 500, 400, 400, 100, "Queen", BLACK)
        self.variableHistory = [[False, "", False, None, False, None]] #gameover, winner, enpassant, enpassent position, needtopromote, promote to piece
        self.history = [[
            [Rook("Black"), Knight("Black"), Bishop("Black"), Queen("Black"), King("Black"), Bishop("Black"), Knight("Black"), Rook("Black")],
            [Pawn("Black")] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [Pawn("White")] * 8,
            [Rook("White"), Knight("White"), Bishop("White"), Queen("White"), King("White"), Bishop("White"), Knight("White"), Rook("White")],
        ]]
        self.moveHistory = []
        self.pgn = ""
        # fools mate
        # self.startPos, self.endPos = [6, 5],[5,5]
        # self.makeMove()
        # self.startPos, self.endPos = [1,4],[2,4]
        # self.makeMove()

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
                    pygame.draw.rect(self.screen, d, pygame.rect.Rect(x + col * SQUARESIZE, y + row * SQUARESIZE, SQUARESIZE, SQUARESIZE))
                else:
                    pygame.draw.rect(self.screen, l, pygame.rect.Rect(x + col * SQUARESIZE, y + row * SQUARESIZE, SQUARESIZE, SQUARESIZE))

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
        #promotion
        if self.needToPromote:
            self.knightButton.draw()
            self.bishopButton.draw()
            self.rookButton.draw()
            self.queenButton.draw()

    def action(self):
        if not self.startPos or (self.startPos and not self.endPos):
            col = (pygame.mouse.get_pos()[0] - self.x) // SQUARESIZE if not self.flipped else 7 - ((pygame.mouse.get_pos()[0] - self.x) // SQUARESIZE)
            row = (pygame.mouse.get_pos()[1] - self.y) // SQUARESIZE if not self.flipped else 7 - ((pygame.mouse.get_pos()[1] - self.y) // SQUARESIZE)
            if row > 7 or col > 7 or row < 0  or col < 0:
                self.startPos = self.endPos = None
                return
            if not self.startPos and self.board[row][col] != EMPTY and self.board[row][col].colour == self.turn:
                self.startPos = [row,col]
            elif not self.endPos and self.startPos:
                self.endPos = [row,col]

        if self.startPos and self.endPos:
            if (self.board[self.startPos[0]][self.startPos[1]].name == WPAWN and self.startPos[0] == 1 and self.endPos[0] == 0) or (self.board[self.startPos[0]][self.startPos[1]].name == BPAWN and self.startPos[0] == 6 and self.endPos[0] == 7):
                self.needToPromote = True
            if not self.needToPromote or (len(self.endPos) == 3):
                if self.endPos in self.validMoves(self.startPos):
                    temp = [self.startPos, self.endPos]
                    self.makeMove()
                    return temp
                else:
                    self.startPos = self.endPos = None
                    if self.board[row][col] != EMPTY and self.board[row][col].colour == self.turn:
                        self.startPos = [row,col]
            else:
                if self.knightButton.clicked():
                    if self.board[self.startPos[0]][self.startPos[1]].name == WPAWN:
                        self.endPos.append(WKNIGHT)
                    else:
                        self.endPos.append(BKNIGHT)
                    return self.action()
                elif self.bishopButton.clicked():
                    if self.board[self.startPos[0]][self.startPos[1]].name == WPAWN:
                        self.endPos.append(WBISHOP)
                    else:
                        self.endPos.append(BBISHOP)
                    return self.action()
                elif self.rookButton.clicked():
                    if self.board[self.startPos[0]][self.startPos[1]].name == WPAWN:
                        self.endPos.append(WROOK)
                    else:
                        self.endPos.append(BROOK)
                    return self.action()
                elif self.queenButton.clicked():
                    if self.board[self.startPos[0]][self.startPos[1]].name == WPAWN:
                        self.endPos.append(WQUEEN)
                    else:
                        self.endPos.append(BQUEEN)
                    return self.action()

    def makeMove(self):
        c = c1  = c2 = e = e1 = e2 = False
        if self.turn == "White":
            self.pgn = self.pgn + str((len(self.history) + 1) // 2) + "."

        

        if self.board[self.startPos[0]][self.startPos[1]].name == WPAWN and self.board[self.endPos[0]][self.endPos[1]] == EMPTY and self.endPos[0] == self.startPos[0] - 1:
            if self.endPos[1] == self.startPos[1] - 1 or self.endPos[1] == self.startPos[1] + 1:
                e = True
                e1 = True
                  
        elif self.board[self.startPos[0]][self.startPos[1]].name == BPAWN and self.board[self.endPos[0]][self.endPos[1]] == EMPTY and self.endPos[0] == self.startPos[0] + 1:
            if self.endPos[1] == self.startPos[1] - 1 or self.endPos[1] == self.startPos[1] + 1:
                e = True
                e2 = True

        
        
        # castling handling
        if self.board[self.startPos[0]][self.startPos[1]].name == WKING or self.board[self.startPos[0]][self.startPos[1]].name == BKING:
            if self.startPos[1] == 4 and self.endPos[1] == 6:
                c = True
                c1 = True
            if self.startPos[1] == 4 and self.endPos[1] == 2:
                c = True
                c2 = True
                
        
        if not c and not e:
            if self.board[self.startPos[0]][self.startPos[1]].name[5:] == "Knight":
                self.pgn = self.pgn + "N"
            elif self.board[self.startPos[0]][self.startPos[1]].name[5:] == "Bishop":
                self.pgn = self.pgn + "B"
            elif self.board[self.startPos[0]][self.startPos[1]].name[5:] == "Rook":
                self.pgn = self.pgn + "R"
            elif self.board[self.startPos[0]][self.startPos[1]].name[5:] == "Queen":
                self.pgn = self.pgn + "Q"
            elif self.board[self.startPos[0]][self.startPos[1]].name[5:] == "King":
                self.pgn = self.pgn + "K"
            
            for row in range(8):
                for col in range(8):
                    if [row,col] != self.startPos and self.board[row][col] != EMPTY and self.board[row][col].name == self.board[self.startPos[0]][self.startPos[1]].name:
                        for m in self.fetchMoves([row,col]):
                            if m[1] == self.endPos:
                                if col == self.startPos[1]:
                                    self.pgn = self.pgn + chr(col + 97)
                                elif row == self.startPos[0]:
                                    self.pgn = self.pgn + str(8 - row)
            
            if self.board[self.endPos[0]][self.endPos[1]] != EMPTY:
                if self.board[self.startPos[0]][self.startPos[1]].name == WPAWN or self.board[self.startPos[0]][self.startPos[1]].name == BPAWN:
                    self.pgn = self.pgn + chr(self.startPos[1] + 97) +  "x"
                else:
                    self.pgn = self.pgn + "x"
            
            self.pgn = self.pgn + self.indexCoordinateTranslate(self.endPos)
        
        if c1:
            self.pgn = self.pgn + "O-O"
            self.board[self.startPos[0]][7].moved = True
            self.board[self.startPos[0]][5], self.board[self.startPos[0]][7] = self.board[self.startPos[0]][7], EMPTY
        if c2:
            self.pgn = self.pgn + "O-O-O"
            self.board[self.startPos[0]][0].moved = True
            self.board[self.startPos[0]][3], self.board[self.startPos[0]][0] = self.board[self.startPos[0]][0], EMPTY
        if e1:
            self.pgn = self.pgn + chr(self.startPos[1] + 97) + "x" + self.indexCoordinateTranslate(self.endPos)
            self.board[self.endPos[0] + 1][self.endPos[1]] = EMPTY
        if e2:
            self.pgn = self.pgn + chr(self.startPos[1] + 97) + "x" + self.indexCoordinateTranslate(self.endPos)
            self.board[self.endPos[0] - 1][self.endPos[1]] = EMPTY

        # enpassent handling
        if self.board[self.startPos[0]][self.startPos[1]].name == BPAWN and self.startPos[0] == 1 and self.endPos[0] == 3:
            self.enpassent = True
            self.enpassentPosition = self.endPos
        elif self.board[self.startPos[0]][self.startPos[1]].name == WPAWN and self.startPos[0] == 6 and self.endPos[0] == 4:
            self.enpassent = True
            self.enpassentPosition = self.endPos
        else:
            self.enpassent = False
            self.enpassentPosition = None   
        # Promotion handling
        if len(self.endPos) == 3:
            self.pgn = self.pgn + "="
            if self.endPos[2][5:] == "Knight":
                self.pgn = self.pgn + "N"
            elif self.endPos[2][5:] == "Bishop":
                self.pgn = self.pgn + "B"
            elif self.endPos[2][5:] == "Rook":
                self.pgn = self.pgn + "R"
            elif self.endPos[2][5:] == "Queen":
                self.pgn = self.pgn + "Q"

            if self.endPos[2][5:] == "Pawn":
                self.board[self.startPos[0]][self.startPos[1]] = Pawn(self.endPos[2][:5])
            elif self.endPos[2][5:] == "Knight":
                self.board[self.startPos[0]][self.startPos[1]] = Knight(self.endPos[2][:5])
            elif self.endPos[2][5:] == "Bishop":
                self.board[self.startPos[0]][self.startPos[1]] = Bishop(self.endPos[2][:5])
            elif self.endPos[2][5:] == "Rook":
                self.board[self.startPos[0]][self.startPos[1]] = Rook(self.endPos[2][:5])
            elif self.endPos[2][5:] == "Queen":
                self.board[self.startPos[0]][self.startPos[1]] = Queen(self.endPos[2][:5])
            self.needToPromote = False

        #--
        self.board[self.startPos[0]][self.startPos[1]].moved = True
        self.board[self.endPos[0]][self.endPos[1]], self.board[self.startPos[0]][self.startPos[1]] =  self.board[self.startPos[0]][self.startPos[1]], EMPTY
        
        # check if game over
        if self.turn == "White":
            if self.checkForMate("Black"):
                self.gameOver = True
                self.winner = self.turn
                self.pgn = self.pgn + "#1-0"
        else:
            if self.checkForMate("White"):
                self.gameOver = True
                self.winner = self.turn
                self.pgn = self.pgn + "#0-1"
        
        if self.checkForCheck("White" if self.turn == "Black" else "Black") and not self.gameOver:
            self.pgn = self.pgn + "+"

        numberOfKnights = [0,0] #[white, black]
        numberOfBishops = [0,0] #[white, black]
        numberOfRooks = [0,0]   #[white, black]
        numberOfQueens = [0,0]  #[white, black]
        numberOfPawns = 0
        for row in self.board:
            for piece in row:
                if piece != EMPTY:
                    if piece.name == WPAWN or piece.name == BPAWN:
                        numberOfPawns += 1
                    elif piece.name == WKNIGHT:
                        numberOfKnights[0] += 1
                    elif piece.name == BKNIGHT:
                        numberOfKnights[1] += 1
                    elif piece.name == WBISHOP:
                        numberOfBishops[0] += 1
                    elif piece.name == BBISHOP:
                        numberOfBishops[1] += 1
                    elif piece.name == WROOK:
                        numberOfRooks[0] += 1
                    elif piece.name == BROOK:
                        numberOfRooks[1] += 1
                    elif piece.name == WQUEEN:
                        numberOfQueens[0] += 1
                    elif piece.name == BQUEEN:
                        numberOfQueens[1] += 1
        
        if numberOfPawns == 0:
            if numberOfQueens[0] == 0 and numberOfQueens[1] == 0 and numberOfRooks[0] == 0 and numberOfRooks[1] == 0:
                if numberOfBishops[0] == 0 and numberOfBishops[1] == 0 and numberOfKnights[0] == 0 and numberOfKnights[1] == 0:
                    self.gameOver = True
                    self.winner = "Draw"
                elif numberOfBishops[0] == 0 and numberOfBishops[1] == 0 and (numberOfKnights[1] == 1 or numberOfKnights[1] == 1):
                    self.gameOver = True
                    self.winner = "Draw"
                elif numberOfKnights[0] == 0 and numberOfKnights[1] == 0:
                    if ((numberOfBishops[0] == 1 and numberOfBishops[1] == 0) or (numberOfBishops[0] == 0 and numberOfBishops[1] == 1)):
                        self.gameOver = True
                        self.winner = "Draw"

                    elif (numberOfBishops[0] == 1 and numberOfBishops[1] == 1):
                        for row in range(8):
                            for col in range(8):
                                if self.board[row][col] != EMPTY:
                                    if self.board[row][col].name == WBISHOP:
                                        whiteBishopPosition = [row,col]
                                    elif self.board[row][col].name == BBISHOP:
                                        blackBishopPosition = [row,col]
                        if ((whiteBishopPosition[0] + whiteBishopPosition[1]) % 2 == 0 and (blackBishopPosition[0] + blackBishopPosition[1]) % 2 == 0) or ((whiteBishopPosition[0] + whiteBishopPosition[1]) % 2 != 0 and (blackBishopPosition[0] + blackBishopPosition[1]) % 2 != 0):
                            self.gameOver = True
                            self.winner = "Draw"

        self.moveHistory.append([self.startPos, self.endPos])

        self.startPos = self.endPos = None
        self.turn = "White" if self.turn == "Black" else "Black"
        
        # stalemate check
        allMoves = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] != EMPTY and self.board[row][col].colour == self.turn:
                    moves = self.validMoves([row,col])
                    for move in moves:
                        allMoves.append(move)
        if len(allMoves) == 0 and self.winner == None:
            self.gameOver = True
            self.winner = "Draw"
        
        if self.winner == "Draw":
            self.pgn = self.pgn + "1/2-1/2"
        
        
        self.pgn = self.pgn + " "

        temp = []
        for row in range(8):
            r = []
            for col in range(8):
                if self.board[row][col] == EMPTY:
                    r.append(EMPTY)
                else:
                    if self.board[row][col].name[5:] == "Pawn":
                        r.append(Pawn(self.board[row][col].name[:5]))
                    elif self.board[row][col].name[5:] == "Knight":
                        r.append(Knight(self.board[row][col].name[:5]))
                    elif self.board[row][col].name[5:] == "Bishop":
                        r.append(Bishop(self.board[row][col].name[:5]))
                    elif self.board[row][col].name[5:] == "Rook":
                        r.append(Rook(self.board[row][col].name[:5]))
                    elif self.board[row][col].name[5:] == "Queen":
                        r.append(Queen(self.board[row][col].name[:5]))
                    elif self.board[row][col].name[5:] == "King":
                        r.append(King(self.board[row][col].name[:5]))
                    if self.board[row][col].moved:
                        r[len(r) - 1].moved = True
            temp.append(r)
        self.history.append(temp)
        self.variableHistory.append([copy.deepcopy(self.gameOver), copy.deepcopy(self.winner), copy.deepcopy(self.enpassent), copy.deepcopy(self.enpassentPosition), copy.deepcopy(self.needToPromote), copy.deepcopy(self.promoteToPiece)])

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
                        if startPos[0] + 1 != 7:
                            moves.append([startPos[0] + 1, startPos[1]])
                        else:
                            moves.append([startPos[0] + 1, startPos[1], BKNIGHT])
                            moves.append([startPos[0] + 1, startPos[1], BBISHOP])
                            moves.append([startPos[0] + 1, startPos[1], BROOK])
                            moves.append([startPos[0] + 1, startPos[1], BQUEEN])

                        if startPos[0] == 1 and self.board[startPos[0] + 2][startPos[1]] == EMPTY:
                            moves.append([startPos[0] + 2, startPos[1]])
                    
                    if startPos[1] + 1 < 8 and (self.board[startPos[0] + 1][startPos[1] + 1] != EMPTY and self.board[startPos[0] + 1][startPos[1] + 1].colour != colour):
                        if startPos[0] + 1 != 7:
                            moves.append([startPos[0] + 1, startPos[1] + 1])
                        else:
                            moves.append([startPos[0] + 1, startPos[1] + 1, BKNIGHT])
                            moves.append([startPos[0] + 1, startPos[1] + 1, BBISHOP])
                            moves.append([startPos[0] + 1, startPos[1] + 1, BROOK])
                            moves.append([startPos[0] + 1, startPos[1] + 1, BQUEEN])
                        
                    if startPos[1] - 1 > -1 and (self.board[startPos[0] + 1][startPos[1] - 1] != EMPTY and self.board[startPos[0] + 1][startPos[1] - 1].colour != colour):
                        if startPos[0] + 1 != 7:
                            moves.append([startPos[0] + 1, startPos[1] - 1])
                        else:
                            moves.append([startPos[0] + 1, startPos[1] - 1, BKNIGHT])
                            moves.append([startPos[0] + 1, startPos[1] - 1, BBISHOP])
                            moves.append([startPos[0] + 1, startPos[1] - 1, BROOK])
                            moves.append([startPos[0] + 1, startPos[1] - 1, BQUEEN])
                        

                    if self.enpassent and startPos[1] + 1 < 8 and self.board[startPos[0] + 1][startPos[1] + 1] == EMPTY and self.enpassentPosition == [startPos[0], startPos[1] + 1] and self.board[startPos[0]][startPos[1] + 1].colour != colour:
                        moves.append([startPos[0] + 1, startPos[1] + 1])
                    
                    if self.enpassent and startPos[1] - 1 > -1 and self.board[startPos[0] + 1][startPos[1] - 1] == EMPTY and self.enpassentPosition == [startPos[0], startPos[1] - 1] and self.board[startPos[0]][startPos[1] - 1].colour != colour:
                        moves.append([startPos[0] + 1, startPos[1] - 1])

            elif self.board[startPos[0]][startPos[1]].name == WPAWN:
                if startPos[0] - 1  > -1:
                    if self.board[startPos[0] - 1][startPos[1]] == EMPTY:
                        if startPos[0] - 1  != 0:
                            moves.append([startPos[0] - 1, startPos[1]])
                        else:
                            moves.append([startPos[0] - 1, startPos[1], WKNIGHT])
                            moves.append([startPos[0] - 1, startPos[1], WBISHOP])
                            moves.append([startPos[0] - 1, startPos[1], WROOK])
                            moves.append([startPos[0] - 1, startPos[1], WQUEEN])
                            
                        if startPos[0] == 6 and self.board[startPos[0] - 2][startPos[1]] == EMPTY:
                            moves.append([startPos[0] - 2, startPos[1]])
                    
                    if startPos[1] + 1 < 8 and (self.board[startPos[0] - 1][startPos[1] + 1] != EMPTY and self.board[startPos[0] - 1][startPos[1] + 1].colour != colour):
                        if startPos[0] - 1  != 0:
                            moves.append([startPos[0] - 1, startPos[1] + 1])
                        else:
                            moves.append([startPos[0] - 1, startPos[1] + 1, WKNIGHT])
                            moves.append([startPos[0] - 1, startPos[1] + 1, WBISHOP])
                            moves.append([startPos[0] - 1, startPos[1] + 1, WROOK])
                            moves.append([startPos[0] - 1, startPos[1] + 1, WQUEEN])
                    
                    if startPos[1] - 1 > -1 and (self.board[startPos[0] - 1][startPos[1] - 1] != EMPTY and self.board[startPos[0] - 1][startPos[1] - 1].colour != colour):
                        if startPos[0] - 1  != 0:
                            moves.append([startPos[0] - 1, startPos[1] - 1])
                        else:
                            moves.append([startPos[0] - 1, startPos[1] - 1, WKNIGHT])
                            moves.append([startPos[0] - 1, startPos[1] - 1, WBISHOP])
                            moves.append([startPos[0] - 1, startPos[1] - 1, WROOK])
                            moves.append([startPos[0] - 1, startPos[1] - 1, WQUEEN])
                    
                    if self.enpassent and startPos[1] + 1 < 8 and self.board[startPos[0] - 1][startPos[1] + 1] == EMPTY and self.enpassentPosition == [startPos[0], startPos[1] + 1] and self.board[startPos[0]][startPos[1] + 1].colour != colour:
                        moves.append([startPos[0] - 1, startPos[1] + 1])
                    
                    if self.enpassent and startPos[1] - 1 > -1 and self.board[startPos[0] - 1][startPos[1] - 1] == EMPTY and self.enpassentPosition == [startPos[0], startPos[1] - 1] and self.board[startPos[0]][startPos[1] - 1].colour != colour:
                        moves.append([startPos[0] - 1, startPos[1] - 1])                   

            elif self.board[startPos[0]][startPos[1]].name == WKNIGHT or self.board[startPos[0]][startPos[1]].name == BKNIGHT:
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

    def undoMove(self):
        if len(self.history) > 1:
            self.history.pop()
            self.variableHistory.pop()
            self.moveHistory.pop()
            temp = []
            for row in range(8):
                r = []
                for col in range(8):
                    if self.history[len(self.history) - 1][row][col] == EMPTY:
                        r.append(EMPTY)
                    else:
                        if self.history[len(self.history) - 1][row][col].name[5:] == "Pawn":
                            r.append(Pawn(self.history[len(self.history) - 1][row][col].name[:5]))
                        elif self.history[len(self.history) - 1][row][col].name[5:] == "Knight":
                            r.append(Knight(self.history[len(self.history) - 1][row][col].name[:5]))
                        elif self.history[len(self.history) - 1][row][col].name[5:] == "Bishop":
                            r.append(Bishop(self.history[len(self.history) - 1][row][col].name[:5]))
                        elif self.history[len(self.history) - 1][row][col].name[5:] == "Rook":
                            r.append(Rook(self.history[len(self.history) - 1][row][col].name[:5]))
                        elif self.history[len(self.history) - 1][row][col].name[5:] == "Queen":
                            r.append(Queen(self.history[len(self.history) - 1][row][col].name[:5]))
                        elif self.history[len(self.history) - 1][row][col].name[5:] == "King":
                            r.append(King(self.history[len(self.history) - 1][row][col].name[:5]))
                        if self.history[len(self.history) - 1][row][col].moved:
                            r[len(r) - 1].moved = True
                temp.append(r)
            self.board = temp
            self.gameOver, self.winner, self.enpassent, self.enpassentPosition, self.needToPromote, self.promoteToPiece = copy.deepcopy(self.variableHistory[len(self.variableHistory) - 1][0]), copy.deepcopy(self.variableHistory[len(self.variableHistory) - 1][1]), copy.deepcopy(self.variableHistory[len(self.variableHistory) - 1][2]), copy.deepcopy(self.variableHistory[len(self.variableHistory) - 1][3]), copy.deepcopy(self.variableHistory[len(self.variableHistory) - 1][4]), copy.deepcopy(self.variableHistory[len(self.variableHistory) - 1][5])
            self.turn = "White" if self.turn == "Black" else "Black"
            self.startPos = None
            self.endPos = None
            if len(self.pgn) > 0:
                self.pgn = self.pgn[:len(self.pgn) - 1]
            self.pgn = self.pgn
            while len(self.pgn) > 0 and self.pgn[len(self.pgn)-1] != " ":
                self.pgn = self.pgn[:len(self.pgn) - 1]
        
    def allMoves(self):
        allmoves = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] != EMPTY and self.board[row][col].colour == self.turn:
                    moves = self.validMoves([row,col])
                    for move in moves:
                        allmoves.append([[row,col], move])
        return allmoves

    def indexCoordinateTranslate(self, data):
        if type(data) is list: #[row,column] to filerank
            return chr(data[1] + 97) + str(8 - data[0])
        elif type(data) is str: #filerank to [row,column]
            return [8 - int(data[1]), ord(data[0]) - 97]
