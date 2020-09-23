# Standard imports
# import math

# PyPI imports
from numpy import sin, cos, tan, sqrt, pi
from scipy.optimize import root

# Globals
deg2rad = pi / 180


def oblique_shock(theta, mach_before, pressure_before, temperature_before, gamma):
    beta_initial_guess = 10 * deg2rad
    beta_1 = root(theta_mach_2_beta, beta_initial_guess, args=(theta, mach_before, gamma)).x[0]
    mach_after = (1 / sin(beta_1 - theta)) * sqrt((1 + ((gamma - 1) / 2) * (mach_before * sin(beta_1)) ** 2) /
                                                  (gamma * (mach_before * sin(beta_1)) ** 2 - (gamma - 1) / 2))
    pressure_after = pressure_before * (1 + (2 * gamma / (gamma + 1)) * ((mach_before * sin(beta_1)) ** 2 - 1))
    temperature_after = temperature_before * (pressure_after / pressure_before) * \
                        ((2 + (gamma - 1) * (mach_before * sin(beta_1)) ** 2) /
                         ((gamma + 1) * (mach_before * sin(beta_1)) ** 2))
    return mach_after, pressure_after, temperature_after, beta_1


def theta_mach_2_beta(beta, theta, mach, gamma):
    res = 2 * (1 / tan(beta)) * ((mach * sin(beta)) ** 2 - 1) / ((mach ** 2) * (gamma + cos(2 * beta)) + 2) - theta
    return res


def main(mach, theta, alt):
    t = 227
    p = 1172
    gamma = 1.4

    mach_2, p_2, t_2, beta_1 = oblique_shock(theta, mach, p, t, gamma)

    print('Before oblique shock wave')
    print('mach: %.3f' % mach)
    print('pres: %.3f kPa' % (p / 1e3))
    print('temp: %.3f K' % t)
    print('theta: %.3f deg' % (theta / deg2rad))
    print('')
    print('After oblique shock wave')
    print('mach: %.3f' % mach_2)
    print('pres: %.3f kPa' % (p_2 / 1e3))
    print('temp: %.3f K' % t_2)
    print('beta: %.3f deg' % (beta_1 / deg2rad))


if __name__ == '__main__':
    mach_1 = 10
    theta = 5 * deg2rad
    alt = 30000
    main(mach_1, theta, alt)
