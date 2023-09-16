import pygame
from constants import *
from widgets import TextBox, Button, Label
from game import Game
import socket
import random

def close():
    pygame.quit()

def getColours(SERVER, username):
    SERVER.send("[THEME]".encode())
    SERVER.recv(BYTES).decode()
    SERVER.send(username.encode())
    d = eval(SERVER.recv(BYTES).decode())
    SERVER.send("Recieved".encode())
    l = eval(SERVER.recv(BYTES).decode())
    SERVER.send("Recieved".encode())
    h = eval(SERVER.recv(BYTES).decode())
    return d, l, h

def evaluate(board, colour):
    knightScores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

    bishopScores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                    [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                    [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                    [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                    [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                    [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                    [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                    [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

    rookScores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

    queenScores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                    [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                    [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                    [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                    [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                    [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                    [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                    [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

    whitePawnScores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
                [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
                [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
                [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
                [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
                [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
                [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
                [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]
    
    blackPawnScores = [[0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
                [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
                [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
                [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
                [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
                [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
                [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
                [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]]
    value = 0
    for row in board.board:
        for piece in row:
            if piece != EMPTY:
                if piece.colour == colour:
                    value = value + piece.value
                else:
                    value = value - piece.value
    for row in range(8):
        for col in range(8):
            if board.board[row][col] != EMPTY:
                name = board.board[row][col].name
                thisColour = board.board[row][col].colour
                if thisColour == colour:
                    if name == BPAWN:
                        value = value + blackPawnScores[row][col]
                    if name == WPAWN:
                        value = value + whitePawnScores[row][col]
                    if name == WKNIGHT or name == BKNIGHT:
                        value = value + knightScores[row][col]
                    if name == WBISHOP or name == BBISHOP:
                        value = value + bishopScores[row][col]
                    if name == WROOK or name == BROOK:
                        value = value + rookScores[row][col]
                    if name == WQUEEN or name == BQUEEN:
                        value = value + queenScores[row][col]
                else:
                    if thisColour == colour:
                        if name == BPAWN:
                            value = value - blackPawnScores[row][col]
                        if name == WPAWN:
                            value = value - whitePawnScores[row][col]
                        if name == WKNIGHT or name == BKNIGHT:
                            value = value - knightScores[row][col]
                        if name == WBISHOP or name == BBISHOP:
                            value = value - bishopScores[row][col]
                        if name == WROOK or name == BROOK:
                            value = value - rookScores[row][col]
                        if name == WQUEEN or name == BQUEEN:
                            value = value - queenScores[row][col]

    return value

def negamax(board, depth, alpha, beta, colour):
    if depth == 0 or board.gameOver:
        return evaluate(board, colour)
    maximum = -10000
    moves = board.allMoves()
    random.shuffle(moves)
    for move in moves:
        board.startPos = move[0]
        board.endPos = move[1]
        board.makeMove()
        value = -negamax(board, depth - 1, -alpha, -beta, "White" if colour == "Black" else "Black")
        maximum = max(value, maximum)
        board.undoMove()
        alpha = max(alpha, value)
        if beta <= alpha:
            return maximum
    return maximum

def getAIMove(board, depth, AIColour):
    moves = board.allMoves()
    max = -10000
    for move in moves:
        board.startPos = move[0]
        board.endPos = move[1]
        board.makeMove()

        value = -negamax(board, depth - 1, -10000, 10000, AIColour)
        board.undoMove()
        if value > max:
            max = value
            bestMove = move
    return bestMove

def onePlayer(SCREEN, SERVER, username, depth):
    board = Game(SCREEN)
    d, l, h = getColours(SERVER, username)
    backButton = Button(SCREEN, 1110, 650, 280, 100, "Back")
    label = Label(SCREEN, 1194, 450, "")
    colour = "White" if random.randint(0,1) == 0 else "Black"
    AIColour = "White" if colour == "Black" else "Black"
    board.flipped = True if colour == "Black" else False
    run = True
    while run:
        SCREEN.fill(DARKGREY)
        board.drawBoard(300, 0, d, l, h)
        if board.gameOver:
            if board.winner != "Draw":
                label.setText(board.winner + " Wins!!")
            else:
                label.setText(board.winner)
            label.draw()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if board.turn == colour:
                    board.action()
                    board.drawBoard(300, 0, d, l, h)
                if backButton.clicked():
                    mainMenu(SCREEN, SERVER, username)
                    return
            if event.type == pygame.QUIT:
                run = False
        backButton.draw()
        pygame.display.flip()
        if board.turn == AIColour and not board.gameOver:
            move = getAIMove(board, depth, AIColour)
            board.startPos = move[0]
            board.endPos = move[1]
            board.action()
    close()        

def levelChooser(SCREEN, SERVER, username):
    board = Game(SCREEN)
    d, l, h = getColours(SERVER, username)
    backButton = Button(SCREEN, 1110, 650, 280, 100, "Back")
    easy = Button(SCREEN, 500, 250, 400, 100, "Easy", BLACK)
    medium = Button(SCREEN, 500, 350, 400, 100, "Medium", BLACK)
    hard = Button(SCREEN, 500, 450, 400, 100, "Hard", BLACK)
    run = True
    while run:
        SCREEN.fill(DARKGREY)
        board.flipped = board.turn == "Black"
        board.drawBoard(300, 0, d, l, h)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backButton.clicked():
                    mainMenu(SCREEN, SERVER, username)
                    return
                if easy.clicked():
                    onePlayer(SCREEN, SERVER, username, 1)
                elif medium.clicked():
                    onePlayer(SCREEN, SERVER, username, 2)
                elif hard.clicked():
                    onePlayer(SCREEN, SERVER, username, 3)

            if event.type == pygame.QUIT:
                run = False
        easy.draw()
        medium.draw()
        hard.draw()
        backButton.draw()
        pygame.display.flip()
    close()

def twoPlayer(SCREEN, SERVER, username):
    board = Game(SCREEN)
    d, l, h = getColours(SERVER, username)
    backButton = Button(SCREEN, 1110, 650, 280, 100, "Back")
    undoButton = Button(SCREEN, 1110, 525, 280, 100, "Undo")
    label = Label(SCREEN, 1194, 450, "")
    run = True
    while run:
        SCREEN.fill(DARKGREY)
        board.flipped = board.turn == "Black"
        board.drawBoard(300, 0, d, l, h)
        if board.gameOver:
            if board.winner != "Draw":
                label.setText(board.winner + " Wins!!")
            else:
                label.setText(board.winner)
            label.draw()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.action()
                if backButton.clicked():
                    mainMenu(SCREEN, SERVER, username)
                    return
                if undoButton.clicked():
                    board.undoMove()
            if event.type == pygame.QUIT:
                run = False
        undoButton.draw()
        backButton.draw()
        pygame.display.flip()
    close()

def local(SCREEN, SERVER, username):
    board = Game(SCREEN)
    d, l, h = getColours(SERVER, username)
    label = Label(SCREEN, 1155, 450, "Waiting for players")
    backButton = Button(SCREEN, 1110, 650, 280, 100, "Back")

    SERVER.send("[LOCAL]".encode())
    SERVER.recv(BYTES).decode()

    run = True
    while run:
        SCREEN.fill(DARKGREY)
        board.drawBoard(300, 0, d, l, h)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backButton.clicked():
                    SERVER.send("Stop".encode())
                    mainMenu(SCREEN, SERVER, username)
                    return
            if event.type == pygame.QUIT:
                SERVER.send("Stop".encode())
                pygame.quit()
                return
        label.draw()
        backButton.draw()
        SERVER.send("Waiting".encode())
        data = SERVER.recv(BYTES).decode()
        if data == "Found Match":
            run = False
        pygame.display.flip()
    SERVER.send("Ready".encode())
    
    colour = SERVER.recv(BYTES).decode()
    board.flipped = colour == "Black"
    run = True
    while run:
        SCREEN.fill(DARKGREY)
        board.drawBoard(300, 0 ,d, l, h)
        data = "Waiting"
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if board.turn == colour:
                    move = board.action()
                    if move:
                        data = str(move)
                if backButton.clicked():
                    SERVER.send("Resign".encode())
                    mainMenu(SCREEN, SERVER, username)
                    return
            if event.type == pygame.QUIT:
                SERVER.send("Resign".encode())
                pygame.quit()
                return
        SERVER.send(data.encode())
        data = SERVER.recv(BYTES).decode()
        if data == "Resign":
            run = False
        elif data != "Waiting":
            opponentsMove = eval(data)
            board.startPos = opponentsMove[0]
            board.endPos = opponentsMove[1]
            board.action()
            if board.gameOver:
                SERVER.send("Resign".encode())
                mainMenu(SCREEN, SERVER, username)
                return
        backButton.draw()
        pygame.display.flip()
    mainMenu(SCREEN, SERVER, username)

def rules(SCREEN, SERVER, username):
    rulesImage = pygame.image.load("Assets/Rules.png").convert_alpha()
    backButton = Button(SCREEN, 1110, 650, 280, 100, "Back")
    run = True
    while run:
        SCREEN.blit(rulesImage, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backButton.clicked():
                    mainMenu(SCREEN, SERVER, username)
                    return
            if event.type == pygame.QUIT:
                run = False
        backButton.draw()
        pygame.display.flip()
    close()


def mainMenu(SCREEN, SERVER, username):
    board = Game(SCREEN)
    localButton = Button(SCREEN, 1110, 50, 280, 100, "Local")
    twoPlayerButton = Button(SCREEN, 1110, 250, 280, 100, "Two Player")
    onePlayerButton = Button(SCREEN, 1110, 450, 280, 100, "One Player")
    archiveButton = Button(SCREEN, 1110, 650, 280, 100, "Archive")
    themesButton = Button(SCREEN, 10, 250, 280, 100, "Themes")
    rulesButton = Button(SCREEN, 10, 450, 280, 100, "Rules")
    settingsButton = Button(SCREEN, 10, 650, 280, 100, "Settings")
    LOGO = pygame.image.load("Assets/Logo.png").convert_alpha()
    d, l, h = getColours(SERVER, username)
    run = True
    while run:
        SCREEN.fill(DARKGREY)
        board.drawBoard(300,0, d, l, h)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if twoPlayerButton.clicked():
                    twoPlayer(SCREEN, SERVER, username)
                    return
                if localButton.clicked():
                    local(SCREEN, SERVER, username)
                    return
                if onePlayerButton.clicked():
                    levelChooser(SCREEN, SERVER, username)
                    return
                if rulesButton.clicked():
                    rules(SCREEN, SERVER, username)
                    return
            if event.type == pygame.QUIT:
                run = False
        localButton.draw()
        twoPlayerButton.draw()
        onePlayerButton.draw()
        archiveButton.draw()
        SCREEN.blit(LOGO, (10,50))
        themesButton.draw()
        rulesButton.draw()
        settingsButton.draw()
        pygame.display.flip()
    close()

def registerLogic(SERVER, fn, ln, u, p, cp):
    if fn and ln and u and p and cp:
        if p == cp:
            SERVER.send("[REGISTER]".encode())
            SERVER.recv(BYTES).decode()
            SERVER.send(fn.encode())
            SERVER.recv(BYTES).decode()
            SERVER.send(ln.encode())
            SERVER.recv(BYTES).decode()
            SERVER.send(u.encode())
            SERVER.recv(BYTES).decode()
            SERVER.send(p.encode())
            SERVER.recv(BYTES).decode()
            SERVER.send(cp.encode())
            result = SERVER.recv(BYTES).decode()
        else:
            result = "Passwords do not match"
    else:
        result = "Please fill in ALL the information"
    return True if result == "True" else result

def register(SCREEN, SERVER):
    firstName = TextBox(SCREEN, 133,50,500,100, "First Name")
    lastName = TextBox(SCREEN, 766,50,500,100, "Last Name")
    username = TextBox(SCREEN, 133,250,500,100, "Username")
    password = TextBox(SCREEN, 766,250,500,100, "Password")
    confirmPassword = TextBox(SCREEN, 133,450,500,100, "Confirm Password")
    registerButton = Button(SCREEN, 766, 450, 500, 100, "Create Account")
    back = Button(SCREEN, 450, 650, 500, 100, "Back")
    output = Label(SCREEN, 500, 575, "")

    run = True
    while run:
        SCREEN.fill(DARKGREY)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if registerButton.clicked():
                    result = registerLogic(SERVER, firstName.text, lastName.text, username.text, password.text, confirmPassword.text)
                    if result == True:
                        login(SCREEN, SERVER)
                        return
                    else:
                        output.setText(result)
                if back.clicked():
                    login(SCREEN, SERVER)
                    return
                firstName.toggleSelected()
                lastName.toggleSelected()
                username.toggleSelected()
                password.toggleSelected()
                confirmPassword.toggleSelected()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    result = registerLogic(SERVER, firstName.text, lastName.text, username.text, password.text, confirmPassword.text)
                    if result == True:
                        login(SCREEN, SERVER)
                        return
                if event.key == pygame.K_BACKSPACE:
                    firstName.remove()
                    lastName.remove()
                    username.remove()
                    password.remove()
                    confirmPassword.remove()
            if event.type == pygame.TEXTINPUT:
                firstName.add(event.text)
                lastName.add(event.text)
                username.add(event.text)
                password.add(event.text)
                confirmPassword.add(event.text)
            if event.type == pygame.QUIT:
                run = False
        firstName.draw()
        lastName.draw()
        username.draw()
        password.draw(show="*")
        confirmPassword.draw(show="*")
        registerButton.draw()
        back.draw()
        output.draw()
        pygame.display.flip()
    close()

def successfulLogin(SERVER, username, password):
    if not username or not password:
        return False
    
    SERVER.send("[LOGIN]".encode())
    SERVER.recv(BYTES).decode()
    SERVER.send(username.encode())
    SERVER.recv(BYTES).decode()
    SERVER.send(password.encode())
    result = SERVER.recv(BYTES).decode()
    return True if result == "True" else False

def login(SCREEN, SERVER):
    loginButton = Button(SCREEN, 450,450,500,100, "Login")
    registerButton = Button(SCREEN, 450,650,500,100, "Create an account")
    username = TextBox(SCREEN, 450,50,500,100, "Username")
    password = TextBox(SCREEN, 450,250,500,100, "Password")
    incorrectLabel = Label(SCREEN,550,590,"")
    run = True
    while run:
        SCREEN.fill(DARKGREY)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if loginButton.clicked():
                    if successfulLogin(SERVER, username.text, password.text):
                        mainMenu(SCREEN, SERVER, username.text)
                        return
                    else:
                        incorrectLabel.setText("Incorrect Username or password")
                if registerButton.clicked():
                    register(SCREEN, SERVER)    
                    return
                username.toggleSelected()
                password.toggleSelected()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if successfulLogin(SERVER, username.text, password.text):
                        mainMenu(SCREEN, SERVER, username.text)
                        return
                    else:
                        incorrectLabel.setText("Incorrect Username or password")
                if event.key == pygame.K_BACKSPACE:
                    username.remove()
                    password.remove()
            if event.type == pygame.TEXTINPUT:
                username.add(event.text)
                password.add(event.text)
            if event.type == pygame.QUIT:
                run = False
        loginButton.draw()
        registerButton.draw()
        incorrectLabel.draw()
        username.draw()
        password.draw(show="*")
        pygame.display.flip()
    close()

def start():
    try:
        SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SERVER.connect((HOST, PORT))
    except:
        print("Server Not Online")
        return
    pygame.init()
    SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Chess")
    login(SCREEN, SERVER)

if __name__ == "__main__":
    start()