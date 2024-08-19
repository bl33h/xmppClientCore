# Copyright (C), 2024-2025, bl33h 
# fileName: main.py
# author: Sara Echeverria
# version: I
# creation: 01/08/2024
# last modification: 18/08/2024
# references: https://docs.python.org/3/library/asyncio.html

import os
import asyncio
import logging
from dotenv import load_dotenv
from connection import Connection, newUser

# configure logging to show only error messages
logging.basicConfig(level=logging.ERROR)
logging.getLogger('slixmpp').setLevel(logging.ERROR)

# load environment variables from .env file
load_dotenv()

# get the domain from the .env file
domain = os.getenv('DOMAIN')

def main():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    while True:
        print("\n--- welcome to the xmpp client core chat ---")
        print("[1.] log in")
        print("[2.] sign up")
        print("[3.] delete existing account")
        print("[4.] exit")
        option = input("• enter your option: ")
        
        if option == "1":
            print("\ncredentials are required to log in.")
            username = input("-> username: ")
            password = input("-> password: ")
            jid = f"{username}@{domain}"
            xmppClient = Connection(jid, password)
            xmppClient.connect(disable_starttls=True, use_ssl=False)
            xmppClient.process(forever=False)
            if xmppClient.loggedIn:
                print("you are in!")
                
        elif option == "2":
            print("\nlet's create a new account.")
            username = input("-> username: ")
            password = input("-> password: ")
            jid = f"{username}@{domain}"
            status = newUser(jid, password)
            statusMessage = "\nyou just created an account!\n" if status else "\n!there was an error, try again\n"
            print(statusMessage)
        elif option == "3":
            pass
        elif option == "4":
            break
        else:
            print("!error, invalid option.")

if __name__ == "__main__":
    main()