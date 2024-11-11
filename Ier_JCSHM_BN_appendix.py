# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 11:45:48 2023

@author: ierim
"""
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD


# Define the structure of the Bayesian Network
ABCD_model = BayesianNetwork([('A', 'C'),
                             ('B', 'C'),
                             ('C', 'D')])

#Then set up the relationships (the CPDs)
A_cpd = TabularCPD(
                variable = 'A',
                variable_card = 2,
                values = [[.2],[.8]]) # Assume a1 = 0, a2 = 1


B_cpd = TabularCPD(
                variable = 'B',
                variable_card = 2,
                values = [[.7],[.3]]) # Assume b1 = 0, b2 = 1

D_cpd = TabularCPD(
                    variable = 'D',
                    variable_card = 2,
                    values = [[.95, .8, .5],
                             [.05, .2, .5]],
                    evidence = ['C'],
                    evidence_card = [3]) # Assume d1 = 0, d2 = 1

C_cpd = TabularCPD(
                        variable = 'C', 
                        variable_card = 3,
                        values = [[.5, .8, .8, .9],
                                 [.3, .15, .1, .08],
                                 [.2, .05, .1, .02]],
                        evidence = ['A', 'B'],
                        evidence_card = [2,2]) # Assume c1 = 0, c2 = 1, c3=2

# Add the relationships to your model
ABCD_model.add_cpds(A_cpd, B_cpd, D_cpd, C_cpd)

# Verify the structure of the model
ABCD_model.get_cpds()

####################################
# Make inference on the model
####################################

from pgmpy.inference import VariableElimination

ABCD_infer = VariableElimination(ABCD_model)

# Query only 'C' to get its marginal probability distribution
prob_C = ABCD_infer.query(variables=['C'])
print(prob_C)

# Query 'C' with evidence that 'A' is in state 'a1'
prob_C_given_A_a1 = ABCD_infer.query(variables=['C'], evidence={'A': 0})  
print(prob_C_given_A_a1)

# Query 'A' with evidence that 'C' is in state 'c3'
prob_A_given_C_c3 = ABCD_infer.query(variables=['A'], evidence={'C': 2})  # Assuming c3 is represented by 2
print(prob_A_given_C_c3)


