import sys
from numpy import sin, cos, tan, sqrt, pi, arctan2, linspace, meshgrid
from scipy.optimize import root
import matplotlib.pyplot as plt
deg2rad = pi / 180


def theta_mach_2_beta(beta, theta, mach, gamma):
    res = abs(2 * (1 / tan(beta)) * ((mach * sin(beta)) ** 2 - 1) /
        ((mach ** 2) * (gamma + cos(2 * beta)) + 2) - tan(theta))
    return res


def numerator(beta, mach):
    mach_normal = mach * sin(beta)
    num = 2 * (1 / tan(beta)) * ((mach_normal) ** 2 - 1)
    return num


def denominator(beta, mach, gamma):
    den = (mach ** 2) * (gamma + cos(2 * beta)) + 2
    return den


def get_limit(beta_guess, mach, gamma):
    beta = root(denominator, beta_guess, args=(mach, gamma)).x[0]
    return beta


def get_theta(beta, mach, gamma):
    theta = arctan2(numerator(beta, mach), denominator(beta, mach, gamma))
    return theta


def get_beta_from_theta_mach(theta, mach, gamma):
	beta_initial_guess = 10 * deg2rad
	beta = root(theta_mach_2_beta, beta_initial_guess, args=(theta, mach, gamma)).x[0]
	return beta


def main(args):
    [beta, theta, mach, gamma] = args
    beta = theta_mach_2_beta(beta, theta, mach, gamma)
    print('beta: %.3f deg' % (beta / deg2rad))
    return beta


gamma = 1.4
b = linspace(pi / 2, 0, 20) / deg2rad
m = linspace(1.05, 15, 20)
bb, mm = meshgrid(b, m)
t = get_theta(bb, mm, gamma)
# h = plt.contourf(b, m , t)
h = plt.contour(bb, mm, t, 20, cmap='RdGy')
plt.show()


for b, t, m in zip(bb, t, mm):
    print('theta:%8.2f' % (t / deg2rad), '|', 'beta:%8.2f' % (b / deg2rad), '|', 'mach:%8.2f' % m)

if __name__ == '__main__':
    args = [9.5 * deg2rad, 5 * deg2rad, 8, 1.4]
    main(args)
