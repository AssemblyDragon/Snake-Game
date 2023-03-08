import pygame


class Cube:

    def __init__(self, color, surface, pos, grid_dist, slabY, head=False, direction={"x": 0, "y": 0}):
        self.color = color
        self.surface = surface
        self.head = head
        self.grid_dist = grid_dist
        self.slabY = slabY
        self.pos = [pos[0]-1, pos[1]-1]
        self.exact_pos = [None, None]
        self.dir = direction
        self.headCenter = []
        self.head_center()

    def head_center(self):
        if self.dir["x"] == -1:
            self.headCenter = [(self.grid_dist/4, self.grid_dist/4), (self.grid_dist/4, 3*self.grid_dist/4)]

        if self.dir["x"] == 1:
            self.headCenter = [(3*self.grid_dist/4, self.grid_dist/4), (3*self.grid_dist/4, 3*self.grid_dist/4)]

        if self.dir["y"] == -1:
            self.headCenter = [(self.grid_dist/4, self.grid_dist/4), (3*self.grid_dist/4, self.grid_dist/4)]

        if self.dir["y"] == 1:
            self.headCenter = [(self.grid_dist/4, 3*self.grid_dist/4), (3*self.grid_dist/4, 3*self.grid_dist/4)]

    def draw(self, pos=None, direction=None):
        if pos:
            self.pos = pos

        self.exact_pos = [self.pos[0] * self.grid_dist, self.pos[1] * self.grid_dist + self.slabY]
        self.surface.fill(self.color, (tuple(self.exact_pos), (self.grid_dist, self.grid_dist)))

        if self.head:
            if direction:
                self.dir = direction
                self.head_center()

            pygame.draw.circle(self.surface, (255, 255, 255), (self.exact_pos[0] + self.headCenter[0][0],
                                                               self.exact_pos[1] + self.headCenter[0][1]), 4)
            pygame.draw.circle(self.surface, (255, 255, 255), (self.exact_pos[0] + self.headCenter[1][0],
                                                               self.exact_pos[1] + self.headCenter[1][1]), 4)
