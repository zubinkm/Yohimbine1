from biorefineries.lipidcane import chemicals
from biosteam.units import FedBatch, MixerSettler, BinaryDistillation
from biosteam import Stream, settings, System
from thermosteam.reaction import Reaction
from thermosteam import Chemicals, Chemical

# Setting the chemicals and its properties

# Adding models using Antoine method in thermosteam
# antoine parameters are assumed

def User_antoine_model(T):
         return 10**(10.116 -  1687.537 / (T - 42.98))


def User_antoine_model2(T):
    return 0.001   # assumption

chem = Chemicals(chemicals, cache=True)
YH = Chemical('yohimbine', phase_ref='s')
YH.Tb = 543

YH.Psat.add_method(f=User_antoine_model, Tmin=273.20, Tmax=720.20)
YH.V.L.add_method(f=User_antoine_model2, Tmin=273.20, Tmax=720.20)
YH.copy_models_from(chem['Ethanol'])
chem.append(YH)
settings.set_thermo(chem)
YH.show()

# Using the same feed stream as the one given in biosteam for fermentation

feed = Stream('Fedbatch_feed',
               Water=1.20e+1,
               Glucose=3.89e+5,
               O2=3.89e+3,
               Sucrose=2.14e+01,
               DryYeast=1.03e+01,
               units='kg/hr',
               T=300,
              )


# Importing the module I created for fed batch fermentation (saved in biosteam/units)
# Kinetic constants are all assumed from a previous problem I solved and not related to YH
# 50 m3 volume given in the question is applied in the said module

F1 = FedBatch('F1',
                   ins=feed, outs=('CO2', 'product'),
                   tau=1, efficiency=0.90, V=50,  iskinetic=True)
F1.fermentation_reaction = Reaction('O2 + Glucose -> 2yohimbine + 2CO2',  'Glucose', F1.efficiency, chem)
F1.simulate()
F1.results()
F1.show()
print(F1.outs[1])

# Adding LLE to the outlet of fermentation tank

feed = Stream('Feed')
feed.copy_flow(F1.effluent, ['Yeast'], exclude=True)
solvent = Stream('solvent', Ethanol=500)
MS1 = MixerSettler('MS1', ins=(feed, solvent), outs=('raffinate', 'extract'))
MS1.simulate()
MS1.results()
MS1.show()

feed = MS1.outs[1]

# Assuming low temperature keeping in mind that YH can undergo degradation at high T
feed.T = 320

# Fraction values unaltered from biosteam example

D1 = BinaryDistillation('D1', ins=feed,
                         outs=('distillate', 'bottoms_product'),
                         LHK=('yohimbine', 'Water'),
                         y_top=0.99, x_bot=0.01, k=2,
                         is_divided=True)
D1.simulate()
D1.results()
# D1.show(T='degC', P='atm', composition=True)

# Using flowsheet creation in biosteam, I am creating my system with the given path

manual_sys = System('manual_sys', path=[F1, MS1, D1])
manual_sys.simulate()
manual_sys.show()

# Importing the FED Batch TEA module (same as the one in biosteam TEA documentation)

from _fedBatchTEA import FedBatchTEA

price = {'YH': 0.3}

# Values are unaltered from the lipid cane example in biosteam

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

lipidcane_tea.show()

print(lipidcane_tea.get_cashflow_table())