## Line Following AGV with Bluetooth Control - Setup Guide
This guide explains how to set up the Raspberry Pi Pico W2 and Pololu 3pi+ 2040 Robot for the networked line-following AGV project.
# Hardware Requirements

Pololu 3pi+ 2040 Robot
Raspberry Pi Pico W2 (with Bluetooth)
USB cables for programming both devices
Line track (black line on white background)
Computer with Python and required tools installed

# Software Requirements

MicroPython for the Pico W2
Lingua Franca C runtime for the Pololu 3pi+ 2040
Terminal software (e.g., Thonny for MicroPython)

# Setup Instructions
Step 1: Prepare the Pololu 3pi+ 2040 Robot

Install Lingua Franca toolchain

Follow the Lingua Franca installation guide for C target
Ensure you have the Raspberry Pi Pico SDK installed


Compile the Line Following Program

Navigate to the Polou Robot Code directory
Compile the FinalProject.lf Lingua Franca program:

lfc FinalProject.lf

This will generate a build directory with the compiled firmware


Flash the Robot

Connect the Pololu robot to your computer via USB
Hold the BOOTSEL button while connecting to enter bootloader mode
Copy the generated .uf2 file from the build directory to the mounted drive
The robot will automatically reboot with the new firmware



Step 2: Prepare the Raspberry Pi Pico W2

Install MicroPython

Download the latest MicroPython firmware for the Raspberry Pi Pico W
Connect the Pico W2 to your computer while holding the BOOTSEL button
Copy the MicroPython UF2 file to the mounted drive
The Pico will reboot with MicroPython installed


Upload the BLE Code

Use a tool like Thonny or rshell to connect to the Pico W2
Copy the following files to the Pico:

ble_advertising.py
ble_simple_peripheral.py
main.py





Step 3: Connect the Devices

Wire the UART Connection

Connect the UART pins between the Pico W2 and the Pololu robot:

Pico W2 TX (GPIO 4) → Pololu 3pi+ RX (GPIO 29)
Pico W2 RX (GPIO 5) → Pololu 3pi+ TX (GPIO 28)
Connect GND between both devices
Optionally, provide power from the Pololu to the Pico W2




Mount the Pico W2 on the Pololu Robot

Securely attach the Pico W2 to the robot
Ensure all connections are stable during robot movement



Step 4: Test the System

Power on the Robot

The display should show "CALIBRATING" during startup
Roll the robot over the line to calibrate the line sensors
After calibration, it should switch to "FOLLOWING" mode


Test Bluetooth Connectivity

Use a Bluetooth app on your phone or computer to scan for the "Alim's Pico" device
Connect to the device
The display should show "BLE Connected" when connected
Send test commands (FORWARD, STOP, SPEED 5, etc.)
Verify that the robot responds to the commands



Command Reference

FORWARD: Resume or continue forward motion
STOP: Halt the robot
REVERSE: Move in reverse along the path
SPEED x: Set speed (x = 1-9, with 9 being fastest)
STATE: Request current robot status

Troubleshooting

If the robot doesn't respond to commands, check the UART connections
If Bluetooth connection fails, reset the Pico W2
For line following issues, adjust the line sensor calibration
Check battery levels if the robot is behaving erratically

LED Indicators

Robot status is shown on the OLED display
