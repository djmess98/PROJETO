import tkinter as tk
from tkinter import messagebox
import sqlite3
from database import create_tables

class RegisterWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Registro de Utilizador")
        self.geometry("300x300")

        self.create_widgets()

    def create_widgets(self):
        self.username_label = tk.Label(self, text="Nome de Utilizador:")
        self.username_label.pack()

        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.nif_label = tk.Label(self, text="NIF (9 dígitos):")
        self.nif_label.pack()

        self.nif_entry = tk.Entry(self)
        self.nif_entry.pack()

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        register_button = tk.Button(self, text="Registar", command=self.register)
        register_button.pack(pady=20)

    def register(self):
        username = self.username_entry.get()
        nif = self.nif_entry.get()
        password = self.password_entry.get()

        # Chame a função create_tables() antes de verificar a existência do usuário
        create_tables()

        if self.validate_input(username, nif, password):
            if self.check_existing_user(username, nif):
                self.add_user(username, password, nif)
                messagebox.showinfo("Registro de Utilizador", "Registro bem-sucedido.")
                self.destroy()
            else:
                messagebox.showerror("Registro de Utilizador", "Nome de Utilizador ou NIF já existentes.")

    def validate_input(self, username, nif, password):
        if len(username) == 0 or len(nif) == 0 or len(password) == 0:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return False
        return True

    def check_existing_user(self, username, nif):
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? OR nif=?", (username, nif))
        user = cursor.fetchone()
        conn.close()
        return user is None

    def add_user(self, username, nif, password):
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (username, nif, password))
        conn.commit()
        conn.close()