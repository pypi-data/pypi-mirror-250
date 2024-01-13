import math

import numpy as np
import pytest

from rastafari import WeightsDict, ddaf_line_subpixel, even_odd_polygon_fill


def assert_weights(weights: WeightsDict, true_weights: WeightsDict) -> None:
    # compare calculated weights for each cell with true weights
    for cell in true_weights:
        assert cell in weights, f"missing cell {cell} in weights"
        assert weights[cell] == pytest.approx(true_weights[cell], 1e-4)


def test_ddaf_line_subpixel() -> None:
    # upper right quadrant, within grid extent
    weights: WeightsDict = {}
    x0, y0, x1, y1 = (2.0, 2.0, 6.0, 6.0)
    length = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    extent = (0.0, 0.0, 10.0, 10.0)
    ddaf_line_subpixel(x0, y0, x1, y1, weights, length, extent, 1.0, 1.0)
    true_weights = {(7, 2): 0.25, (6, 3): 0.25, (5, 4): 0.25, (4, 5): 0.25}

    assert_weights(weights, true_weights)

    # lower left quadrant, within grid extent
    weights = {}
    x0, y0, x1, y1 = (6, 6, 2, 2)
    length = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    extent = (0, 0, 10, 10)
    ddaf_line_subpixel(x0, y0, x1, y1, weights, length, extent, 1, 1)
    true_weights = {(7, 2): 0.25, (6, 3): 0.25, (5, 4): 0.25, (4, 5): 0.25}

    assert_weights(weights, true_weights)

    # lower left quadrant, within grid extent
    weights = {}
    x0, y0, x1, y1 = (-3, 3, -5, 4)
    length = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    extent = (-5, -5, 5, 5)
    ddaf_line_subpixel(x0, y0, x1, y1, weights, length, extent, 1, 1)
    true_weights = {(1, 0): 0.5, (1, 1): 0.5, (2, 2): 0.0}

    assert_weights(weights, true_weights)

    # completely outside grid extent
    weights = {}
    x0, y0, x1, y1 = (-3, 3, -5, 4)
    length = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    extent = (1000, 1000, 100000, 10000)
    ddaf_line_subpixel(x0, y0, x1, y1, weights, length, extent, 1, 1)
    assert len(weights) == 0


def test_ddaf_line_subpixel_diagonal() -> None:
    # diagonal line, two crossings
    weights: WeightsDict = {}
    x0, y0, x1, y1 = (0.25, 0.75, 1.25, 1.75)
    length = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    extent = (0, 0, 2, 2)
    ddaf_line_subpixel(x0, y0, x1, y1, weights, length, extent, 1, 1)
    assert_weights(weights, {(0, 0): 0.5, (1, 0): 0.25, (0, 1): 0.25})
    assert sum(weights.values()) == pytest.approx(1.0, 1e-6)


def test_ddaf_line_subpixel_contained() -> None:
    # diagonal line, no crossings
    weights: WeightsDict = {}
    x0, y0, x1, y1 = (1.1, 1.1, 1.9, 1.9)
    length = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    extent = (0, 0, 5, 5)
    ddaf_line_subpixel(x0, y0, x1, y1, weights, length, extent, 1, 1)
    assert weights == {(3, 1): 1}
    assert sum(weights.values()) == pytest.approx(1.0, 1e-6)

    # vertical line, no crossings
    weights = {}
    x0, y0, x1, y1 = (1.1, 1.1, 1.1, 1.9)
    length = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    extent = (0, 0, 5, 5)
    ddaf_line_subpixel(x0, y0, x1, y1, weights, length, extent, 1, 1)
    assert weights == {(3, 1): 1}
    assert sum(weights.values()) == pytest.approx(1.0, 1e-6)

    # horizontal line, no crossings
    weights = {}
    x0, y0, x1, y1 = (1.1, 1.1, 1.9, 1.1)
    length = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    extent = (0, 0, 5, 5)
    ddaf_line_subpixel(x0, y0, x1, y1, weights, length, extent, 1, 1)
    assert weights == {(3, 1): 1}
    assert sum(weights.values()) == pytest.approx(1.0, 1e-6)


def test_ddaf_resolution_non_uniform() -> None:
    # horizontal line, no crossings
    weights: WeightsDict = {}
    x0, y0, x1, y1 = (5, 7, 15, 7)
    length = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    extent = (0, 0, 20, 25)
    ddaf_line_subpixel(x0, y0, x1, y1, weights, length, extent, 2, 5)
    assert weights == {
        (3, 2): 0.1,
        (3, 3): 0.2,
        (3, 4): 0.2,
        (3, 5): 0.2,
        (3, 6): 0.2,
        (3, 7): 0.1,
    }
    assert sum(weights.values()) == pytest.approx(1.0, 1e-6)


def test_ddaf_line_subpixel_vertical() -> None:
    # vertical line, 3 crossings
    weights: WeightsDict = {}
    x0, y0, x1, y1 = (1.5, 1.5, 1.5, 3.9)
    length = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    extent = (0, 0, 5, 5)
    ddaf_line_subpixel(x0, y0, x1, y1, weights, length, extent, 1, 1)
    assert weights == {(3, 1): 0.5 / 2.4, (2, 1): 1 / 2.4, (1, 1): 0.9 / 2.4}
    assert sum(weights.values()) == pytest.approx(1.0, 1e-6)

    # vertical line, 1 y-crossing
    weights = {}
    x0, y0, x1, y1 = (1.5, 1.5, 1.5, 2.5)
    length = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    extent = (0, 0, 5, 5)
    ddaf_line_subpixel(x0, y0, x1, y1, weights, length, extent, 1, 1)
    assert weights == {(3, 1): 0.5, (2, 1): 0.5}
    assert sum(weights.values()) == pytest.approx(1.0, 1e-6)

    # vertical line, no crossings
    weights = {}
    x0, y0, x1, y1 = (1.5, 1.5, 1.5, 1.9)
    length = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    extent = (0, 0, 5, 5)
    ddaf_line_subpixel(x0, y0, x1, y1, weights, length, extent, 1, 1)
    assert weights == {(3, 1): 1}
    assert sum(weights.values()) == pytest.approx(1.0, 1e-6)


