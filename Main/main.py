import pygame
from constants import *
from widgets import TextBox, Button, Label
from game import Game
import socket
import random
from Stack import Stack

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
    if board.gameOver:
        if board.winner == colour:
            return 1000
        elif board.winner == "Draw":
            return 0
        else:
            return -1000

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
    if depth == 0 or board.winner != "":
        print(board.moveHistory[2:], "eval: ", round(evaluate(board, colour)), "Colour: ", colour)
        return None, evaluate(board, colour)
    maximum = -100000000
    moves = board.allMoves()
    # random.shuffle(moves)
    for move in moves:
        board.startPos = move[0]
        board.endPos = move[1]
        board.makeMove()
        currentMove, value = negamax(board, depth - 1, -alpha, -beta, "White" if colour=="Black" else "Black")
        board.undoMove() 
        value = -value if depth == 1 else value
        if value**2 == 1000000:
            print(value, maximum) 
        if value > maximum:
            maximum = value
            bestMove = move
        alpha = max(alpha, value)
        if beta <= alpha:
            return bestMove, maximum
    return bestMove, maximum

def onePlayer(SCREEN, SERVER, username, depth):
    board = Game(SCREEN)
    d, l, h = getColours(SERVER, username)
    backButton = Button(SCREEN, 1110, 650, 280, 100, "Back")
    label = Label(SCREEN, 1194, 450, "")
    colour = "White" if random.randint(0,0) == 0 else "Black"
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
            move, v = negamax(board, depth, -10000, 10000, AIColour)
            print(move, v)
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

def themes(SCREEN, SERVER, username):
    theme1 = Button(SCREEN, 50, 100, 200, 200, "")
    theme2 = Button(SCREEN, 50, 500, 200, 200, "")
    theme3 = Button(SCREEN, 1150, 100, 200, 200, "")
    theme4 = Button(SCREEN, 1150, 500, 200, 200, "")
    board = Game(SCREEN)
    d, l, h = getColours(SERVER, username)
    SERVER.send("[GETALLCOLOURS]".encode())
    data = eval(SERVER.recv(BYTES).decode())

    colours = []
    for theme in data:
        for colour in theme:
            colours.append(tuple([int(colour) for colour in colour.split(",")]))
    
    run = True
    while run:
        SCREEN.fill(DARKGREY)
        board.drawBoard(300, 0, d, l, h)

        pygame.draw.rect(SCREEN,colours[1],(50,100,100,100))
        pygame.draw.rect(SCREEN,colours[0],(150,100,100,100))
        pygame.draw.rect(SCREEN,colours[0],(50,200,100,100))
        pygame.draw.rect(SCREEN,colours[1],(150,200,100,100))
        pygame.draw.rect(SCREEN,colours[2],(50,100,200,200), 5)

        pygame.draw.rect(SCREEN,colours[4],(50,500,100,100))
        pygame.draw.rect(SCREEN,colours[3],(150,500,100,100))
        pygame.draw.rect(SCREEN,colours[3],(50,600,100,100))
        pygame.draw.rect(SCREEN,colours[4],(150,600,100,100))
        pygame.draw.rect(SCREEN,colours[5],(50,500,200,200), 5)

        pygame.draw.rect(SCREEN,colours[7],(1150,100,100,100))
        pygame.draw.rect(SCREEN,colours[6],(1250,100,100,100))
        pygame.draw.rect(SCREEN,colours[6],(1150,200,100,100))
        pygame.draw.rect(SCREEN,colours[7],(1250,200,100,100))
        pygame.draw.rect(SCREEN,colours[8],(1150,100,200,200), 5)

        pygame.draw.rect(SCREEN,colours[10],(1150,500,100,100))
        pygame.draw.rect(SCREEN,colours[9],(1250,500,100,100))
        pygame.draw.rect(SCREEN,colours[9],(1150,600,100,100))
        pygame.draw.rect(SCREEN,colours[10],(1250,600,100,100))
        pygame.draw.rect(SCREEN,colours[11],(1150,500,200,200), 5)

        if theme1.clicked():
            d, l, h = colours[0], colours[1], colours[2]
        if theme2.clicked():
            d, l, h = colours[3], colours[4], colours[5]
        if theme3.clicked():
            d, l, h = colours[6], colours[7], colours[8]
        if theme4.clicked():
            d, l, h = colours[9], colours[10], colours[11]
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if theme1.clicked():
                    SERVER.send("[SETTHEME]".encode())
                    SERVER.recv(BYTES).decode()
                    SERVER.send(str([username, 1]).encode())
                    SERVER.recv(BYTES).decode()
                    mainMenu(SCREEN, SERVER, username)
                    return
                if theme2.clicked():
                    SERVER.send("[SETTHEME]".encode())
                    SERVER.recv(BYTES).decode()
                    SERVER.send(str([username, 2]).encode())
                    SERVER.recv(BYTES).decode()
                    mainMenu(SCREEN, SERVER, username)
                    return
                if theme3.clicked():
                    SERVER.send("[SETTHEME]".encode())
                    SERVER.recv(BYTES).decode()
                    SERVER.send(str([username, 3]).encode())
                    SERVER.recv(BYTES).decode()
                    mainMenu(SCREEN, SERVER, username)
                    return
                if theme4.clicked():
                    SERVER.send("[SETTHEME]".encode())
                    SERVER.recv(BYTES).decode()
                    SERVER.send(str([username, 4]).encode())
                    SERVER.recv(BYTES).decode()
                    mainMenu(SCREEN, SERVER, username)
                    return
                
            if event.type == pygame.QUIT:
                run = False
        pygame.display.flip()
    close()

