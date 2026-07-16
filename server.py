import socket
import threading
import csv
import os
import hashlib
import re
import time
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000
SESSION_TIMEOUT = 300

clients = []
usernames = {}
user_info = {}
failed_attempts = {}

stats = {
    "connected_users": 0,
    "messages_processed": 0,
    "broadcast_messages": 0,
    "private_messages": 0
}

CHAT_HISTORY = "chat_history.csv"
USERS_FILE = "users.csv"
SECURITY_LOG = "security_log.txt"


# ------------------------------------
# Hash Password
# ------------------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ------------------------------------
# Validate Input
# ------------------------------------
def validate_input(username, password):
    if len(username) < 3:
        return False, "Username must be at least 3 characters."

    if not re.match(r"^[A-Za-z0-9_]+$", username):
        return False, "Username can contain only letters, numbers and _"

    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    return True, ""


# ------------------------------------
# Security Log
# ------------------------------------
def write_security_log(event):
    with open(SECURITY_LOG, "a") as file:
        file.write(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {event}\n"
        )


# ------------------------------------
# Register User
# ------------------------------------
def register_user(username, password):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as file:
            file.write("username,password_hash\n")

    with open(USERS_FILE, "r") as file:
        for line in file.readlines()[1:]:
            user = line.strip().split(",")
            if len(user) >= 2 and user[0] == username:
                return False

    with open(USERS_FILE, "a") as file:
        file.write(f"{username},{hash_password(password)}\n")
    return True


# ------------------------------------
# Verify Login
# ------------------------------------
def verify_user(username, password):
    if not os.path.exists(USERS_FILE):
        return False

    with open(USERS_FILE, "r") as file:
        for line in file.readlines()[1:]:
            user = line.strip().split(",")
            if len(user) >= 2:
                if user[0] == username and user[1] == hash_password(password):
                    return True
    return False


# ------------------------------------
# Create chat history file if missing
# ------------------------------------
if not os.path.exists(CHAT_HISTORY):
    with open(CHAT_HISTORY, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "sender", "receiver", "message_type", "message"])


# ------------------------------------
# Save every message
# ------------------------------------
def save_history(sender, receiver, msg_type, message):
    with open(CHAT_HISTORY, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            sender,
            receiver,
            msg_type,
            message
        ])


