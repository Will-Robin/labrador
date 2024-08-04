import sys
import time
import serial
import keyboard
from drop_tracker import DropTracker
import serial.tools.list_ports


def connect_arduino(pid, vid):
    """
    Connect to an Arduino device.
    """

    # Search for a specific Arduino clone attached to to a com port.
    for p in serial.tools.list_ports.comports():
        if p.pid == pid and p.vid == vid:
            return try_connect(p.device, 9600)


def try_connect(com_port, baud_rate):
    try:
        arduino = serial.Serial(com_port, baud_rate, timeout=1)
        print("Waiting for Arduino drop counter connection...")
        while not arduino.isOpen:
            time.sleep(1)
        print("Arduino connected!")
        return arduino
    except serial.SerialException:
        return None


def close_program(arduino):
    """
    Close the program, closing ports, etc.
    """
    arduino.close()
    sys.exit(1)


def handle_drop(tracker: DropTracker, record_drops: bool):
    """
    Make decisions on what to do with a drop.
    """
    # Increment drop count
    tracker.detect_drop()
    if record_drops:
        # Log the drop as collected
        tracker.collect_drop()
        tracker.write_log()
        return (
            f"Drop detected at {round(tracker.time, 2)} s (drop: {tracker.drop_count})"
        )
    else:
        return ""


def run_sample_collection(tracker: DropTracker, arduino):
    """
    Run the sample collection routine.
    """

    print(
        """
    Sample collection initiated.
    - Press `p` to pause drop recording,
    - Press `s` to restart drop recording,
    - Press `q` to finish collection.
    """
    )

    record_drops = True
    message = ""
    prev_message = len(message)
    result = ""
    while True:
        if keyboard.is_pressed("p"):
            record_drops = False
            message = "Drop recording paused."

        if keyboard.is_pressed("s"):
            record_drops = True
            message = "Drop recording resumed."

        if keyboard.is_pressed("q"):
            print("Cancelling drop recording.")
            break

        # Check if Arduino response is a drop
        if arduino.readline() == b"1\r\n":
            result = handle_drop(tracker, record_drops)
            message += result

        if message != "":
            print(" " * 100, end="\r")
            print(message, end="\r")

        prev_message = len(message)
        message = ""

    return True
