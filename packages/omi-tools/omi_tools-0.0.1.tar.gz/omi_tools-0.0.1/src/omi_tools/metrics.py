import numpy as np
from scipy.stats import norm


def u(kriging_mean: np.array,
      kriging_std: np.array,
      current_max: float):
    """Calculate scaled position of the Kriging mean on a given position related to the current
    maximum

    Args:
        kriging_mean (list): Kriging mean for all inputs in X
        kriging_std (list): Kriging standard deviation for all inputs in X
        current_max (float): Current maximum of the objective function

    Returns:
        float: scaled position of Kriging mean on all considered x
    """

    u_x = (kriging_mean - current_max) / kriging_std

    return u_x


def expected_improvement(kriging_mean: np.array,
                         kriging_std: np.array,
                         current_max: float):
    """Calculate potential to improve the current maximum on all considered inputs

    Args:
        kriging_mean (list): Kriging mean for all inputs in X
        kriging_std (list): Kriging standard deviation for all inputs in X
        current_max (float): Current maximum of the objective function

    Returns:
        int: scaled position of Kriging mean on all considered x
    """

    u_x = u(kriging_mean, kriging_std, current_max)
    ei_x = kriging_std * (u_x * norm.cdf(u_x) + norm.pdf(u_x))

    return ei_x

def mae(y: np.array,
        kriging_mean: np.array,
        x_lim: np.array,
        x_nbr: np.array):
    """mean absolute error metric"""

    return abs(y - kriging_mean).sum() * (x_lim[1] - x_lim[0]) / x_nbr


def rmse(y: np.array,
         kriging_mean: np.array,
         x_lim: np.array,
         x_nbr: np.array):
    """root mean squared error metric"""

    return (((y - kriging_mean) ** 2).sum() * (x_lim[1] - x_lim[0]) / x_nbr) ** 0.5
