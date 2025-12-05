import socket, threading, time, struct

IP = "localhost"
PORT = 10001
PORT_PUMP = 10012
PORT_VALV = 10013
MAX_VAL = 100
N_BIT = 10
PAUSE = 1 # in sec

# val: valore da normalizzare
# max_val: massimo valore assunto da val
# n_bit: numero di bit
#
# res: valore normalizzato a <bit> bit convertito in int
def norm(val, max_val=MAX_VAL, n_bit=N_BIT):
    bit_val = 0
    if n_bit == 0:
        bit_val = 0
    else:
        bit_val = 2**n_bit
    
    n = val*bit_val//max_val
    return ((int)(n))

def main():
    while True:            
        try:
            # RECEIVE DATA FROM SIMULINK USING UDP SOCKET

            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.bind((IP, PORT))
            data, address = udp_socket.recvfrom(1024)
            data = struct.unpack('d',data)[0]
            data = norm(data)
            print(f"Received data from {address}: {data}")

            # SEND DATA TO RASPBERRY USING SPI

        except KeyboardInterrupt:
            udp_socket.close()
            print("UDP server stopped.")
        
        time.sleep(PAUSE)