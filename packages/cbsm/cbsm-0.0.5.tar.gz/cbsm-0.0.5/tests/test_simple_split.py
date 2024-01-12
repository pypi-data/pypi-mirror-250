import numpy as np

from cbsm.splitting import split

def test_split():
    center_info = np.array([[1.0, 1.0, 1.0],
                             [1.5, 1.5, 1.0],
                             [3.0, 3.0, 1.0]])
    delta_x = 1.0
    delta_y = 1.0
    split_result = split(center_info, delta_x, delta_y)

    assert split_result[:, 2].tolist() == [1.0, 1.0, 2.0]

def test_diagonal_split():
    center_info = np.array([[1.0, 1.0, 1.0],
                             [1.5, 1.5, 1.0],
                             [0, 0, 1.0]])
    delta_x = 1.0
    delta_y = 1.0
    split_result = split(center_info, delta_x, delta_y)

    assert split_result[:, 2].tolist() == [1.0, 1.0, 1.0]