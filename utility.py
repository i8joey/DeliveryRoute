import csv
from datetime import datetime, timedelta
from package import Package

#creating packages, reading notes and then setting status
#csv file has 40 packages total
def load_packages(truck1, truck2, truck3, extra_packages, together, all_packages):
    with open('packages.csv', mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            status = "at hub"
            time_str = row['deadline']
            # creates time object for deadline
            try:
                time_obj = datetime.strptime(time_str, '%I:%M %p').time()
            except ValueError:
                time_obj = datetime.strptime("11:59 PM", "%I:%M %p").time()
            package = Package(row['address'], row['city'], row['state'], row['zip'], time_obj, row['weight'], status,
                              row['note'])
            id = row['package_id']
            # packages that must be delivered together are put in the same truck
            if id in together:
                truck1.load_package(id, package)
                continue
            # sorts packages into trucks depending on the note
            if "Must be delivered with" in row['note']:
                package_list = row['note'].replace("Must be delivered with", "").strip().split(",")
                for i in package_list:
                    together.add(int(i))
                truck1.load_package(id, package)
            elif "Delayed on flight" in package.note:
                truck2.load_package(id, package)
            elif "Can only be on truck 2" in package.note:
                truck2.load_package(id, package)
            elif "Wrong address" in package.note:
                truck3.load_package(id, package)
            elif package.deadline <= datetime.strptime("10:30 AM", "%I:%M %p").time():
                truck1.load_package(id, package)
            else:
                package.status = "at hub"
                extra_packages[id] = package
            all_packages[id] = package

def load_extras(truck1, truck2, truck3, extra_packages):
    for truck in [truck1, truck2, truck3]:
        while truck.count < 16 and extra_packages:
            id, package = extra_packages.popitem()
            truck.load_package(id, package)

def add_clean_data(locations):
    with open('distance.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            locations.append(row)

    # cleaning and filling in the rest of the data
    for row in range(1, len(locations)):
        locations[row][0] = locations[row][0].replace("\n", " ").replace("(", "").replace(")", "").lstrip()
        for col in range(1, len(locations[row])):
            locations[0][col] = locations[0][col].replace("\n", " ").replace("(", "").replace(")", "").lstrip()
            if locations[row][col] == '':
                locations[row][col] = locations[col][row]

def deliver_package(truck, starting, locations, all_packages):
    closest = Package
    shortest = 999.00
    for i in truck.packages:
        location = truck.packages[i].address + " " + truck.packages[i].zip
        column = locations[0].index(location)
        row = locations[0].index(starting)
        if float(locations[row][column]) < float(shortest):
            shortest = locations[row][column]
            closest = i
    truck.unload_pacakge(closest)
    all_packages[closest].status = "delivered"
    truck.mileage += float(shortest)
    return closest, shortest, all_packages[closest].address + " " + all_packages[closest].zip
