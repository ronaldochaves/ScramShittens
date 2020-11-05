from numpy import sqrt

C_p = 1084
combustor_length = 9.5
combustor_height = 0.6
A = combustor_height * combustor_length
LHV = 120e6


def main(args):
	[mach_before, mach_after, gamma, temperature_total_before] = args
    temperature_total_after = temperature_total_before * ((((1 + gamma*(mach_before ** 2)) / (1 + gamma*(mach_after ** 2))) * (
        mach_after / mach_before)) ** 2) * ((2 + (gamma - 1) * (mach_after ** 2)) / (2 + (gamma - 1) * (mach_before ** 2)))
    air_flow = pressure_before * A * mach_before * sqrt(gamma / (R * temperature_before))
    Q = air_flow * C_p * (temperature_total_after - temperature_total_before)
    fuel_flow = Q / LHV
    flow_after = air_flow + fuel_flow
    return flow_after, temperature_total_after


if __name__ == '__main__':
	args = [4, 3, 1.4, 1000]
	main(args)

keyword = ['Recurso', 'padrão', 'conforme', 'abnt']
