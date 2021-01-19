from numpy import pi, sqrt, array
from ISA import atmosphere_setup, get_temperature, get_pressure, sound_speed, density
from oblique_shock import oblique_shock
from combustion import combustion
from expansion_wave import expansion
from area_ratio_expansion import area_ratio

# Inputs
gamma = 1.4
Cp = 1084
combustor_length = 9.5
combustor_height = 0.6
A = combustor_height * combustor_length
LHV = 120e6
molar_mass = 28.96442
R_universal = 8314.32
width = 0.5
h = 2.2
R = R_universal / molar_mass


def preliminary_design(altitude, thetas, velocity, mach_exit_combustion):
	# Atmosphere / Free stream
	atmosphere_setup()
	T1 = get_temperature(altitude)
	p1 = get_pressure(altitude)
	a1 = sound_speed(gamma, R, T1)
	rho1 = density(T1, p1, R)
	u1 = velocity
	mach1 = u1 / a1
	print('** Free Stream **')
	print('Altitude: %.3f km' % (altitude / 1e3))
	print('mach1: %.3f' % mach1, 'a1: %.3f m/s' % a1, 'u1: %.3f m/s' % u1)
	print('p1: %.3f kPa' % (p1 / 1e3), 'T1: %.3f K' % T1, 'rho1: %.3f kg/m^3' % rho1)

	# 1st shock wave - external
	A1 = width * h
	theta1 = thetas[0]
	mach2, p2, T2, beta1 = oblique_shock(theta1, mach1, p1, T1, gamma)
	rho2 = density(T2, p2, R)
	a2 = sound_speed(gamma, R, T2)
	u2 = a2 * mach2
	print('')
	print('** After shock wave 1 - external compression **')
	print('mach2: %.3f' % mach2, 'a2: %.3f m/s' % a2, 'u2: %.3f m/s' % u2)
	print('p2: %.3f kPa' % (p2 / 1e3), 'T2: %.3f K' % T2, 'rho2: %.3f kg/m^3' % rho2)
	print('theta1: %.3f deg' % (theta1 * 180 / pi), 'beta1: %.3f deg' % (beta1 * 180 / pi))

	# 2nd shock wave - external
	theta2 = thetas[1]
	mach3, p3, T3, beta2 = oblique_shock(theta2, mach2, p2, T2, gamma)
	rho3 = density(T3, p3, R)
	a3 = sound_speed(gamma, R, T3)
	u3 = a3 * mach3
	print('')
	print('** After shock wave 2 - external compression **')
	print('mach3: %.3f' % mach3, 'a3: %.3f m/s' % a3, 'u3: %.3f m/s' % u3)
	print('p3: %.3f kPa' % (p3 / 1e3), 'T3: %.3f K' % T3, 'rho3: %.3f kg/m^3' % rho3)
	print('theta2: %.3f deg' % (theta2 * 180 / pi), 'beta2: %.3f deg' % (beta2 * 180 / pi))

	# 3rd shock wave - internal
	theta3 = thetas[2]
	mach4, p4, T4, beta3 = oblique_shock(theta3, mach3, p3, T3, gamma)
	rho4 = density(T4, p4, R)
	a4 = sound_speed(gamma, R, T4)
	u4 = a4 * mach4
	print('')
	print('** After shock wave 3 - external compression **')
	print('mach4: %.3f' % mach4, 'a4: %.3f m/s' % a4, 'u4: %.3f m/s' % u4)
	print('p4: %.3f kPa' % (p4 / 1e3), 'T4: %.3f K' % T4, 'rho4: %.3f kg/m^3' % rho4)
	print('theta3: %.3f deg' % (theta3 * 180 / pi), 'beta3: %.3f deg' % (beta3 * 180 / pi))
	
	# 4th shock wave
	theta4 = thetas[3]
	mach5, p5, T5, beta4 = oblique_shock(theta4, mach4, p4, T4, gamma)
	rho5 = density(T5, p5, R)
	a5 = sound_speed(gamma, R, T5)
	u5 = a5 * mach5
	print('')
	print('** After shock wave 4 - shock on lip/ on corner - internal compression **')
	print('mach5: %.3f' % mach5, 'a5: %.3f m/s' % a5, 'u5: %.3f m/s' % u5)
	print('p5: %.3f kPa' % (p5 / 1e3), 'T5: %.3f K' % T5, 'rho4: %.3f kg/m^3' % rho5)
	print('theta4: %.3f deg' % (theta4 * 180 / pi), 'beta4: %.3f deg' % (beta4 * 180 / pi))
	To5 = T5 * (1 + ((gamma - 1) / 2) * (mach5 ** 2))
	A5 = rho1 * u1 * A1 / (rho5 * u5)
	mass_flow5 = p5 * A5 * mach5 * sqrt(gamma / (R * T5))

	# Combustion
	mach6 = mach_exit_combustion
	mass_flow6, To6 = combustion([To5, mach5, mach6, gamma, Cp, mass_flow5])
	T6 = To6 / ((1 - (gamma - 1) / 2) * (mach6 ** 2))
	a6 = sound_speed(gamma, R, T6)
	u6 = a6 * mach6
	p6 = mass_flow6 / (A * mach6 * sqrt(gamma / (R * T6)))
	po6 = p6 * (1 + ((gamma - 1) / 2) * mach6 ** 2)
	rho6 = density(T6, p6, R)
	print('')
	print('** After combustion chamber **')
	print('Combustor area: %.3f' % A5)
	print('mach6: %.3f' % mach6, 'a6: %.3f m/s' % a6, 'u6: %.3f m/s' % u6)
	print('p6: %.3f kPa' % (p6 / 1e3), 'T6: %.3f K' % T6, 'rho6: %.3f kg/m^3' % rho6)

	# Expansion
	mach7 = 3.37
	p7, mu6, mu7 = expansion([mach6, mach7, p6, gamma])
	T7 = To6 / ((1 - (gamma - 1) / 2) * (mach7 ** 2))
	a7 = sound_speed(gamma, R, T7)
	u7 = a7 * mach7
	rho7 = density(T7, p7, R)
	print('')
	print('** After expansion wave **')
	print('mach7: %.3f' % mach7, 'a7: %.3f m/s' % a7, 'u7: %.3f m/s' % u7)
	print('p7: %.3f kPa' % (p7 / 1e3), 'T7: %.3f K' % T7, 'rho7: %.3f kg/m^3' % rho7)
	print('mu6: %.3f deg' % (mu6 * 180 / pi), 'mu7: %.3f deg' % (mu7 * 180 / pi))


if __name__ == '__main__':
	altitude = 20000
	thetas = array([7.5, 8.6, 10.3, 4.27]) * pi / 180
	velocity = 1710
	mach_exit_combustion = 2.2
	preliminary_design(altitude, thetas, velocity, mach_exit_combustion)
