import usb.core
import usb.util
import time

# Define the Vendor ID and Product ID of the Pico
VENDOR_ID = 0x2E8A  # Raspberry Pi's VID (adjust if different)
PRODUCT_ID = 0x000A  # Example PID (adjust if different)

# Endpoint addresses (should match your Pico's configuration)
BULK_IN_EP = 0x81  # Endpoint for receiving data from Pico
BULK_OUT_EP = 0x02  # Endpoint for sending data to Pico
PACKET_SIZE = 64  # Endpoint packet size

# Find the Pico USB device
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if dev is None:
    raise ValueError("Device not found")

# Set configuration if needed (only needed if device has multiple configurations)
dev.set_configuration()


def send_data(data):
    """Send data to the Pico."""
    if isinstance(data, str):
        data = data.encode()  # Encode string data to bytes
    dev.write(BULK_OUT_EP, data, timeout=1000)


def receive_data():
    """Receive data from the Pico."""
    try:
        data = dev.read(BULK_IN_EP, PACKET_SIZE, timeout=1000)
        return bytes(data).decode()  # Decode bytes to string if needed
    except usb.core.USBError as e:
        if e.errno == 110:  # Timeout error
            return None
        else:
            raise


# Example usage: Send and receive data in a loop
while True:
    # Send a message to the Pico
    send_data("Hello from Host")

    # Wait briefly for a response
    time.sleep(0.1)

    # Receive and print the response
    response = receive_data()
    if response:
        print("Received:", response)

    # Repeat every second
    time.sleep(1)
