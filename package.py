from datetime import datetime

class Package:
    ALLOWED_STATUSES = ["at hub", "routing", "delivered"]

    def __init__(self, address, city, state, zip, deadline, weight, status, note=None):
        if status not in self.ALLOWED_STATUSES:
            raise ValueError("status must be one of %s" % ", ".join(self.ALLOWED_STATUSES))
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.note = note
        self.delivery_time = datetime.strptime("8:00 AM", "%I:%M %p").time()
        self.truck = None


