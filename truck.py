from package import Package

class Truck:
    def __init__(self):
        self.packages = {}
        self.count = 0

    def load_package(self, package_id, package):
        package.status="routing"
        self.packages[package_id] = package
        self.count+= 1