# Copyright (C), 2024-2025, bl33h 
# fileName: criticalUt.py
# author: Sara Echeverria
# version: I
# creation: 19/08/2024
# last modification: 19/08/2024

# --- failed authentication ---
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