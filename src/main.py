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

        tk.Label(self, text=message).pack(pady=10)

        # entries
        self.username_entry = tk.Entry(self, width=entry_width)
        self.username_entry.pack(pady=5)
        self.password_entry = tk.Entry(self, show="*", width=entry_width)
        self.password_entry.pack(pady=5)

        # frame for buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=10)

        # buttons
        tk.Button(self.button_frame, text="Ok", command=self.onOk).pack(side=tk.LEFT)
        tk.Label(self.button_frame, width=2).pack(side=tk.LEFT)
        tk.Button(self.button_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT)

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

        self.login_btn = tk.Button(self.root, text="Log In", command=self.login)
        self.login_btn.pack(pady=5)

        self.signup_btn = tk.Button(self.root, text="Sign Up", command=self.signup)
        self.signup_btn.pack(pady=5)

        self.deleteAccount_btn = tk.Button(self.root, text="Delete Existing Account", command=self.deleteAccount)
        self.deleteAccount_btn.pack(pady=5)

        self.exit_btn = tk.Button(self.root, text="Exit", command=self.root.destroy)
        self.exit_btn.pack(pady=5)

    # --- log in ---
    def login(self):
        dialog = LoginDialog(self.root, "Log In", "Enter your credentials:", dialog_width=500, entry_width=30)
        if dialog.result:
            username, password = dialog.result
            if username and password:
                jid = f"{username}@{DOMAIN}"
                xmpp_client = LoggedActions(jid, password)
                xmpp_client.connect(disable_starttls=True, use_ssl=False)
                xmpp_client.process(forever=False)

    # --- sign up ---
    def signup(self):
        dialog = LoginDialog(self.root, "Sign Up", "Enter your credentials:", dialog_width=500, entry_width=30)
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
            messagebox.showinfo("Delete Account", f"!The account [{xmpp_delete.boundjid.bare}] has been deleted")
        else:
            self.root.after(500, lambda: self.checkDeletionStatus(xmpp_delete))

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleUserInterface(root)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    root.mainloop()