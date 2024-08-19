# Copyright (C), 2024-2025, bl33h 
# fileName: connection.py
# author: Sara Echeverria
# version: I
# creation: 18/08/2024
# last modification: 19/08/2024
# References: https://docs.python.org/3/library/logging.html, https://pypi.org/project/slixmpp/, https://github.com/poezio/slixmpp
# https://pypi.org/project/xmpppy/, https://pypi.org/project/python-dotenv/

import os
import xmpp
import slixmpp
import logging
from dotenv import load_dotenv

# configure logging to show only error messages
logging.basicConfig(level=logging.ERROR)
logging.getLogger('slixmpp').setLevel(logging.ERROR)

# load environment variables from .env file
load_dotenv()

# get the domain from the .env file
domain = os.getenv('DOMAIN')

class Connection(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.startSession)
        self.add_event_handler("failed_auth", self.failedAuth)
        self.loggedIn = False

    # --- start the session ---
    async def startSession(self, event):
        self.send_presence()
        await self.get_roster()
        self.loggedIn = True
        self.disconnect()

# --- sign up a new user ---
def newUser(jid, password):
    
    # connect to the server
    xmppJid = xmpp.JID(jid)
    xmppAccount = xmpp.Client(xmppJid.getDomain(), debug=[])
    xmppAccount.connect()

    # status to create the account.
    xmppStatus = xmpp.features.register(
        xmppAccount,
        xmppJid.getDomain(),
        { "username": xmppJid.getNode(), "password": password }
    )

    return bool(xmppStatus)