"""
Tests.

@author: Carlos Ramos Carreño
@license: MIT
"""

import urllib.error

from skdatasets.repositories import cran
from skdatasets.repositories.cran import fetch


def test_cran_geyser():
    """Tests CRAN geyser dataset."""
    fetch("geyser")


def test_cran_geyser_return_X_y():
    """Tests CRAN geyser dataset."""
    X, y = fetch("geyser", return_X_y=True)


def test_cran_latest_version_offline(tmp_path, monkeypatch):
    """Tests that the offline fallback keeps the CRAN version string."""
    monkeypatch.setattr(cran, "get_data_home", lambda: str(tmp_path))
    # fetch_tgz() stores each package in <data home>/cran/<file name>/
    for version in ("1.2-3", "1.2-10", "1.2.4", "1.0"):
        (tmp_path / "cran" / f"mypkg_{version}.tar.gz").mkdir(parents=True)

    assert cran._get_latest_version_offline("mypkg") == "1.2-10"
    assert cran._get_latest_version_offline("otherpkg") is None


def test_cran_version_offline_url(tmp_path, monkeypatch):
    """Tests the URLs built from the offline version when CRAN is unreachable."""
    monkeypatch.setattr(cran, "get_data_home", lambda: str(tmp_path))
    (tmp_path / "cran" / "mypkg_1.2-3.tar.gz").mkdir(parents=True)

    def offline(*args, **kwargs):
        raise urllib.error.URLError("offline")

    monkeypatch.setattr(cran, "_get_latest_version_online", offline)

    assert cran._get_urls("mypkg", dataset_name="data") == (
        f"{cran.CRAN_URL}/src/contrib/mypkg_1.2-3.tar.gz",
        f"{cran.CRAN_URL}/src/contrib/Archive/mypkg/mypkg_1.2-3.tar.gz",
    )
