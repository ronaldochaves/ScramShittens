from numpy import sin, cos, tan, sqrt, pi

from beta_theta_mach import get_beta_from_theta_mach

deg2rad = pi / 180


def oblique_shock(theta, mach_before, pressure_before, temperature_before, gamma):
    beta_guess = 10 * deg2rad
    beta = get_beta_from_theta_mach(beta_guess, theta, mach_before, gamma)
    mach_after = get_mach_after_oblique_shock(mach_before, theta, beta, gamma)
    pressure_after = get_pressure_after_oblique_shock(mach_before, pressure_before, beta, gamma)
    temperature_after = get_temperature_after_oblique_shock(mach_before, pressure_before, beta, gamma, temperature_before)
    return mach_after, pressure_after, temperature_after, beta


def get_pressure_after_oblique_shock(mach_before, pressure_before, beta, gamma):
    pressure_after = pressure_before * \
        (1 + (2 * gamma / (gamma + 1)) * ((mach_before * sin(beta)) ** 2 - 1))
    return pressure_after


def get_temperature_after_oblique_shock(mach_before, pressure_before, beta, gamma, temperature_before):
    pressure_after = get_pressure_after_oblique_shock(mach_before, pressure_before, beta, gamma)
    temperature_after = temperature_before * (pressure_after / pressure_before) * \
        ((2 + (gamma - 1) * (mach_before * sin(beta)) ** 2) /
         ((gamma + 1) * (mach_before * sin(beta)) ** 2))
    return temperature_after


def get_mach_after_oblique_shock(mach_before, theta, beta, gamma):
    mach_after = (1 / sin(beta - theta)) * sqrt((1 + ((gamma - 1) / 2) * (mach_before * sin(beta)) ** 2) /
                                                (gamma * (mach_before * sin(beta)) ** 2 - (gamma - 1) / 2))
    return mach_after


def main(theta, mach, alt):
    temperature = 227
    pressure = 1172
    gamma = 1.4

    mach_2, p_2, t_2, beta = oblique_shock(theta, mach, pressure, temperature, gamma)

    print('Before oblique shock wave')
    print('mach: %.3f' % mach)
    print('theta: %.3f deg' % (theta / deg2rad))
    print('pres: %.3f kPa' % (pressure / 1e3))
    print('temp: %.3f K' % temperature)
    print('')
    print('After oblique shock wave')
    print('beta: %.3f deg' % (beta / deg2rad))
    print('mach: %.3f' % mach_2)
    print('pres: %.3f kPa' % (p_2 / 1e3))
    print('temp: %.3f K' % t_2)


if __name__ == '__main__':
    mach_1 = 10
    theta = 5 * deg2rad
    alt = 30000
    main(theta, mach_1, alt)
