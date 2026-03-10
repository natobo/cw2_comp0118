import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import ArtistAnimation


def make_from_volume(volume, title):
    """
    Creates a video from a 3D volume, where the last dimension is traversed
    over time.

    Each frame consists of a 2D slice, with the last dimension representing
    time. The video features a colorbar which is correct and constant for the
    entire duration.
    """
    # The figure needs to be created before the artists.
    fig = plt.figure()
    fig.suptitle(title)
    slices = (volume[..., t] for t in range(volume.shape[2]))

    # Set the vmin and vmax to the global min and max so the colours are
    # consistent across frames.
    min = np.min(volume)
    max = np.max(volume)
    artists = [[plt.imshow(slice, vmin=min, vmax=max)] for slice in slices]

    # Add colorbar. It doesn't matter which frame it attaches to since they all
    # have the same mapping.
    plt.colorbar()
    return ArtistAnimation(fig, artists, interval=250)
