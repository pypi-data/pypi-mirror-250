import numpy as np

from cbsm.zoning import zoning

def test_zoning():
    X = np.array([1.0, 2.0, 3.0])
    Y = np.array([2.0, 3.0, 4.0])
    Z = np.zeros((X.shape[0], 1))
    Vx = np.array([1.0, 2.0, 3.0])
    delta_p = 2.0

    zone_map = zoning(X, Y, Z, Vx, delta_p)
    print(zone_map)
    assert zone_map[:, 4].tolist() == [1, 2, 2]