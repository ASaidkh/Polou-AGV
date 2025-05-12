import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
from machine import Pin, UART
import time

# Set up BLE
ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble, "Alim's Pico")

# Set up onboard LED for status
led = Pin("LED", Pin.OUT)

# Set up UART
uart = UART(1, baudrate=115200, tx=4, rx=5)  # Adjust pins and baudrate as needed

# Define a function to handle incoming BLE data
def handle_command(data):
    decoded = data.decode("utf-8").strip()
    print("Received BLE command:", decoded)

    # Forward command to UART device
    if decoded.startswith("FORWARD") or decoded.startswith("STOP") or decoded.startswith("REVERSE"):
        uart.write(decoded + "\n")

    elif decoded.startswith("SPEED"):
        parts = decoded.split()
        if len(parts) == 2 and parts[1].isdigit() and 1 <= int(parts[1]) <= 9:
            uart.write(decoded + "\n")
        else:
            sp.send("Invalid SPEED command. Use: SPEED x (1–9)")

    elif decoded == "STATE":
        uart.write("STATE\n")

    else:
        sp.send("Unknown command.")

# BLE write callback
def on_rx(data):
    handle_command(data)

# Main loop
uart_buffer = b""
while True:
    if sp.is_connected():
        sp.on_write(on_rx)

       
        if uart.any():
            uart_buffer += uart.read(uart.any())

            #only send complete lines
            if b"\n" in uart_buffer:
                lines = uart_buffer.split(b"\n")
                for line in lines[:-1]:
                    try:
                        print("Recieved data: ", line.decode("utf-8").strip())
                        sp.send(line.decode("utf-8").strip())
                    except:
                        sp.send("Error decoding UART.")
                uart_buffer = lines[-1]  # Keep any incomplete line in the buffer

    time.sleep(0.05)  # Slightly shorter sleep for more responsive I/O

