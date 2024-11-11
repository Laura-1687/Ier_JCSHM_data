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

# Then set up the relationships (the CPDs)
A_cpd = TabularCPD(
                variable='A',
                variable_card=2,
                values=[[.2], [.8]])  # Assume a1 = 0, a2 = 1

B_cpd = TabularCPD(
                variable='B',
                variable_card=2,
                values=[[.7], [.3]])

D_cpd = TabularCPD(
                    variable='D',
                    variable_card=2,
                    values=[[.95, .8, .5],
                             [.05, .2, .5]],
                    evidence=['C'],
                    evidence_card=[3])

C_cpd = TabularCPD(
                        variable='C', 
                        variable_card=3,
                        values=[[.5, .8, .8, .9],
                                 [.3, .15, .1, .08],
                                 [.2, .05, .1, .02]],
                        evidence=['A', 'B'],
                        evidence_card=[2, 2])

# Add the relationships to your model
ABCD_model.add_cpds(A_cpd, B_cpd, D_cpd, C_cpd)

# Verify the structure of the model
ABCD_model.get_cpds()

####################################
# Make inference on the model
####################################

from pgmpy.inference import VariableElimination

ABCD_infer = VariableElimination(ABCD_model)

# Interactive section for user input

# Ask user for the variable they want to query
query_variable = input("Enter the variable you want to query (e.g., 'A', 'B', 'C', or 'D'): ").strip()

# Ask user if they want to provide evidence
evidence_input = input("Do you want to provide evidence? (yes/no): ").strip().lower()

evidence = {}
if evidence_input == 'yes':
    while True:
        evidence_var = input("Enter evidence variable (e.g., 'A', 'B', 'C', or 'D') or 'done' to finish: ").strip()
        if evidence_var.lower() == 'done':
            break
        evidence_state = int(input(f"Enter the state for {evidence_var} (e.g., '0' for a1, '1' for a2): ").strip())
        evidence[evidence_var] = evidence_state

# Perform the query with the specified evidence
result = ABCD_infer.query(variables=[query_variable], evidence=evidence)
print("\nResult:")
print(result)



