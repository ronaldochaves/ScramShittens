import sys
from numpy import sin, cos, tan, sqrt, pi, arctan2, linspace, meshgrid, random, where, inf
from scipy.optimize import root
import matplotlib as mpl
import matplotlib.pyplot as plt
from labellines import labelLine, labelLines

gamma = 1.4
deg2rad = pi / 180
mpl.rc('lines', linewidth=2, linestyle='-')


def theta_mach_2_beta(beta, theta, mach, gamma):
    res = abs(numerator(beta, mach) / denominator(beta, mach, gamma) - tan(theta))
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
    theta = arctan2(2 * sin(beta) ** 2, tan(beta) * (gamma + cos(2 * beta)))
    return theta


def get_beta_from_theta_mach(beta_guess, theta, mach, gamma):
    beta = root(theta_mach_2_beta, beta_guess,
                args=(theta, mach, gamma)).x[0]
    return beta


def plot_beta_theta_mach():    
    b = linspace(pi / 2, 0.1, 20)    
    m = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 2, 2.2, 2.5, 3, 4, 5, 6, 8, 15, inf]

    plt.figure()
    xvals = []
    for mach in m:
        if mach != inf:
            theta = get_theta(b, mach, gamma)
        else:
            theta = get_theta_mach_inf(b, gamma)
        theta = theta[where(theta > 0)] * 180 / pi
        beta = b[where(theta > 0)] * 180 / pi
        xvals.append(max(theta))
        plt.plot(theta, beta, color=random.rand(3,), label='%3.1f' % mach)
    labelLines(plt.gca().get_lines(), xvals=xvals, zorder=2.5, align=False)
    plt.xlabel(r'$\theta$ [deg]')
    plt.ylabel(r'$\beta$ [deg]')
    plt.grid()
    plt.show()


def main(args):
    [beta_guess, theta, mach, gamma] = args
    beta = get_beta_from_theta_mach(beta_guess, theta, mach, gamma)
    # beta = get_beta_from_theta_mach(beta_guess * deg2rad, theta * deg2rad, mach, gamma)
    print('beta: %.3f deg' % (beta / deg2rad))
    return beta


if __name__ == '__main__':
    args = [9.5 * deg2rad, 5 * deg2rad, 10, gamma]
    # args = [9.5, 5, 10, gamma]
    main(args)
    plot_beta_theta_mach()