def test_ddaf_multiple_lines() -> None:
    # two lines, one crossing
    weights: WeightsDict = {}
    x0, y0, x1, y1, x2, y2 = (1.5, 1.3, 1.5, 1.8, 2.5, 1.8)
    length = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2) + math.sqrt(
        (x2 - x1) ** 2 + (y2 - y1) ** 2
    )
    extent = (0, 0, 5, 5)
    assert length == 1.5
    ddaf_line_subpixel(x0, y0, x1, y1, weights, length, extent, 1, 1)
    assert weights == {(3, 1): 0.5 / 1.5}
    ddaf_line_subpixel(x1, y1, x2, y2, weights, length, extent, 1, 1)
    assert weights == {(3, 1): 1 / 1.5, (3, 2): 0.5 / 1.5}
    assert sum(weights.values()) == pytest.approx(1.0, 1e-6)


def test_ddaf_multiple_lines_two_crossings() -> None:
    # vertical + diagonal line, two crossings
    weights: WeightsDict = {}
    x0, y0, x1, y1, x2, y2 = (0.25, 0.25, 0.25, 0.75, 1.25, 1.75)
    length = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2) + math.sqrt(
        (x2 - x1) ** 2 + (y2 - y1) ** 2
    )
    extent = (0, 0, 2, 2)
    ddaf_line_subpixel(x0, y0, x1, y1, weights, length, extent, 1, 1)
    assert weights == {(1, 0): 0.5 / length}
    ddaf_line_subpixel(x1, y1, x2, y2, weights, length, extent, 1, 1)
    assert_weights(
        weights,
        {
            (0, 0): 0.5 * math.sqrt(2) / length,
            (1, 0): (0.25 * math.sqrt(2) + 0.5) / length,
            (0, 1): 0.25 * math.sqrt(2) / length,
        },
    )
    assert sum(weights.values()) == pytest.approx(1.0, 1e-6)


def test_ddaf_multiple_lines_no_crossings() -> None:
    # vertical + horizontal line, no crossings
    weights: WeightsDict = {}
    x0, y0, x1, y1, x2, y2 = (0.25, 0.25, 0.25, 0.75, 0.75, 0.75)
    length = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2) + math.sqrt(
        (x2 - x1) ** 2 + (y2 - y1) ** 2
    )
    extent = (0, 0, 2, 2)
    ddaf_line_subpixel(x0, y0, x1, y1, weights, length, extent, 1, 1)
    assert weights == {(1, 0): 0.5 / length}
    ddaf_line_subpixel(x1, y1, x2, y2, weights, length, extent, 1, 1)
    assert weights == {(1, 0): 1 / length}
    assert sum(weights.values()) == pytest.approx(1.0, 1e-6)


def test_even_odd_polygon_fill() -> None:
    """Test rasterizing different polygons."""

    nodes = np.array([(1.5, 1.0), (4.0, 1.0), (4.0, 4.0), (2.5, 3.0), (1.5, 1.0)])

    # simple polygon without subgrid refinement
    weights: WeightsDict = {}
    extent = (0, 0, 10, 10)
    nx = 10
    ny = 10
    even_odd_polygon_fill(nodes, weights, extent, nx, ny, subgridcells=1)
    true_weights = {
        (8, 1): 1 / 6,
        (7, 2): 1 / 6,
        (8, 2): 1 / 6,
        (6, 3): 1 / 6,
        (7, 3): 1 / 6,
        (8, 3): 1 / 6,
    }

    assert_weights(weights, true_weights)

    # simple polygon with subgrid refinement
    weights = {}
    extent = (0, 0, 10, 10)
    nx = 10
    ny = 10
    even_odd_polygon_fill(nodes, weights, extent, nx, ny, subgridcells=2)
    true_weights = {
        (6, 3): 0.1363636,
        (7, 3): 0.18181818,
        (8, 3): 0.18181818,
        (6, 2): 0.04545454,
        (8, 2): 0.18181818,
        (8, 1): 0.0909090,
        (7, 2): 0.181818,
    }

    assert_weights(weights, true_weights)

    # complex polygon without subgrid refinement
    nodes2 = np.array(
        [
            (1.5, 1.0),
            (2.5, 5.5),
            (3.5, 1.0),
            (5.0, 6.5),
            (7.0, 0.0),
            (1.5, 1.0),
        ]
    )

    weights = {}
    extent = (0, 0, 10, 10)
    nx = 10
    ny = 10

    even_odd_polygon_fill(nodes2, weights, extent, nx, ny, subgridcells=1)

    true_weights = {
        (6, 4): 0.05,
        (5, 4): 0.05,
        (4, 4): 0.05,
        (5, 5): 0.05,
        (7, 3): 0.05,
        (8, 1): 0.05,
        (8, 5): 0.05,
        (7, 5): 0.05,
        (7, 1): 0.05,
        (8, 3): 0.05,
        (7, 4): 0.05,
        (6, 2): 0.05,
        (6, 5): 0.05,
        (9, 4): 0.05,
        (9, 6): 0.05,
        (9, 5): 0.05,
        (8, 4): 0.05,
        (5, 2): 0.05,
        (7, 2): 0.05,
        (8, 2): 0.05,
    }

    assert_weights(weights, true_weights)
