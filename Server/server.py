import socket
import sqlite3
import threading
import random
import datetime
import time
import requests
from Queue import Queue
from Stack import Stack

HOST = "192.168.0.36"
# HOST = "172.25.9.98"

PORT = 1234
BYTES = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) ## allows this port to be reused

server.bind((HOST, PORT))
server.listen()

lobby = []
def matchMaking():
    while True:
        if len(lobby) >= 2:
            player1 = lobby[0]
            lobby.remove(player1)
            player2 = lobby[0]
            lobby.remove(player2)
            threading.Thread(target=localPlay, args=(player1, player2)).start()

def localPlay(player1, player2):
    # the threading module can give priority to this thread over the handler thread therefore ...
    time.sleep(0.5) ## ...makes sure we dont recieve "waiting" and send "match found" before continuing with recieving the username (handler - elif data == "[LOCAL]" - while loop - else statement)
    p1data = []
    p2data = []
    p1data.append(player1.recv(BYTES).decode()) 
    p2data.append(player2.recv(BYTES).decode()) 

    if random.randint(0,1) == 0:
        player1.send("White".encode())
        player2.send("Black".encode())
        p1data.append("White") 
        p2data.append("Black")
    else:
        player1.send("Black".encode())
        player2.send("White".encode())
        p1data.append("Black")
        p2data.append("White ")
    
    while True:
        player1data = eval(player1.recv(BYTES).decode()) ##[(move(list)/resign(string)/waiting(string)), pgn(string)]
        player2data = eval(player2.recv(BYTES).decode()) ##[(move(list)/resign(string)/waiting(string)), pgn(string)]
        p1move = str(player1data[0])
        p2move = str(player2data[0])
        
        ## variable names is w for waiting, m for a move, and r for resign
        ## for instance, if player 1 sends waiting, and player 2 sends resign, wr would be True
        ww = p1move == "Waiting" and p2move == "Waiting"
        mw = p1move[0] == "[" and p2move == "Waiting"
        wm = p1move == "Waiting" and p2move[0] == "["
        rw = p1move == "Resign" and p2move == "Waiting"
        wr = p1move == "Waiting" and p2move == "Resign"
        rm = p1move == "Resign" and p2move[0] == "["
        mr = p1move[0] == "[" and p2move == "Resign"
        rr = p1move == "Resign" and p2move == "Resign" ## very rare due to processing speed but still a possibility

        if rw or rr or rm or mw:
            pgn = player1data[1]
        elif wr or mr or rr or wm:
            pgn = player2data[1]
        else:
            pgn = player1data[1]
        
        if ww: ## both are waiting
            player1.send("Waiting".encode())
            player2.send("Waiting".encode())

        elif mw: ## player 1 sent a move and player 2 is waiting
            if "-" in pgn: ## if the game is over 
                player1.send("Game Over".encode())
                threading.Thread(target=handler, args=(player1,)).start()
                player2.send("Game Over".encode())
                threading.Thread(target=handler, args=(player2,)).start()
                saveGame(p1data, p2data, pgn)
                return

            else:
                player1.send("Waiting".encode())
                player2.send(str(player1data[0]).encode())
        
        elif wm: ## player 1 is waiting and player 2 sent a move
            if "-" in pgn: ## if the game is over
                player2.send("Game Over".encode())
                threading.Thread(target=handler, args=(player2,)).start()
                player1.send("Game Over".encode())
                threading.Thread(target=handler, args=(player1,)).start()
                saveGame(p1data, p2data, pgn)
                return

            else:
                player2.send("Waiting".encode())
                player1.send(str(player2data[0]).encode())
        
        elif rw or wr or rr or rm or mr: ## either payer resigned
            player1.send("Game Over".encode())
            threading.Thread(target=handler, args=(player1,)).start()
            player2.send("Game Over".encode())
            threading.Thread(target=handler, args=(player2,)).start()
            saveGame(p1data, p2data, pgn)
            return

