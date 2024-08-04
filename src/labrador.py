#!/usr/bin/env python
# coding: utf-8

import sys
from datetime import datetime
from pathlib import Path

from operations import connect_arduino
from operations import close_program
from operations import run_sample_collection

from drop_tracker import DropTracker


def main():
    # Connect to the Arduino
    # Note that the identification process relies upon pid and vid values wich
    # are specific to a given device. If a new Arduino (-like) device is used,
    # these values must be replaced. (hard coded to suit compilation into an
    # executable using `pyinstaller`)
    pid = 29987
    vid = 6790
    arduino = connect_arduino(pid, vid)

    if arduino is None:
        print(
            f"""Failed to connect to arduino. Please check:
        - the Arduino is connected to the computer
        - you are using the correct Arduino (pid = {pid}, vid = {vid})
        The program will now quit.
        """
        )
        _ = input("Hit return to exit.")
        sys.exit(1)

    # Initialise a log file
    tracker = DropTracker("Experiment")

    _ = input("Press return to start the drop timer.")
    print("Experiment initiated, timer started.")
    now = datetime.now()

    Path("data").mkdir(parents=True, exist_ok=True)

    filename = f"data/Experiment_{now.strftime('%d%m%Y%H%M%S')}.csv"
    tracker.initialise_log(filename)

    # Wait to start sample collection
    _ = input("Hit return to start sample collection")
    print("Sample collection in progress.")
    # clear signal queue
    arduino.flushInput()

    # Start sample collection
    run_sample_collection(tracker, arduino)

    print(f"Total drops: {tracker.drop_count}.")
    print(f"Collected drops: {tracker.collected_drops}.")

    close_program(arduino)


if __name__ == "__main__":
    main()
