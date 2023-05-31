import socket

# Server address and port
server_address = ('127.0.0.1', 12345)

# Path to the photo you want to send
# C:\Skola_LS_23\Tymovy projekt\TestovacieFotky
photo_path = r"D:\School\TimovyProjekt\TimovyProjekt\TestovacieFotky\RealSensePic0.jpg"

# Read the photo file as binary data
with open(photo_path, 'rb') as file:
    photo_data = file.read()

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect(server_address)
print('Connected to server:', server_address)

try:
    # Send the photo data to the server
    client_socket.sendall(photo_data)
except Exception as e:
    print(e)
finally:
    # Close the client socket
    client_socket.close()
