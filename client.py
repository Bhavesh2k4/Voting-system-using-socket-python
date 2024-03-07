import socket
import pickle
import tkinter as tk
from PIL import Image, ImageTk
import ssl

SERVER_HOST = '10.1.2.4'
SERVER_PORT = 8080
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


context = ssl.create_default_context()
context.check_hostname = True
context.verify_mode = ssl.CERT_REQUIRED

context.load_verify_locations(cafile='server.crt')

ssl_client_socket = context.wrap_socket(client_socket, server_hostname=SERVER_HOST)

try:
    ssl_client_socket.connect((SERVER_HOST, SERVER_PORT))
except ssl.SSLError as e:
    print(f"SSL Handshake Failed: {e}")
    exit()

print("SSL Handshake Successful!")


server_cert = ssl_client_socket.getpeercert()
print("Server Certificate:")
print(f"  Issuer: {server_cert['issuer']}")
print(f"  Subject: {server_cert['subject']}")
print(f"  Expiration Date: {server_cert['notAfter']}")

def send_data(socket, data):
    serialized_data = pickle.dumps(data)
    socket.send(serialized_data)

def view_live_updates():
    try:
        live_updates_request = {'action': 'get_live_updates'}
        send_data(ssl_client_socket, live_updates_request)
        live_updates_response = ssl_client_socket.recv(1024)
        
        if not live_updates_response:
            print("No data received from server")
            return

        live_updates_response = pickle.loads(live_updates_response)

        if 'candidates' in live_updates_response:
            candidates = live_updates_response['candidates']
            live_updates_text.config(state=tk.NORMAL)
            live_updates_text.delete(1.0, tk.END)
            live_updates_text.insert(tk.END, "\nLive Updates:\n")
            for candidate in candidates:
                live_updates_text.insert(tk.END, f"Candidate {candidate[0]} ({candidate[1]}): {candidate[2]} votes\n")
            live_updates_text.config(state=tk.DISABLED)
    except (ConnectionAbortedError, EOFError) as e:
        print("Connection error:", e)

def check_eligibility_and_cast_vote():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    date_of_birth = dob_entry.get()
    pesu_srn = pesu_srn_entry.get()

    eligibility_request = {
        'action': 'check_eligibility',
        'first_name': first_name,
        'last_name': last_name,
        'date_of_birth': date_of_birth,
        'pesu_srn': pesu_srn
    }

    send_data(ssl_client_socket, eligibility_request)
    eligibility_response = pickle.loads(ssl_client_socket.recv(1024))

    if eligibility_response['status'] == 'success':
        eligibility_status_label.config(text=eligibility_response['message'])

        candidate_choice = candidate_srn_entry.get()

        vote_request = {
            'action': 'cast_vote',
            'pesu_srn': pesu_srn,
            'candidate_choice': candidate_choice
        }

        send_data(ssl_client_socket, vote_request)

        vote_response = pickle.loads(ssl_client_socket.recv(1024))
        vote_status_label.config(text=vote_response['message'])

    else:
        eligibility_status_label.config(text=f"Voter eligibility check failed. Reason: {eligibility_response['message']}")

root = tk.Tk()
root.title("Voter's Portal")

background_image = Image.open("bcg_image.jpg")
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

font_style = ("Poppins", 11, "bold")

heading_label = tk.Label(root, text="VOTER'S PORTAL", font=("Poppins", 20, "bold"))
heading_label.pack(pady=20)

voter_frame = tk.Frame(root)
voter_frame.pack(pady=10)

tk.Label(voter_frame, text="First Name: ", font=font_style).grid(row=0, column=0, padx=5, pady=5)
first_name_entry = tk.Entry(voter_frame, font=font_style)
first_name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(voter_frame, text="Last Name: ", font=font_style).grid(row=1, column=0, padx=5, pady=5)
last_name_entry = tk.Entry(voter_frame, font=font_style)
last_name_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(voter_frame, text="Date of Birth (DD-MM-YYYY): ", font=font_style).grid(row=2, column=0, padx=5, pady=5)
dob_entry = tk.Entry(voter_frame, font=font_style)
dob_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(voter_frame, text="PESU_SRN: ", font=font_style).grid(row=3, column=0, padx=5, pady=5)
pesu_srn_entry = tk.Entry(voter_frame, font=font_style)
pesu_srn_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(voter_frame, text="Candidate SRN: ", font=font_style).grid(row=4, column=0, padx=5, pady=5)
candidate_srn_entry = tk.Entry(voter_frame, font=font_style)
candidate_srn_entry.grid(row=4, column=1, padx=5, pady=5)

vote_button = tk.Button(root, text="Check Eligibility and Cast Vote", command=check_eligibility_and_cast_vote, font=font_style)
vote_button.pack(pady=5)

eligibility_status_label = tk.Label(root, text="", font=font_style)
eligibility_status_label.pack(pady=5)

live_updates_frame = tk.Frame(root)
live_updates_frame.pack(pady=10)

live_updates_text = tk.Text(live_updates_frame, width=50, height=10, state=tk.DISABLED, font=font_style)
live_updates_text.pack()

live_updates_button = tk.Button(root, text="View Live Updates", command=view_live_updates, font=font_style)
live_updates_button.pack(pady=5)

vote_status_label = tk.Label(root, text="", font=font_style)
vote_status_label.pack(pady=5)

root.mainloop()

ssl_client_socket.close()
