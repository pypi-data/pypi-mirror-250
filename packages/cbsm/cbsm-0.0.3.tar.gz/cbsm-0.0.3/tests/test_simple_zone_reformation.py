import numpy as np

from cbsm.zone_reformation import zone_reformation

def test_zone_reformation():
    zone_map = np.array([[1.0, 2.0, 3.0, 4.0, 5.0],
                            [1.0, 2.0, 3.0, 4.0, 5.0],
                            [0, 0, 0, 0, 0],
                            [1.0, 2.0, 2.0, 2.0, 0.5],
                            [1.0, 2.0, 2.0, 2.0, 1.0]])
    delta_x = (5-1)/15.0
    delta_y = (5-2)/35.0
    grid_info = zone_reformation(zone_map, delta_x, delta_y, 15, 35)
    print("grid info:", grid_info)