def adminRegisterLogic(SEVER, fn, ln, u, p, cp):
    if fn and ln and u and p and cp:
        if p == cp:
            if len(p) > 8:
                symbol = False
                capital = False
                number = False
                for character in p:
                    if character.isnumeric():
                        number = True
                    elif character.isalpha() and character.isupper():
                        capital = True
                    elif not character.isalpha():
                        symbol = True
                
                if symbol and capital and number:
                    SEVER.send("[CREATEADMIN]".encode())
                    SEVER.recv(BYTES).decode()
                    SEVER.send(str([fn,ln,u,p,cp]).encode())
                    result = SEVER.recv(BYTES).decode()
                else:
                    result = "Password needs to contain an uppercase, symbol and number"
            else:
                result = "Password is too short"
        else:
            result = "Passwords do not match"
    else:
        result = "Please enter all the information"
    return True if result == "True" else result

def createAdmin(SCREEN, SERVER, username, i, j):
    firstName = TextBox(SCREEN, 133,50,500,100, "First Name")
    lastName = TextBox(SCREEN, 766,50,500,100, "Last Name")
    usernameBox = TextBox(SCREEN, 133,250,500,100, "Username")
    password = TextBox(SCREEN, 766,250,500,100, "Password")
    confirmPassword = TextBox(SCREEN, 133,450,500,100, "Confirm Password")
    registerButton = Button(SCREEN, 766, 450, 500, 100, "Create Admin")
    back = Button(SCREEN, 450, 650, 500, 100, "Back")
    output = Label(SCREEN, 500, 575, "")

    run = True
    while run:
        SCREEN.fill(DARKGREY)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if registerButton.clicked():
                    result = adminRegisterLogic(SERVER, firstName.text, lastName.text, usernameBox.text, password.text, confirmPassword.text)
                    if result == True:
                        adminSettings(SCREEN, SERVER, username, i, j)
                        return
                    else:
                        output.setText(result)
                if back.clicked():
                    adminSettings(SCREEN, SERVER, username, i, j)
                    return
                firstName.toggleSelected()
                lastName.toggleSelected()
                usernameBox.toggleSelected()
                password.toggleSelected()
                confirmPassword.toggleSelected()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    firstName.remove()
                    lastName.remove()
                    usernameBox.remove()
                    password.remove()
                    confirmPassword.remove()
            if event.type == pygame.TEXTINPUT:
                firstName.add(event.text)
                lastName.add(event.text)
                usernameBox.add(event.text)
                password.add(event.text)
                confirmPassword.add(event.text)
            if event.type == pygame.QUIT:
                run = False
        firstName.draw()
        lastName.draw()
        usernameBox.draw()
        password.draw(show="*")
        confirmPassword.draw(show="*")
        registerButton.draw()
        back.draw()
        output.draw()
        pygame.display.flip()
    close()

