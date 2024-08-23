# Copyright (C), 2024-2025, bl33h 
# fileName: loggedActions.py
# author: Sara Echeverria
# version: I
# creation: 19/08/2024
# last modification: 20/08/2024
# References: https://pypi.org/project/slixmpp/, https://xmpp.org/extensions/xep-0029.html

import base64
import slixmpp
from aioconsole import ainput
from criticalUt import loadDomain, failedAuth, pluginsInteraction, handlersInteraction

# load and prepare the domain using the function
DOMAIN = loadDomain()

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
        self.add_event_handler("message", self.messageNotis)
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
        # file exclusive
        # Reference: https://pypi.org/project/xmpp-http-upload/
        if message["type"] == "chat":
            if message["body"].startswith("file://"):
                cont = message["body"].split("://")
                ext = cont[1]
                info = cont[2]
                processedInfo = base64.b64decode(info)
                with open(f"./files/receivedFile.{ext}", "wb") as fileW:
                    fileW.write(processedInfo)
                print(f"\n❑  you just got a FILE from {str(message['from']).split('/')[0]}: ./files/receivedFile.{ext}.\n")

            # actual message (other types)
            else:
                groupSender = str(message["from"])
                currentReceiver = groupSender.split("/")[0]

                if currentReceiver == self.receiversCredential:
                    print(f"\n\n{currentReceiver}: {message['body']}")
                else:
                    print(f"\n❑ you just got a message from [{currentReceiver}]\n")
    
    # --- join a room ---
    async def joinGroup(self, roomsName):
        # append the domain to the room name
        fullRoomName = f"{roomsName}@conference.{DOMAIN}"
        self.group = fullRoomName
        
        # join the group
        await self.plugin["xep_0045"].join_muc(room=fullRoomName, nick=self.boundjid.user)
        print(f"\nyou are currently chatting in {fullRoomName}.\n")

        # group chat loop
        while (True):

            message = await ainput("type your message: ")

            # exit the chat
            if (message == "exit"):
                self.current_chatting_jid = ""
                self.plugin["xep_0045"].leave_muc(room=fullRoomName, nick=self.boundjid.user)
                self.group = ""
                break

            # actual message
            else:
                print(f"{self.usersCredential.split('@')[0]}: {message}")
                self.send_message(mto=fullRoomName, mbody=message, mtype="groupchat")
    
    # --- participate in different rooms ---
    async def groupMessage(self):
        print("1. join group")
        print("2. exit\n")
        roomsOpt = input("• enter your option: ")

        if roomsOpt == "1":
            joiningRoom = input("what's the room's name?: ")
            await self.joinGroup(joiningRoom)

        elif roomsOpt == "2":
            pass
    
    # --- notify a group's message ---
    async def messageNotis(self, message):
        groupSender = message["mucnick"]

        # process the notification
        if (groupSender != self.boundjid.user):
            print(f"❑ {groupSender} in {message['from']}: {message['body']}\n")
    
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
                await self.groupMessage()
            
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