import numpy as np

def calculate_gamma_beta_momentum(energy, mass):
    '''
    calculate_gamma_beta_momentum(energy, mass) takes the energy and mass of a particle and outputs it's Lorentz Gamma Factor, Beta and relativistic momentum
    
    Energy and mass must be in the same units (in natural units). For example, if energy is in GeV, mass must be in GeV. 
    The function outputs momentum also in that same units.
    '''
    gamma= (energy/mass)
    momentum= np.sqrt(energy**2 - mass**2)
    beta=momentum/energy
    return float(gamma),float(beta),float(momentum)
