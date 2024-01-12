import numpy as np

class Result:
    zone_map: np.ndarray
    grid_info: np.ndarray
    volume: np.ndarray

    def __init__(self, zone_map, grid_info, volume):
        # grid info: x_min, y_min, x_max, y_max, zone, zone_count, suface_zone, mean_value_vx, mean_value_vy
        self.zone_map = zone_map
        self.grid_info = grid_info
        self.volume = volume

    def sortGridInfo(self):
        sort_index = np.lexsort((self.grid_info[:, 3], self.grid_info[:, 2], 
                                 self.grid_info[:, 1], self.grid_info[:, 0], 
                                 self.grid_info[:, 4]))
        self.grid_info = self.grid_info[sort_index]