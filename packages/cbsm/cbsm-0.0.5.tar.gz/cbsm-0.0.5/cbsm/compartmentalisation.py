import os
import sys 

from cbsm.zoning import zoning
from cbsm.zone_reformation import zone_reformation
from cbsm.volume_calculation import calculate_volume
from cbsm.overlap import overlap
from cbsm.result import Result
from cbsm.plot import Plotter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io



def CM(X, Y, Vx, Vy, number_X=15, number_Y=35, merge_tolerance=19, delta_px=0, delta_py=0):
    """
    Compute compartment map for two-dimensional data.

    Parameters
    ----------
    X : array_like
        X-coordinates of the data points.
    Y : array_like
        Y-coordinates of the data points.
    Vx : array_like
        X-component of the vector field at each data point, i.e. velocity.
    Vy : array_like
        Y-component of the vector field at each data point, i.e. velocity.
    number_X : int, optional
        Number of grid cells along the X-axis, default is 15.
    number_Y : int, optional
        Number of grid cells along the Y-axis, default is 35.
    merge_tolerance : int, optional
        Tolerance for merging compartments, default is 19.
    delta_px : float, optional
        Acceptable tolerance along the X-axis, default is 0.
    delta_py : float, optional
        Acceptable tolerance along the Y-axis, default is 0.

    Returns
    -------
    tuple
        A tuple containing:
        - grid_info (array): Information about each cell in the grid (x_min, x_max, y_min, y_max, zone, count, surface zone, vx_mean, vy_mean).
        - volume (float): Total volume of each compartment.
        - img (BytesIO): Image buffer containing a plot of the compartment maps.

    Notes
    -----
    - Negative values in X are set to zero.

    Examples
    --------
    >>> X = [1, 2, 3, 4]
    >>> Y = [5, 6, 7, 8]
    >>> Vx = [0.1, 0.2, 0.3, 0.4]
    >>> Vy = [0.5, 0.6, 0.7, 0.8]
    >>> grid_info, volume, img = CM(X, Y, Vx, Vy)
    """


    # Set negative values to zero
    X = np.array(X)
    Y = np.array(Y)
    Vx = np.array(Vx)
    Vy = np.array(Vy)
    index = np.where(X <= 0)
    for i in index:
        X = np.delete(X, i)
        Y = np.delete(Y, i)
        Vy = np.delete(Vy, i)
        Vx = np.delete(Vx, i)

    # Find max and min values of R and Y
    Max_X = np.max(X)
    Max_Y = np.max(Y)
    Min_X = np.min(X)
    Min_Y = np.min(Y)

    # 1. Initialization
    delta_X = (Max_X - Min_X) / number_X
    delta_Y = (Max_Y - Min_Y) / number_Y

    # Target variables
    par = np.column_stack((Vx, Vy))

    # Acceptable homogeneity tolerance range within a compartment
    delta_p = [delta_px, delta_py]
    Z = np.zeros((X.shape[0], 1))
    grid_info = np.zeros((X.shape[0], 6, par.shape[1]))

    resultArray = []
    plotter = Plotter(num_plots=3)

    for i in range(2):
        zone_map = zoning(X, Y, Z, par[:, i], delta_p[i])
        grid_info = zone_reformation(
            zone_map, delta_X, delta_Y, number_X, number_Y, i, merge_tolerance)
        volume = calculate_volume(grid_info)
        result = Result(zone_map, grid_info, volume)
        result.sortGridInfo()
        resultArray.append(result)
        plotter.add_plot(result.grid_info, title=("Radial Velocity" if i == 0 else "Axial Velocity"))

    grid_info = overlap(resultArray[0].grid_info, resultArray[1].grid_info, 
                        delta_X, delta_Y, merge_tolerance)
    plotter.add_plot(grid_info, title="Overlap")

    volume = calculate_volume(grid_info)

    # save plot as image
    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)

    return (grid_info, volume, img)


# method to run with default test data
def compartmentalise():
    np.set_printoptions(threshold=np.inf)
    np.set_printoptions(linewidth=np.inf)

    filename = "app/resources/2_A310_60_BM_160rpm_FlowStats_003.xlsx"
    print(os.getcwd())
    number_X = 15
    number_Y = 35
    merge_tolerance = 19

    # Read CFD data
    data = pd.read_excel(filename)
    CFD_data = data.values

    # Extract data
    # start at 5 to avoid the header
    X = CFD_data[5:, 9]
    Y = CFD_data[5:, 1]
    Vx = CFD_data[5:, 7]
    Vy = CFD_data[5:, 6]

    # Set negative values to zero
    index = np.where(X <= 0)
    for i in index:
        X = np.delete(X, i)
        Y = np.delete(Y, i)
        Vy = np.delete(Vy, i)
        Vx = np.delete(Vx, i)

    # Find max and min values of R and Y
    Max_X = np.max(X)
    Max_Y = np.max(Y)
    Min_X = np.min(X)
    Min_Y = np.min(Y)

    # 1. Initialization
    delta_X = (Max_X - Min_X) / number_X
    delta_Y = (Max_Y - Min_Y) / number_Y

    # Target variables
    par = np.column_stack((Vx, Vy))

    # Acceptable homogeneity tolerance range within a compartment
    delta_p = [0, 0]
    Z = np.zeros((X.shape[0], 1))
    grid_info = np.zeros((X.shape[0], 6, par.shape[1]))

    resultArray = []
    plotter = Plotter(num_plots=3)

    for i in range(2):
        zone_map = zoning(X, Y, Z, par[:, i], delta_p[i])
        grid_info = zone_reformation(
            zone_map, delta_X, delta_Y, number_X, number_Y, i, merge_tolerance=merge_tolerance)
        volume = calculate_volume(grid_info)

        result = Result(zone_map=zone_map, grid_info=grid_info, volume=volume)
        result.sortGridInfo()
        resultArray.append(result)
        plotter.add_plot(result.grid_info, title=("Radial Velocity" if i == 0 else "Axial Velocity"))

    grid_info = overlap(resultArray[0].grid_info, resultArray[1].grid_info, 
                        delta_X, delta_Y, merge_tolerance)
    volume = calculate_volume(grid_info)

    plotter.add_plot(grid_info, title="Overlap")
    #plt.legend(loc='upper right')
    plt.show()

    return (grid_info, volume)

def main():
    compartmentalise()
if __name__=="__main__":
    main()
