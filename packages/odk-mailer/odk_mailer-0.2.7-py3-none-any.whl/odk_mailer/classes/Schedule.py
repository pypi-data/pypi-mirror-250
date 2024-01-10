import time
from datetime import datetime

class Schedule:
    now: bool   # can be removed in future
    timestamp: int

    def __init__(self, data: []):
        self.now = data["now"]        

        if self.now:
            self.timestamp = int(time.time())

        else:
            _datetime = datetime.fromisoformat(data["datetime"])
            self.timestamp = int(datetime.timestamp(_datetime))