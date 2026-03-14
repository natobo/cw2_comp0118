import numpy as np
from matplotlib import pyplot as plt

import data
import output
import video

VOLUMES_DIR = output.get_dir("volumes")
SEG_PLOTS_DIR = output.get_dir("seg_plots")
SEGMENT_NAMES = [
    "Unassigned",
    "Extra-CSF",
    "GM",
    "WM",
    "Deep GM",
    "Brainstem+Pons",
]


def format_segment_label(seg_id):
    if 0 <= seg_id < len(SEGMENT_NAMES):
        return f"Segment {seg_id} ({SEGMENT_NAMES[seg_id]})"
    return f"Segment {seg_id} (Unknown-{seg_id})"


def main():
    for id in data.get_ids()[:3]:
        dataset = data.load_dataset(id)
        make_visualizations(dataset)


def make_visualizations(dataset):
    output_dir = output.get_dir(dataset.id)
    echo_times = data.get_echo_times()

    make_z_volume_video(dataset, 20, output_dir, echo_times)
    make_z_volume_video(dataset, 25, output_dir, echo_times)
    make_z_volume_video(dataset, 30, output_dir, echo_times)

    make_segment_plots(dataset, output_dir, echo_times)


def make_z_volume_video(dataset, z, output_dir, echo_times=None):
    """Creates a video of the readings over a slice over time."""
    volume_video = video.make_from_volume(
        dataset.reg[..., z, :],
        f"id={dataset.id}, z={z} volume",
        echo_times=echo_times,
    )
    # Save in two places for easier comparison between datasets.
    volume_video.save(output_dir / f"volume_z_{z}.mp4")
    volume_video.save(VOLUMES_DIR / f"{z}-{dataset.id}.mp4")
    plt.close()


def make_segment_plots(dataset, output_dir, echo_times):
    """Plot segment-wise mean signal intensity over echo times."""
    _, _, _, time_steps = dataset.reg.shape
    segment_count = dataset.seg.shape[3]

    fig, ax = plt.subplots(figsize=(8, 5))

    plotted = 0
    for seg_id in range(segment_count):
        curve = np.zeros(time_steps, dtype=float)
        # Scale by the total presence of the segment.
        scale = float(np.sum(dataset.seg[..., seg_id]))
        if scale <= 0:
            continue

        for step in range(time_steps):
            curve[step] = (
                np.tensordot(dataset.seg[..., seg_id], dataset.reg[..., step], axes=3)
                / scale
            )

        x = np.asarray(echo_times[: len(curve)], dtype=float)
        label = format_segment_label(seg_id)
        ax.plot(x, curve, marker="o", linewidth=1.8, markersize=4, label=label)
        plotted += 1

    ax.set_title("Signal Intensity by Segment Over Echo Time")
    ax.set_xlabel("Echo Time (ms)")
    ax.set_ylabel("Mean Segment Signal Intensity")
    ax.grid(True, alpha=0.3, linestyle="--")

    if plotted > 0:
        ax.legend(fontsize=8, ncol=2)

    fig.suptitle(f"id={dataset.id}", fontsize=13)
    fig.tight_layout()
    # Save in two places for easier comparison between datasets.
    fig.savefig(output_dir / "seg_plots", bbox_inches="tight")
    fig.savefig(SEG_PLOTS_DIR / str(dataset.id), bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
