# 011220424

import csv
import datetime
import Truck
from HashTable import HashMap
from Package import Package


# Load CSV addresses into a dictionary
# Used encoding to remove BOM characters
# Source: Google Gemini (November 21, 2026), https://gemini.google.com
# O(N)
def load_addresses(filename):
    address_dict = {}
    with open(filename, encoding="utf-8-sig") as file:
        for row in csv.reader(file):
            if row:
                index = int(row[0])
                street = row[2].strip()
                address_dict[street] = index
    return address_dict


# Get matrix index for a given address string
# O(N)
def get_address_id(address, address_map):
    clean = address.strip()
    if clean in address_map:
        return address_map[clean]

    for key in address_map:
        if clean in key:
            address_map[clean] = address_map[key]
            return address_map[key]

    raise ValueError("Address not found: %s" % address)



# O(N^2)
# create distance table from CSV file
def load_distances(filename):
    with open(filename, encoding="utf-8-sig") as file:
        return list(csv.reader(file))


# Read packages from CSV and insert them into the hash table
# O(N^2)
def load_packages(filename, hash_table):
    with open(filename, encoding="utf-8-sig") as file:
        for row in csv.reader(file):
            if len(row) == 0:
                continue
            pkg_id = int(row[0])
            package = Package(
                pkg_id,
                row[1],  # address
                row[2],  # city
                row[3],  # state
                row[4],  # zip
                row[5],  # deadline
                row[6],  # weight
                "At Hub"
            )
            hash_table.insert(pkg_id, package)

# Find distance between two addresses
# O(1)
def distance_between(distances, address1, address2):
    dist = distances[address1][address2]
    if dist == "":
        dist = distances[address2][address1]
    return float(dist)


# Order packages to deliver using nearest neighbor algorithm
# O(N^2)
def nearest_neighbor(truck, hash_table, address_map, distances):
    undelivered = []
    for pkg_id in truck.packages:
        undelivered.append(hash_table.lookup(pkg_id))

    truck.packages.clear()

    while len(undelivered) > 0:
        shortest_distance = 1000.0
        next_package = None
        current_idx = get_address_id(truck.address, address_map)

        for pkg in undelivered:
            pkg_idx = get_address_id(pkg.address, address_map)
            dist = distance_between(distances, current_idx, pkg_idx)
            if dist < shortest_distance:
                shortest_distance = dist
                next_package = pkg

        truck.packages.append(next_package.ID)
        undelivered.remove(next_package)
        truck.mileage += shortest_distance
        truck.address = next_package.address
        truck.time += datetime.timedelta(hours=shortest_distance / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.departure


class Main:
    address_map = load_addresses("CSV/Addresses.csv")
    distances = load_distances("CSV/Distances.csv")
    package_hash_table = HashMap()
    load_packages("CSV/Packages.csv", package_hash_table)

    # Update package 9 to its corrected address before routing to Truck 2
    # O(1)
    package_nine = package_hash_table.lookup(9)
    package_nine.address = "410 S State St"
    package_nine.zipcode = "84111"

    # Load trucks
    t1 = Truck.Truck(
        16, 18, None, [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40],
        0.0, "4001 South 700 East", datetime.timedelta(hours=8)
    )
    t2 = Truck.Truck(
        16, 18, None, [3, 9, 12, 17, 18, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39],
        0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20)
    )
    t3 = Truck.Truck(
        16, 18, None, [2, 4, 5, 6, 7, 8, 10, 11, 25, 28, 32, 33],
        0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5)
    )

    # Route trucks
    nearest_neighbor(t1, package_hash_table, address_map, distances)
    nearest_neighbor(t2, package_hash_table, address_map, distances)

    # set truck 3 departure to the first car to leave
    t3.departure = min(t1.time, t2.time)
    t3.time = t3.departure
    nearest_neighbor(t3, package_hash_table, address_map, distances)

    # Welcome message and mileage info
    print("Western Governors University Parcel Service (WGUPS)")
    print(
        "Truck 1:", round(t1.mileage, 2), "miles,",
        "Truck 2:", round(t2.mileage, 2), "miles,",
        "Truck 3:", round(t3.mileage, 2), "miles"
    )
    print("Total mileage:", round(t1.mileage + t2.mileage + t3.mileage, 2), "miles")

    # user welcome message
    status = input("To begin, type 'status' (or 'q' to quit): ")
    while status != "q":
        if status == "status":
            try:
                user_time = input("To check package status, enter a time using HH:MM:SS format: ").strip()
                h, m, s = user_time.split(":")
                converted_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

                package_type = input("To view the status of an individual package, type 'one'. To see the status of all packages, type 'all': " )
                # O(N)
                if package_type == "one":
                    one = int(input("Enter the numeric package ID between 1 and 40 (inclusive): ").strip())
                    package = package_hash_table.lookup(one)
                    if package is None:
                        print("Package ID not found.")
                    else:
                        package.update_status(converted_time)
                        print(package)
                # O(N^2)
                elif package_type == "all":
                    for package_id in range(1, 41):
                        package = package_hash_table.lookup(package_id)
                        package.update_status(converted_time)
                        print(package)
                else:
                    print("Invalid. Type 'one' or 'all'.")

            except ValueError:
                print("Invalid. Check your time or number format and try again.")
        else:
            print("Invalid. Type 'status' or 'q'.")

        status = input("To try again, type 'status' (or 'q' to quit): ")

    print("Goodbye")
