# Copyright (C), 2024-2025, bl33h 
# fileName: main.py
# author: Sara Echeverria
# version: I
# creation: 24/08/2024
# last modification: 24/08/2024
# References: https://slixmpp.readthedocs.io/en/latest/api/xmlstream/xmlstream.html

import slixmpp
from slixmpp.xmlstream.stanzabase import ET

# reference: class & functions created with help of chatgpt4
# -> prompt1: "i have the following files to implement a xmpp client (i uploaded the files), review them"
# -> promt2: "i already have a functioning deleting account function (previously placed in the connection.py file), 
# despite that, i am encoutering an error related to the correct async function implementation. give me the code base solution,
# place the comments and documentation in a similar way to the other files"

# --- delete account ---
class DeleteExistentAccount(slixmpp.ClientXMPP):

    def __init__(self, jid, password):
        super().__init__(jid=jid, password=password)
        self.user_to_delete = jid
        self.add_event_handler("session_start", self.start)

    # --- start the session ---
    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        await self.deleteAccount()
        self.disconnect()

    # --- actual deleting account async function ---
    async def deleteAccount(self):
        response = self.Iq()
        response["from"] = self.boundjid.user
        response["type"] = "set"

        # stanza to remove the account
        fragment = ET.fromstring(
            "<query xmlns='jabber:iq:register'><remove/></query>"
        )

        response.append(fragment)
        await response.send()
        deletedUser = self.boundjid.jid.split("/")[0]
        print(f"\n!the account [{deletedUser}] has been deleted\n")