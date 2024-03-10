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

## MySQL Database setup:
terminal-> 
" mysql -u root -p (macos) or open mysql command line client(windows) "

- create database networking;(if database is not created yet);

- use networking;
  
- create table voters(
first_name varchar(255) NOT NULL,
last_name varchar(255) NOT NULL,
date_of_birth varchar(255) NOT NULL,
pesu_srn varchar(25) PRIMARY KEY,
has_voted tinyint(1) DEFAULT='0');

- create table candidates(
candidate_id varchar(255) PRIMARY KEY,
candidate_name varchar(255) NOT NULL,
votes_recieved int DEFAULT='0');

## To generate self signed SSL certificate
https://www.openssl.org/source/   
download the file and verify installation using  " openssl --version "

IN CMD/TERMINAL :

- "openssl genrsa -out server.key 2048"
- "openssl req -new -key server.key -out server.csr"
- "openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt"
Enter the details and save them somewhere (useful later)

NOTE: If for some reason you get an error stating cerfificate not valid for the given IP , try

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt -subj "/C=<country code >/ST=<state>/L <location>/O=< >U/OU=< >/CN=< >/emailAddress=< >" -addtext "subjectAltName = IP:<your IP>"

you can find our IP by :
ifconfig(mac /linux) or ipconfig(windows)

