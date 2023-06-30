import pygame
from constants import *
from widgets import TextBox, Button, Label
from game import Game
import sqlite3
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chess")

def getColours(username):
    con = sqlite3.connect("Chess.db")
    con.row_factory = lambda cursor, row: row[0]
    cursor = con.cursor()
    sql = "select darkSquare from Themes where themeID = (select themeID from Accounts where username = ?)"
    d = eval(cursor.execute(sql,(username,)).fetchall()[0])
    sql = "select lightSquare from Themes where themeID = (select themeID from Accounts where username = ?)"
    l = eval(cursor.execute(sql,(username,)).fetchall()[0])
    sql = "select highlight from Themes where themeID = (select themeID from Accounts where username = ?)"
    h = eval(cursor.execute(sql,(username,)).fetchall()[0])
    return d, l, h

def twoPlayer(username):
    board = Game(SCREEN)
    d, l, h = getColours(username)
    backButton = Button(SCREEN, 1110, 650, 280, 100, "Back")
    run = True
    while run:
        SCREEN.fill(DARKGREY)
        board.flipped = board.turn == "Black"
        board.drawBoard(300, 0, d, l, h)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.action()
                if backButton.clicked():
                    mainMenu(username)
                    return
            if event.type == pygame.QUIT:
                run = False
        backButton.draw()
        pygame.display.flip()
    pygame.quit()

def mainMenu(username):
    board = Game(SCREEN)
    localButton = Button(SCREEN, 1110, 50, 280, 100, "Local")
    twoPlayerButton = Button(SCREEN, 1110, 250, 280, 100, "Two Player")
    onePlayerButton = Button(SCREEN, 1110, 450, 280, 100, "One Player")
    archiveButton = Button(SCREEN, 1110, 650, 280, 100, "Archive")
    accountButton = Button(SCREEN, 10, 50, 280, 100, "Account")
    themesButton = Button(SCREEN, 10, 250, 280, 100, "Themes")
    rulesButton = Button(SCREEN, 10, 450, 280, 100, "Rules")
    settingsButton = Button(SCREEN, 10, 650, 280, 100, "Settings")
    d, l, h = getColours(username)
    run = True
    while run:
        SCREEN.fill(DARKGREY)
        board.drawBoard(300,0, d, l, h)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if twoPlayerButton.clicked():
                    twoPlayer(username)
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
    pygame.quit()

def registerLogic(fn, ln, u, p, cp):
    con = sqlite3.connect("Chess.db")
    con.row_factory = lambda cursor, row: row[0] #puts each username in a list for rather than a tuple in a list
    cursor = con.cursor()
    existingUsernames = cursor.execute("select username from Accounts").fetchall()
    con.commit()
    con.close()
    if u in existingUsernames:
        return "Username already exists"
    elif p != cp:
        return "Passwords do not match"
    elif not fn or not ln or not u or not p or not cp:
        return "Please fill in ALL the information"
    else:
        con = sqlite3.connect("Chess.db")
        cursor = con.cursor()
        sql = "insert into Accounts (username, firstName, lastName, password) values(?,?,?,?)"
        cursor.execute(sql,(u, fn, ln, p,))
        con.commit()
        con.close()
        return True

def register():
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
                    result = registerLogic(firstName.text, lastName.text, username.text, password.text, confirmPassword.text)
                    if result == True:
                        login()
                        return
                    else:
                        output.setText(result)
                if back.clicked():
                    login()
                    return
                firstName.toggleSelected()
                lastName.toggleSelected()
                username.toggleSelected()
                password.toggleSelected()
                confirmPassword.toggleSelected()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    result = registerLogic(firstName.text, lastName.text, username.text, password.text, confirmPassword.text)
                    if result == True:
                        login()
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
    pygame.quit()

def successfulLogin(username, password):
    con = sqlite3.connect("Chess.db")
    cursor = con.cursor()
    sql = "select username from Accounts where username = ?"
    userfound = True if cursor.execute(sql,(username,)).fetchall() else False
    sql = "select password from Accounts where password = ? and username = ?"
    correctpass = True if cursor.execute(sql,(password, username,)).fetchall() else False
    con.commit()
    con.close()
    return True if userfound and correctpass else False

def login():
    loginButton = Button(SCREEN, 450,450,500,100, "Login")
    registerButton = Button(SCREEN, 450,650,500,100, "Create an account")
    username = TextBox(SCREEN, 450,50,500,100, "Username")
    password = TextBox(SCREEN, 450,250,500,100, "Password")
    run = True
    while run:
        SCREEN.fill(DARKGREY)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if loginButton.clicked():
                    if successfulLogin(username.text, password.text):
                        mainMenu(username.text)
                        return
                if registerButton.clicked():
                    register()
                    return
                username.toggleSelected()
                password.toggleSelected()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if successfulLogin(username.text, password.text):
                        mainMenu(username.text)
                        return
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
        username.draw()
        password.draw(show="*")
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    login()