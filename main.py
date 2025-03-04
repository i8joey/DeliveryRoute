from package import Package
from truck import Truck
import csv
from datetime import datetime


together = set() #list of packages that need to be delivered together
extra_packages = {} #extra packages that can be delivered at any time before end of day

#each truck has a limit of 16 packages, and we are limited to 3 trucks
truck1 = Truck() #packages that need to be delivered early and that need to be delivered together
truck2 = Truck() #delayed packages and packages requested to be on truck 2
truck3 = Truck() #wrong address and rest of packages

#creating packages, reading notes and then setting status
#csv file has 40 packages total
with open('packages.csv', mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        status = "hub"
        time_str = row['deadline']
        #creates time object for deadline
        try:
            time_obj = datetime.strptime(time_str, '%I:%M %p').time()
        except ValueError:
            time_obj = datetime.strptime("11:59 PM", "%I:%M %p").time()
        package = Package(row['address'], row['city'], row['state'], row['zip'], time_obj, row['weight'], status,
                          row['note'])
        id = row['package_id']
        #packages that must be delivered together are put in the same truck
        if id in together:
            truck1.load_package(id, package)
            continue
        #sorts packages into trucks depending on the note
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
            package.status = "hub"
            extra_packages[id] = package

#distributes remaining packages while each truck stays under the limit
trucks = [truck1, truck2, truck3]
for truck in trucks:
    while truck.count < 16 and extra_packages:
        id, package = extra_packages.popitem()
        truck.load_package(id, package)

#filling in the upper half of the distance table while using the bottom half
locations = []

with open('distance.csv', mode='r', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        locations.append(row)

#cleaning and filling in the rest of the data
for row in range(1, len(locations)):
    locations[row][0] = locations[row][0].replace("\n", " ").replace("(", "").replace(")", "").lstrip()
    for col in range(1, len(locations[row])):
        locations[0][col] = locations[0][col].replace("\n", " ").replace("(", "").replace(")", "").lstrip()
        if locations[row][col] == '':
            locations[row][col] = locations[col][row]

starting = "HUB"
#getting indexes using the column then using the two numbers to get the distance between two points
'''
for i in truck1.packages:
    location = truck1.packages[i].address + " " + truck1.packages[i].zip
    column = locations[0].index(location)
    row = locations[0].index(starting)
'''
''' loop through the trucks outside of the while loop
inside the while loop - find the closest package
deliver it
update current location
continue till finished
'''
for truck in trucks:
    while truck.count > 0:
        closest = ""
        for i in truck.packages:
            location = truck.packages[i].address + " " + truck.packages[i].zip
            column = locations[0].index(location)
            row = locations[0].index(starting)
















