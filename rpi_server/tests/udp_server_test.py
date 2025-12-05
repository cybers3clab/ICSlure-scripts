import socket
import time

print("Starting server...")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

pins = [False, False, False]
i = 0
while True:
    msg = ""
    for pin in pins:
        msg += "1" if pin else "0"
    n = int(msg, 2)
    sock.sendto(n.to_bytes(1, "little", signed=False), ("localhost", 29900))
    print(f"Sent: {msg}")

    pins[i] = not pins[i]
    i = (i + 1) % 3

    time.sleep(5)