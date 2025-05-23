import bluetooth
import time
from ble_advertising import advertising_payload
from micropython import const
from machine import Pin, UART

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

# Single UUID for the UART service and one characteristic
_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_CHAR = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),  # TX and RX on same characteristic
    _FLAG_READ | _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE | _FLAG_NOTIFY,
)
_UART_SERVICE = (_UART_UUID, (_UART_CHAR,))

uart = UART(1, baudrate=115200, tx=4, rx=5)  # Adjust pins and baudrate as needed

class BLESimplePeripheral:
    def __init__(self, ble, name="mpy-uart"):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle,),) = self._ble.gatts_register_services((_UART_SERVICE,))
        self._connections = set()
        self._write_callback = None
        self._payload = advertising_payload(name=name, services=[_UART_UUID])
        self._advertise()

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            uart.write("Connected\n")
            print("New connection", conn_handle)
            self._connections.add(conn_handle)

        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            uart.write("Disconnected\n")
            print("Disconnected", conn_handle)
            self._connections.remove(conn_handle)
            self._advertise()

        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            if value_handle == self._handle and self._write_callback:
                value = self._ble.gatts_read(self._handle)
                self._write_callback(value)

    def send(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle, data)

    def is_connected(self):
        return len(self._connections) > 0

    def on_write(self, callback):
        self._write_callback = callback

    def _advertise(self, interval_us=500000):
        print("Starting advertising")
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

