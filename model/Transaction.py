from datetime import datetime
from datetime import timezone


# parse timestamp
def convert_time(timestamp):
    d = datetime.fromisoformat(timestamp[:-1]).astimezone(timezone.utc)
    return d


class Transaction:
    def __init__(self, payer, points, timestamp):
        self.payer = payer
        self.points = points
        self.timestamp = convert_time(timestamp)

    def __str__(self):
        return "payer:{}, points:{}, timestamp:{}".format(self.payer, self.points, self.timestamp)
