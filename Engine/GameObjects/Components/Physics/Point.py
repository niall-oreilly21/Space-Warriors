class Point:
    def __init__(self, bounds, data):
        self.bounds = bounds
        self.data = data

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.data.parent.name == other.data.parent.name
        return False
