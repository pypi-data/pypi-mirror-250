import numpy as np
import pyproj
from pytest import approx

from rastafari import resample_band


def test_resample_band() -> None:
    band = np.array([[1, 2], [3, 4]])
    source_extent = (0, 0, 100, 100)
    source_nodata = -9999
    target_extent = (0, 0, 25, 25)
    target_nx = 2
    target_ny = 2

    source_srid = 3006
    target_srid = 3006

    # upsampling to a finer target grid
    index_array, weights = resample_band(
        band,
        source_extent,
        source_nodata,
        target_extent,
        target_nx,
        target_ny,
        source_srid,
        target_srid,
    )

    assert np.all(weights == np.array([0.1875, 0.1875, 0.1875, 0.1875]))

    # using different srid's
    source_srid = 3006
    target_srid = 3857

    # tranform srs for corners
    transformer = pyproj.Transformer.from_crs(3006, 3857, always_xy=True)
    (x1, x2), (y1, y2) = transformer.transform(source_extent[::2], source_extent[1::2])

    # adding some margin to target extent to make sure whole source_grid is
    # covered
    target_extent = (x1 - 100, y1 - 100, x2 + 100, y2 + 100)
    index_array, weights = resample_band(
        band,
        source_extent,
        source_nodata,
        target_extent,
        target_nx,
        target_ny,
        source_srid,
        target_srid,
    )
    assert weights.sum() == approx(10.0, 1e-4)

    # sorting into a coarser target grid
    target_extent = (0, 0, 200, 200)
    target_nx = 2
    target_ny = 2
    index_array, weights = resample_band(
        band,
        source_extent,
        source_nodata,
        target_extent,
        target_nx,
        target_ny,
        source_srid,
        target_srid,
    )

    assert np.all(weights == np.array([10.0]))