# ------------------------------------
# Show last 5 messages after reconnect
# ------------------------------------
def show_last_messages(username, client):
    if not os.path.exists(CHAT_HISTORY):
        return

    rows = []
    with open(CHAT_HISTORY, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["sender"] == username:
                rows.append(row)

    rows = rows[-5:]
    if rows:
        client.send("\n===== Last 5 Messages =====\n".encode())
        for row in rows:
            line = f'{row["timestamp"]} -> {row["receiver"]}: {row["message"]}\n'
            client.send(line.encode())
        client.send("===========================\n".encode())


# ------------------------------------
# Broadcast message
# ------------------------------------
def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except Exception:
                pass


# ------------------------------------
# Send private message
# ------------------------------------
def private_message(sender_socket, sender_name, target_name, message):
    if target_name not in usernames.values():
        sender_socket.send(f"User '{target_name}' not found.\n".encode())
        return

    for sock, name in usernames.items():
        if name == target_name:
            text = f"[PRIVATE] {sender_name}: {message}"
            sock.send(text.encode())
            sender_socket.send(f"[To {target_name}] {message}".encode())
            
            stats["private_messages"] += 1
            save_history(sender_name, target_name, "PRIVATE", message)
            return


# ------------------------------------
# Send online user list
# ------------------------------------
def send_user_list(client):
    online = [usernames[sock] for sock in clients]
    text = "\nOnline Users\n------------------\n" + "\n".join(online) + "\n"
    client.send(text.encode())


# ------------------------------------
# Handle one client
# ------------------------------------
def handle_client(client):
    while True:
        try:
            msg = client.recv(1024).decode()
            if not msg:
                break

            stats["messages_processed"] += 1
            sender = usernames[client]

            # Ignore background commands
            if msg.strip() == "/list":
                send_user_list(client)
                continue

            # Update activity only for real user actions
            user_info[sender]["last_activity"] = datetime.now()

            if msg.startswith("/msg "):
                parts = msg.split(" ", 2)
                if len(parts) < 3:
                    client.send("Usage: /msg username message\n".encode())
                    continue
                private_message(client, sender, parts[1], parts[2])
                continue

            message = f"[{sender}] {msg}"
            broadcast(message.encode(), client)
            stats["broadcast_messages"] += 1
            save_history(sender, "ALL", "BROADCAST", msg)

        except Exception:
            break

    # Disconnect routine
    username = usernames.get(client)
    if client in clients:
        clients.remove(client)
    if client in usernames:
        del usernames[client]
        
    if username and username in user_info:
        user_info[username]["status"] = "Offline"
        stats["connected_users"] -= 1
        broadcast(f"\n*** {username} left the chat ***\n".encode())
        print(f"{username} disconnected.")
        write_security_log(f"LOGOUT : {username}")
        
    client.close()


# ------------------------------------
# Session Timeout Monitor
# ------------------------------------
def session_timeout_monitor():
    while True:
        current = datetime.now()
        for client in clients[:]:
            username = usernames.get(client)
            if username is None:
                continue

            last = user_info[username]["last_activity"]
            elapsed = (current - last).total_seconds()
            
            # Print for testing/debugging purposes
            # print(f"[{username}] Inactive for: {elapsed:.1f}s")

            if elapsed >= SESSION_TIMEOUT:
                print(f"Session timeout for {username}")
                write_security_log(f"SESSION TIMEOUT : {username}")

                try:
                    client.send("SESSION_TIMEOUT".encode())
                except Exception:
                    pass

                try:
                    client.shutdown(socket.SHUT_RDWR)
                except Exception:
                    pass

                try:
                    client.close()
                except Exception:
                    pass

        time.sleep(2)


# ------------------------------------
# Accept new clients
# ------------------------------------
def receive():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Advanced Chat Server running on port {PORT}...\n")

    while True:
        client, address = server.accept()
        try:
            request = client.recv(1024).decode().strip()
            parts = request.split("|")

            if len(parts) != 3:
                client.send("Invalid Request".encode())
                client.close()
                continue

            action, username, password = parts[0], parts[1], parts[2]

            if action == "REGISTER":
                valid, message = validate_input(username, password)
                if not valid:
                    write_security_log(f"REGISTER FAILED : {username} ({message})")
                    client.send(message.encode())
                    client.close()
                    continue

                if register_user(username, password):
                    write_security_log(f"REGISTER SUCCESS : {username}")
                    client.send("Registration Successful".encode())
                else:
                    write_security_log(f"REGISTER FAILED : {username} (Username Exists)")
                    client.send("Username already exists".encode())
                client.close()
                continue

            if action == "LOGIN":
                if username not in failed_attempts:
                    failed_attempts[username] = 0
                
                if failed_attempts[username] >= 5:
                    client.send("Account Locked. Too many failed login attempts.".encode())
                    client.close()
                    continue

                if not verify_user(username, password):
                    failed_attempts[username] += 1
                    write_security_log(f"LOGIN FAILED : {username}")
                    
                    remaining = 5 - failed_attempts[username]

                    if remaining <= 0:
                        write_security_log(f"ACCOUNT LOCKED : {username}")
                        client.send("Account Locked. Too many failed login attempts.".encode())
                    else:
                        client.send(
                            f"Invalid username or password.\nAttempts Remaining: {remaining}".encode()
                        )
                    client.close()
                    continue
                
                if username in usernames.values():
                    client.send("User already logged in".encode())
                    client.close()
                    continue
                
                failed_attempts[username] = 0
                write_security_log(f"LOGIN SUCCESS : {username}")
                client.send("LOGIN_SUCCESS\n".encode())
                
                ready_msg = client.recv(1024).decode().strip()
                if ready_msg != "READY":
                    client.close()
                    continue

            # Complete the connection process
            clients.append(client)
            usernames[client] = username
            
            user_info[username] = {
                "ip": address[0],
                "port": address[1],
                "login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "Online",
                "last_activity": datetime.now()
            }
            stats["connected_users"] += 1

            print("=" * 50)
            print(f"User Connected : {username}")
            print(f"IP Address     : {address[0]}")
            print(f"Port           : {address[1]}")
            print("=" * 50)

            broadcast(f"\n*** {username} joined the chat ***\n".encode())
            show_last_messages(username, client)

            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()

        except Exception as e:
            client.close()
            print(f"Error accepting connection: {e}")


if __name__ == "__main__":
    print("=" * 50)
    print(" Advanced Multi-Client Chat Server ")
    print("=" * 50)

    threading.Thread(
        target=session_timeout_monitor,
        daemon=True
    ).start()

    receive()
