import pygame
from cube import Cube


class Cubes:
    def __init__(self, color, surface, clock, speed, direction, grid_distance, slabY, head_pos, num, number_of_grids):
        self.color = color
        self.surface = surface
        self.clock = clock
        self.speed = speed
        self.direction = direction
        self.head_pos = head_pos
        self.num = num
        self.grid_dist = grid_distance
        self.slabY = slabY
        self.cubes = []
        self.cubes_position = []
        self.clock_static_time = 0
        self.turns = []
        self.number_of_grids = number_of_grids-1
        self.can_move = 1
        self.add_cube = False
        self.cubes.append(Cube(self.color, self.surface, self.head_pos, self.grid_dist, self.slabY, True, self.direction))
        temp = self.head_pos
        self.cubes_position.append(self.head_pos)
        for i in range(num-1):
            temp = (temp[0]-self.direction["x"], temp[1]-self.direction["y"])
            self.cubes.append(Cube(self.color, self.surface, temp, self.grid_dist, self.slabY))
            self.cubes_position.append(temp)
        self.score = 0

    def draw(self):
        for i in range(len(self.cubes)):
            self.cubes[i].draw(self.cubes_position[i])
        self.head_pos = self.cubes_position[0]

    def move(self):
        if pygame.time.get_ticks() - self.clock_static_time > self.speed:
            self.clock_static_time = pygame.time.get_ticks()
            self.can_move = 1

    def turn(self, direction):
        self.direction = direction

    def forward(self):
        if self.can_move:
            self.cubes.insert(1, self.cubes.pop(-1))
            self.cubes[1].draw(self.cubes_position[0])
            self.cubes_position.insert(1, self.cubes_position[0])
            if self.add_cube:
                self.cubes.append(Cube(self.color, self.surface, self.cubes_position[-1], self.grid_dist, self.slabY))
                self.cubes_position.append(self.cubes_position[-1])
                del self.cubes_position[-2]
                self.num += 1
                self.cubes[-1].draw(self.cubes_position[-1])
                self.add_cube = False
                self.speed -= 5
                self.score += 1
            else:
                self.cubes_position.pop(-1)
            self.head_pos = (self.head_pos[0] + self.direction["x"],
                             self.head_pos[1] + self.direction["y"])
            if self.head_pos[0] > self.number_of_grids:
                self.head_pos = (0, self.head_pos[1])
            elif self.head_pos[0] < 0:
                self.head_pos = (self.number_of_grids, self.head_pos[1])
            if self.head_pos[1] > self.number_of_grids:
                self.head_pos = (self.head_pos[0], 0)
            elif self.head_pos[1] < 0:
                self.head_pos = (self.head_pos[0], self.number_of_grids)
            self.cubes_position[0] = self.head_pos
            self.cubes[0].draw(self.cubes_position[0], self.direction)
            self.can_move = 0

    def internal_collision(self):
        for i in range(len(self.cubes_position)):
            if self.cubes_position.count(self.cubes_position[i]) > 1:
                return True
        return False
