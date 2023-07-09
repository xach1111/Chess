import pygame
from constants import *
from widgets import TextBox, Button, Label
from game import Game
import socket


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

def twoPlayer(SCREEN, SERVER, username):
    board = Game(SCREEN)
    d, l, h = getColours(SERVER, username)
    backButton = Button(SCREEN, 1110, 650, 280, 100, "Back")
    label = Label(SCREEN, 1194, 450, "")
    run = True
    while run:
        SCREEN.fill(DARKGREY)
        board.flipped = board.turn == "Black"
        board.drawBoard(300, 0, d, l, h)
        if board.gameOver:
            label.setText(board.winner + " Wins!!")
            label.draw()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.action()
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
    accountButton = Button(SCREEN, 10, 50, 280, 100, "Account")
    themesButton = Button(SCREEN, 10, 250, 280, 100, "Themes")
    rulesButton = Button(SCREEN, 10, 450, 280, 100, "Rules")
    settingsButton = Button(SCREEN, 10, 650, 280, 100, "Settings")
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
            if event.type == pygame.QUIT:
                run = False
        localButton.draw()
        twoPlayerButton.draw()
        onePlayerButton.draw()
        archiveButton.draw()
        accountButton.draw()
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