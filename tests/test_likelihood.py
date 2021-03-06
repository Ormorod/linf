"""
Test get_likelihood in two trivial cases simple enough to work out by hand.
"""
import numpy as np
from scipy.special import erf
from linf import LinfLikelihood
from linf.helper_functions import create_theta


def test_likelihood():
    """
    Test the likelihood function against a trivial case with just sigma_y.

    There are two datapoints at (0, 0) and (1, 1), and the interpolation function
    is a single straight line between the same two points. Sigma is set to 1.

    The value for the likelihood in this case should be -ln(2π).
    """
    x_min, x_max = 0, 1
    x_nodes = np.array([])
    y_nodes = np.array([0, 1])
    theta = create_theta(x_nodes, y_nodes)

    x_data = np.array([0, 1])
    y_data = np.array([0, 1])
    sigma = 1

    l = LinfLikelihood(x_min, x_max, x_data, y_data, sigma, adaptive=False)
    assert l(theta)[0] == -np.log(2 * np.pi)


def test_likelihood_sigma_x():
    """
    Test the likelihood function against a trivial case with sigma_x and sigma_y.

    There are two datapoints at (0, 0) and (1, 1), and the interpolation function
    is a single straight line between the same two points. Sigma is set to 1 for
    both x and y.

    The value for the likelihood in this case should be ln[(1/16π)(erf(1)-erf(0))(erf(0)-erf(-1))].
    """

    x_min, x_max = 0, 1
    x_nodes = np.array([])
    y_nodes = np.array([0, 1])
    theta = create_theta(x_nodes, y_nodes)

    x_data = np.array([0, 1])
    y_data = np.array([0, 1])
    sigma = np.array([1, 1])

    l = LinfLikelihood(x_min, x_max, x_data, y_data, sigma, adaptive=False)
    assert np.isclose(
        l(theta)[0], np.log((erf(1) - erf(0)) * (erf(0) - erf(-1)) / (16 * np.pi))
    )
