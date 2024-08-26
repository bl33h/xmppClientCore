# xmppClientCore

A Python-based XMPP client that provides user authentication, contact management, group chat, and account management functionalities through a user-friendly interface built with Tkinter.

<p align="center">
  <br>
  <img src="https://i.imgur.com/UlPi1k3.png" alt="pic" width="500">
  <br>
</p>
<p align="center" >
  <a href="#Files">Files</a> •
  <a href="#Features">Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#note">How To Use</a>
</p>

## Files

- **main.py**: The main entry point for the XMPP client. This file initializes the application and handles the core logic, including setting up the connection to the XMPP server and managing the user interface.
- **loggedActions.py**: Handles logging actions and events within the client, providing a record of user activities and server responses.
- **contactsRelated.py**: Manages all contacts-related functionalities, including retrieving contact lists, adding, deleting, and updating contacts.
- **criticalUt.py**: Contains critical utility functions used across the project, such as handling errors, managing configurations, and ensuring that essential services are operational.
- **connection.py**: Establishes and maintains the connection to the XMPP server. This file is responsible for handling the connection lifecycle, including reconnection logic and network error handling.
- **deleteAccount.py**: Manages the process of account deletion, allowing users to remove their account from the XMPP server securely.

## Features

The project provides the following features:

- **User Authentication**: Secure login and logout functionality.
- **Contact Management**: Add, remove, and update contacts in your XMPP roster.
- **Group Chat**: Create and join group chats on the XMPP server, allowing for real-time communication in rooms.
- **Message Sending and Receiving**: Send and receive messages to/from individual contacts or group chats.
- **Files exchange**: Send and receive files to/from direct messages, they will be saved in the files directory.
- **Account Management**: Manage your XMPP account, including deleting your account from the server.
- **Logging**: All critical actions and events are logged for auditing and debugging purposes.
- **Graphical User Interface**: User-friendly interface built using Tkinter for ease of use.

## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com), [Python](https://www.python.org), [slixmpp](https://slixmpp.readthedocs.io/en/latest/), [base64](https://docs.python.org/3/library/base64.html), [asyncio](https://docs.python.org/3/library/asyncio.html), and [Tkinter](https://docs.python.org/es/3/library/tkinter.html) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/bl33h/xmppClientCore

# Open the folder
$ cd src

# Run the project
$ python main.py
```

## Note
Ensure that your .env file is inside the src directory and contains the following environment variables, appropriately configured with your XMPP server details:
- **SERVICE_URL**=ws://yourdomain.com:7070/ws/
- **DOMAIN**=yourdomain.com
- **RESOURCE**=example
