import tkinter as tk
from tkinter import messagebox
import sqlite3
from database import *
from expense_manager_window import ExpenseManagerWindow


class LoginWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Login")
        self.geometry("300x300")

        self.create_widgets()

    def create_widgets(self):
        self.username_label = tk.Label(self, text="Nome de utilizador:")
        self.username_label.pack()

        self.username_entry = tk.Entry(self)
        self.username_entry.pack()


        self.password_label = tk.Label(self, text="Password::")
        self.password_label.pack()

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        login_button = tk.Button(self, text="Login", command=self.login)
        login_button.pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.verify_login(username, password):
            self.destroy()
            expense_manager_window = ExpenseManagerWindow(self.master, username)


    def verify_login(self, username, password):
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            return True
        else:
            messagebox.showerror("Erro de Login", "Credenciais inválidas.")
            return False
