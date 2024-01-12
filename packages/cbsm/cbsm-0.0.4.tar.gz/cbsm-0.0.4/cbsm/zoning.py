import numpy as np

def zoning(X, Y, Z, target, delta_p):
    """
    Create a simple compartment map based on the specified parameters.

    Parameters
    ----------
    X : array_like
        X-coordinates of compartments.
    Y : array_like
        Y-coordinates of compartments.
    Z : array_like
        Z-coordinates of compartments.
    target : array_like
        Target variable values.
    delta_p : float
        Acceptable homogeneity tolerance range within a compartment.

    Returns
    -------
    array
        Zone map with classification based on the specified parameters.

    Examples
    --------
    >>> X = np.array([1.0, 2.0, 3.0])
    >>> Y = np.array([2.0, 3.0, 4.0])
    >>> Z = np.array([3.0, 4.0, 5.0])
    >>> target = np.array([4.0, 5.0, 6.0])
    >>> delta_p = 0.1
    >>> zone_map = zoning(X, Y, Z, target, delta_p)
    """

    CFD = np.column_stack((X, Y, Z, target))
    sort_index = np.lexsort((CFD[:, 2], CFD[:, 1], CFD[:, 0], CFD[:, 3]))
    CFD_sorted = CFD[sort_index]


    zone_map = np.zeros((CFD_sorted.shape[0], 5))

    zone_map[:, :4] = CFD_sorted[:, :4]

    # Classifying
    for j in range(0, X.shape[0]):
        if zone_map[j, 3] < delta_p:
            zone_map[j, 4] = 1
        else:
            zone_map[j, 4] = 2

    return zone_map