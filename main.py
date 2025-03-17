#ID - 011657817

from operator import truediv
from wsgiref.handlers import format_date_time

from package import Package
from truck import Truck
from datetime import datetime, timedelta
from utility import load_packages, load_extras, add_clean_data, deliver_package
import copy

all_packages = {} #list of all packages to track their status
together = set() #list of packages that need to be delivered together
extra_packages = {} #extra packages that can be delivered at any time before end of day

snapshot = {} #snapshot of all deliveries whenever a package is delivered (for UI)

start_time = datetime.combine(datetime.today(), datetime.strptime("8:00 AM", "%I:%M %p").time())
locations = []

#each truck has a limit of 16 packages, and we are limited to 3 trucks
truck1 = Truck() #packages that need to be delivered early and that need to be delivered together
truck2 = Truck() #delayed packages and packages requested to be on truck 2
truck3 = Truck() #wrong address and rest of packages

load_packages(truck1, truck2, truck3, extra_packages, together, all_packages)

#distributes remaining packages while each truck stays under the limit
load_extras(truck1, truck2, truck3, extra_packages)

#filling in the upper half of the distance table while using the bottom half
add_clean_data(locations)
starting = locations[0][1]
#Delivering the packages and adding mileage to calculate delivery time
for truck in [truck1, truck2, truck3]:
    truck.departure_time = start_time
    hold_snap = {}
    for i in truck.packages.values():
        i.status = "routing"
        i.delivery_time = start_time.time()
    while truck.count > 0:
        # comparing distances and selecting the shortest distance
        closest, shortest, starting = deliver_package(truck, starting, locations, all_packages)
        start_time += timedelta(hours=float(shortest) / float(18))
        snapshot[start_time.time()] = copy.deepcopy(all_packages)
        all_packages[closest].delivery_time = start_time.time()
        if start_time.time() >= datetime.strptime("10:20 AM", "%I:%M %p").time():
            all_packages['9'].address = "410 S State St"
            all_packages['9'].city = "Salt Lake City"
            all_packages['9'].state = "UT"
            all_packages['9'].zip = "84111"
    truck.return_time = start_time

#Interface
print("Delivery Complete!")
print("Truck1:")
print("Departure Time :",truck1.departure_time.time())
print("Return Time :", truck1.return_time.time())
print("Drive Time: ", round(truck1.mileage/18, 2), "Hours")
print("Total Distance: ", truck1.mileage)

print()
print("Truck2:")
print("Departure Time :",truck2.departure_time.time())
print("Return Time :", truck2.return_time.time())
print("Drive Time: ", round(truck2.mileage/18, 2), "Hours")
print("Total Distance: ", truck2.mileage)

print()
print("Truck3:")
print("Departure Time :",truck3.departure_time.time())
print("Return Time :", truck3.return_time.time())
print("Drive Time: ", round(truck3.mileage/18, 2), "Hours")
print("Total Distance: ", truck3.mileage)

print()
print("Total Distance: ", truck1.mileage + truck2.mileage + truck3.mileage, "Miles")
print("Total Time: ", round((truck1.mileage + truck2.mileage + truck3.mileage)/18, 2), "Hours")
while True:
    print("p - Package Information Lookup")
    print("e - Exit")
    response = input()
    if response == "e":
        break
    elif response == "p":
        print("Please enter a time to find package information. Eg. 9:09 AM")
        time1 = datetime.strptime(input(), "%I:%M %p").time()
        closest_time = min(list(snapshot.keys()), key=lambda t: abs(datetime.combine(datetime.min, t) - datetime.combine(datetime.min, time1)))
        for i in snapshot[closest_time]:
            print("Package ID:", i , snapshot[closest_time][i].status, "at", snapshot[closest_time][i].delivery_time, ", Delivery Address:", snapshot[closest_time][i].address, ", Deadline:", snapshot[closest_time][i].deadline, ", On Truck:", snapshot[closest_time][i].truck)
    else:
        print("Please enter a valid input.")
