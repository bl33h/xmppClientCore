# Copyright (C), 2024-2025, bl33h 
# fileName: main.py
# author: Sara Echeverria
# version: I
# creation: 01/08/2024
# last modification: 19/08/2024
# References: https://docs.python.org/3/library/asyncio.html, https://docs.python.org/3/library/logging.html, https://pypi.org/project/python-dotenv/

import os
import idna
import asyncio
import logging
from dotenv import load_dotenv
from loggedActions import LoggedActions
from connection import Connection, newUser

# configure logging to show only error messages
logging.basicConfig(level=logging.ERROR)
logging.getLogger('slixmpp').setLevel(logging.ERROR)

# load environment variables from .env file
load_dotenv()

# get the domain from the .env file and prepare it using idna
DOMAIN = os.getenv('DOMAIN')
if DOMAIN:
    DOMAIN = idna.encode(DOMAIN).decode('utf-8')

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
            pass
        
        # --- exit ---
        elif option == "4":
            break
        
        else:
            print("!error, invalid option.")

if __name__ == "__main__":
    main()
