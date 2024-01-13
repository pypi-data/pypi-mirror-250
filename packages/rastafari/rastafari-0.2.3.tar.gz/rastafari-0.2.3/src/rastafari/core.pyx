import cython

from cpython.mem cimport PyMem_Free, PyMem_Malloc
from libc.math cimport abs, ceil, floor, int, round, sqrt

import numpy as np


@cython.cdivision(True)
@cython.wraparound(False)
@cython.boundscheck(False)
cpdef int ddaf_line_subpixel(
    double x0,
    double y0,
    double x1,
    double y1,
    dict weights,
    double length,
    (double, double, double, double) grid_extent,
    double grid_dx,
    double grid_dy
):
    """Rasterize line using DDA (Digital Differential Analyzer) algorithm.

    The algorithm is adjusted to give weights corresponding to fraction of line
    intersected by each cell. This allows emissions to be assigned to the
    correct cell.

    Cells are identified by tuple (row, col)
    If cell already exists in weights, current weight are added
    weights are multiplied by segment-length / length
    to ensure sum of weights equals 1.0

    Args:
        x0: start node x-coordianate
        y0: start node y-coordianate
        x1: end node x-coordianate
        y1: end node y-coordianate
        weights: dict with (row, col) as key and weight as value
        grid_extent: grid corners as (x1, y1, x2, y2)
        grid_dx: cellsize in x-direction
        grid_dy: cellsize in y-direction

    """
    # tolerance used in rasterization
    cdef float TOLERANCE = 1e-6
    cdef int i, ind
    cdef double gx0, gy0, gx1, gy1
    gx0, gy0, gx1, gy1 = grid_extent

    # if outside of rectangle
    if (
        (x0 < gx0 and x1 < gx0)
        or (x0 > gx1 and x1 > gx1)
        or (y0 < gy0 and y1 < gy0)
        or (y0 > gy1 and y1 > gy1)
    ):
        return 0

    cdef double segment_length = sqrt((x1 - x0)**2 + (y1 - y0)**2)

    # transfer to pixel coordinates (from lower left corner)
    cdef double x0p, x1p, y0p, y1p, xdiff, intersection_length, old_dist, x_diff, y_diff
    x0p = (x0 - gx0) / grid_dx
    x1p = (x1 - gx0) / grid_dx
    y0p = (y0 - gy0) / grid_dy
    y1p = (y1 - gy0) / grid_dy

    cdef int grid_ny, grid_nx, nx, a1x, a0x, ny, a0y, a1y, row, col, xi, yi
    grid_ny = int(round((gy1 - gy0) / grid_dy))
    grid_nx = int(round((gx1 - gx0) / grid_dx))

    cdef double ax, dx, ac, bx, value
    # x-axis pixel cross
    a0x = 1
    a1x = 0
    nx = -1
    if x0p < x1p:
        a0x = int(ceil(x0p))
        a1x = int(floor(x1p))
        dx = (y1p - y0p) / (x1p - x0p)
        ax = a0x
        bx = y0p + (a0x - x0p) * dx
        nx = int(a1x - a0x)
    elif x0p > x1p:
        a0x = int(ceil(x1p))
        a1x = int(floor(x0p))
        dx = (y1p - y0p) / (x1p - x0p)
        ax = a0x
        bx = y1p + (a0x - x1p) * dx
        nx = int(a1x - a0x)
    cdef double ay, by
    # y-axis pixel cross
    a0y = 1
    a1y = 0
    ny = -1
    if y0p < y1p:
        a0y = int(ceil(y0p))
        a1y = int(floor(y1p))
        dy = (x1p - x0p) / (y1p - y0p)
        ay = a0y
        by = x0p + (a0y - y0p) * dy
        ny = int(a1y - a0y)
    elif y0p > y1p:
        a0y = int(ceil(y1p))
        a1y = int(floor(y0p))
        dy = (x1p - x0p) / (y1p - y0p)
        ay = a0y
        by = x1p + (a0y - y1p) * dy
        ny = int(a1y - a0y)

    # nr of crossings
    cdef int nc = nx + ny + 2
    cdef double *crossings_x = <double *> PyMem_Malloc(nc * sizeof(double))
    cdef double *crossings_y = <double *> PyMem_Malloc(nc * sizeof(double))
    cdef double *dist = <double *> PyMem_Malloc(nc * sizeof(double))
    cdef double swap_dist, swap_x, swap_y
    cdef double last_cross_x, last_cross_y, cross_x, cross_y, d

    try:
        crossings_x[0] = 0.0
        crossings_y[0] = 0.0

        if a0x <= a1x:
            for i in range(nx + 1):
                crossings_x[i] = ax
                crossings_y[i] = bx
                bx += dx
                ax += 1
        if a0y <= a1y:
            for i in range(nx + 1, nc):
                crossings_y[i] = ay
                crossings_x[i] = by
                by += dy
                ay += 1
        if (nx == -1) and (ny == -1):
            row = grid_ny - <int>ceil(y0p)
            col = int(floor(x0p))
            if (row, col) in weights:
                weights[(row, col)] += segment_length/length
            elif not (row < 0 or row >= grid_ny or col < 0 or col >= grid_nx):
                weights[(row, col)] = segment_length/length
            return 0

        # calculate distance in normal coordinates (not pixel coordinates)

        for i in range(nc):
            x_diff = grid_dx * (crossings_x[i] - x0p)
            y_diff = grid_dy * (crossings_y[i] - y0p)
            dist[i] = sqrt(x_diff ** 2 + y_diff ** 2)
        # sort crossings by dist array, via a bubble-sort.
        i = 0
        while i < nc - 1:
            if dist[i] > dist[i + 1]:
                swap_dist = dist[i]
                swap_x = crossings_x[i]
                swap_y = crossings_y[i]
                dist[i] = dist[i + 1]
                crossings_x[i] = crossings_x[i + 1]
                crossings_y[i] = crossings_y[i + 1]
                dist[i + 1] = swap_dist
                crossings_x[i + 1] = swap_x
                crossings_y[i + 1] = swap_y
                if i:
                    i -= 1
            else:
                i += 1

        last_cross_x = -9999.0
        last_cross_y = -9999.0
        old_dist = 0.0

        for i in range(nc):
            d = dist[i]
            cross_x = crossings_x[i]
            cross_y = crossings_y[i]

            # crossing in a cell corner - i.e. the same point crossing
            # the grid lines in both x and y direction, only the first is processed
            if cross_x == last_cross_x and cross_y == last_cross_y:
                continue
            #if np.all(cross == last_cross):
            #    continue

            intersection_length = d - old_dist
            x_diff = cross_x - floor(cross_x)
            y_diff = cross_y - floor(cross_y)

            if abs(x_diff) < TOLERANCE:
                # crossing gridline in x direction
                if x0p < x1p:
                    xi = <int>(cross_x) - 1
                else:
                    xi = <int>(cross_x)
            else:
                xi = int(cross_x)

            if abs(y_diff) < TOLERANCE:
                # crossing gridline in y direction
                if y0p < y1p:
                    yi = <int>(cross_y) - 1
                else:
                    yi = <int>(cross_y)
            else:
                yi = int(cross_y)

            row = grid_ny - yi - 1
            col = xi
            value = intersection_length / length

            # add indices if within the grid dimensions
            if (row, col) in weights:
                weights[(row, col)] += value
            elif not (row < 0 or row >= grid_ny or col < 0 or col >= grid_nx):
                weights[(row, col)] = value

            old_dist = d
            last_cross_x = cross_x
            last_cross_y = cross_y

        # if end-node of segment does not coincede with last cell border crossing
        # the weight needs to be added for the last grid cell along the line
        if crossings_x[nc - 1] != x1p or crossings_y[nc -1] != y1p:
            intersection_length = segment_length - old_dist
            value = intersection_length / length
            row = grid_ny - <int>(ceil(y1p))
            col = <int>(floor(x1p))

            # add indices if within the grid dimensions
            if (row, col) in weights:
                weights[(row, col)] += value
            elif not (row < 0 or row >= grid_ny or col < 0 or col >= grid_nx):
                weights[(row, col)] = value
    finally:
        PyMem_Free(crossings_x)
        PyMem_Free(crossings_y)
        PyMem_Free(dist)

