import socket
import threading
import pickle
import mysql.connector
import ssl

# Server Configuration
SERVER_HOST = '10.1.2.4' 
SERVER_PORT = 8080

SSL_CERTIFICATE = 'server.crt'
SSL_PRIVATE_KEY = 'server.key'

connection = mysql.connector.connect(host="localhost", user="root", password="chaitanya1705", database="networking")
print("[CONNECTION DB]:Connected to mysql")

cursor = connection.cursor()
print("[CONNECTION DB]: created cursor for queries")

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

#for admin client to modify voters/candidates
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(SSL_CERTIFICATE, SSL_PRIVATE_KEY)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket programming(server)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)

def send_data(socket, data):
    my_data = pickle.dumps(data)
    socket.send(my_data)

def remove_voter(cursor, connection, pesu_srn):
    cursor.execute("DELETE FROM voters WHERE pesu_srn = %s", (pesu_srn,))
    connection.commit()
    return {'status': 'success', 'message': 'Voter removed successfully.'}

def remove_candidate(cursor, connection, candidate_id):
    cursor.execute("DELETE FROM candidates WHERE candidate_id = %s", (candidate_id,))
    connection.commit()
    return {'status': 'success', 'message': 'Candidate removed successfully.'}

def handle_client(client_socket, cursor, connection):
    client_address = client_socket.getpeername()
    hostname = socket.gethostname()
    print(f"{hostname}{client_address} connected.")
    
    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        request_data = pickle.loads(data)
        action = request_data['action']

        if action == 'check_eligibility':
            first_name = request_data['first_name']
            last_name = request_data['last_name']
            date_of_birth = request_data['date_of_birth']
            pesu_srn = request_data['pesu_srn']

            cursor.execute("SELECT * FROM voters WHERE first_name = %s AND last_name = %s AND date_of_birth = %s AND pesu_srn = %s",(first_name, last_name, date_of_birth, pesu_srn))
            voter = cursor.fetchone()

            if not voter:
                response = {'status': 'failure', 'message': 'You are not in the voters list.'}
                client_socket.send(pickle.dumps(response))
                break

            if voter[4]==1:  
                # Check if the voter has already voted
                response = {'status': 'failure', 'message': 'You have already voted.'}
                client_socket.send(pickle.dumps(response))
                break

            response = {'status': 'success', 'message': 'You are eligible to vote.', 'pesu_srn': pesu_srn}
            client_socket.send(pickle.dumps(response))

            # Wait for the vote details from the client
            vote_data = client_socket.recv(1024)
            if not vote_data:
                break

            vote_request_data = pickle.loads(vote_data)
            vote_action = vote_request_data['action']

            if vote_action == 'cast_vote':
                candidate_choice = vote_request_data['candidate_choice']

                cursor.execute("UPDATE candidates SET votes_recieved = votes_recieved + 1 WHERE candidate_id = %s", (candidate_choice,))
                cursor.execute("UPDATE voters SET has_voted = TRUE WHERE pesu_srn = %s", (pesu_srn,))
                connection.commit()

                response = {'status': 'success', 'message': 'Vote cast successfully.'}
                client_socket.send(pickle.dumps(response))
                break

        elif action == 'get_candidates':
            # Retrieve candidate information from the database
            cursor.execute("SELECT * FROM candidates")
            candidates = cursor.fetchall()
            response = {'candidates': candidates}
            client_socket.send(pickle.dumps(response))

        elif action == 'get_live_updates':
            # Retrieve live updates on vote counts from the database
            cursor.execute("SELECT * FROM candidates")
            candidates = cursor.fetchall()
            response = {'candidates': candidates}
            client_socket.send(pickle.dumps(response))

        elif action == 'add_voter':
            # admin_client
            if request_data.get('admin_username') == ADMIN_USERNAME and request_data.get('admin_password') == ADMIN_PASSWORD:
                first_name = request_data['first_name']
                last_name = request_data['last_name']
                date_of_birth = request_data['date_of_birth']
                pesu_srn = request_data['pesu_srn']

                cursor.execute("INSERT INTO voters (first_name, last_name, date_of_birth, pesu_srn) VALUES (%s, %s, %s, %s)",
                               (first_name, last_name, date_of_birth, pesu_srn))
                connection.commit()

                response = {'status': 'success', 'message': 'Voter added successfully.'}
            else:
                response = {'status': 'failure', 'message': 'Admin credentials are incorrect.'}

            client_socket.send(pickle.dumps(response))

        elif action == 'add_candidate':
            if request_data.get('admin_username') == ADMIN_USERNAME and request_data.get('admin_password') == ADMIN_PASSWORD:
                candidate_id=request_data['candidate_id']
                candidate_name = request_data['candidate_name']

                # Insert candidate into the candidates table
                cursor.execute("INSERT INTO candidates (candidate_id, candidate_name, votes_recieved) VALUES (%s, %s, %s)", (candidate_id, candidate_name, 0))
                connection.commit()

                response = {'status': 'success', 'message': 'Candidate added successfully.'}
            else:
                response = {'status': 'failure', 'message': 'Admin credentials are incorrect.'}

            client_socket.send(pickle.dumps(response))

        
        elif action == 'remove_voter':
            if request_data.get('admin_username') == ADMIN_USERNAME and request_data.get('admin_password') == ADMIN_PASSWORD:
                pesu_srn = request_data['pesu_srn']
                response = remove_voter(cursor, connection, pesu_srn)
            else:
                response = {'status': 'failure', 'message': 'Admin credentials are incorrect.'}
            client_socket.send(pickle.dumps(response))

        elif action == 'remove_candidate':
            if request_data.get('admin_username') == ADMIN_USERNAME and request_data.get('admin_password') == ADMIN_PASSWORD:
                candidate_id = request_data['candidate_id']
                response = remove_candidate(cursor, connection, candidate_id)
            else:
                response = {'status': 'failure', 'message': 'Admin credentials are incorrect.'}
            client_socket.send(pickle.dumps(response))

        elif action == 'disconnect':
            break
    print(f"{hostname}{client_address} Disconnected.")
    client_socket.close()

print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

try:
    while True:
        # Accept a connection using the SSL-wrapped server socket
        client_socket, addr = server_socket.accept()
        ssl_client_socket = context.wrap_socket(client_socket, server_side=True)

        # Start a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(ssl_client_socket, cursor, connection))
        client_handler.start()

except Exception as e:
    print(f"Server error: {str(e)}")
finally:
    server_socket.close()
    connection.close()
