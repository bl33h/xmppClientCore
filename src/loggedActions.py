# Copyright (C), 2024-2025, bl33h 
# fileName: loggedActions.py
# author: Sara Echeverria
# version: I
# creation: 19/08/2024
# last modification: 19/08/2024
# References: https://pypi.org/project/slixmpp/

import os
import idna
import base64
import slixmpp
from aioconsole import ainput
from dotenv import load_dotenv
from criticalUt import failedAuth, pluginsInteraction, handlersInteraction

# load environment variables from .env file
load_dotenv()

# get the domain from the .env file and prepare it using idna
DOMAIN = os.getenv('DOMAIN')
if not DOMAIN:
    raise ValueError("DOMAIN environment variable is not set or is empty.")
DOMAIN = idna.encode(DOMAIN).decode('utf-8')

class LoggedActions(slixmpp.ClientXMPP):
    # --- logged user parameters ---
    def __init__(self, jid, password):
        super().__init__(jid=jid, password=password)
        self.receiversCredential = ""
        self.usersCredential = jid
        self.loggedUser = False
        self.group = ""
        handlersInteraction(self)
        pluginsInteraction(self)
        self.add_event_handler("session_start", self.startSession)
        self.add_event_handler("failed_auth", failedAuth)

    # --- start the session ---
    async def startSession(self, event):
        self.send_presence(pshow="chat", pstatus="--- you are now connected to the chat ---")
        self.loggedUser = True
        await self.get_roster()
        await self.actions()

    # --- send a direct message ---
    async def directMessage(self):
        username = input("who would you like to send a message to? (username): ")
        dmReceiver = f"{username}@{DOMAIN}"
        self.receiversCredential = dmReceiver
        print(f"\nyou are currently chatting with {dmReceiver}.")

        # chat loop
        while True:
            message = await ainput("\ntype your message: ")

            # exit the chat
            if message == "exit":
                self.usersCredential = ""
                break
            
            # message is a file
            else:
                print(f"{self.usersCredential.split('@')[0]}: {message}")
                self.send_message(mto=dmReceiver, mbody=message, mtype="chat")
    
    # --- receive messages ---
    # reference: https://slixmpp.readthedocs.io/en/latest/getting_started/sendlogout.html
    async def getMessages(self, message):
        if message["type"] == "chat":
            if message["body"].startswith("file://"):
                cont = message["body"].split("://")
                ext = cont[1]
                info = cont[2]
                processedInfo = base64.b64decode(info)
                with open(f"./files/received_file.{ext}", "wb") as fileW:
                    fileW.write(processedInfo)
                print(f"\n<!> {str(message['from']).split('/')[0]} has sent you a file: ./files/received_file.{ext}.\n")

            # unsupported type
            else:
                emitter = str(message["from"])
                currentReceiver = emitter.split("/")[0]

                if currentReceiver == self.receiversCredential:
                    print(f"\n\n{currentReceiver}: {message['body']}")
                else:
                    print(f"\n❑ you just got a message from [{currentReceiver}]\n")

    # --- actions available for the logged user ---
    async def actions(self):
        while self.loggedUser:
            print("you are in!")
            print("\n--- You are currently logged in and your options are ---")
            print("[1] send a message")
            print("[2] send a group message")
            print("[3] update status (presence)")
            print("[4] view contacts")
            print("[5] check the info of a specific contact")
            print("[6] add a contact")
            print("[7] exit")
            option = input("• enter your option: ")

            # --- send a dm ---
            if option == "1":
                await self.directMessage()
            
            # --- send a group message ---
            elif option == "2":
                pass
            
            # --- update status ---
            elif option == "3":
                pass
            
            # --- view contacts ---
            elif option == "4":
                pass
            
            # --- check the info of a specific contact ---
            elif option == "5":
                pass
            
            # --- add a contact ---
            elif option == "6":
                pass
            
            # --- exit ---
            elif option == "7":
                break

            else:
                print("!error, invalid option")