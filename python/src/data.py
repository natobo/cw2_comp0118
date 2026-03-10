from pathlib import Path

import nibabel as nib

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data-adolescent"
METADATA_DIR = DATA_DIR.parent / "metadata"
ECHO_TIMES_PATH = METADATA_DIR / "TEs.txt"
IDS_PATH = METADATA_DIR / "ids.txt"


def load_file(filename, append_file_extension=True):
    """Loads a nifti file from the data directory."""
    if append_file_extension:
        filename += ".nii.gz"
    return nib.load(DATA_DIR / filename)


def get_echo_times():
    """Returns the list of echo times for the data."""
    with open(ECHO_TIMES_PATH, "r") as times_file:
        return [float(time) for time in times_file.readline().split()]


def get_ids():
    """Returns the full list of valid data ids."""
    with open(IDS_PATH, "r") as id_file:
        as_strings = id_file.readlines()
    return [int(id) for id in as_strings]


def load_dataset(id):
    """
    Loads the dataset corresponding to the given id.

    Favour calling this over calling the Dataset constructor directly.
    """
    return Dataset(id)


class Dataset:
    """
    Represents a full dataset.

    Contains the following:
    - raw t2 data
    - reg(ularized?) t2 data
    - brain mask
    - segmentation data
    - parcellation data
    - simplified parcellation data (par_lobe)
    - fully parcellated data
    """

    prefix = "Epicure"

    def __init__(self, id):
        """
        This interface is unstable. Favour calling data.load instead of
        directly creating an instance of this class.
        """
        self.id = id
        self.prefix += str(id)
        self.mask = self._load_mask()
        self.par = self._load_file("_par1")
        self.par_lobe = self._load_file("_par2")
        self.reg = self._load_file("_reg")
        self.seg = self._load_file("_seg1")
        self.raw = self._load_file("")
        self.fullp = self._load_file("-fullp")

    def _load_mask(self):
        return load_file(f"{self.prefix}-mask1").dataobj

    def _load_file(self, suffix):
        return load_file(f"{self.prefix}-qt2{suffix}").dataobj
