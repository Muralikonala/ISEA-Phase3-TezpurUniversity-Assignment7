# ISEAPhase3-TezpurUniversity-Assignment8

## GUI Based Multi-Client Chat Application Using TCP

### Student Details

- **Name:** Murali Konala
- **Roll Number:** 323506402101
- **Course:** B.Tech CSE
- **Assignment:** Phase 3 - Assignment 8

---

## Project Description

This project is a GUI-based Multi-Client Chat Application developed using Python Socket Programming and Tkinter. It supports multiple clients communicating simultaneously through a TCP server while providing authentication, private messaging, chat history, session management, and performance monitoring.

---

## Features

- User Registration
- User Login Authentication
- Password Hashing (SHA-256)
- GUI Chat Interface (Tkinter)
- Multi-Client Communication
- Broadcast Messaging
- Private Messaging
- Online Users List
- Chat History Storage (CSV)
- Session Timeout
- Graceful Client Disconnection
- Connection Management
- Improved Exception Handling
- Configuration Management using `config.json`
- Thread-safe Scalability Enhancement
- Performance Monitoring
- CPU & Memory Usage Measurement
- Delay & Throughput Measurement
- Performance Graph Generation

---

## Technologies Used

- Python 3
- Socket Programming
- Tkinter
- Multithreading
- JSON
- CSV
- psutil
- pandas
- matplotlib
- Wireshark

---

## Project Structure

```
ISEAPhase3-TezpurUniversity-Assignment8/
│
├── server.py
├── client_gui.py
├── config.json
├── users.csv
├── chat_history.csv
├── security_log.txt
├── performance_results.csv
├── generate_graphs.py
├── delay_graph.png
├── throughput_graph.png
├── cpu_graph.png
├── memory_graph.png
├── README.md
└── report.pdf
```

---

## Installation

Install required packages:

```bash
pip install psutil pandas matplotlib
```

Ubuntu:

```bash
sudo apt install python3-psutil
pip3 install pandas matplotlib
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

---

## Performance Evaluation

The application records:

- Message Delay
- Throughput
- CPU Usage
- Memory Usage

Results are stored in:

```
performance_results.csv
```

Graphs generated:

- Delay vs Connected Clients
- Throughput vs Connected Clients
- CPU Usage vs Connected Clients
- Memory Usage vs Connected Clients

---

## Wireshark Verification

Display filter:

```
tcp.port == 5000
```

Captured Operations:

- TCP Handshake
- Login
- Broadcast Message
- Private Message
- Client Disconnect

---

## Assignment Tasks Completed

| Task | Status |
|------|--------|
| Connection Management | ✅ |
| Reliability Enhancement | ✅ |
| Scalability Enhancement | ✅ |
| Configuration Management | ✅ |
| Performance Evaluation | ✅ |
| Wireshark Verification | ✅ |
| GitHub Update | ✅ |
| Handwritten Reflection | ✅ |

---

## Future Improvements

- End-to-End Encryption
- File Sharing
- Voice Chat
- Group Chat
- Database Integration
- Automatic Reconnection
- Message Delivery Status

---

## Author

**Murali Konala**

B.Tech Computer Science and Engineering

GitHub Repository:

```
GitHub Repository:

ISEAPhase3-TezpurUniversity-MultiClientChat
```