import socket

client_socket = socket.socket()
base_directory = ""


# Opens a client socket on the given port
def open_socket(port_number):
    host = socket.gethostname()
    port = port_number
    client_socket.connect((host, port))


# Sends text to the open socket
def send_query_to_socket(message):
    client_socket.sendall((message + '\n').encode())

    data = client_socket.recv(100000).decode()
    return data


# Sends an exact query to the open socket
def collect_exact_query(file_name):
    return send_query_to_socket("Exact_Query:" + file_name)


def set_base_directory():
    client_socket.sendall(("Base_path_directory_request" + '\n').encode())

    data = client_socket.recv(100000).decode()
    return data[:-2]
