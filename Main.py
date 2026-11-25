# 011220424

import csv
import datetime
import Truck
from HashTable import HashMap
from Package import Package


# Read CSV addresses and load into a list
# O(N)
def load_addresses(filename):
    # initialize empty array (list)
    addresses = []
    # Used encoding to remove BOM characters
    # Citing source Google Gemini (November 21, 2026), https://gemini.google.com
    with open(filename, encoding="utf-8-sig") as file:
        # reads one row at a time
        for row in csv.reader(file):
            # skips empty lines and adds to list if present, after stripping whitespace
            if row:
                addresses.append(row[2].strip())
    return addresses


# Get address index
# O(N)
def get_address_id(address, address_list):
    # if address exists, return index associated with it
    if address in address_list:
        return address_list.index(address)
    # second loop in case of formatting differences since it will still find location
    for i in range(len(address_list)):
        if address in address_list[i]:
            return i
    return None


# create list of lists from CSV distance file
# O(N^2)
def load_distances(filename):
    # Used encoding to remove BOM characters
    # Citing source Google Gemini (November 21, 2026), https://gemini.google.com
    with open(filename, encoding="utf-8-sig") as file:
        # creates a 2D distance matrix
        return list(csv.reader(file))


# Read packages from CSV and insert them into the hash table
# O(N^2)
def load_packages(filename, hash_table):
    # Used encoding to remove BOM characters
    # Citing source Google Gemini (November 21, 2026), https://gemini.google.com
    with open(filename, encoding="utf-8-sig") as file:
        for row in csv.reader(file):
            # skips blank lines
            if row:
                # convert from string to int so it can be hashed correctly
                package_id = int(row[0])
                # creates instance of Package with the following attributes
                package = Package(
                    package_id,
                    row[1].strip(),  # address
                    row[2],  # city
                    row[3],  # state
                    row[4],  # zip
                    row[5],  # deadline
                    row[6],  # weight
                    "At Hub"
                )
                # inserts key-value pair into the appropriate bucket of the hash table
                hash_table.insert(package_id, package)

# Find distance between two addresses in the distance matrix
# O(1)
def distance_between(proximity, address1, address2):
    # get distance from the distance matrix
    dist = proximity[address1][address2]
    # if the lookup lands on the wrong side of the grid, flip indices to find correct distance.
    # The table can be inverted to find the correct value
    if dist == "":
        dist = proximity[address2][address1]
    return float(dist)


# Order packages using nearest neighbor algorithm
# O(N^2)
# this is a greedy algorithm, which means it chooses the closest option but not necessarily the best
# in other words, it does not look ahead for the optimized route, which could end up increasing overall mileage
def nearest_neighbor(truck, hash_table, address_list, distance_from_address):
    # initialize empty array
    undelivered = []
    # looks through the packages manually assigned to each truck
    for package_id in truck.packages:
        # get undelivered packages from hash table
        undelivered.append(hash_table.lookup(package_id))
    # clear initial list so it can be ordered by the choices of the NN Algorithm
    truck.packages.clear()

    while undelivered:
        # convert current address to corresponding index in the distance matrix
        current_id = get_address_id(truck.address, address_list)
        # assume the first package is the closest and compare the rest
        closest = undelivered[0]
        # calculate shortest mileage between current location and any undelivered locations
        shortest = distance_between(distance_from_address, current_id, get_address_id(closest.address, address_list))

        # go through undelivered packages and update shortest if shorter distance is found
        for undelivered_package in undelivered:
            package_id = get_address_id(undelivered_package.address, address_list)
            distance = distance_between(distance_from_address, current_id, package_id)
            if distance < shortest:
                shortest = distance
                closest = undelivered_package
        # add closest package to next delivery
        truck.packages.append(closest.ID)
        # remove from undelivered
        undelivered.remove(closest)
        # update truck mileage
        truck.mileage += shortest
        # update truck address
        truck.address = closest.address
        # adds time to truck's clock based on 18 mph speed limit
        truck.time += datetime.timedelta(hours=shortest / 18)
        # updates delivery status
        closest.departure_time = truck.departure
        closest.delivery_time = truck.time


if __name__ == "__main__":
    # load CSV files and populate hash table
    address_list = load_addresses("CSV/Addresses.csv")
    distances = load_distances("CSV/Distances.csv")
    package_hash_table = HashMap()
    load_packages("CSV/Packages.csv", package_hash_table)

    # Update package 9 to its corrected address after 10:20 before routing to Truck 2
    # O(N)
    package_nine = package_hash_table.lookup(9)
    package_nine.address = "410 S State St"
    package_nine.zipcode = "84111"

    # first to leave
    truck1 = Truck.Truck(
        capacity=16,
        speed=18,
        load=None,
        packages=[1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40],
        mileage=0.0,
        address="4001 South 700 East",
        departure=datetime.timedelta(hours=8)
    )

    # departs at 10:20 after address correction
    truck2 = Truck.Truck(
        capacity=16,
        speed=18,
        load=None,
        packages=[3, 9, 12, 17, 18, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39],
        mileage=0.0,
        address="4001 South 700 East",
        departure=datetime.timedelta(hours=10, minutes=20)
    )

    # leaves at 9:05 but must wait for a driver to return
    truck3 = Truck.Truck(
        capacity=16,
        speed=18,
        load=None,
        packages=[2, 4, 5, 6, 7, 8, 10, 11, 25, 28, 32, 33],
        mileage=0.0,
        address="4001 South 700 East",
        departure=datetime.timedelta(hours=9, minutes=5)
    )

    # Route trucks
    nearest_neighbor(truck1, package_hash_table, address_list, distances)
    nearest_neighbor(truck2, package_hash_table, address_list, distances)

    # set truck 3 departure to the first car to return - only two drivers are available
    if truck1.time < truck2.time:
       truck3.departure = truck1.time
    else:
       truck3.departure = truck2.time

    truck3.time = truck3.departure
    nearest_neighbor(truck3, package_hash_table, address_list, distances)

    print("WGUPS Tracking Program")
    print(f"Truck 1: {truck1.mileage:.1f} miles, Truck 2: {truck2.mileage:.1f} miles, truck 3: {truck3.mileage:.1f} miles")
    print("Total mileage:", round(truck1.mileage + truck2.mileage + truck3.mileage, 2), "miles")

    # user wil be prompted to enter correct input
    while True:
        status = input("Type 'status' for package info or 'q' to quit: ")

        if status.strip().lower() == 'q':
            print("Goodbye")
            break

        # convert to lowercase and remove whitespace
        elif status.strip().lower() != "status":
            print("Wrong, try again")
            continue

        try:
            # user will be prompted to enter a valid time
            user_time = input("Enter a valid time in HH:MM:SS format: ")
            h, m, s = user_time.split(":")
            converted_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

            package_type = input("To check status of one package, type 'one'. To check status of all packages, type 'all': " )
            # O(N)
            if package_type.strip().lower() == "one":
                one = int(input("Enter package ID (1-40): "))
                package = package_hash_table.lookup(one)
                # return error message if not found and update time if found
                if package is None:
                    print("ID not found.")
                else:
                    package.update_status(converted_time)
                    print(package)
            # O(N^2)
            elif package_type.strip().lower() == "all":
                for package_id in range(1, 41):
                    package = package_hash_table.lookup(package_id)
                    package.update_status(converted_time)
                    print(package)
            else:
                print("Wrong, try again.")


        except ValueError:
            print("Wrong, try again.")


