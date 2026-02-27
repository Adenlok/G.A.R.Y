
import serial.tools.list_ports
import threading
import serial
import time
import sys
import serial.tools


ports = list(serial.tools.list_ports.comports())

print("Available Ports:")

for p in ports:

    print(f"- Device: {p.device} | Description: {p.description}")

if not ports:

    print("No USB devices detected! Check your cable.")

# Update this to match your discovered port (ACM0 or ACM1)
PORT = '/dev/ttyACM2' 

try:
    ser = serial.Serial(PORT, 115200, timeout=1)
    time.sleep(2) # Give Uno time to reboot
    print(f"Connected to {PORT} at 115200 baud.")
except Exception as e:
    print(f"Error: {e}")
    sys.exit()


def read_serial():
    """Background thread to constantly update motor stats"""
    while True:
        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').strip()
                if line.startswith("TELEMETRY:"):
                    parts = line.split(":")[1].split(",")
                    telemetry["distL"] = int(parts[0])
                    telemetry["distR"] = int(parts[1])
                    telemetry["speedL"] = int(parts[2])
                    telemetry["speedR"] = int(parts[3])
                    
                    # Optional: Print a live dashboard line
                    sys.stdout.write(f"\rDist: L:{telemetry['distL']} R:{telemetry['distR']} | Speed: L:{telemetry['speedL']} R:{telemetry['speedR']}      ")
                    sys.stdout.flush()
            except:
                pass

# Start the background listener
thread = threading.Thread(target=read_serial, daemon=True)
thread.start()

def main():
    print("Motor Controller with Odometry Started.")
    try:
        while True:
            user_input = input("\nEnter SpeedL,SpeedR: ")
            ser.write(f"{user_input}\n".encode())
            read_serial()
    except KeyboardInterrupt:
        ser.write(b"0,0\n")
        ser.close()

if __name__ == "__main__":
    main()