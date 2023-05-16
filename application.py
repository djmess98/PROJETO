import tkinter as tk
from login_window import LoginWindow
from register_window import RegisterWindow
from expense_manager_window import ExpenseManagerWindow

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GestSoft")
        self.geometry("300x200")

        self.create_widgets()

    def create_widgets(self):
        login_button = tk.Button(self, text="Login", command=self.open_login_window)
        login_button.pack(pady=20)

        register_button = tk.Button(self, text="Registo de Utilizador", command=self.open_register_window)
        register_button.pack()

    def open_login_window(self):
        login_window = LoginWindow(self)
        login_window.grab_set()

    def open_register_window(self):
        register_window = RegisterWindow(self)
        
    def open_expense_manager_window(self, username):
        expense_manager_window = ExpenseManagerWindow(self, username)
        expense_manager_window.grab_set()