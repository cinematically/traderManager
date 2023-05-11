import datetime

class Logger:
    def __init__(self):
        self.log_file = "log.txt"

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[traderManager] | Time: {timestamp} | {message}\n"
        with open(self.log_file, "a") as f:
            f.write(formatted_message)
        print(formatted_message)
