import numpy as np
import matplotlib.pyplot as plt

from cbsm.splitting import split


def cubing2(zone_map, delta_X, delta_Y, number_X, number_Y):
    """
    Cubing2 algorithm for processing compartment maps.

    Parameters
    ----------
    zone_map : array_like
        Zone map containing information about each compartment.
    delta_X : float
        Acceptable tolerance along the X-axis.
    delta_Y : float
        Acceptable tolerance along the Y-axis.
    number_X : int
        Number of grid cells along the X-axis.
    number_Y : int
        Number of grid cells along the Y-axis.

    Returns
    -------
    array
        Processed grid information.

    Notes
    -----
    - The function uses the split function from the app.services.scaledown.app.splitting module.

    Examples
    --------
    >>> zone_map = np.array([[1.0, 2.0, 3.0, 4.0, 5.0],
    ...                      [2.0, 3.0, 4.0, 5.0, 5.0],
    ...                      [3.0, 4.0, 5.0, 6.0, 6.0]])
    >>> delta_X = 0.1
    >>> delta_Y = 0.2
    >>> number_X = 10
    >>> number_Y = 20
    >>> cubing2_result = cubing2(zone_map, delta_X, delta_Y, number_X, number_Y)
    """

    min_x = np.min(zone_map[:, 0])
    min_y = np.min(zone_map[:, 1])

    # associate the sub-compartments to their grids
    grid_info = []
    mean_info = []
    for i in range(number_X):
        x_min = min_x + i * delta_X
        x_max = x_min + delta_X
        input_x_row_min = np.where(
            zone_map[:, 0] > x_min - 0.000001 * delta_X)[0]
        input_x_row_max = np.where(
            zone_map[:, 0] < x_max + 0.000001 * delta_X)[0]
        indicator_X = np.intersect1d(input_x_row_min, input_x_row_max)
        for j in range(number_Y):
            y_min = min_y + j * delta_Y
            y_max = y_min + delta_Y
            input_y_row_min = np.where(
                zone_map[:, 1] > y_min - 0.000001 * delta_Y)[0]
            input_y_row_max = np.where(
                zone_map[:, 1] < y_max + 0.000001 * delta_Y)[0]
            indicator_Y = np.intersect1d(input_y_row_min, input_y_row_max)
            indicator = np.intersect1d(indicator_X, indicator_Y)
            input = zone_map[indicator, :]
            row_size_input = input[:, 0].shape[0]
            if row_size_input > 1:
                k_in = 1
                while input[k_in, 4] == input[k_in - 1, 4]:
                    k_in = k_in + 1
                    if k_in == row_size_input:
                        break
                # find dominant zone
                counter_old = k_in
                counter_new = 1
                zone_in = input[0, 4]
                if k_in < row_size_input:
                    for k in range(k_in, row_size_input):
                        counter_new = 0
                        while input[k, 4] == input[k-1, 4]:
                            k += 1
                            counter_new += 1
                            if k == row_size_input:
                                break
                        if counter_new > counter_old:
                            zone_in = input[k-1, 4]
                            counter_old = counter_new
                zone_map[indicator, 4] = zone_in
                grid_info.append([x_min, x_max, y_min, y_max,
                                 zone_in, 0])
                mean_info.append(np.mean(input[:, 3]))
    grid_info = np.array(grid_info, dtype=float)
    sort_index = np.lexsort(
        (grid_info[:, 3], grid_info[:, 2], grid_info[:, 1], grid_info[:, 0], grid_info[:, 4]))
    grid_info = grid_info[sort_index]
    zone_order = np.min(grid_info[:, 4])
    # start zone number from 1
    grid_info[:, 4] = grid_info[:, 4] - (zone_order - 1)

    # split zones at non continues interfaces
    zero_index = np.where(grid_info[:, 4] == 0)[0]
    grid_info = np.delete(grid_info, zero_index, 1)


    x_center = np.divide(np.add(grid_info[:, 0], grid_info[:, 1]), 2)
    y_center = np.divide(np.add(grid_info[:, 2], grid_info[:, 3]), 2)
    info = np.column_stack((x_center, y_center, grid_info[:, 4]))
    #put grid_info[:, 4]
    center_info = split(info, delta_X, delta_Y)
    grid_info[:, 0] = center_info[:, 0] - delta_X / 2
    grid_info[:, 1] = center_info[:, 0] + delta_X / 2
    grid_info[:, 2] = center_info[:, 1] - delta_Y / 2
    grid_info[:, 3] = center_info[:, 1] + delta_Y / 2
    grid_info[:, 4] = center_info[:, 2]
    grid_info[:, 5] = center_info[:, 3]
    grid_info = np.column_stack((grid_info, center_info[:, 4], mean_info))
    
    return grid_info
