from numpy import sqrt

Cp = 1084
combustor_length = 9.5
combustor_height = 0.6
A = combustor_height * combustor_length
LHV = 120e6


def rayleight_flow(temperature_total_before, mach_before, mach_after, gamma):
    temperature_total_after = temperature_total_before * ((((1 + gamma*(mach_before ** 2)) / (1 + gamma*(mach_after ** 2))) * (
        mach_after / mach_before)) ** 2) * ((2 + (gamma - 1) * (mach_after ** 2)) / (2 + (gamma - 1) * (mach_before ** 2)))
    return temperature_total_after


def heat(air_flow, Cp, temperature_total_before, temperature_total_after):
    Q = air_flow * Cp * (temperature_total_after - temperature_total_before)
    return Q


def inlet_fuel_flow(Q, LHV):
    fuel_flow = Q / LHV
    return fuel_flow


def combustion(args):
    [temperature_total_before, mach_before, desired_mach_after, gamma, Cp, air_flow] = args
    temperature_total_after = rayleight_flow(temperature_total_before, mach_before, desired_mach_after, gamma)
    Q = heat(air_flow, Cp, temperature_total_before, temperature_total_after)
    fuel_flow = inlet_fuel_flow(Q, LHV)
    flow_after = air_flow + fuel_flow
    return flow_after, temperature_total_after


if __name__ == '__main__':
    args = [4, 3, 1.4, 1000]
    main(args)
