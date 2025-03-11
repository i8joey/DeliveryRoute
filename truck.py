from package import Package

class Truck:
    def __init__(self):
        self.packages = {}
        self.count = 0
        self.mileage = 0.00
        self.departure_time = None
        self.return_time = None

    def load_package(self, package_id, package):
        self.packages[package_id] = package
        self.count += 1

    def unload_pacakge(self, package_id):
        package = self.packages.pop(package_id)
        self.count -=1