def saveGame(p1data, p2data, pgn):
    con = sqlite3.connect("Chess.db")
    cursor = con.cursor()
    sql = "insert into Games (whitePlayerID, blackPlayerID, PGN) values (?,?,?)"
    if p1data[1] == "White":
        cursor.execute(sql,(p1data[0], p2data[0], pgn))
        sql = "SELECT MAX(gameID) FROM Games where whitePlayerID = ? and blackPlayerID = ? and PGN = ?" ## aggregation
        gameID = cursor.execute(sql, (p1data[0], p2data[0], pgn)).fetchall()[0][0]
    else:
        cursor.execute(sql,(p2data[0], p1data[0], pgn))
        sql = "SELECT MAX(gameID) FROM Games where whitePlayerID = ? and blackPlayerID = ? and PGN = ?" ## aggregation
        gameID = cursor.execute(sql, (p2data[0], p1data[0], pgn)).fetchall()[0][0]
    
    sql = "insert into AccountGameLink (username, gameID) values (?,?)"
    cursor.execute(sql, (str(p1data[0]), gameID))
    cursor.execute(sql, (str(p2data[0]), gameID))
    
    con.commit()
    con.close()

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
                    con = sqlite3.connect("Chess.db")
                    cursor = con.cursor()
                    sql = "Select username from Accounts where accountType = 'Student' and username = ?"
                    if cursor.execute(sql, (username,)).fetchall():
                        today = datetime.date.today().strftime('%d/%m/%y')
                        sql = "insert or ignore into Attendance (username, date) values (?, ?)"
                        cursor.execute(sql, (username, today))
                    con.commit()
                    con.close()
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

            elif data == "[CREATEADMIN]":
                client.send("Starting admin register sequence".encode())
                data = eval(client.recv(BYTES).decode())
                con = sqlite3.connect("Chess.db")
                con.row_factory = lambda cursor, row: row[0]
                cursor = con.cursor()
                existingUsernames = cursor.execute("select username from Accounts").fetchall()
                con.commit()
                con.close()
                if data[2] in existingUsernames:
                    client.send("Username already exists".encode())
                else:
                    con = sqlite3.connect("Chess.db")
                    cursor = con.cursor()
                    sql = "insert into Accounts (username, firstName, lastName, password, accountType) values (?,?,?,?,?)"
                    cursor.execute(sql,(data[2], data[0], data[1], data[3], "Admin"))
                    con.commit()
                    con.close()
                    client.send("True".encode())

            elif data == "[ISADMIN]":
                client.send("Checking...".encode())
                user = client.recv(BYTES).decode()
                con = sqlite3.connect("Chess.db")
                cursor = con.cursor()
                sql = "Select username from Accounts where accountType = 'Admin' and username = ?"
                message = "True" if cursor.execute(sql, (user,)).fetchall() else "False"
                client.send(message.encode())
                con.commit()
                con.close()
            
            elif data == "[FETCHUSERS]":
                con = sqlite3.connect("Chess.db")
                cursor = con.cursor()
                sql = "select username, firstName, lastName, accountType from Accounts"
                data = cursor.execute(sql).fetchall()
                con.commit()
                con.close()
                result = []
                for user in data:
                    result.append([attribute for attribute in user])
                client.send(str(result).encode())

            elif data == "[RESETPASSWORD]":
                client.send("Username?".encode())
                u = client.recv(BYTES).decode()
                con = sqlite3.connect("Chess.db")
                cursor = con.cursor()
                sql = "update Accounts set password = 'Password_123' where username = ?"
                cursor.execute(sql, (u,))
                con.commit()
                con.close()
                client.send("Successful".encode())
            
            elif data == "[DELETEUSER]":
                client.send("Username?".encode())
                u = client.recv(BYTES).decode()
                con = sqlite3.connect("Chess.db")
                cursor = con.cursor()
                sql = "DELETE FROM AccountGameLink where gameID in (SELECT gameID from Games where whitePlayerID = ? or BlackPlayerID = ?)"
                cursor.execute(sql, (u,u))
                sql = "DELETE from Games where whitePlayerID = ? or BlackPlayerID = ?"
                cursor.execute(sql, (u,u))
                sql = "DELETE from Attendance where username = ?"
                cursor.execute(sql, (u,))
                sql = "DELETE from Accounts where username = ?"
                cursor.execute(sql, (u,))
                print("REached")
                con.commit()
                con.close()
                client.send("Successful".encode())
                print("REached")

            elif data == "[ERASEATTENDANCE]":
                con = sqlite3.connect("Chess.db")
                cursor = con.cursor()
                sql = "DROP TABLE Attendance;"
                cursor.execute(sql)
                sql = "CREATE TABLE 'Attendance' ( 'username'	TEXT, 'date'	TEXT, PRIMARY KEY('date','username'), FOREIGN KEY('username') REFERENCES 'Accounts'('username'))"
                cursor.execute(sql)
                con.commit()
                con.close()
                client.send("Sucessful".encode())

            elif data == "[GETDATA]":
                client.send("Username?".encode())
                username = client.recv(BYTES).decode()
                con = sqlite3.connect("Chess.db")
                cursor = con.cursor()
                data = []
                sql = "Select username from Accounts where username = ?"
                data.append(cursor.execute(sql, (username,)).fetchall()[0][0])
                sql = "Select firstName from Accounts where username = ?"
                data.append(cursor.execute(sql, (username,)).fetchall()[0][0])
                sql = "Select lastName from Accounts where username = ?"
                data.append(cursor.execute(sql, (username,)).fetchall()[0][0])
                sql = "Select accountType from Accounts where username = ?"
                data.append(cursor.execute(sql, (username,)).fetchall()[0][0])
                con.commit()
                con.close()
                client.send(str(data).encode())
            
            elif data == "[CHANGEPASS]":
                client.send("data?".encode())
                data = eval(client.recv(BYTES).decode())
                username, password = data[0], data[1]
                con = sqlite3.connect("Chess.db")
                cursor = con.cursor()
                sql = "Update Accounts Set password = ? Where username = ?"
                cursor.execute(sql, (password, username))
                con.commit()
                con.close()

            elif data == "[CHANGENAME]":
                client.send("Username?".encode())
                data = eval(client.recv(BYTES).decode())
                con = sqlite3.connect("Chess.db")
                cursor = con.cursor()
                sql = "Update Accounts Set firstName = ?, lastName = ? Where username = ?"
                cursor.execute(sql, (data[1], data[2], data[0]))
                con.commit()
                con.close()
                client.send("Successful".encode())
            
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
                con.commit()
                con.close()
                client.send(d.encode())
                client.recv(BYTES).decode()
                client.send(l.encode())
                client.recv(BYTES).decode()
                client.send(h.encode())
            
            elif data == "[GETALLCOLOURS]":
                con = sqlite3.connect("Chess.db")
                cursor = con.cursor()
                data = cursor.execute("select darkSquare, lightSquare, highLight from Themes").fetchall()
                client.send(str(data).encode())
                con.commit()
                con.close()
            
            elif data == "[SETTHEME]":
                client.send("username and theme?".encode())
                data = eval(client.recv(BYTES).decode())
                con = sqlite3.connect("Chess.db")
                cursor = con.cursor()
                sql = "update Accounts set themeID = ? where username = ?"
                cursor.execute(sql, (data[1],data[0]))
                client.send("Theme changed".encode())
                con.commit()
                con.close()

            elif data == "[LOCAL]": 
                client.send("Starting Local Sequence".encode())
                lobby.append(client)
                while True:
                    a = client.recv(BYTES).decode()
                    if  a == "Stop":
                        client.send("Stopping matchmaking system".encode())
                        lobby.remove(client)
                        break
                    else:
                        if client not in lobby:
                            client.send("Match Found".encode())
                            return
                        else:
                            client.send("Searching".encode())

            elif data == "[FETCHGAMES]":
                client.send("Username?".encode())
                username = client.recv(BYTES).decode()
                con = sqlite3.connect("Chess.db")
                cursor = con.cursor()
                sql = "SELECT count(PGN) from Games INNER JOIN AccountGameLink on Games.gameID = AccountGameLink.gameID WHERE username = ?" ## Aggregate sql
                count = int(cursor.execute(sql, (username,)).fetchall()[0][0])
                sql = "SELECT whitePlayerID, blackPlayerID, PGN from Games INNER JOIN AccountGameLink on Games.gameID = AccountGameLink.gameID WHERE username = ?"
                data = cursor.execute(sql, (username,)).fetchall()
                con.commit()
                con.close()
                result = Queue(count * 2) ## half for dequing the reverse order, and half for enquing the correct order
                for game in data:
                    result.Enqueue([attribute for attribute in game])
                stack = Stack(count)
                for i in range(count):
                    stack.push(result.Dequeue())
                for i in range(count):
                    result.Enqueue(stack.pop())
                reverseddata = []
                for i in range(count):
                    reverseddata.append(result.Dequeue())
                
                # it is likely that the number of bit that contain every game played is too large, so a header is sent first
                client.send(str(len(str(reverseddata).encode())).encode()) # sends the number of bits being sent over
                client.recv(BYTES).decode()
                client.send(str(reverseddata).encode())

            elif data == "[STOCKFISH]": ## Stockfish API
                client.send("FEN?".encode())
                fen = client.recv(BYTES).decode()
                response = requests.get(f"https://stockfish.online/api/stockfish.php?fen={fen}&depth=13&mode=bestmove") ## https://stockfish.online/
                move = response.json() ## parsing JSON
                client.send(move.get("data")[9:13].encode())

        except Exception as error:
            print(type(error).__name__, "-", error)
            break

threading.Thread(target=matchMaking).start()
while True:
    client, addr = server.accept()
    print("connection established")
    threading.Thread(target=handler, args=[client,]).start()  
    