def viewUser(SCREEN, SERVER, username, userDetails, i, j):
    label = Label(SCREEN, 450, 75, userDetails)
    resetPasswordButton = Button(SCREEN, 450, 250, 500, 100, "Reset Password: Password_123")
    deleteUserButton = Button(SCREEN, 450, 450, 500, 100, "Delete User")
    backButton = Button(SCREEN, 450, 650, 500, 100, "Back")

    run = True
    while run:
        SCREEN.fill(DARKGREY)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resetPasswordButton.clicked():
                    SERVER.send("[RESETPASSWORD]".encode())
                    SERVER.recv(BYTES).decode()
                    SERVER.send(str(eval(userDetails)[0]).encode())
                    SERVER.recv(BYTES).decode()
                    adminSettings(SCREEN, SERVER, username, i, j)
                    return
                if deleteUserButton.clicked():
                    SERVER.send('[DELETEUSER]'.encode())
                    SERVER.recv(BYTES).decode()
                    SERVER.send(str(eval(userDetails)[0]).encode())
                    SERVER.recv(BYTES).decode()
                    adminSettings(SCREEN, SERVER, username, i, j)
                    return
                if backButton.clicked():
                    adminSettings(SCREEN, SERVER, username, i, j)
                    return
            if event.type == pygame.QUIT:
                run = False

        label.draw()
        resetPasswordButton.draw()
        deleteUserButton.draw()
        backButton.draw()
        pygame.display.flip()
    close()

