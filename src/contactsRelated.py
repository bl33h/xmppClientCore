# Copyright (C), 2024-2025, bl33h 
# fileName: contactsRelated.py
# author: Sara Echeverria
# version: I
# creation: 19/08/2024
# last modification: 24/08/2024
# References: https://pypi.org/project/slixmpp/, https://xmpp.org/extensions/xep-0029.html

import slixmpp
from criticalUt import loadDomain

# load and prepare the domain using the function
DOMAIN = loadDomain()

# --- send a friend request ---
async def sendFriendRequest(xmpp_client: slixmpp.ClientXMPP):
    friendsUser = input("who would you like to send a friend request to? (username): ")
    potentialFriendsUser = f"{friendsUser}@{DOMAIN}"
    xmpp_client.send_presence_subscription(potentialFriendsUser)
    print("-> you just sent a friend request to", potentialFriendsUser)
    await xmpp_client.get_roster()

# --- manage incoming requests ---
async def requestsManagement(xmpp_client: slixmpp.ClientXMPP, presence):
    print(f"received presence from {presence['from']} of type {presence['type']}")
   
    # reciprocate the subscription request
    if presence["type"] == "subscribe":
        
        xmpp_client.send_presence(pto=presence['from'], ptype='subscribed')
        if not xmpp_client.usersContacts[presence['from']].subscription_to:
            xmpp_client.send_presence_subscription(presence['from'], ptype='subscribe')
        print(f"accepted and reciprocated subscription with {presence['from']}")
    
    # confirm mutual subscription status
    elif presence['type'] == 'subscribed':
        await xmpp_client.get_roster()
        roster_item = xmpp_client.usersContacts[presence['from']]
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
        presence = "xa"
    elif status == "3":
        presence = "away"
    elif status == "4":
        presence = "dnd"
    else:
        presence = "available"

    description = input("your description will be: ")
    self.send_presence(pshow=presence, pstatus=description)
    await self.get_roster()

# --- show contact's information ---
async def friendsInfo(self):
    friendsUser = input("\nwhat's the contact you would like to check? (username): ")
    fullUsername = f"{friendsUser}@{DOMAIN}"

    # user's contacts
    usersContacts = self.client_roster

    # unexisting user
    found = False

    if not usersContacts:
        print("\n!error, no contacts found !")
        return

    # presence mapping
    presenceMapping = {
        "available": "available",
        "xa": "extended away",
        "away": "away",
        "dnd": "do not disturb"
    }

    # check if the user is in the contacts
    for contact in usersContacts.keys():
        
        if contact == fullUsername:

            found = True
            print(f"\n-> friend's full username: {contact}")

            presenceVal = "Offline"
            status = "None"

            # friends info
            for _, presence in usersContacts.presence(contact).items():
                presenceType = presence["show"] or "Offline"
                presenceVal = presenceMapping.get(presenceType, "Offline")

                status = presence["status"] or "None"

            print(f"-> friends status: {presenceVal}")
            print(f"-> friends description: {status}\n")

    # user not in the contacts
    if not found:
        print("\n!you are not friends with this user, send a friend request to get more info !")

# --- show the list of contacts ---
async def friendsList(self):
    usersContacts = self.client_roster

    # empty list
    if (not usersContacts):
        print("you have no contacts yet, send a friend request to get started !")
        return

    # friends in the list
    for contact in usersContacts.keys():

        if (contact == self.boundjid.bare):
            continue

        print(f"\n• friend's full username: [{contact}]")
        presenceVal = "offline"
        status = "none"

        for _, presence in usersContacts.presence(contact).items():
            presenceVal = presence["show"] or "offline"
            status = presence["status"] or "none"

        print(f"-> friends status: {presenceVal}")
        print(f"-> friends description: {status}")