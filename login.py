import customtkinter
import sqlite3

class Login():
    def __init__(self):
        self.successfullLogin = False
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")
        self.root = customtkinter.CTk()
        self.root.geometry("600x450")
        self.root.resizable(False,False)
        self.root.title("Chess")
        self.frame = customtkinter.CTkFrame(master=self.root)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.titleLable = customtkinter.CTkLabel(master=self.frame, text="Welcome to Chess")
        self.loginRegisterLable = customtkinter.CTkLabel(master=self.frame, text="Dont have an account? Register")
        self.userEntry = customtkinter.CTkEntry(master=self.frame, placeholder_text="Username")
        self.passEntry = customtkinter.CTkEntry(master=self.frame, placeholder_text="Password", show="*")
        self.loginButton = customtkinter.CTkButton(master=self.frame, text="Login", command=self.loginLogic)
        self.registerButton = customtkinter.CTkButton(master=self.frame, text="Register", command=self.register)
        self.loginLable = customtkinter.CTkLabel(master=self.frame, text="Logging in...")
        self.blankspace = customtkinter.CTkLabel(master=self.frame, text="                                   ")

        self.registerlable = customtkinter.CTkLabel(master=self.frame, text="Create an Account.")
        self.firstName = customtkinter.CTkEntry(master=self.frame, placeholder_text="First Name")
        self.lastName = customtkinter.CTkEntry(master=self.frame, placeholder_text="Last Name")
        self.gender = customtkinter.CTkOptionMenu(master=self.frame, values= ["Male", "Female", "Other"])
        self.newUserEntry = customtkinter.CTkEntry(master=self.frame, placeholder_text="Create a Username")
        self.newPassEntry = customtkinter.CTkEntry(master=self.frame, placeholder_text="Create a Password", show="*")
        self.confirmPass = customtkinter.CTkEntry(master=self.frame, placeholder_text="Confirm Password", show="*")
        self.saveButton = customtkinter.CTkButton(master=self.frame, text="Save", command=self.addAccount)
        self.backButton = customtkinter.CTkButton(master=self.frame, text="Back", command=self.login)
        self.successfullLoginLable = customtkinter.CTkLabel(master=self.frame, text="Logging in...")
        self.unsuccessfullLoginLable = customtkinter.CTkLabel(master=self.frame, text="Invalid Password or Username")
        self.passwordMatchError = customtkinter.CTkLabel(master=self.frame, text="Passwords don't match")
        self.existingUsername = customtkinter.CTkLabel(master=self.frame, text="Username already exists")
        self.missingdata = customtkinter.CTkLabel(master=self.frame, text="Please fill all the boxes")

    def clearScreen(self):
        self.titleLable.grid_forget()
        self.userEntry.grid_forget()
        self.passEntry.grid_forget()
        self.loginButton.grid_forget()
        self.loginRegisterLable.grid_forget()
        self.registerButton.grid_forget()
        self.successfullLoginLable.grid_forget()
        self.unsuccessfullLoginLable.grid_forget()
        self.blankspace.grid_forget()
        self.registerlable.grid_forget()
        self.firstName.grid_forget()
        self.lastName.grid_forget()
        self.newUserEntry.grid_forget()
        self.newPassEntry.grid_forget()
        self.confirmPass.grid_forget()
        self.saveButton.grid_forget()
        self.backButton.grid_forget()
        self.gender.grid_forget()

    def login(self):
        self.clearScreen()
        self.blankspace.grid(pady=12,padx=10, row = 1, column = 1)
        self.titleLable.grid(pady=12,padx=10, row = 1, column = 2)
        self.userEntry.grid(pady=12, padx=10,row = 2, column = 2)
        self.passEntry.grid(pady=12, padx=10, row = 3, column = 2)
        self.loginButton.grid(pady=12, padx=10, row = 4, column = 2)
        self.loginRegisterLable.grid(pady=12,padx=10, row = 6, column = 2)
        self.registerButton.grid(pady=12, padx=10 ,row = 7, column = 2)
        self.root.mainloop()

    def register(self):
        self.clearScreen()
        self.newUserEntry.delete(0, "end")
        self.firstName.delete(0, "end")
        self.lastName.delete(0, "end")
        self.newPassEntry.delete(0, "end")
        self.confirmPass.delete(0, "end")
        # to do --> fix the placeholder text which does not appear at the start
        self.registerlable.grid(pady=12,padx=10, row=1, column=1)
        self.firstName.grid(pady=12,padx=10,row=2, column=1)
        self.lastName.grid(pady=12,padx=10, row=2, column=2)
        self.newUserEntry.grid(pady=12, padx=10, row=2, column=3)
        self.newPassEntry.grid(pady=12, padx=10, row=3, column=1)
        self.confirmPass.grid(pady=12, padx=10, row=3, column=2)
        self.gender.grid(pady=12, padx=10, row=3, column=3)
        self.saveButton.grid(pady=12,padx=10, row=4, column=3)
        self.backButton.grid(pady=12,padx=10, row=4, column=1)
        self.root.mainloop()

    def loginLogic(self):
        self.successfullLoginLable.grid_forget()
        self.unsuccessfullLoginLable.grid_forget()
        self.username = self.userEntry.get()
        self.password = self.passEntry.get()
        con = sqlite3.connect("Chess.db")
        cursor = con.cursor()
        sql = "select username from Accounts where username = ?"
        userfound = True if cursor.execute(sql,(self.username,)).fetchall() else False
        sql = "select password from Accounts where password = ?"
        correctpass = True if cursor.execute(sql,(self.password,)).fetchall() else False
        con.commit()
        con.close()
        self.successfullLogin = True if userfound and correctpass else False
        self.successfullLoginLable.grid(pady=12,padx=10,row=8, column=2) if self.successfullLogin else self.unsuccessfullLoginLable.grid(pady=12,padx=10,row=8, column=2)
        if self.successfullLogin: 
            self.root.destroy()
    
    def addAccount(self):
        self.existingUsername.grid_forget()
        self.passwordMatchError.grid_forget()
        self.missingdata.grid_forget()
        con = sqlite3.connect("Chess.db")
        con.row_factory = lambda cursor, row: row[0] #puts each username in a list for rather than a tuple in a list
        cursor = con.cursor()
        existingUsernames = cursor.execute("select username from Accounts").fetchall()
        con.commit()
        con.close()
        if self.newUserEntry.get() in existingUsernames:
            self.existingUsername.grid(pady=12,padx=10, row=5, column=1)
        elif self.newPassEntry.get() != self.confirmPass.get():
            self.passwordMatchError.grid(pady=12,padx=10, row=5, column=1)
        elif not self.firstName.get() and not self.lastName.get() and not self.newUserEntry.get() and not self.newPassEntry.get() and not self.confirmPass.get():
            self.missingdata.grid(pady=12,padx=10, row=5, column=1)
        else:
            con = sqlite3.connect("Chess.db")
            cursor = con.cursor()
            sql = "insert into Accounts (username, firstName, lastName, gender, password) values(?,?,?,?,?)"
            cursor.execute(sql,(self.newUserEntry.get(),self.firstName.get(), self.lastName.get(), self.gender.get(), self.newPassEntry.get(),))
            con.commit()
            con.close()
            self.login()
        
        

    def destroy(self):
        self.root.destroy()