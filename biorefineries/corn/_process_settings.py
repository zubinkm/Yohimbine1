# -*- coding: utf-8 -*-
# BioSTEAM: The Biorefinery Simulation and Techno-Economic Analysis Modules
# Copyright (C) 2020, Yoel Cortes-Pena <yoelcortes@gmail.com>
# 
# This module is under the UIUC open-source license. See 
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.
"""
"""
import biosteam as bst

__all__ = ('load_process_settings', 'price',)

def load_process_settings():
    bst.process_tools.default_utilities()
    bst.CE = 567 # 2013
    bst.PowerUtility.price = 0.07 # Value from Chinmay's report; 0.07, in original
    HeatUtility = bst.HeatUtility
    lps = HeatUtility.get_agent('low_pressure_steam')
    Water = lps.chemicals.Water
    lps.T = 152 + 273.15
    lps.P = Water.Psat(lps.T)
    lps.heat_transfer_efficiency = 1.0
    lps.regeneration_price = price['Steam'] * Water.MW
    for agent in HeatUtility.heating_agents:
        agent.regeneration_price = price['Steam'] * Water.MW
    cw = HeatUtility.get_agent('cooling_water')
    cw.regeneration_price = 0.073e-3 * Water.MW
    cw.T = 25. + 273.15


# Raw material price (USD/kg)
price = {
    'Ethanol': 0.48547915353569393, 
    'Corn': 0.13227735731092652, # Value from Chinmay's report; 0.08476585075177462 in original
    'DDGS': 0.12026, # Value from Chinmay's report; 0.09687821462905594, in original
    'Yeast': 1.86, #* 3.045 / (63.335 + 3.045), # 1.86 in Chinmay's report; 0.907310526171629 in original
    'Enzyme': 2.25, # Value from Chinmay's report; 3.20739717428309 in original
    'Denaturant': 0.4355069727002459,
    'Sulfuric acid': 0.08971711759613593,
    'Ammonia': 0.4485966110937889,
    'Caustic': 0.14952852932689323,
    'Lime': 0.19937504680689405,
    'Steam': 12.86e-3, # Value from Chinmay's report; 17.08e-3 in original lipidcane report 
    'Crude oil': 0.56,
}