@cython.cdivision(True)
def even_odd_polygon_fill(
    points,
    dict weights,
    (double, double, double, double) grid_extent,
    int grid_nx,
    int grid_ny,
    int subgridcells=2
):
    """Rasterize polygon using even-odd rule and add values to grid.
    from public domain code found at http://alienryderflex.com/polygon_fill/

    args:
        points: numpy array with points ((X, Y))
        grid_extent: grid corners as (x1, y1, x2, y2)
        grid_nx: number of cells in x-direction
        grid_ny: number of cells in y-direction

    kwargs:
        subgridcells: divide each cell side into a number of subgridcells
    """
    gx0, gy0, gx1, gy1 = grid_extent

    # grid is refined to better resolve the polygon shape
    cdef int nx = grid_nx * subgridcells
    cdef int ny = grid_ny * subgridcells

    # calculate grid cell-size
    cdef double grid_dy = (gy1 - gy0) / ny
    cdef double grid_dx = (gx1 - gx0) / nx

    # get bounding box of polygon
    cdef double xmax = points[:, 0].max()
    cdef double xmin = points[:, 0].min()
    cdef double ymax = points[:, 1].max()
    cdef double ymin = points[:, 1].min()

    # bounding box in pixel coordinates
    cdef int xmin_p = int((xmin - gx0) / grid_dx)
    cdef int xmax_p = int(ceil((xmax - gx0) / grid_dx))
    cdef int ymin_p = int((ymin - gy0) / grid_dy)
    cdef int ymax_p = int(ceil((ymax - gy0) / grid_dy))

    # convert points to pixel coordinates
    pp = np.copy(points)
    cdef double[:, :] pp_view = pp
    cdef Py_ssize_t ii
    for ii in range(pp.shape[0]):
        pp_view[ii, 0] = (pp_view[ii, 0] - gx0) / grid_dx
        pp_view[ii, 1] = (pp_view[ii, 1] - gy0) / grid_dy

    cdef int rowmin = min((max((0, ny - ymax_p)), ny))
    cdef int rowmax = max((min((ny, ny - ymin_p)), 0))
    cdef int colmin = min((max((0, int(xmin_p))), ceil(xmax_p)))
    cdef int colmax = min((nx - 1, int(max(ceil(xmax_p), 0))))

    subgrid = np.zeros((rowmax - rowmin, colmax - colmin))
    cdef int number_of_nodes = pp.shape[0]

    cdef int filled_cells = 0

    cdef int intersections = 0
    cdef list nodeX = []
    cdef int i, j
    cdef double swap

    #  Find intersections along scanline (rows) (y in pixel coordinates)
    for y in np.arange(ymin_p + 0.5, ymax_p):
        intersections = 0
        nodeX = []

        # Build a list of intersections
        j = number_of_nodes - 1
        for i in range(number_of_nodes):
            if (pp[i, 1] < y and pp[j, 1] >= y) or (pp[j, 1] < y and pp[i, 1] >= y):
                intersections += 1

                # incremental scan line method
                # m = (y[k+1] - y[k]) / (x[k+1] - x[k])
                # y[k+1] - y[k] = 1
                # x[k+1] = x[k] + 1 / m

                nodeX.append(
                    pp[i, 0]
                    + (y - pp[i, 1]) / (pp[j, 1] - pp[i, 1]) * (pp[j, 0] - pp[i, 0])
                )
            j = i

        #  Sort the intersections, via a simple bubble-sort.
        i = 0
        while i < intersections - 1:
            if nodeX[i] > nodeX[i + 1]:
                swap = nodeX[i]
                nodeX[i] = nodeX[i + 1]
                nodeX[i + 1] = swap
                if i:
                    i -= 1
            else:
                i += 1

        #  Fill the pixels between node pairs.
        for i in range(0, intersections, 2):
            if nodeX[i] >= colmax:
                break
            if nodeX[i + 1] > colmin:
                if nodeX[i] < colmin:
                    nodeX[i] = colmin
                if nodeX[i + 1] > colmax:
                    nodeX[i + 1] = colmax
                for pixelX in np.arange(nodeX[i], nodeX[i + 1]):
                    subgrid[int(ny - y) - rowmin, int(pixelX) - colmin] = 1
                    filled_cells += 1

    # sub-grid indices of non-zero values
    index_array = subgrid.nonzero()

    # if no intersections, there will be no rows in the index arrays,
    # then the full subgrid is considered to represent the polygon
    if index_array[0].shape[0] == 0:
        index_array = np.where(subgrid == 0)

    # grid indices for refined grid
    row_index = index_array[0] + rowmin
    col_index = index_array[1] + colmin

    # grid indices for target grid
    # integer division by number of subgridcells to convert indices to the
    # original grid
    row_index = np.floor_divide(row_index, subgridcells)
    col_index = np.floor_divide(col_index, subgridcells)

    # sum of pixel weights should be 1.0
    cdef double pixel_weight = 1 / index_array[0].shape[0]

    cdef int row
    cdef int col
    for row, col in zip(row_index, col_index):
        weights.setdefault((row, col), 0)
        weights[(row, col)] += pixel_weight
