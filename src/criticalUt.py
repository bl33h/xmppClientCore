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