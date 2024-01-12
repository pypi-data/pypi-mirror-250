import numpy as np
import matplotlib.pyplot as plt

from cbsm.cubing2 import cubing2
from cbsm.merge import merge


def zone_reformation(zone_map, delta_X, delta_Y, number_X, number_Y, i=0, merge_tolerance=19):
    """
    Reform compartments based on the specified delta values and grid parameters.

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
    i : int, optional
        Index parameter, default is 0.
    merge_tolerance : int, optional
        Tolerance for merging compartments, default is 19.

    Returns
    -------
    array
        Updated grid information after zone reformation.

    Notes
    -----
    - The function uses the cubing2 function from the app.services.scaledown.app.cubing2 module.
    - The function uses the merge function from the app.services.scaledown.app.merge module.

    Examples
    --------
    >>> zone_map = np.array([[1.0, 2.0, 3.0, 4.0, 5.0],
    ...                      [2.0, 3.0, 4.0, 5.0, 5.0],
    ...                      [3.0, 4.0, 5.0, 6.0, 6.0]])
    >>> delta_X = 0.1
    >>> delta_Y = 0.2
    >>> number_X = 15
    >>> number_Y = 35
    >>> i = 0
    >>> merge_tolerance = 19
    >>> reformed_grid_info = zone_reformation(zone_map, delta_X, delta_Y, number_X, number_Y, i, merge_tolerance)
    """
    
    grid_info = cubing2(zone_map, delta_X, delta_Y, number_X, number_Y)
    # sort grid info by zone
    grid_info = np.array(grid_info)
    sort_index = np.lexsort(
        (grid_info[:, 3], grid_info[:, 2], grid_info[:, 1], grid_info[:, 0], grid_info[:, 4]))
    grid_info = grid_info[sort_index]

    # merge compartments
    grid_info = merge(grid_info, merge_tolerance, delta_X, delta_Y)
    sort_index = np.lexsort(
        (grid_info[:, 3], grid_info[:, 2], grid_info[:, 1], grid_info[:, 0], grid_info[:, 4]))
    grid_info = grid_info[sort_index]
    return grid_info
