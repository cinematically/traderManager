import datetime

class Logger:
    def __init__(self, prefix="[Application]"):
        self.prefix = prefix
        self.log_file = f"traderManager_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{self.prefix} | Time: {timestamp} | {message}"
        print(log_message)

        with open(self.log_file, "a") as file:
            file.write(log_message + "\n")
