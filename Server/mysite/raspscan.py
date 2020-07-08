# import asyncio
# import websockets

# async def hello(websocket, path):
#     name = await websocket.recv()
#     print(f"< {name}")

# start_server = websockets.serve(hello, "192.168.2.14", 8090)

# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()
# import socket
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('192.168.2.14', 8090))
# client.send(b"HELLO, How are you ? Welcome to Akash hacking World")
# from_server = client.recv(4096)
# client.close()
