# Copyright (C), 2024-2025, bl33h 
# fileName: main.py
# author: Sara Echeverria
# version: I
# creation: 01/08/2024
# last modification: 19/08/2024
# References: https://docs.python.org/3/library/asyncio.html, https://docs.python.org/3/library/logging.html, https://pypi.org/project/python-dotenv/
# https://xmpp.org/extensions/xep-0029.html

import asyncio
import logging
from criticalUt import loadDomain
from loggedActions import LoggedActions
from connection import newUser, Connection

# configure logging to show only error messages
logging.basicConfig(level=logging.ERROR)
logging.getLogger('slixmpp').setLevel(logging.ERROR)

DOMAIN = loadDomain()

# --- actions for everybody ---
def main():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    while True:
        print("\n--- Welcome to the XMPP Client Core Chat ---")
        print("[1] log in")
        print("[2] sign up")
        print("[3] delete existing account")
        print("[4] exit")
        option = input("• enter your option: ")

        # --- log in ---
        if option == "1":
            username = input("-> username: ")
            password = input("-> password: ")
            jid = f"{username}@{DOMAIN}"
            xmppClient = LoggedActions(jid, password)
            xmppClient.connect(disable_starttls=True, use_ssl=False)
            xmppClient.process(forever=False)
        
        # --- sign up ---
        elif option == "2":
            username = input("-> username (without @domain): ")
            jid = f"{username}@{DOMAIN}"
            password = input("-> password: ")
            print(f"-> your full username is: {jid}")
            newUser(jid, password)
        
        # --- delete account ---
        elif option == "3":
            username = input("-> username (without @domain): ")
            jid = f"{username}@{DOMAIN}"
            password = input("-> password: ")
            xmpp_delete = Connection(jid, password)
            xmpp_delete.connect(disable_starttls=True, use_ssl=False)
            asyncio.run(xmpp_delete.process(forever=False))
        
        # --- exit ---
        elif option == "4":
            break
        
        else:
            print("!error, invalid option")

if __name__ == "__main__":
    main()