import sys, json, threading
import socket
import board, busio, digitalio, mcp48xx
import time

RPI_PINS = {
    "cs": [board.D25, board.D16],
    "pins": [board.D22, board.D27, board.D17]
}

RECEIVE_DELAY = 0.2
SEND_DELAY = 0.2


def simToPLC_handler(src, dst):
    # --UDP SOCKET SETUP--
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Datagram socket
    sock.bind((src["ip"], src["port"])) # Bind to address and port

    # --SETUP DAC--
    spi = busio.SPI(board.SCK, board.MOSI) # SPI bus
    cs = digitalio.DigitalInOut(RPI_PINS["cs"][dst["cs"]]) # Chip select
    dac = mcp48xx.MCP4811(spi, cs) # DAC interface

    try:
        while(True):
            # Read data from packet received on UDP socket
            data, _ = sock.recvfrom(1024)

            # Decode data
            data = int.from_bytes(data, "little", signed=False)
            # Send data to DAC
            try:
                dac.raw_value = data
            except AttributeError:
                print(f"Failed to send data \"{data}\" to DAC{dst['cs']}")

            # Slow down loop
            time.sleep(RECEIVE_DELAY)
    finally:
        sock.close()

def plcToSim_handler(src, dst):
    # --GPIO SETUP--
    pins = []
    for (i, pin) in zip(range(len(src)), src):
        pins[i] = digitalio.DigitalInOut(RPI_PINS["pins"][pin])
        pins[i].direction = digitalio.Direction.OUTPUT

    # --UDP SOCKET SETUP--
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Datagram socket

    try:
        while(True):
            # Read data from GPIO
            msg = ""
            for pin in pins:
                msg += "1" if pin.value else "0"

            # Encode data
            data = int(msg, 2)

            # Send data to UDP socket
            sock.sendto(data.to_bytes(1, "little", signed=False), (dst["ip"], dst["port"]))  # Send data to UDP socket

            # Slow down loop
            time.sleep(SEND_DELAY)
    finally:
        sock.close()

if __name__ == "__main__":
    # --LOAD CONFIGURATION--
    # Get configuration file name from argument
    confFileName = sys.argv[1]
    # Get configuration file data
    conf = {}
    with open(confFileName) as f:
        conf = json.load(f)
    print(f"Configuration file \"{confFileName}\": {len(conf)} signals loaded")

    # --SETUP SIGNAL THREADS--
    # Start threads for each signal to manage between PLC and Simulation
    for signal in conf:
        # Get signal configuration data
        signalType = conf[signal]["type"]
        src = conf[signal]["src"]
        dst = conf[signal]["dst"]

        # Create thread for signal type
        if signalType == "simToPLC":
            x = threading.Thread(target=simToPLC_handler, args=(src, dst))
            x.start()
            print(f"{signal}: {src} -> {dst}")
        elif signalType == "plcToSim":
            x = threading.Thread(target=plcToSim_handler, args=(src, dst))
            x.start()
            print(f"{signal}: {src} -> {dst}")
        else:
            print(f"Unknown signal type \"{signalType}\" for signal \"{signal}\"")
