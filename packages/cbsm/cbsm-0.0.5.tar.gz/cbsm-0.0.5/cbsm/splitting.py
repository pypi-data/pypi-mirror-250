import numpy as np
import networkx as nx

def split(center_info, delta_x, delta_y):
    """
    Split connected compartments in center_info based on specified delta values.

    Parameters
    ----------
    center_info : array_like
        Center information containing information about each compartment with their respective center coordinates.
    delta_X : float
        Acceptable tolerance along the X-axis.
    delta_Y : float
        Acceptable tolerance along the Y-axis.

    Returns
    -------
    array
        Updated center information with split zones.

    Notes
    -----
    - The function uses the within_delta function from the same module.
    - The function uses the surface_count function from the same module.

    Examples
    --------
    >>> center_info = np.array([[1.0, 2.0, 3.0],
    ...                         [2.0, 3.0, 4.0],
    ...                         [3.0, 4.0, 5.0]])
    >>> delta_x = 0.1
    >>> delta_y = 0.2
    >>> split_result = split(center_info, delta_x, delta_y)
    """

    zone_data = center_info
    zone_data = np.column_stack((zone_data, np.zeros(zone_data.shape[0]), np.zeros(zone_data.shape[0])))

    G = nx.Graph()

    for row in zone_data:
        x, y, zone, _, _ = row
        G.add_node((x, y), zone=zone)

    def add_edges(graph, zone_data, delta_x, delta_y):
        rows, cols = zone_data.shape[0], zone_data.shape[1]
        for i in range(rows):
            x1, y1, _, _, _= zone_data[i]
            for j in range(i + 1, rows):
                x2, y2, _, _, _ = zone_data[j]
                if within_delta((x1, y1), (x2, y2), delta_x, delta_y) and zone_data[i,2] == zone_data[j,2]:
                    graph.add_edge((x1, y1), (x2, y2))

    add_edges(G, zone_data, delta_x, delta_y)

    connected_components = list(nx.connected_components(G))

    # Assign unique zone numbers to disconnected components
    unique_zone_number = 1
    for component in connected_components:
        for node in component:
            x, y = node
            zone_data[(zone_data[:, 0] == x) & (zone_data[:, 1] == y), 2] = unique_zone_number
            # set count of connected nodes in zone
            zone_data[(zone_data[:, 0] == x) & (zone_data[:, 1] == y), 3] = len(component)
        unique_zone_number += 1

    zone_data = surface_count(zone_data, delta_x, delta_y)

    return zone_data

def within_delta(coord1, coord2, delta_x, delta_y):
        x1, y1 = coord1
        x2, y2 = coord2
        # 1.1 magic number from tannaz method
        return abs(x1 - x2) < 1.1 * delta_x and abs(y1 - y2) < 1.1 * delta_y

def surface_count(zone_data, delta_x, delta_y):
    for i, row in enumerate(zone_data):
        neighbours = []
        for j, row2 in enumerate(zone_data):
            if i != j:
                if within_delta(row[0:2], row2[0:2], delta_x, delta_y) & (row[2] != row2[2]):
                    neighbours.append(row2)
        zone_count = {}
        for n in neighbours:
            if n[2] in zone_count:
                zone_count[n[2]] += 1
            else:
                zone_count[n[2]] = 1

        max_zone_count = 0
        max_zone = 0
        for key, value in zone_count.items():
            if value > max_zone_count:
                max_zone_count = value
                max_zone = key
        zone_data[i, 4] = max_zone

    #find most common zone for each zone
    zone_list = np.unique(zone_data[:, 2])
    for zone in zone_list:
        zone_index = np.where(zone_data[:, 2] == zone)
        count = np.bincount(zone_data[zone_index, 4][0].astype(int))
        max_count = 0
        max_i = 0
        for i, num in enumerate(count):
            if num > max_count and i != 0:
                max_count = num
                max_i = i
        zone_data[zone_index, 4] = max_i
        
    return zone_data