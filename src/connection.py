# Copyright (C), 2024-2025, bl33h 
# fileName: connection.py
# author: Sara Echeverria
# version: I
# creation: 18/08/2024
# last modification: 24/08/2024
# References: https://docs.python.org/3/library/logging.html, https://pypi.org/project/slixmpp/, https://github.com/poezio/slixmpp
# https://pypi.org/project/xmpppy/, https://pypi.org/project/python-dotenv/, https://xmpp.org/extensions/xep-0029.html

import xmpp
import slixmpp
import logging
from criticalUt import loadDomain
from slixmpp.xmlstream.stanzabase import ET

# configure logging to show only error messages
logging.basicConfig(level=logging.ERROR)
logging.getLogger('slixmpp').setLevel(logging.ERROR)

DOMAIN = loadDomain()

class Connection(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.user_to_delete = jid
        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        await self.delete()
        self.disconnect()

    async def delete(self):
        response = self.Iq()
        response["from"] = self.boundjid
        response["type"] = "set"

        fragment = ET.fromstring(
            "<query xmlns='jabber:iq:register'><remove/></query>"
        )

        response.append(fragment)
        try:
            await response.send()
            deleted_user = self.boundjid.bare
            print(f"\n!the account [{deleted_user}] has been deleted")
        except Exception as e:
            print(f"!error deleting account: [{e}]")

# --- sign up a new user ---
def newUser(jid, password):
    xmppJid = xmpp.JID(jid)
    xmppAccount = xmpp.Client(xmppJid.getDomain(), debug=[])
    xmppAccount.connect()

    xmppStatus = xmpp.features.register(
        xmppAccount,
        xmppJid.getDomain(),
        { "username": xmppJid.getNode(), "password": password }
    )

    return bool(xmppStatus)