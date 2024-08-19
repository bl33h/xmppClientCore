# Copyright (C), 2024-2025, bl33h 
# fileName: loggedActions.py
# author: Sara Echeverria
# version: I
# creation: 19/08/2024
# last modification: 19/08/2024
# References: https://pypi.org/project/slixmpp/

import slixmpp
import asyncio
from criticalUt import failedAuth

class LoggedActions(slixmpp.ClientXMPP):
    # --- logged user parameters ---
    def __init__(self, jid, password):
        super().__init__(jid=jid, password=password)
        self.receiverCredential = ""
        self.userCredential = jid
        self.loggedUser = False
        self.group = ""
        self.add_event_handler("session_start", self.startSession)
        self.add_event_handler("failed_auth", failedAuth)

    # --- start the session ---
    async def startSession(self, event):
        self.send_presence(pshow="chat", pstatus="--- you are now connected to the chat ---")
        self.loggedUser = True
        await self.get_roster()
        await self.actions()

    # --- actions available for the logged user ---
    def actions(self):
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
                pass
            
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
                self.disconnect()
                break

            else:
                print("!error, invalid option.")