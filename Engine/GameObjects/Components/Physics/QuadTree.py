import pygame

from App.Constants.Application import Application


class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary  # Rectangle representing the boundary of the quadtree
        self.capacity = capacity  # Maximum number of objects a node can hold
        self.objects = []  # List of objects contained in the quadtree
        self.subdivided = False  # Flag indicating if the quadtree has been subdivided
        self.children = [None] * 4  # List of child quadtrees (NW, NE, SW, SE)

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.width / 2
        h = self.boundary.height / 2

        nw_boundary = pygame.Rect(x, y, w, h)
        ne_boundary = pygame.Rect(x + w, y, w, h)
        sw_boundary = pygame.Rect(x, y + h, w, h)
        se_boundary = pygame.Rect(x + w, y + h, w, h)

        self.children[0] = QuadTree(nw_boundary, self.capacity)
        self.children[1] = QuadTree(ne_boundary, self.capacity)
        self.children[2] = QuadTree(sw_boundary, self.capacity)
        self.children[3] = QuadTree(se_boundary, self.capacity)

        self.subdivided = True

    def insert(self, obj):
        if not self.boundary.contains(obj.bounds):
            return False  # Object is outside the quadtree's boundary

        if len(self.objects) < self.capacity:
            self.objects.append(obj)
            return True  # Object successfully inserted

        if not self.subdivided:
            self.subdivide()

        # Insert the object into the appropriate child quadtree(s)
        for child in self.children:
            if child.insert(obj):
                return True

        return False  # Object does not fit entirely within any child quadtree

    def remove(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)
            # Remove the object from the current quadtree

        if self.subdivided:
            for child in self.children:
                child.remove(obj)
            # Recursively remove the object from the child quadtrees if they exist

    def query(self, range_boundary):
        result = []

        for obj in self.objects:
            if range_boundary.colliderect(obj.bounds) or obj.bounds.contains(range_boundary):
                result.append(obj)

        if self.subdivided:
            for child in self.children:
                result.extend(child.query(range_boundary))

        return result



