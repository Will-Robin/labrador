import time


class DropTracker:
    def __init__(
        self,
        exp_code: str,
    ):
        self.exp_code = ""
        self.drop_count = 0
        self.collected_drops = 0
        self.start_time = time.time()
        self.log_file = f"{exp_code}"

    def initialise_log(self, filename: str):
        """
        Create a log file to write to.
        """
        self.start_time = time.time()
        self.log_file = filename
        with open(self.log_file, "w") as file:
            file.write("sample_number,drop_number,time/ s\n")

    def detect_drop(self):
        """
        Detect a drop without collecting it.
        """
        self.drop_count += 1

    def collect_drop(self):
        """
        Respond to a collected drop.
        """
        # Increment sample number, time
        self.time = time.time() - self.start_time
        self.collected_drops += 1

    def write_log(self):
        """
        Write current state to a log file.
        """
        with open(self.log_file, "a") as file:
            file.write(f"{self.collected_drops},{self.drop_count},{self.time}\n")
