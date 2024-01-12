import numpy as np

def calculate_volume(grid_info):
    """
    Calculate volumes for each compartment based on the grid information.

    Parameters
    ----------
    grid_info : array_like
        Grid information containing details about each cell.

    Returns
    -------
    array
        Volume for each compartment.

    Examples
    --------
    >>> grid_info = np.array([[1.0, 2.0, 3.0, 4.0, 1.0, 5.0],
    ...                       [2.0, 3.0, 4.0, 5.0, 1.0, 6.0],
    ...                       [3.0, 4.0, 5.0, 6.0, 2.0, 7.0]])
    >>> volume_result = calculate_volume(grid_info)
    """

    zones = np.unique(grid_info[:, 4])

    dx = grid_info[:, 1]**2 - grid_info[:, 0]**2
    dy = grid_info[:, 3] - grid_info[:, 2]

    volumes = np.pi * dx * dy

    volume = np.zeros((zones.shape[0], 2))
    for i, zone in enumerate(zones):
        volume[i, 0] = zone
        volume[i, 1] = np.sum(volumes[grid_info[:, 4] == zone])
    
    return volume
