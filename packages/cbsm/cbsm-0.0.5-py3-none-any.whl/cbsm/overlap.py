import numpy as np
from cbsm.merge import merge
from cbsm.splitting import surface_count

def overlap(grid_info1, grid_info2, delta_x, delta_y, merge_tolerance=19):
    """
    Identify overlapping compartments between two sets of grid information.

    Parameters
    ----------
    grid_info1 : array_like
        Grid information for the first set of compartments.
    grid_info2 : array_like
        Grid information for the second set of compartments.
    delta_X : float
        Acceptable tolerance along the X-axis.
    delta_Y : float
        Acceptable tolerance along the Y-axis.
    merge_tolerance : int, optional
        Tolerance for merging compartments, default is 19.

    Returns
    -------
    array
        New grid_info build by overlapping compartments from grid_info1 and grid_info2.

    Notes
    -----
    - The function uses the merge function from the app.services.scaledown.app.merge module.
    - The function uses the surface_count function from the app.services.scaledown.app.splitting module.

    Examples
    --------
    >>> grid_info1 = np.array([[1.0, 2.0, 3.0, 4.0, 5.0],
    ...                        [2.0, 3.0, 4.0, 5.0, 5.0],
    ...                        [3.0, 4.0, 5.0, 6.0, 6.0]])
    >>> grid_info2 = np.array([[1.5, 2.5, 3.5, 4.5, 7.0],
    ...                        [2.5, 3.5, 4.5, 5.5, 7.0],
    ...                        [3.5, 4.5, 5.5, 6.5, 8.0]])
    >>> delta_x = 0.1
    >>> delta_y = 0.2
    >>> merge_tolerance = 15
    >>> overlap_result = overlap(grid_info1, grid_info2, delta_x, delta_y, merge_tolerance)
    """
        
    overlaps = np.zeros((grid_info1.shape[0], 9))
    zone_combinations = {}
    zone_count = 0

    for compartment in grid_info1:
        #find compartments in grid_info2 within delta_x and delta_y
        indices = np.where(np.sum((grid_info2[:, 0:4] - compartment[0:4])**2, axis=1) < 
                           0.001 * min(delta_x, delta_y))[0]
        if (len(indices) > 0):
            zone1 = compartment[4]
            search_compartments = grid_info2[indices]
            for i, compartment2 in enumerate(search_compartments):
                zone2 = compartment2[4]
                if (zone1, zone2) in zone_combinations.keys():
                    #already exists
                    zone = zone_combinations[(zone1, zone2)]
                else:
                    zone_count += 1
                    zone = zone_count
                    zone_combinations[(zone1, zone2)] = zone
                new_compartment = [compartment2[0], compartment2[1], 
                                   compartment2[2], compartment2[3], zone, 
                                   compartment2[5], compartment2[6], 
                                   compartment[7], compartment2[7]]
                overlaps[indices[i]] = new_compartment
    #count number of compartments in each zone
    for zone in zone_combinations.values():
        indices = np.where(overlaps[:, 4] == zone)[0]
        overlaps[indices, 5] = len(indices)

    #update surface zone
    center_overlaps = np.column_stack((np.sum(overlaps[:, 0:2], axis=1) / 2, 
                                       np.sum(overlaps[:, 2:4], axis=1) / 2, 
                                       overlaps[:, 4:8]))
    surface_overlaps = surface_count(center_overlaps, delta_x, delta_y)
    overlaps[:, 6] = surface_overlaps[:, 4]

    #merge zones
    overlaps = merge(overlaps, merge_tolerance, delta_x, delta_y)

    return overlaps

