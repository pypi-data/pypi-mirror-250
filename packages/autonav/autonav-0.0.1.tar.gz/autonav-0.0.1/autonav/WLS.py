"""This module contains the WLS algorithm."""
import cmath
import itertools
import math

from autonav.random_generator import randomGenerator
from autonav.velocity import _velocity
from numpy import array, asarray, cos, dot, eye, float32, median, sin, sqrt
from numpy.lib import scimath
from numpy.linalg import norm, solve
from numpy.typing import NDArray


def wls(
    a_i: NDArray, n: int, k: int, sigma: float, destinations: NDArray, initial_uav_position: list, noise_seed=0
) -> NDArray:
    """This function executes the WLS algorithm.

    Args:
        a_i (NDArray): The true position of the anchors in 3D.
        n (int): The number of anchors.
        k (int): The number of measurements.
        sigma (float): The noise level in meters.
        destinations (NDArray): The intermediate points need for navigation in 3D.
        initial_uav_position (list): The initial UAV position in 3D.
        noise_seed (int): The seed to generate the noise.

    Returns:
        The estimated trajectory computed using the WLS algorithm for the given input scenario
        and the true trajectory that the UAV followed.
    """
    x_true = initial_uav_position[:]
    ww = 0
    n_dest = len(destinations) - 1
    estimated_trajectory = []
    true_trajectory = []
    while ww <= n_dest:
        distance = math.sqrt(
            (x_true[0] - destinations[ww][0]) ** 2
            + (x_true[1] - destinations[ww][1]) ** 2
            + (x_true[2] - destinations[ww][2]) ** 2
        )
        while distance > 1:
            x = x_true[0:3]
            # ---------------------------------------------------------------------
            # Simulation part
            # ---------------------------------------------------------------------
            di_k = sqrt(((x[0] - a_i[0, :]) ** 2) + ((x[1] - a_i[1, :]) ** 2) + ((x[2] - a_i[2, :]) ** 2))
            di_k = array([di_k]).T
            # di_k = di_k + (sigma * randn(n, k))
            noise_seed += 1  # I need to change the seed in each iteration, otherwise does not work.
            di_k = di_k + (sigma * randomGenerator(n, k, noise_seed))
            d_i = median(di_k, axis=1)
            d_i = array([d_i]).T
            # ---------------------------------------------------------------------
            # Estimation part
            # ---------------------------------------------------------------------
            xi_est = []
            phi_i = []
            alpha_i = []
            for ii in range(0, n):
                a2 = []
                b2 = []
                kk = [ii + 1]
                for jj in range(0, n):
                    total = 0
                    if a_i[0, ii] == a_i[0, jj]:
                        total += 1
                    if a_i[1, ii] == a_i[1, jj]:
                        total += 1
                    if ii != jj and total > 0:
                        kk.append(jj + 1)
                for uu in range(0, len(array(list(itertools.combinations(kk, 2))))):
                    combinations = array(list(itertools.combinations(kk, 2)))
                    gg = combinations[uu, 0]
                    hh = combinations[uu, 1]
                    a2.append(2 * (a_i[0:3, gg - 1] - a_i[0:3, hh - 1]).T)
                    b2.append(
                        d_i[hh - 1] ** 2 - d_i[gg - 1] ** 2 - norm(a_i[0:3, hh - 1]) ** 2 + norm(a_i[0:3, gg - 1]) ** 2
                    )
                a2 = asarray(a2, dtype=float32)
                b2 = asarray(b2, dtype=float32)
                xi_est.append(solve(dot(a2.T, a2) + (1 * 10 ** (-6)) * eye(3), dot(a2.T, b2)))
                di_xy = norm(xi_est[0][0:2])
                xi_est[ii][2] = (
                    cmath.sqrt((d_i[0] ** 2)[0] - (di_xy**2)).real + cmath.sqrt((d_i[0] ** 2)[0] - (di_xy**2)).imag
                )
                phi_i.append(
                    math.atan2((xi_est[ii][1] - a_i[1, ii])[0], (xi_est[ii][0] - a_i[0, ii])[0]) * 180 / math.pi
                )
                alpha_i.append(
                    math.acos((xi_est[ii][2] - a_i[2, ii])[0] / (norm(xi_est[:][ii] - a_i[:, ii].reshape(len(a_i), 1))))
                    * 180
                    / math.pi
                )
            phi_i = asarray(phi_i, dtype=float32)
            alpha_i = asarray(alpha_i, dtype=float32)
            u_i_1 = cos(phi_i * math.pi / 180).T
            u_i_2 = sin(alpha_i * math.pi / 180).T
            u_i_3 = sin(phi_i * math.pi / 180).T
            u_i_4 = cos(alpha_i * math.pi / 180).T
            u_i = array([[u_i_1 * u_i_2], [u_i_3 * u_i_2], [u_i_4]], dtype=float32).reshape(3, n)
            a = asarray(u_i.T, dtype=float32)
            b = d_i + sum(u_i * a_i).T.reshape(n, 1)
            w_i = asarray((1 / d_i) / (sum(1 / d_i)))
            w = asarray(eye(n) * scimath.sqrt(w_i))
            x_est = asarray(solve(dot(dot(a.T, w.T), dot(w, a)), dot(dot(a.T, w.T), dot(w, b))).real)
            estimated_trajectory.append(x_est[:, 0])
            true_trajectory.append(x_true[:])
            uav_velocity = _velocity(x_est[:, 0], destinations[ww, :])
            x_true[0] = x_true[0] + uav_velocity[0]
            x_true[1] = x_true[1] + uav_velocity[1]
            x_true[2] = x_true[2] + uav_velocity[2]
            distance = math.sqrt(
                (x_true[0] - destinations[ww][0]) ** 2
                + (x_true[1] - destinations[ww][1]) ** 2
                + (x_true[2] - destinations[ww][2]) ** 2
            )
        ww += 1
    return array([array(estimated_trajectory), array(true_trajectory)])