def sortUsers(array, index): ## Merge Sort
    if len(array) > 1:
        left = array[:len(array)//2]
        right = array[len(array)//2:]

        sortUsers(left, index)
        sortUsers(right, index)

        i = 0
        j = 0
        k = 0
        while i < len(left) and j < len(right):
            if left[i][index].lower() < right[j][index].lower():
                array[k] = left[i]
                i += 1
            else:
                array[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            array[k] = left[i]
            i += 1
            k += 1
        
        while j < len(right):
            array[k] = right[j]
            j += 1
            k += 1

def adminSettings(SCREEN, SERVER, username, i, j):
    page = 1
    resetAttendance = Button(SCREEN, 133,50,500,100, "Reset/Erase Attendance")
    createAdminButton = Button(SCREEN, 766,50,500,100, "Create Admin")
    backButton = Button(SCREEN, 450,650,500,100, "Back")
    previousButton = Button(SCREEN, 300, 535, 400, 60, "Previous")
    nextButton = Button(SCREEN, 700, 535, 400, 60, "Next")
    sortButton = Button(SCREEN,25, 250, 250, 100, "Sort: Username")
    ascendingButton = Button(SCREEN,1125, 250, 250, 100, "Ascending")
    if j == 1:
        ascendingButton.setText("Descending")

    if i == 1:
        sortButton.setText("Sort: First Name")
    elif i == 2:
        sortButton.setText("Sort: Last Name")
    elif i == 3:
        sortButton.setText("Sort: Account")

    SERVER.send("[FETCHUSERS]".encode())
    userdata = eval(SERVER.recv(BYTES).decode()) ## [username, first name, last name, account type]
    
    sortUsers(userdata, i)
    
    if j == 1:
        a = Stack()
        for user in userdata:
            a.push(user)
        userdata = []
        while not a.isEmpty():
            userdata.append(a.pop())
        

    buttons = []
    index = 0
    count = 0
    
    while index != len(userdata):
        buttons.append(Button(SCREEN, 300, 175 + (count * 60), 800, 60, str(userdata[index])))
        index += 1
        count += 1
        if count == 6:
            count = 0

    run = True
    while run:
        SCREEN.fill(DARKGREY)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if createAdminButton.clicked():
                    createAdmin(SCREEN, SERVER, username, i, j)
                    return
                if resetAttendance.clicked():
                    SERVER.send("[ERASEATTENDANCE]".encode())
                    SERVER.recv(BYTES).decode()
                    settings(SCREEN, SERVER, username)
                    return
                if nextButton.clicked():
                    page = page + 1 if page < (len(userdata) / 6) else page
                if previousButton.clicked():
                    page = page - 1 if page != 1 else page
                if sortButton.clicked():
                    if i == 0:
                        adminSettings(SCREEN, SERVER, username, 1, j)
                        return
                    elif i == 1:
                        adminSettings(SCREEN, SERVER, username, 2, j)
                        return
                    elif i == 2:
                        adminSettings(SCREEN, SERVER, username, 3, j)
                        return
                    elif i == 3:
                        adminSettings(SCREEN, SERVER, username, 0, j)
                        return
                if ascendingButton.clicked():
                    adminSettings(SCREEN, SERVER, username, i, 0 if j == 1 else 1)
                    return
                if backButton.clicked():
                    settings(SCREEN, SERVER, username)
                    return
                
                for button in range(len(buttons)): #only check buttons which are displayed on the page
                    if button < 6 * page and button >= 6 * (page -1) and buttons[button].clicked():
                        viewUser(SCREEN, SERVER, username, buttons[button].text, i, j)
                        return

            if event.type == pygame.QUIT:
                run = False

        resetAttendance.draw()
        createAdminButton.draw()
        previousButton.draw()
        sortButton.draw()
        ascendingButton.draw()
        nextButton.draw()
        backButton.draw()
        for button in range(len(buttons)):
            if button >= 6 * (page - 1) and button < 6 * page:
                buttons[button].draw()
        pygame.display.flip()
    close()

def changePassword(SCREEN, SERVER, username):
    currentPassword = TextBox(SCREEN, 450,50,500,100, "Current password")
    newPassword = TextBox(SCREEN, 450,250,500,100, "New password")
    confirmPassword = TextBox(SCREEN, 450,450,500,100, "Confirm password")
    changePasswordButton = Button(SCREEN, 750,650,500,100, "Change Password")
    backButton = Button(SCREEN, 150, 650, 500, 100, "Back")
    resultLable = Label(SCREEN, 600, 600, "")
    run = True
    while run:
        SCREEN.fill(DARKGREY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.TEXTINPUT:
                currentPassword.add(event.text)
                newPassword.add(event.text)
                confirmPassword.add(event.text)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    currentPassword.remove()
                    newPassword.remove()
                    confirmPassword.remove()
            if event.type == pygame.MOUSEBUTTONDOWN:
                currentPassword.toggleSelected()
                newPassword.toggleSelected()
                confirmPassword.toggleSelected()
                if backButton.clicked():
                    settings(SCREEN, SERVER, username)
                    return
                if changePasswordButton.clicked():
                    if newPassword.text == confirmPassword.text:
                        if successfulLogin(SERVER, username, currentPassword.text):
                            SERVER.send("[CHANGEPASS]".encode())
                            SERVER.recv(BYTES).decode()
                            SERVER.send(str([username, newPassword.text]).encode())
                            currentPassword = TextBox(SCREEN, 450,50,500,100, "Current password")
                            newPassword = TextBox(SCREEN, 450,250,500,100, "New password")
                            confirmPassword = TextBox(SCREEN, 450,450,500,100, "Confirm password")
                            resultLable.setText("Succesfully Changed")
                        else:
                            resultLable.setText("Incorrect Password")
                    else:
                        resultLable.setText("Passwords don't match")
            
        currentPassword.draw(show="*")
        newPassword.draw(show="*")
        confirmPassword.draw(show="*")
        resultLable.draw()
        changePasswordButton.draw()
        backButton.draw()
        pygame.display.flip()
    close()

def changeName(SCREEN, SERVER, username):
    firsName = TextBox(SCREEN, 450,50,500,100, "First Name")
    lastName = TextBox(SCREEN, 450,250,500,100, "Last Name")
    saveButton = Button(SCREEN, 450,450,500,100, "Save")
    backButton = Button(SCREEN, 450,650,500,100, "Back")

    run = True
    while run:
        SCREEN.fill(DARKGREY)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                firsName.toggleSelected()
                lastName.toggleSelected()
                if saveButton.clicked() and firsName.text != "" and lastName.text != "":
                    SERVER.send("[CHANGENAME]".encode())
                    SERVER.recv(BYTES).decode()
                    SERVER.send(str([username, firsName.text, lastName.text]).encode())
                    SERVER.recv(BYTES).decode()
                    settings(SCREEN, SERVER, username)
                    return
                if backButton.clicked():
                    settings(SCREEN, SERVER, username)
                    return
            if event.type == pygame.TEXTINPUT:
                firsName.add(event.text)
                lastName.add(event.text)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                firsName.remove()
                lastName.remove()
            if event.type == pygame.QUIT:
                run = False
        firsName.draw()
        lastName.draw()
        saveButton.draw()
        backButton.draw()
        pygame.display.flip()
    close()

def settings(SCREEN, SERVER, username):
    SERVER.send("[ISADMIN]".encode())
    SERVER.recv(BYTES).decode()
    SERVER.send(username.encode())
    admin = True if SERVER.recv(BYTES).decode() == "True" else False
    adminButton = Button(SCREEN,450,50,500,100, "Admin Options") if admin else None

    SERVER.send("[GETDATA]".encode())
    SERVER.recv(BYTES).decode()
    SERVER.send(username.encode())
    data = eval(SERVER.recv(BYTES).decode())
    changePasswordButton = Button(SCREEN, 450, 450, 500, 100, "Change Password")
    usernameLable = Label(SCREEN, 100, 50, "ID Number: " + data[0]) if admin else Label(SCREEN, 450, 50, "ID Number: " + data[0])
    firstNameLable = Label(SCREEN, 100, 100, "First Name: " + data[1]) if admin else Label(SCREEN, 450, 100, "First Name: " + data[1])
    lastNameLable = Label(SCREEN, 100, 150, "Last Name: " + data[2]) if admin else Label(SCREEN, 450, 150, "Last Name: " + data[2])
    accountTypeLable = Label(SCREEN, 100, 200, "Account Type: " + data[3]) if admin else Label(SCREEN, 450, 200, "Account Type: " + data[3])
    
    changeNameButton = Button(SCREEN,450,250,500,100, "Change Name")
    logoutButton = Button(SCREEN,750,650,500,100, "Logout")
    backButton = Button(SCREEN, 150,650,500,100, "Back")

    run = True
    while run:
        SCREEN.fill(DARKGREY)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if changePasswordButton.clicked():
                    changePassword(SCREEN, SERVER, username)
                    return
                elif admin and adminButton.clicked():
                    adminSettings(SCREEN, SERVER, username, 0, 0)
                    return
                elif changeNameButton.clicked():
                    changeName(SCREEN, SERVER, username)
                    return
                elif logoutButton.clicked():
                    login(SCREEN, SERVER)
                    return
                if backButton.clicked():
                    mainMenu(SCREEN, SERVER, username)
                    return
                
            if event.type == pygame.QUIT:
                run = False

        usernameLable.draw()
        firstNameLable.draw()
        lastNameLable.draw()
        accountTypeLable.draw()
        changePasswordButton.draw()
        changeNameButton.draw()
        logoutButton.draw()
        backButton.draw()
        if admin:
            adminButton.draw()
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
                if themesButton.clicked():
                    themes(SCREEN, SERVER, username)
                    return
                if rulesButton.clicked():
                    rules(SCREEN, SERVER, username)
                    return
                if settingsButton.clicked():
                    settings(SCREEN, SERVER, username)
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
            if len(u) == 9 and u.isnumeric():
                if len(p) > 8:
                    symbol = False
                    capital = False
                    number = False
                    for character in p:
                        if character.isnumeric():
                            number = True
                        elif character.isalpha() and character.isupper():
                            capital = True
                        elif not character.isalpha():
                            symbol = True
                    
                    if symbol and capital and number:
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
                        result = "Password needs to contain an uppercase, symbol and number"
                else:
                    result = "Password is too short"
            else:
                result = "Please enter valid ID number"
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