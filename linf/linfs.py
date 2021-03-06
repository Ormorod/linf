"""
Linear INterpolation Functions.

theta refers to the full set of parameters for an adaptive linear interpolation model,
[n, y0, x1, y1, x2, y2, ..., x_n, y_n, y_n+1],
where n is the greatest allowed value of ceil(n).

The reason for the interleaving of x and y is it avoids the need to know n.
"""
import numpy as np

from linf.helper_functions import (
    get_theta_n,
    get_x_nodes_from_theta,
    get_y_nodes_from_theta,
)


class Linf:
    """
    linf with end nodes at x_min and x_max.

    x_min: float
    x_max: float > x_min

    Returns:
    linf(x, theta)

    theta in format [y0, x1, y1, x2, y2, ..., x_(N-2), y_(N-2), y_(N-1)] for N nodes.
    """

    def __init__(self, x_min, x_max):
        self.x_min = x_min
        self.x_max = x_max

    def __call__(self, x, theta):
        """
        linf with end nodes at x_min and x_max

        theta = [y0, x1, y1, x2, y2, ..., x_(N-2), y_(N-2), y_(N-1)] for N nodes.

        y0 and y_(N-1) are the y values corresponding to x_min and x_max respecively.

        If theta only contains a single element, the linf is constant at that value.
        If theta is empty, the linf if comstant at -1 (cosmology!)
        """
        if 0 == len(theta):
            return np.full_like(x, -1)
        if 1 == len(theta):
            return np.full_like(x, theta[-1])
        return np.interp(
            x,
            np.concatenate(
                (
                    [self.x_min],
                    get_x_nodes_from_theta(theta, adaptive=False),
                    [self.x_max],
                )
            ),
            get_y_nodes_from_theta(theta, adaptive=False),
        )


class AdaptiveLinf(Linf):
    """
    Adaptive linf which allows the number of parameters being used to vary.

    x_min: float
    x_max: float > x_min

    Returns:
    adaptive_linf(x, theta)

    The first element of theta is N; floor(N)-2 is number of interior nodes used in
    the linear interpolation model.

    theta = [N, y0, x1, y1, x2, y2, ..., x_(Nmax-2), y_(Nmax-2), y_(Nmax-1)],
    where Nmax is the greatest allowed value of floor(N).

    if floor(N) = 1, the linf is constant at theta[-1] = y_(Nmax-1).
    if floor(N) = 0, the linf is constant at -1 (cosmology!)
    """

    def __call__(self, x, theta):
        """
        The first element of theta is N; floor(N)-2 is number of interior nodes used in
        the linear interpolation model. This is then used to select the
        appropriate other elements of params to pass to linf()

        theta = [N, y0, x1, y1, x2, y2, ..., x_(Nmax-2), y_(Nmax-2), y_(Nmax-1)],
        where Nmax is the greatest allowed value of floor(N).

        if floor(N) = 1, the linf is constant at theta[-1] = y_(Nmax-1).
        if floor(N) = 0, the linf is constant at -1 (cosmology!)
        """
        return super().__call__(x, get_theta_n(theta))
