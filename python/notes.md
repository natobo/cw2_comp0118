Before running, make sure you have the adolescent data (`cmbi_data` in the onedrive), in a directory called `data-adolescent`, located in the project root directory.

To run, create a virtual environment and activate it, then install the dependencies and run the `main.py` file. The results will be in a newly-created directory called `output`.

```bash
# You can also use uv or your preferred tool.
python -m venv .venv
# This line will vary depending on operating system.
source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

The code takes 15 minutes to run on my machine. You can see the earlier results much sooner though. The code will break on the last dataset because it has repeated readings (mentioned below).
Each dataset has 3 videos of the readings across slices (z=constant) over time, plus one plot of readings averaged across each segment.
Two copies of each output are saved in different places to make it easier to compare across datasets.
One copy is in a per-dataset directory. The other is grouped in directories called `seg_plots` and `volumes`.

Most of the readings appear to be (mostly) monotonic and mono-exponential (which appear as straight lines on the log-y plots), but many of them have a sharper drop right at the start. Besides segment 0, segment 1 appears to be the least conforming to this mono-exponentiality assumption as the plot almost always seems to be curving upwards for this segment.
In some datasets some of the segments have non-monotonic readings, but this is usually limited to just a small bump which can probably be attributed to measurement noise.

Segment 0 is the least well-behaved in the sense that it is generally most disimilar to the other readings and the most likely to not be monotonic. This is generally expected and not super relevant since segment zero corresponds to skull and background, ie. not brain matter.
Initially, the other segments tend to be, from highest to lowest, 5, 4, 2, 3, 1, thought 4 and 2 are often swapped. The ordering tends to stay the same over time, although segment 1 appears to consistently decay slower than the rest and ends up being the highest by the end.

Interesting datasets:
- 17065: A surge in the readings across the board right at the start. Probably some external factor? Or a jolt or something in the machine, that sort of thing.
- 74067: Does not have the full 10 readings.
- 78004: Does not have the full 10 readings.
- 98865: Appears to have repeated readings so there are 20 instead of the expected 10. The code breaks on this dataset.

Further work on this part of the coursework:
- Need to figure out exactly what the segmentation data is supposed to represent. Some of the values are negative which doesn't make much sense...
- It would be nice if the volume videos were adjusted to match the echo times (I totally forgot about these until the very end).
- It would be useful to plot readings from sample voxels from each dataset to see the behaviour at a more granular level.
- Possibly see if the readings or behaviour varies as we move closer/further from the brain's boundaries?
- Map the segment numbers to what they actually represent.
- What is that sharp drop at the start of most readings?
- From the prompt:
  - What imaging factors might affect the results of the model-fitting?
  - Does the data from any subject violate these assumptions more often?
  - How might these artefacts affect the estimation of the model parameters?
