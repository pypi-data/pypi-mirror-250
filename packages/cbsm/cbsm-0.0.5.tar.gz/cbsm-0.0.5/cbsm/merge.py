import numpy as np
import networkx as nx

from cbsm.splitting import surface_count, within_delta


def merge(grid_info, merge_tolerance, delta_x, delta_y):
    """
    Merge compartments based on specified merge tolerance and spatial proximity.

    Parameters
    ----------
    grid_info : array_like
        Grid information containing information about each compartment.
    merge_tolerance : int
        Tolerance for merging compartments.
    delta_X : float
        Acceptable tolerance along the X-axis.
    delta_Y : float
        Acceptable tolerance along the Y-axis.

    Returns
    -------
    array
        Merged grid information.

    Notes
    -----
    - The function uses the surface_count function from the app.services.scaledown.app.splitting module.
    - The function uses the within_delta function from the app.services.scaledown.app.splitting module.

    Examples
    --------
    >>> grid_info = np.array([[1.0, 2.0, 3.0, 4.0, 5.0],
    ...                        [2.0, 3.0, 4.0, 5.0, 5.0],
    ...                        [3.0, 4.0, 5.0, 6.0, 6.0]])
    >>> merge_tolerance = 15
    >>> delta_x = 0.1
    >>> delta_y = 0.2
    >>> merged_grid_info = merge(grid_info, merge_tolerance, delta_x, delta_y)
    """
        
    merge_list = np.where(grid_info[:, 5] < merge_tolerance)

    # merge zones smaller zones
    for i in merge_list[0]:
        prev_zone_count = grid_info[i, 5]
        grid_info[i, 4] = grid_info[i, 6]
        index = np.where(grid_info[:, 4] == grid_info[i, 4])
        grid_info[index, 5] = prev_zone_count + 1

    # merge disconnected compartments
    for idx, compartment in enumerate(grid_info):
        neighbour_zone_counts = {}
        neighbour_zone_counts[compartment[4]] = 1
        for n in grid_info:
            if within_delta(((compartment[0] + compartment[1]) / 2, (compartment[2] + compartment[3]) / 2), 
                            ((n[0] + n[1]) / 2, (n[2] + n[3])/2), delta_x, delta_y):
                if n[4] in neighbour_zone_counts.keys():
                    neighbour_zone_counts[n[4]] += 1
                else:
                    neighbour_zone_counts[n[4]] = 1

        # find max zone
        max_zone_count = neighbour_zone_counts[compartment[4]]
        max_zone = compartment[4]
        for key, value in neighbour_zone_counts.items():
            if value > max_zone_count:
                max_zone_count = value
                max_zone = key

        if compartment[4] != max_zone:
            index = np.where(grid_info[:, 4] == max_zone)
            grid_info[index, 5] += 1
            index2 = np.where(grid_info[:, 4] == compartment[4])
            grid_info[index2, 5] -= 1

            zone_count = grid_info[index[0], 5][0]
            grid_info[idx, 4] = max_zone
            grid_info[idx, 5] = zone_count
    
    # update zone numbers to start at 1
    zone_list = np.unique(grid_info[:, 4])
    grid_info_copy = grid_info.copy()
    for i, zone in enumerate(zone_list):
        grid_info[(grid_info_copy[:, 4] == zone), 4] = i + 1

    # update surface zone count
    new_surface = surface_count(np.column_stack((np.zeros(grid_info.shape[0]),
                                                 np.zeros(grid_info.shape[0]),
                                                 grid_info[:, 4], grid_info[:, 5],
                                                 grid_info[:, 6])), delta_x, delta_y)
    grid_info[:, 6] = new_surface[:, 4]

    return grid_info