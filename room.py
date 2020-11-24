import numpy as np

class Room:
    def __init__(self, size=(15, 15), two_doors=False):
        # size of the room
        self.size = size

        # size of the door
        self.door_size = size[1]/15

        if two_doors:
            self.left_door_location = np.array([0, size[1]/2])
            self.right_door_location = np.array([size[0], size[1]/2])
            # setting up walls
            self.walls = np.array([[[0, 0], [0, size[1]/2]],
                                   [[0, size[1]/2+self.door_size], [0, size[1]]],
                                   [[0, size[1]], [size[0], size[1]]],
                                   [[size[0], size[1]], [size[0], size[1]/2+self.door_size]],
                                   [[size[0], size[1]/2-self.door_size], [size[0], 0]],
                                   [[size[0], 0], [0, 0]]])
        else:
            # door location - right
            self.door_location = np.array([size[0], size[1]/2])
            # setting up walls
            self.walls = np.array([[[0, 0], [0, size[1]]],
                                   [[0, size[1]], [size[0], size[1]]],
                                   [[size[0], size[1]], [size[0], size[1]/2+self.door_size]],
                                   [[size[0], size[1]/2-self.door_size], [size[0], 0]],
                                   [[size[0], 0], [0, 0]]])
