
def area_ratio(M_in, M_out, gamma, T_in, p_in, rho_in):
	A_out = A_in * (M_in / M_out) * ((1 + ((gamma - 1) / 2) * M_out ** 2) /
	                               (1 + ((gamma - 1) / 2) * M_in ** 2)) ** ((gamma + 1) / (2 * (gamma - 1)))
	T_out = T_in * (1 + ((gamma - 1) / 2) * M_out ** 2) / (1 + ((gamma - 1) / 2) * M_in ** 2)
	p_out = p_in * (T_out / T_in) ** (gamma / (gamma - 1))
	rho_out = rho_in * (p_out /p_in) * (T_in / T_out)
	return A_out, T_out, p_out, rho_out

def main(args):
	[mach_before, mach_after, temperature_before, pressure_before, density_before] = args
	A_out, p_out, T_out, rho_out = area_ratio_expansion(mach_before, mach_after, gamma, temperature_before, pressure_before, density_before)
	print('A_out: %.3f' % A_out)
	print('T_out: %.3f' % T_out)
	print('p_out: %.3f' % p_out)
	print('A_out: %.3f' % rho_out)


if __name__ == '__main__':
	args = [5, 3, 1.4, 490]
