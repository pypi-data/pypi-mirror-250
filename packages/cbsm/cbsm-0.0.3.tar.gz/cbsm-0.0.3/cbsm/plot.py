import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.cm import ScalarMappable
import matplotlib.colors as mcolors
import numpy as np

class Plotter:
    def __init__(self, num_plots, show_annotations=True):
        self.fig, self.ax = plt.subplots(1, num_plots)
        self.plots_added = 0
        self.fig.set_size_inches(9, 4)
        self.fig.tight_layout(pad=2.0)
        self.show_annotations = show_annotations

    def add_plot(self, grid_info, title):
        # add as sub plot to figure
        ax = self.ax[self.plots_added]
        self.plots_added += 1
        # Define the colormap
        cmap = plt.get_cmap("tab20")
        
        # Create a ScalarMappable to map color values to colors in the colormap
        norm = mcolors.Normalize(vmin=0, vmax=len(cmap.colors) - 1)
        sm = ScalarMappable(cmap=cmap, norm=norm)

        # Plot the filled squares with colors based on the color_value
        for square in grid_info:
            x_min, x_max, y_min, y_max, color_value = square[0], square[1], square[2], square[3], square[4]
            width = x_max - x_min
            height = y_max - y_min
            color = sm.to_rgba(color_value - 1)
            ax.add_patch(patches.Rectangle((x_min, y_min), width, height, 
                                           fill=True, facecolor=color, edgecolor='black', 
                                           linewidth=0.5))

        # get x,y max
        x_max = max(grid_info[:, 1])
        y_max = max(grid_info[:, 3])
        # Set axis limits and labels
        ax.set_xlim(0, x_max)
        ax.set_ylim(0, y_max)
        ax.set_xlabel('Radial')
        ax.set_ylabel('Axial')
        ax.set_title(title)

        if self.show_annotations:
            # annotate zones
            zones = np.unique(grid_info[:, 4])
            for zone in zones:
                # annotate on center of zone
                index = np.where(grid_info[:, 4] == zone)[0]
                zone_center = grid_info[grid_info[:, 4] == zone][len(index) // 2]
                x = (zone_center[0] + zone_center[1]) / 2
                y = (zone_center[2] + zone_center[3]) / 2
                ax.annotate(int(zone), (x, y), color='black', weight='bold', 
                            fontsize=10, ha='center', va='center')


        # Show the colorbar if last plot
        if self.plots_added == len(self.ax):
            cbar = self.fig.colorbar(sm, ax=self.ax, label='Zones', aspect=40, pad=0.03, ticks=range(0, len(cmap.colors)))
            cbar.ax.set_yticklabels(range(1, len(cmap.colors) + 1))