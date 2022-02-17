import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# kinetic constants for monod model
mu_max = 0.5
ks = 0.5
kd = 0.1
yo2 = 0.3
ko2 = 0.1
yps = 0.2
yxs = 0.1
ypx = 0.1
kla = 0.1
p = 101325
m = 0.3

# values to calculate oxygen dependency of the fed batch fermentation
r = 8.314
temp = 298.15
h2 = 33
mw = 32
O2g = ((p * 0.205 * mw) / (r * temp))

# assumption on feed flow rate, F
F = 10


def kinetic_model(z,t,constants):
    # kinetic constants

    mu_max, ks, sf, yo2, yps, kla, p, qs, m , a = constants

    t = np.linspace(0, 50, 1000)  # time steps


    X, P, S, F, O2l  = z      # current concentrations (kg/m3)


    # Compute coefficients
    mu = (mu_max * S) / (ks + S) * (O2l /ko2 + O2l)
    qs = mu / yxs


    # ODE integration
def model(z, t):
    [X, S, P, F, O2l] = z
    # Compute coefficients

    mu = (mu_max * S) / (ks + S) * (O2l / ko2 + O2l)
    qs = mu / yxs
    rS = -(qs + m) * X
    rO2 = (yo2 * rS) + (kla * ((O2g / h2) - O2l))
    t = np.linspace(0, 100, 1000)


    # the differential equations corresponding to mass balances

    dVdt = F # flowrate definition

    dXdt = (mu - kd) * X - (X * F) / V
    if (S<1): # logical statement to start the fed batch once substrate concentration drops below 1
        sf = 100
    else: sf = 0

    dSdt = ((F / V) * (sf - S)) - ((qs + m) * X)

    dPdt = ((-F / V) * P) - (ypx * mu * X)


    dOdt = ((F / V) * O2l) + rO2

    return (dXdt, dSdt, dPdt, dVdt, dOdt)

z0 = [0.1, 0.0, 50, 0.0]  # initial conditions for X, P, S, V, O2l
t = np.linspace(0, 50, 1000)
sol = odeint(model, z0, t)
X, P, S, V, O2l = sol.transpose()


plt.plot(t, X)
plt.plot(t, P)
plt.plot(t, S)
plt.plot(t, V)
plt.plot(t, O2l)

plt.xlabel('Time [hr]')
plt.ylabel('Concentration [g/liter]')
plt.legend(['Cell Conc.',
            'Product Conc.',
            'Substrate Conc.',
            'Volume [liter]'
            'Oxygen Conc'])