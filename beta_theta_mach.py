import sys
from numpy import sin, cos, tan, sqrt, pi, arctan2, linspace, meshgrid, random, where, inf
from scipy.optimize import root
import matplotlib as mpl
import matplotlib.pyplot as plt
from labellines import labelLine, labelLines

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


def get_theta_mach_inf(beta, gamma):
    theta = arctan2(2 * sin (beta) ** 2, tan(beta) * (gamma + cos(2 * beta)))
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

mpl.rc('lines', linewidth=2, linestyle='-')
gamma = 1.4
b = linspace(pi / 2, 0, 20)
m = linspace(1.05, 15, 10)
bb, mm = meshgrid(b, m)
t = get_theta(bb, mm, gamma)
# # h = plt.contourf(b, m , t)
# h = plt.contour(bb, mm, t, 20, cmap='RdGy')
# plt.colorbar()
# plt.xlabel(r'$\beta$')
# plt.ylabel(r'M')
# plt.show()

m = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 2, 2.25, 2.5, 3, 4, 5, 6, 8, 10, 15, inf]
# m = [2, 3, 4, 6]

plt.figure()
xvals = []
for mach in m:
    if mach != inf:
        theta = get_theta(b, mach, gamma)
    else:
        theta = get_theta_mach_inf(b, gamma)
    theta = theta[where(theta > 0)] * 180 / pi
    beta = b[where(theta > 0)] * 180 / pi
    xvals.append((beta[0] + beta[-1])/2)
    plt.plot(beta, theta, color=random.rand(3,), label='%3.2f' % mach)
labelLines(plt.gca().get_lines(), xvals=xvals, zorder=2.5)
plt.xlabel(r'$\beta$ [deg]')
plt.ylabel(r'$\theta$ [deg]')
# plt.legend(loc='best')
plt.grid()
plt.show()

# for b, t, m in zip(bb, t, mm):
#     print('theta:%8.2f' % (t / deg2rad), '|', 'beta:%8.2f' % (b / deg2rad), '|', 'mach:%8.2f' % m)

if __name__ == '__main__':
    args = [9.5 * deg2rad, 5 * deg2rad, 8, 1.4]
    main(args)
