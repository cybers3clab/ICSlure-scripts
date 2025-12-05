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
    udp_send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:            
        try:
            # RECEIVE DATA FROM RASPBERRY USING SPI

            # SEND DATA TO SIMULINK USING UDP SOCKET
            message = 0 # pump value read from gpio
            message = struct.pack('<I',message)
            udp_send_socket.sendto(message, (IP, PORT_PUMP))
            
            message = 1 # valv value read from gpio
            message = struct.pack('<I',message)
            udp_send_socket.sendto(message, (IP, PORT_VALV))
        except KeyboardInterrupt:
            udp_send_socket.close()
            print("UDP server stopped.")