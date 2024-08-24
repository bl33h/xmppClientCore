# Copyright (C), 2024-2025, bl33h 
# fileName: contactsRelated.py
# author: Sara Echeverria
# version: I
# creation: 19/08/2024
# last modification: 23/08/2024
# References: https://pypi.org/project/slixmpp/, https://xmpp.org/extensions/xep-0029.html

import slixmpp
from criticalUt import loadDomain

# load and prepare the domain using the function
DOMAIN = loadDomain()

# --- send a friend request ---
async def sendFriendRequest(xmpp_client: slixmpp.ClientXMPP):
    yourUsername = input("who would you like to send a friend request to? (username): ")
    potentialContactUsername = f"{yourUsername}@{DOMAIN}"
    xmpp_client.send_presence_subscription(potentialContactUsername)
    print("-> you just sent a friend request to", potentialContactUsername)
    await xmpp_client.get_roster()

# --- manage incoming requests ---
async def requestsManagement(xmpp_client: slixmpp.ClientXMPP, presence):
    print(f"received presence from {presence['from']} of type {presence['type']}")
   
    # reciprocate the subscription request
    if presence["type"] == "subscribe":
        xmpp_client.send_presence(pto=presence['from'], ptype='subscribed')
        if not xmpp_client.client_roster[presence['from']].subscription_to:
            xmpp_client.send_presence_subscription(presence['from'], ptype='subscribe')
        print(f"accepted and reciprocated subscription with {presence['from']}")
    
    # confirm mutual subscription status
    elif presence['type'] == 'subscribed':
        await xmpp_client.get_roster()
        roster_item = xmpp_client.client_roster[presence['from']]
        if not (roster_item['subscription_to'] and roster_item['subscription_from']):
            print("subscription not mutual, fixing...")
            xmpp_client.send_presence_subscription(presence['from'], ptype='subscribe')

# --- change the status ---
async def changeStatus(self):
    print("\t[1] available")
    print("\t[2] extended away")
    print("\t[3] away")
    print("\t[4] do not disturb")
    status = input("\nwhat's the number of the status you would like to change to ?: ")

    # available options
    if status == "1":
        presence = "available"
    elif status == "2":
        presence = "extended away"
    elif status == "3":
        presence = "away"
    elif status == "4":
        presence = "do not disturb"
    else:
        presence = "available"

    description = input("your description will be: ")
    self.send_presence(pshow=presence, pstatus=description)
    await self.get_roster()
