# Advanced Multi-Client Chat Application

## Overview

This project is an Advanced Multi-Client Chat Application developed in Python using Socket Programming and Tkinter GUI. It enables multiple users to communicate over a TCP network while implementing authentication, security features, message history, and session management.

---

## Features

### User Authentication
- User Registration
- Secure Login
- SHA-256 Password Hashing
- Duplicate Login Prevention
- Maximum 5 Failed Login Attempts
- Account Lock after Multiple Failed Attempts

### Chat Features
- Multi-Client Chat
- Broadcast Messaging
- Private Messaging
- Online User List
- GUI-Based Client
- Disconnect Button

### Security Features
- Password Encryption (SHA-256)
- Security Log Generation
- Input Validation
- Session Timeout (Automatic Logout)
- Login and Logout Logging

### Data Storage
- User Database (users.csv)
- Chat History (chat_history.csv)
- Security Log (security_log.txt)

### Additional Features
- Displays Last 5 Messages After Login
- Automatic Online User Refresh
- TCP Socket Communication
- Multi-threaded Server

---

## Technologies Used

- Python 3
- Socket Programming
- Tkinter GUI
- Threading
- CSV File Handling
- Hashlib (SHA-256)
- Regular Expressions
- Wireshark (Network Packet Analysis)

---

## Project Structure

```
assignment7/
│
├── server.py
├── client_gui.py
├── users.csv
├── chat_history.csv
├── security_log.txt
├── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Assignment7.git
```

Move into the project directory

```bash
cd Assignment7
```

---

## Running the Server

```bash
python3 server.py
```

---

## Running the Client

```bash
python3 client_gui.py
```

Run multiple client instances to simulate multiple users.

---

## User Registration

1. Enter Server IP
2. Enter Username
3. Enter Password
4. Click Register

The password is securely stored using SHA-256 hashing.

---

## Login

1. Enter registered Username
2. Enter Password
3. Click Login

The application prevents duplicate logins and limits failed login attempts.

---

## Security Features

### Password Hashing

Passwords are stored using SHA-256 encryption.

### Failed Login Protection

- Maximum 5 failed attempts
- Account locking after repeated failures

### Input Validation

- Username must contain only letters, numbers, and underscores.
- Username minimum length: 3 characters.
- Password minimum length: 6 characters.

### Security Logging

The application records:

- Registration Success
- Registration Failure
- Login Success
- Login Failure
- Logout
- Session Timeout
- Account Lock

---

## Chat Features

### Broadcast Message

Send a message to all connected users.

Example

```
Hello Everyone
```

---

### Private Message

Use

```
/msg username message
```

Example

```
/msg lucky Hello
```

---

### Online Users

The application displays all connected users in the right-side panel.

---

### Last Five Messages

After successful login, the server automatically displays the user's last five sent messages.

---

### Session Timeout

Inactive users are automatically disconnected after the configured timeout period.

---

## Wireshark Analysis

The application communicates using:

- Protocol: TCP
- Port: 5000

Packet captures can be monitored using Wireshark on the loopback (`lo`) interface.

---

## Screenshots

Include screenshots of:

- Registration
- Login
- Broadcast Chat
- Private Chat
- Online Users
- Security Log
- Session Timeout
- Wireshark Packet Capture

---

## Future Improvements

- End-to-End Encryption
- SQLite Database
- Group Chat
- File Sharing
- Emoji Support
- Voice Messaging
- Message Delivery Status

---

## Author

**Murali Konala**

B.Tech Computer Science Engineering

Python Socket Programming Assignment

```
