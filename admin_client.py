import tkinter as tk
import socket
import pickle
import ssl

SERVER_HOST = '10.1.2.4'
SERVER_PORT = 8080

def send_data(socket, data):
    serialized_data = pickle.dumps(data)
    socket.send(serialized_data)

def add_voter():
    voter_data = {
        'first_name': first_name_entry.get(),
        'last_name': last_name_entry.get(),
        'date_of_birth': dob_entry.get(),
        'pesu_srn': pesu_srn_entry.get()
    }

    add_voter_request = {
        'action': 'add_voter',
        'admin_username': admin_username,
        'admin_password': admin_password,
        **voter_data
    }

    send_data(ssl_adminclient_socket, add_voter_request)
    add_voter_response = pickle.loads(ssl_adminclient_socket.recv(1024))
    print(add_voter_response)

def remove_voter():
    pesu_srn = pesu_srn_remove_entry.get()

    remove_voter_request = {
        'action': 'remove_voter',
        'admin_username': admin_username,
        'admin_password': admin_password,
        'pesu_srn': pesu_srn
    }

    send_data(ssl_adminclient_socket, remove_voter_request)
    remove_voter_response = pickle.loads(ssl_adminclient_socket.recv(1024))
    print(remove_voter_response)

def add_candidate():
    candidate_data = {
        'candidate_id': candidate_id_entry.get(),
        'candidate_name': candidate_name_entry.get(),
    }

    add_candidate_request = {
        'action': 'add_candidate',
        'admin_username': admin_username,
        'admin_password': admin_password,
        **candidate_data
    }

    send_data(ssl_adminclient_socket, add_candidate_request)
    add_candidate_response = pickle.loads(ssl_adminclient_socket.recv(1024))
    print(add_candidate_response)


def remove_candidate():
    candidate_id = candidate_id_remove_entry.get()

    remove_candidate_request = {
        'action': 'remove_candidate',
        'admin_username': admin_username,
        'admin_password': admin_password,
        'candidate_id': candidate_id
    }

    send_data(ssl_adminclient_socket, remove_candidate_request)
    remove_candidate_response = pickle.loads(ssl_adminclient_socket.recv(1024))
    print(remove_candidate_response)

def exit_program():
    ssl_adminclient_socket.close()
    root.destroy()

root = tk.Tk()
root.title("Admin Menu")

font_style = ("Poppins", 11)

add_voter_frame = tk.Frame(root, pady=10)
add_voter_frame.pack(fill=tk.BOTH, padx=10)

remove_voter_frame = tk.Frame(root, pady=10)
remove_voter_frame.pack(fill=tk.BOTH, padx=10)

add_candidate_frame = tk.Frame(root, pady=10)
add_candidate_frame.pack(fill=tk.BOTH, padx=10)

remove_candidate_frame = tk.Frame(root, pady=10)
remove_candidate_frame.pack(fill=tk.BOTH, padx=10)

tk.Label(add_voter_frame, text="First Name: ", font=font_style).grid(row=0, column=0, padx=5, pady=5)
first_name_entry = tk.Entry(add_voter_frame, font=font_style)
first_name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(add_voter_frame, text="Last Name: ", font=font_style).grid(row=1, column=0, padx=5, pady=5)
last_name_entry = tk.Entry(add_voter_frame, font=font_style)
last_name_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(add_voter_frame, text="Date of Birth (DD-MM-YYYY): ", font=font_style).grid(row=2, column=0, padx=5, pady=5)
dob_entry = tk.Entry(add_voter_frame, font=font_style)
dob_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(add_voter_frame, text="PESU_SRN: ", font=font_style).grid(row=3, column=0, padx=5, pady=5)
pesu_srn_entry = tk.Entry(add_voter_frame, font=font_style)
pesu_srn_entry.grid(row=3, column=1, padx=5, pady=5)

add_voter_button = tk.Button(add_voter_frame, text="Add Voter", command=add_voter, font=font_style)
add_voter_button.grid(row=4, columnspan=2, pady=5)

tk.Label(remove_voter_frame, text="PESU_SRN to Remove: ", font=font_style).grid(row=0, column=0, padx=5, pady=5)
pesu_srn_remove_entry = tk.Entry(remove_voter_frame, font=font_style)
pesu_srn_remove_entry.grid(row=0, column=1, padx=5, pady=5)

remove_voter_button = tk.Button(remove_voter_frame, text="Remove Voter", command=remove_voter, font=font_style)
remove_voter_button.grid(row=1, columnspan=2, pady=5)

tk.Label(add_candidate_frame, text="Candidate's PESU SRN: ", font=font_style).grid(row=0, column=0, padx=5, pady=5)
candidate_id_entry = tk.Entry(add_candidate_frame, font=font_style)
candidate_id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(add_candidate_frame, text="Candidate's Name: ", font=font_style).grid(row=1, column=0, padx=5, pady=5)
candidate_name_entry = tk.Entry(add_candidate_frame, font=font_style)
candidate_name_entry.grid(row=1, column=1, padx=5, pady=5)

add_candidate_button = tk.Button(add_candidate_frame, text="Add Candidate", command=add_candidate, font=font_style)
add_candidate_button.grid(row=2, columnspan=2, pady=5)

tk.Label(remove_candidate_frame, text="Candidate ID to Remove: ", font=font_style).grid(row=0, column=0, padx=5, pady=5)
candidate_id_remove_entry = tk.Entry(remove_candidate_frame, font=font_style)
candidate_id_remove_entry.grid(row=0, column=1, padx=5, pady=5)

remove_candidate_button = tk.Button(remove_candidate_frame, text="Remove Candidate", command=remove_candidate, font=font_style)
remove_candidate_button.grid(row=1, columnspan=2, pady=5)

exit_button = tk.Button(root, text="Exit", command=exit_program, font=font_style)
exit_button.pack(pady=10)

admin_username = 'admin'
admin_password = 'admin123'
adminclient_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
context = ssl.create_default_context()
context.check_hostname = True
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations(cafile='server.crt')
ssl_adminclient_socket = context.wrap_socket(adminclient_socket, server_hostname=SERVER_HOST)
try:
    ssl_adminclient_socket.connect((SERVER_HOST, SERVER_PORT))
except ssl.SSLError as e:
    print(f"SSL Handshake Failed: {e}")
    exit()

print("SSL Handshake Successful!")

# Verify and print server's certificate information
server_cert = ssl_adminclient_socket.getpeercert()
print("Server Certificate:")
print(f"  Issuer: {server_cert['issuer']}")
print(f"  Subject: {server_cert['subject']}")
print(f"  Expiration Date: {server_cert['notAfter']}")

root.mainloop()
