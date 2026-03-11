import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import ArtistAnimation


def make_from_volume(volume, title, echo_times=None):
    """
    Creates a video from a 3D volume, where the last dimension is traversed
    over time.

    Each frame consists of a 2D slice, with the last dimension representing
    time. The video features a colorbar which is correct and constant for the
    entire duration.

    If echo_times is provided, each frame is labelled with its TE value and
    the animation interval is scaled to the mean TE step (in ms), so playback
    speed is proportional to the actual acquisition timing.
    """
    fig, ax = plt.subplots()
    fig.suptitle(title)

    n_frames = volume.shape[2]
    vmin = np.min(volume)
    vmax = np.max(volume)

    # Scale interval so mean TE step maps to a viewable speed (20 ms display
    # per 1 ms of TE). Falls back to 250 ms when no echo times are given.
    if echo_times is not None:
        steps = np.diff(echo_times[:n_frames])
        mean_step = float(np.mean(steps)) if len(steps) > 0 else 1.0
        interval = max(50, mean_step * 20)
    else:
        interval = 250

    artists = []
    for t in range(n_frames):
        im = ax.imshow(volume[..., t], vmin=vmin, vmax=vmax)
        artists_frame = [im]
        if echo_times is not None and t < len(echo_times):
            label = ax.text(
                0.02, 0.97, f"TE = {echo_times[t]:.1f} ms",
                transform=ax.transAxes, color="white", fontsize=10,
                va="top", ha="left",
                bbox=dict(boxstyle="round,pad=0.2", fc="black", alpha=0.5),
            )
            artists_frame.append(label)
        artists.append(artists_frame)

    plt.colorbar(im, ax=ax)
    return ArtistAnimation(fig, artists, interval=interval)
