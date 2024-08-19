# Copyright (C), 2024-2025, bl33h 
# fileName: connection.py
# author: Sara Echeverria
# version: I
# creation: 18/08/2024
# last modification: 18/08/2024
# references: https://pypi.org/project/slixmpp/, https://github.com/poezio/slixmpp

import os
import slixmpp
from dotenv import load_dotenv
import logging

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
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("failed_auth", self.failedAuth)
        self.loggedIn = False

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        self.loggedIn = True
        self.disconnect()

    def failedAuth(self, event):
        errorText = event.get('text', '')
        errorCondition = event.get('condition', '')

        if errorCondition:
            errorMessage = f"!error condition: {errorCondition}"
        elif errorText:
            errorMessage = f"!error text: {errorText}"
        else:
            errorMessage = 'no error message provided'

        print(f"!login failed: {errorMessage}")
        self.disconnect()

# sign up a new user
def newUser(jid, password):
    try:
        # reference: https://github.com/poezio/slixmpp/tree/master/slixmpp/plugins
        xmpp = slixmpp.ClientXMPP(jid, password)
        xmpp.register_plugin('xep_0030')
        xmpp.register_plugin('xep_0004')
        xmpp.register_plugin('xep_0066')
        xmpp.register_plugin('xep_0077')
        xmpp['xep_0077'].force_registration = True

        xmpp.connect()
        xmpp.process(block=True)
        return True
    
    except Exception as e:
        print(f"!error, something went wrong: {e}")
        return False