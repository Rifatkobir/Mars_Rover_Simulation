# =================================
# MARS ROVER - BOUNDARY FUNCTIONS
# =================================

GRID_SIZE = 5


def is_inside_boundary(x, y):
    """
    Check whether the rover is inside the grid.
    """

    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
        return True
    else:
        return False