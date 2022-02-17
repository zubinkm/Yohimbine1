from biorefineries.lipidcane import chemicals
from biosteam.units import FedBatch, MixerSettler, BinaryDistillation
from biosteam import Stream, settings, System
from thermosteam.reaction import Reaction
from thermosteam import Chemicals, Chemical

# Setting the chemicals
chem = Chemicals(chemicals, cache=True)
Et = chem['Ethanol']
YH = Chemical.blank('YH', '64-17-5')
YH.Tb = Et.Tb
YH.copy_models_from(Et)
YH.MW = 40
chem.append(YH)
settings.set_thermo(chem)

# Using the same feed stream as the one given in biosteam for fermentation

feed = Stream('yohimbine_production',
               Water=1.20e+1,
               Glucose=3.89e+7,
               O2=3.89e+7,
               Sucrose=2.14e+01,
               DryYeast=1.03e+01,
               units='kg/hr',
               T=32+273.15,
              )

# Importing the module I created for fed batch fermentation (saved in biosteam/units)
# Kinetic constants are all assumed from a previous problem I solved and not related to YH
# 50 m3 volume given in the question is applied in the said module

F1 = FedBatch('F1',
                   ins=feed, outs=('CO2', 'product'),
                   tau=1, efficiency=0.90, V=50,iskinetic=True)
F1.fermentation_reaction=Reaction('O2 + Glucose -> 2YH + 2CO2',  'Glucose', F1.efficiency, F1.chemicals)
F1.simulate()
F1.show()


import biosteam as bst

# Adding LLE to the outlet of fermentation tank
feed = Stream('Feed')
feed.copy_flow(F1.effluent, ['Yeast'], exclude=True)
solvent = Stream('solvent', Ethanol=500)
MS1 = bst.MixerSettler('MS1', ins=(feed, solvent), outs=('raffinate', 'extract'))
MS1.simulate()
MS1.show()

feed = MS1.outs[1]

# Assuming low temperature keeping in mind that YH can undergo degradation at high T
feed.T = 320

# Fraction values unaltered from biosteam example

D1 = BinaryDistillation('D1', ins=feed,
                         outs=('distillate', 'bottoms_product'),
                         LHK=('YH', 'Water'),
                         y_top=0.99, x_bot=0.01, k=2,
                         is_divided=True)

# Using flowsheet creation in biosteam, I am creating my system with the given path

manual_sys = System('manual_sys', path=[F1, MS1, D1])
manual_sys.simulate()
manual_sys.show()

# Importing the FED Batch TEA module (same as the one in biosteam TEA documentation)

from _fedBatchTEA import FedBatchTEA

lipidcane_tea = FedBatchTEA(system=manual_sys,
                             IRR=0.15,
                             duration=(2018, 2038),
                             depreciation='MACRS7',
                             income_tax=0.35,
                             operating_days=200,
                             lang_factor=3,
                             construction_schedule=(0.4, 0.6),
                             WC_over_FCI=0.05,
                             labor_cost=2.5e6,
                             fringe_benefits=0.4,
                             property_tax=0.001,
                             property_insurance=0.005,
                             supplies=0.20,
                             maintenance=0.01,
                             administration=0.005)

(lipidcane_tea.show())

print(lipidcane_tea.get_cashflow_table())
