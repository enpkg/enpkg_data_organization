"""Utilities for the unit tests."""
from downloaders import BaseDownloader


def retrieve_zenodo_data():
    """Retrieve the data from Zenodo."""
    downloader = BaseDownloader()
    downloader.download(
        "https://zenodo.org/record/8152039/files/dbgkg_tropical_toydataset.tar.gz?download=1",
        "tests/data/dbgkg_tropical_toydataset",
    )
    # ALSO EXTRACT ALL OF THE THINGS!