# Voting Management System

The Voting Management System is a technically sophisticated platform designed to facilitate secure and reliable elections through a client-server architecture. Leveraging advanced technologies such as Python, Tkinter, SSL/TLS encryption, and MySQL database, this system ensures robust functionality and security in the electoral process.

## Components:

### 1. Admin Client:
- Allows administrators to manage voters and candidates efficiently.
- Functionalities include adding and removing voters and candidates.
- Provides an intuitive graphical interface built using Tkinter in Python.
- Utilizes SSL/TLS encryption for secure communication with the server.

### 2. Voter Client:
- Empowers voters to check eligibility and cast their votes securely.
- Features include checking eligibility based on provided credentials and casting votes for preferred candidates.
- User-friendly interface designed with Tkinter and incorporates SSL/TLS encryption for secure communication with the server.

### 3. Server:
- Serves as the central component responsible for handling client requests.
- Manages database interactions for storing voter and candidate information using MySQL.
- Implements SSL/TLS encryption for secure communication with clients.
- Supports functionalities such as checking voter eligibility, casting votes, and providing live updates on vote counts.

### 4. Database:
- MySQL database manages two tables (Voters & Candidates) taking their SRNs as the primary key.

## Security Measures:
- SSL/TLS encryption ensures secure communication between clients and the server, preventing unauthorized access and data tampering.
- Strict authentication mechanisms are implemented to verify the identities of administrators and voters, enhancing system security.

## Usage:
- Clone the repository.
- Set up the MySQL database and configure the server accordingly.
- Run the server script and ensure it is up and running.
- Launch the admin and voter clients, and interact with the system using the provided graphical interfaces.

