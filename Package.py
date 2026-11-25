import datetime

# Create class for packages
class Package:
    def __init__(self, ID, address, city, state, zipcode, deadline, weight, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    def __str__(self):
        if self.status == "Delivered":
            eta = self.delivery_time
        else:
            eta = f"ETA: {self.delivery_time}"
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.address, self.city, self.state, self.zipcode,
                                                       self.deadline, self.weight, eta,
                                                       self.status)

    # O(1)
    def update_status(self, convert_timedelta):
        # handling for package #9 that updates after 10:20
        if self.ID == 9:
            # if before 10:20, display old address
            if convert_timedelta < datetime.timedelta(hours=10, minutes=20):
                self.address = "300 State St"
                self.zipcode = "84103"
            # if after, display correct address
            else:
                self.address = "410 S State St"
                self.zipcode = "84111"
        if self.delivery_time <= convert_timedelta:
            self.status = "Delivered"
        elif self.departure_time <= convert_timedelta:
            self.status = "En route"
        else:
            self.status = "At Hub"