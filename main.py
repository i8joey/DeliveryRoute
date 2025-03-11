from package import Package
from truck import Truck
import csv
from datetime import datetime, timedelta
from utility import load_packages, load_extras, add_clean_data, deliver_packages

all_packages = {} #list of all packages to track their status
together = set() #list of packages that need to be delivered together
extra_packages = {} #extra packages that can be delivered at any time before end of day

locations = []
start_time = datetime.combine(datetime.today(), datetime.strptime("8:00 AM", "%I:%M %p").time())
closest = Package

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
deliver_packages(truck1, truck2, truck3, locations, all_packages, start_time, starting, closest)


















