# Copyright (C), 2024-2025, bl33h 
# fileName: main.py
# author: Sara Echeverria
# version: I
# creation: 01/08/2024
# last modification: 25/08/2024
# References: https://docs.python.org/3/library/asyncio.html, https://docs.python.org/3/library/logging.html, https://pypi.org/project/python-dotenv/
# https://xmpp.org/extensions/xep-0029.html

import asyncio
import logging
import tkinter as tk
from tkinter import font
from tkinter import messagebox
from connection import newUser
from criticalUt import loadDomain
from loggedActions import LoggedActions
from deleteAccount import DeleteExistentAccount

# configure logging to show only error messages
logging.basicConfig(level=logging.ERROR)
logging.getLogger('slixmpp').setLevel(logging.ERROR)

DOMAIN = loadDomain()

# --- dialog for login, sign up and account deletion ---
class LoginDialog(tk.Toplevel):
    def __init__(self, parent, title, message, dialog_width=500, entry_width=30):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)
        self.result = None

        self.configure(bg='#797fa2')

        tk.Label(self, text=message, bg='#797fa2', fg='#dbdcf3', font=('Helvetica', 12)).pack(pady=10)

        # entries
        self.username_entry = tk.Entry(self, width=entry_width, bg='#dbdcf3', fg='#000000', font=('Helvetica', 12))
        self.username_entry.pack(pady=5)
        self.password_entry = tk.Entry(self, show="*", width=entry_width, bg='#dbdcf3', fg='#000000', font=('Helvetica', 12))
        self.password_entry.pack(pady=5)

        # frame for buttons
        self.button_frame = tk.Frame(self, bg='#797fa2')
        self.button_frame.pack(pady=10)

        # buttons
        tk.Button(self.button_frame, text="Ok", command=self.onOk, bg='#797fa2', fg='#dbdcf3', font=('Helvetica', 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Cancel", command=self.destroy, bg='#797fa2', fg='#dbdcf3', font=('Helvetica', 12)).pack(side=tk.LEFT, padx=5)

        # set focus on the username entry
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.geometry(f"{dialog_width}x200+{parent.winfo_rootx() + 50}+{parent.winfo_rooty() + 50}")
        self.username_entry.focus_set()
        self.wait_window(self)

    def onOk(self):
        self.result = (self.username_entry.get(), self.password_entry.get())
        self.destroy()

# --- main user interface ---
class SimpleUserInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("XMPP Client Core Chat")
        self.root.geometry("500x300")
        self.root.configure(bg='#797fa2')

        # Create a frame to center the widgets
        self.frame = tk.Frame(self.root, bg='#797fa2')
        self.frame.pack(expand=True)

        # Add a welcome label with bold font
        bold_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.welcome_label = tk.Label(self.frame, text="Welcome to XMPP Client Core Chat", bg='#797fa2', fg='#dbdcf3', font=bold_font)
        self.welcome_label.pack(pady=10)

        # Add an instructions label with smaller font
        small_font = font.Font(family="Helvetica", size=10)
        self.instructions_label = tk.Label(self.frame, text="choose an option below to proceed, enjoy ! - sara", bg='#797fa2', fg='#dbdcf3', font=small_font)
        self.instructions_label.pack(pady=5)

        # Create buttons with updated styles
        self.login_btn = tk.Button(self.frame, text="Log In", command=self.login, bg='#797fa2', fg='#dbdcf3', font=('Helvetica', 12))
        self.login_btn.pack(pady=5)

        self.signup_btn = tk.Button(self.frame, text="Sign Up", command=self.signup, bg='#797fa2', fg='#dbdcf3', font=('Helvetica', 12))
        self.signup_btn.pack(pady=5)

        self.deleteAccount_btn = tk.Button(self.frame, text="Delete Existing Account", command=self.deleteAccount, bg='#797fa2', fg='#dbdcf3', font=('Helvetica', 12))
        self.deleteAccount_btn.pack(pady=5)

        self.exit_btn = tk.Button(self.frame, text="Exit", command=self.root.destroy, bg='#797fa2', fg='#dbdcf3', font=('Helvetica', 12))
        self.exit_btn.pack(pady=5)

    # --- log in ---
    def login(self):
        dialog = LoginDialog(self.root, "Log In", "Enter your credentials to log in !\nremember that you don't need to place the domain", dialog_width=500, entry_width=30)
        if dialog.result:
            username, password = dialog.result
            if username and password:
                jid = f"{username}@{DOMAIN}"
                xmpp_client = LoggedActions(jid, password)
                xmpp_client.connect(disable_starttls=True, use_ssl=False)
                xmpp_client.process(forever=False)

    # --- sign up ---
    def signup(self):
        dialog = LoginDialog(self.root, "Sign Up", "Enter your credentials to create your account!\nremember that you don't need to place the domain", dialog_width=500, entry_width=30)
        if dialog.result:
            username, password = dialog.result
            if username and password:
                jid = f"{username}@{DOMAIN}"
                newUser(jid, password)
                messagebox.showinfo("Sign Up", f"Account created, your full username is: [{jid}]")

    # --- delete account ---
    def deleteAccount(self):
        dialog = LoginDialog(self.root, "Delete Account", "Enter your credentials for account deletion:", dialog_width=500, entry_width=30)
        if dialog.result:
            username, password = dialog.result
            if username and password:
                jid = f"{username}@{DOMAIN}"
                xmpp_delete = DeleteExistentAccount(jid, password)
                xmpp_delete.connect(disable_starttls=True, use_ssl=False)
                xmpp_delete.process(forever=False)
                self.root.after(500, lambda: self.checkDeletionStatus(xmpp_delete))

    # --- check if the account has been deleted ---
    def checkDeletionStatus(self, xmpp_delete):
        if not xmpp_delete.is_connected():
            messagebox.showinfo("Delete Account", f"The account [{xmpp_delete.boundjid.bare}] has been deleted")
        else:
            self.root.after(500, lambda: self.checkDeletionStatus(xmpp_delete))

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleUserInterface(root)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    root.mainloop()
