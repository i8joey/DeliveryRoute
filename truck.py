from package import Package

class Truck:
    def __init__(self):
        self.packages = {}
        self.count = 0
        self.mileage = 0.00

    def load_package(self, package_id, package):
        package.status="routing"
        self.packages[package_id] = package
        self.count += 1

    def unload_pacakge(self, package_id):
        package = self.packages.pop(package_id)
        self.count -=1