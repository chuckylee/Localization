# import socket

# HOST = '192.168.56.1'  # Standard loopback interface address (localhost)
# PORT = 20019        # Port to listen on (non-privileged ports are > 1023)


# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             data = conn.recv(1024)
#             if data:
#                 print('Received', data)
#             conn.sendall(data)

