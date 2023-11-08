import socket
import sqlite3
import threading
import random
import datetime
HOST = "192.168.0.36"
# HOST = "172.25.10.254"
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

        except Exception as error:
            print(type(error).__name__, "-", error)
            break

while True:
    client, addr = server.accept()
    print("connection established")
    threading.Thread(target=handler, args=[client,]).start()  
    