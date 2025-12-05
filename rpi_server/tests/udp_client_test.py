import socket

print("Starting client...")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("localhost", 29900))

while True:
    data, _ = sock.recvfrom(1024)
    print("" + str(int.from_bytes(data, "little", signed=False)) + f", {len(data)}")