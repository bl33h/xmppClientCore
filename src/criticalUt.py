# Copyright (C), 2024-2025, bl33h 
# fileName: criticalUt.py
# author: Sara Echeverria
# version: I
# creation: 19/08/2024
# last modification: 24/08/2024

import os
import idna
from dotenv import load_dotenv

# --- get and prepare the domain ---
def loadDomain():
    # load environment variables from .env file
    load_dotenv()

    # get the domain from the .env file and prepare it using idna
    DOMAIN = os.getenv('DOMAIN')
    if not DOMAIN:
        raise ValueError("DOMAIN environment variable is not set or is empty.")
    DOMAIN = idna.encode(DOMAIN).decode('utf-8')
    return DOMAIN

# --- failed authentication ---
def failedAuth(event):
    errorText = event.get('text', '')
    errorCondition = event.get('condition', '')
    errorMessage = "unknown error occurred"
    if errorCondition:
        errorMessage = f"error condition: {errorCondition}"
    elif errorText:
        errorMessage = f"error text: {errorText}"
    print(f"!login failed: {errorMessage}")

# --- plugins registration ---
# reference: https://github.com/poezio/slixmpp/tree/master/slixmpp/plugins
def pluginsInteraction(self):
    self.register_plugin("xep_0004")
    self.register_plugin("xep_0030")
    self.register_plugin("xep_0045")
    self.register_plugin("xep_0060")
    self.register_plugin("xep_0050")
    self.register_plugin("xep_0066")
    self.register_plugin("xep_0071")
    self.register_plugin("xep_0085")
    self.register_plugin("xep_0199")
    self.register_plugin("xep_0363")

# --- handlers (events) registration ---
def handlersInteraction(self):
    self.add_event_handler("sessionStart", self.startSession)
    self.add_event_handler("failedAuth", failedAuth)
    self.add_event_handler("message", self.getMessages)
    self.add_event_handler("messageNotis", self.messageNotis)