import numpy as np


class Room:

    def __init__(self, size=(15, 15), two_doors=False):
        # size of the room
        self.size = size

        # size of the door
        self.door_size = size[1] / 15
        self.two_doors = two_doors
        self.spawn_zone = np.array([[1, size[1] - 1], [1, size[1] - 1]])

        if two_doors:
            self.left_door_location = np.array([0, size[1] / 2])
            self.right_door_location = np.array([size[0], size[1] / 2])
            # setting up walls
            self.walls = np.array([[[0, 0], [0, size[1] / 2 - self.door_size / 2]],
                                   [[0, size[1] / 2 + self.door_size / 2], [0, size[1]]],
                                   [[0, size[1]], [size[0], size[1]]],
                                   [[size[0], size[1]], [size[0], size[1] / 2 + self.door_size / 2]],
                                   [[size[0], size[1] / 2 - self.door_size / 2], [size[0], 0]],
                                   [[size[0], 0], [0, 0]]])
        else:
            # door location - right
            self.door_location = np.array([0, size[1] / 2])
            # setting up walls
            self.walls = np.array([[[0, 0], [0, size[1]]],
                                   [[size[0], size[1]], [size[0], size[1] / 2 + self.door_size / 2]],
                                   [[size[0], size[1] / 2 - self.door_size / 2], [size[0], 0]],
                                   [[size[0], 0], [0, 0]],
                                   [[0, size[1]], [size[0], size[1]]]])

    def get_wall(self, n):  # gives back the endpoints of the nth wall
        return self.walls[n, :, :]

    def get_num_walls(self):  # gives back the number of walls
        return len(self.walls)

    def get_spawn_zone(self):  # gives back the spawn_zone
        return self.spawn_zone

    def get_room_size(self):  # gives back the size of the room
        return self.size[0]

    def get_door_location(self):  # gives back the destination the agents want to get to
        return self.door_location

    def get_left_right_door_location(self):  # gives back the destination the agents want to get to
        return [self.left_door_location, self.right_door_location]

    def is_two_doors(self):  # gives back the destination the agents want to get to
        return self.two_doors
