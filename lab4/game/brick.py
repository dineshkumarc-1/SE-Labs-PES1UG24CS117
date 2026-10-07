import pygame

class Brick:
    # Task 4: higher rows (closer to top) are worth more points
    ROW_POINTS = [5, 4, 3, 2, 1]

    def __init__(self, x, y, width, height, row=0):
        self.x           = x
        self.y           = y
        self.width       = width
        self.height      = height
        self.alive       = True
        self.point_value = self.ROW_POINTS[row % len(self.ROW_POINTS)]

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
