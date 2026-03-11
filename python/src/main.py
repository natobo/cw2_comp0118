import numpy as np
from matplotlib import pyplot as plt

import data
import output
import video

VOLUMES_DIR = output.get_dir("volumes")
SEG_PLOTS_DIR = output.get_dir("seg_plots")


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
    """Plots average reading per segment over time."""
    width, height, depth, time_steps = dataset.reg.shape
    segment_count = dataset.seg.shape[3]

    plt.figure()
    for seg_id in range(segment_count):
        curve = []
        # Scale by the total presence of the segment.
        scale = np.sum(dataset.seg[..., seg_id])
        for step in range(time_steps):
            curve.append(
                np.tensordot(dataset.seg[..., seg_id], dataset.reg[..., step], axes=3)
                / scale
            )
        plt.semilogy(echo_times[: len(curve)], curve, label=seg_id)

    plt.legend()
    plt.suptitle(f"id={dataset.id}, reading per segment (log y-axis)")
    # Save in two places for easier comparison between datasets.
    plt.savefig(output_dir / "seg_plots", bbox_inches="tight")
    plt.savefig(SEG_PLOTS_DIR / str(dataset.id), bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()
