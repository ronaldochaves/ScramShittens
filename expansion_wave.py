from numpy import sqrt, arcsin, arctan, pi

deg2rad = pi / 180


def pradtl_meyer(mach, gamma):
	G = (gamma + 1) / (gamma - 1)
	nu = sqrt(G) * arctan(sqrt((mach ** 2 - 1) / G)) - arctan(sqrt(mach ** 2 - 1))
	return nu


def expansion_wave_angle(mach):
	mu = arcsin(1 / mach)
	return mu


def total_pressure(mach, gamma, pressure):
	pressure_total = pressure * (1 + ((gamma - 1) / 2) * mach ** 2) ** (gamma / (gamma - 1))
	return pressure_total


def get_pressure_after_from_total_before(mach_after, gamma, pressure_total_before):
	pressure_after = pressure_total_before * (1 + ((gamma - 1) / 2) * mach_after ** 2) ** (gamma / (1 - gamma))
	return pressure_after


def expansion(args):
	[mach_before, mach_after, pressure_before, gamma] = args
	mu_before = expansion_wave_angle(mach_before)
	nu_before = pradtl_meyer(mach_before, gamma)
	theta_after = pradtl_meyer(mach_after, gamma) - nu_before 
	mu_after = expansion_wave_angle(mach_after)
	pressure_total_before = total_pressure(mach_before, gamma, pressure_before)
	pressure_after = get_pressure_after_from_total_before(mach_after, gamma, pressure_total_before)
	return pressure_after, mu_before, mu_after


def main(args):
	pressure_after, mu_before, mu_after = expansion(args)
	print('pressure_after: %.3f kPa' % (pressure_after / 1e3))
	print('mu_after: %.3f deg' % (mu_after / deg2rad))


if __name__ == '__main__':
    args = [7, 5, 1200, 1.4]
    main(args)
