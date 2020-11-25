from numpy import pi
from ISA import atmosphere_setup, get_temperature, get_pressure
from oblique_shock import oblique_shock
from combustion import combustion

# Inputs
mach1 = 10
mach4 = 5
theta1 = 5 * pi / 180
theta2 = 5 * pi / 180
theta5 = 11 * pi / 180
h = 30000
gamma = 1.4
Cp = 1084
combustor_length = 9.5
combustor_height = 0.6
A = combustor_height * combustor_length
LHV = 120e6
molar_mass = 28.96442
R_universal = 8314.32
R = R_universal / molar_mass

# Atmosphere
atmosphere_setup()
T1 = get_temperature(h)
p1 = get_pressure(h)

# 1st shock wave
mach2, p2, T2, beta1 = oblique_shock(theta1, mach1, p1, T1, gamma)

# 2nd shock wave
mach3, p3, T3, beta2 = oblique_shock(theta2, mach2, p2, T2, gamma)
To3 = T3 * (1 + ((gamma - 1) / 2) * (mach3 ** 2))
mass_flow3 = p3 * A * mach3 * sqrt(gamma / (R * T3))

# Combustion
mass_flow4, To4 = combustion(To3, mach3, mach4, gamma, Cp, mass_flow3)
T4 = To4 / ((1 - (gamma - 1) / 2) * (mach4 ** 2))
p4 = mass_flow4 / (A * mach4 * sqrt(gamma / (R * T4)))
po4 = p4 * (1 + ((gamma - 1) / 2) * mach4 ** 2)

# Expansion
p5 = po4 * (1 + ((gamma - 1) / 2) * mach5 ** 2) ** (gamma / (1 - gamma))