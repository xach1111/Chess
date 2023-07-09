import socket
import sqlite3
import threading
HOST = "192.168.0.36"
PORT = 1234
BYTES = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
server.bind((HOST, PORT))
server.listen()

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
        except:
            print("Disconnected")
            break

while True:
    client, addr = server.accept()
    print("connection established")
    threading.Thread(target=handler, args=[client,]).start()  
    