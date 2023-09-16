import socket
import sqlite3
import threading
import random
# HOST = "192.168.0.36"
HOST = "172.25.10.254"
PORT = 1234
BYTES = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
server.bind((HOST, PORT))
server.listen()
lobby = []

def localPlay(player1, player2):
    while player2.recv(BYTES).decode() != "Ready":
        pass
    if random.randint(0,1) == 0:
        player1.send("White".encode())
        player2.send("Black".encode())
    else:
        player1.send("Black".encode())
        player2.send("White".encode())
    
    player1Move = ""
    player2Move = ""

    while True:
        player1Move = player1.recv(BYTES).decode()
        player2Move = player2.recv(BYTES).decode()

        if player1Move == "Resign":
            threading.Thread(target=handler, args=(player1,)).start()
            player2.send(player1Move.encode())
            threading.Thread(target=handler, args=(player2,)).start()
            break
        else:
            player1.send(player2Move.encode())

        if player2Move == "Resign":
            threading.Thread(target=handler, args=(player2,)).start()
            player1.send(player2Move.encode())
            threading.Thread(target=handler, args=(player1,)).start()
            break
        else:
            player2.send(player1Move.encode())

def handler(client):
    while True:
        try:
            data = client.recv(BYTES).decode()
            if data == "[LOGIN]":
                client.send("Starting Login Sequence".encode())
                username = client.recv(BYTES).decode()
                client.send("Recieved Username".encode())
                password = client.recv(BYTES).decode()
                con = sqlite3.connect("Chess.db")
                cursor = con.cursor()
                sql = "select username from Accounts where username = ?"
                userfound = True if cursor.execute(sql,(username,)).fetchall() else False
                sql = "select password from Accounts where password = ? and username = ?"
                correctpass = True if cursor.execute(sql,(password, username,)).fetchall() else False
                con.commit()
                con.close()
                if userfound and correctpass:
                    client.send("True".encode())
                else:
                    client.send("False".encode())
            elif data == "[REGISTER]":
                client.send("Starting Register Sequence".encode())
                fn = client.recv(BYTES).decode()
                client.send("Recieved Firstname".encode())
                ln = client.recv(BYTES).decode()
                client.send("Recieved Lastname".encode())
                u = client.recv(BYTES).decode()
                client.send("Recieved Username".encode())
                p = client.recv(BYTES).decode()
                client.send("Recieved Password".encode())
                cp = client.recv(BYTES).decode()
                con = sqlite3.connect("Chess.db")
                con.row_factory = lambda cursor, row: row[0] #puts each username in a list for rather than a tuple in a list
                cursor = con.cursor()
                existingUsernames = cursor.execute("select username from Accounts").fetchall()
                con.commit()
                con.close()
                if u in existingUsernames:
                    client.send("Username already exists".encode())
                else:
                    con = sqlite3.connect("Chess.db")
                    cursor = con.cursor()
                    sql = "insert into Accounts (username, firstName, lastName, password) values(?,?,?,?)"
                    cursor.execute(sql,(u, fn, ln, p,))
                    con.commit()
                    con.close()
                    client.send("True".encode())
            elif data == "[THEME]":
                client.send("Fetching Theme Colours".encode())
                username = client.recv(BYTES).decode()
                con = sqlite3.connect("Chess.db")
                con.row_factory = lambda cursor, row: row[0]
                cursor = con.cursor()
                sql = "select darkSquare from Themes where themeID = (select themeID from Accounts where username = ?)"
                d = cursor.execute(sql,(username,)).fetchall()[0]
                sql = "select lightSquare from Themes where themeID = (select themeID from Accounts where username = ?)"
                l = cursor.execute(sql,(username,)).fetchall()[0]
                sql = "select highlight from Themes where themeID = (select themeID from Accounts where username = ?)"
                h = cursor.execute(sql,(username,)).fetchall()[0]
                client.send(d.encode())
                client.recv(BYTES).decode()
                client.send(l.encode())
                client.recv(BYTES).decode()
                client.send(h.encode())
            elif data == "[LOCAL]": 
                matchFound = False
                client.send("Starting Local Sequence".encode())
                for player in lobby:
                    if player != client: # and settings are compatible
                        matchFound = True
                        player2 = player
                if not matchFound: # if this player is the waiter
                    lobby.append(client) # add him to the wait list (lobby)
                    while True: 
                        data = client.recv(BYTES).decode()
                        if data != "Stop":
                            if client in lobby: # check if somone removed him, meaning a match has been found
                                client.send("Waiting".encode())
                            else:
                                client.send("Found Match".encode())
                                return
                        else:
                            lobby.remove(client)
                            break
                else:
                    if client.recv(BYTES).decode() == "Waiting":
                        lobby.remove(player2)
                        client.send("Found Match".encode())
                        client.recv(BYTES).decode() # ready
                        threading.Thread(target=localPlay, args=(client, player2)).start()
                        return
        except:
            print("Disconnected")
            break

while True:
    client, addr = server.accept()
    print("connection established")
    threading.Thread(target=handler, args=[client,]).start()  
    