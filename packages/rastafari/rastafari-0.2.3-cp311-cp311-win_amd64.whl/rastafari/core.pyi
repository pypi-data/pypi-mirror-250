import numpy as np
import numpy.typing as npt

from . import ExtentType, WeightsDict

def ddaf_line_subpixel(
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    weights: WeightsDict,
    length: float,
    grid_extent: ExtentType,
    grid_dx: float,
    grid_dy: float,
) -> int | None: ...
def even_odd_polygon_fill(
    points: npt.NDArray[np.float_],
    weights: WeightsDict,
    grid_extent: ExtentType,
    grid_nx: int,
    grid_ny: int,
    subgridcells: int = 2,
) -> None: ...
