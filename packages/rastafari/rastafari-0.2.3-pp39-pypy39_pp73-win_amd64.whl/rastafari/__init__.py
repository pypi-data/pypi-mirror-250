"""Rasterize vector features to grids."""

import math

import numpy as np
import numpy.typing as npt
import pyproj

from .core import ddaf_line_subpixel, even_odd_polygon_fill

__all__ = [
    "ddaf_line_subpixel",
    "even_odd_polygon_fill",
    "resample_band",
]

__version__ = "0.2.3"

ExtentType = tuple[float, float, float, float]
WeightsDict = dict[tuple[int, int], float]


def resample_band(
    source_grid: npt.NDArray[np.float_],
    source_extent: ExtentType,
    source_nodata: float,
    target_extent: ExtentType,
    target_nx: int,
    target_ny: int,
    source_srid: int,
    target_srid: int,
    subgridcells: int = 2,
) -> tuple[tuple[npt.NDArray[np.intp], ...], npt.NDArray[np.float_]]:
    """Resample raster using inverse nearest neighbour algorithm.

    The original raster is refined and each pixel is sorted into the
    target grid.

    args:
        source_grid: original raster as a numpy array ((X, Y))
        source_extent: extent of the original raster
        source_nodata: nodata value of source raster
        target_extent: target extent coordinates as (x1, y1, x2, y2)
        target_nx: number of cells in x-direction of target grid
        target_ny: number of cells in y-direction of target grid
        source_srid: srid of source raster as integer
        target_srid: srid of target raster as integer
    kwargs:
        subgridcells: divide each cell side by this factor to
          increase accuracy in resampling
    """
    # target extent
    tx0, ty0, tx1, ty1 = target_extent

    # source extent
    sx0, sy0, sx1, sy1 = source_extent

    sny = source_grid.shape[0]
    snx = source_grid.shape[1]

    # calculate grid cell-size
    target_dy = (ty1 - ty0) / target_ny
    target_dx = (tx1 - tx0) / target_nx

    source_dy = (sy1 - sy0) / sny
    source_dx = (sx1 - sx0) / snx

    # refinement factor < 0 means sorting into a coarser target grid
    refinement_factor = max(
        source_dx * subgridcells / target_dx, source_dy * subgridcells / target_dy
    )

    target_grid = np.zeros((target_ny, target_nx), dtype=float)

    # set nodata values to zero (if added by ST_Clip in emission query)
    source_grid[source_grid == source_nodata] = 0
    # upsample the source grid for improved accuracy
    if refinement_factor > 1 and subgridcells > 1:
        refinement_factor = math.ceil(refinement_factor)
        # values are divided to maintain raster sum after upsampling
        source_grid = (
            (source_grid / (refinement_factor * refinement_factor))
            .repeat(refinement_factor, axis=0)
            .repeat(refinement_factor, axis=1)
        )

        # adjust cell size to upsampled grid
        source_dx /= refinement_factor
        source_dy /= refinement_factor

    # get row and col indices of nonzero cells
    source_rows, source_cols = np.nonzero(source_grid)

    # get cell centre coordinates of non-zero cells
    ccx = sx0 + (source_cols + 0.5) * source_dx
    ccy = sy1 - (source_rows + 0.5) * source_dy
    cell_centers = np.vstack((ccx, ccy)).T
    if cell_centers.size == 0:
        # all cells are zero in source grid
        return ((), np.array([]))

    # if target srid is different from source srid,
    # transform cell centers to target srid
    if source_srid != target_srid:
        transformer = pyproj.Transformer.from_crs(
            source_srid, target_srid, always_xy=True
        )
        transformer.transform(cell_centers[:, 0], cell_centers[:, 1], inplace=True)

    # get indices within output bounds
    target_cols = ((cell_centers[:, 0] - tx0) / target_dx).astype(int)
    target_rows = target_ny - (np.ceil((cell_centers[:, 1] - ty0) / target_dy)).astype(
        int
    )
    # handle edge case (row or col = ny or ny)
    target_cols = np.clip(target_cols, 0, target_nx - 1, target_cols)
    target_rows = np.clip(target_rows, 0, target_ny - 1, target_rows)

    # create mask array for cells within target extent
    cells_within_target_extent = (
        (cell_centers[:, 0] >= tx0)
        & (cell_centers[:, 0] < tx1)
        & (cell_centers[:, 1] >= ty0)
        & (cell_centers[:, 1] < ty1)
    )
    np.add.at(
        target_grid,
        (
            target_rows[cells_within_target_extent],
            target_cols[cells_within_target_extent],
        ),
        source_grid[
            source_rows[cells_within_target_extent],
            source_cols[cells_within_target_extent],
        ],
    )
    return (target_grid.nonzero(), target_grid[target_grid > 0].ravel())
