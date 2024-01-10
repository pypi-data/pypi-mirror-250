import numpy as np
import os
import sys
sys.path.append(os.path.abspath("./src"))
import syso

# Test file for Syso, create a syso project, run a for loop with arbitrary trials running through N experiments which randomly pass or fail
# Syso is used to keep track of the experiments


project_name = "Test_syso"
syso.remove_project(project_name)
syso_project = syso.setup(project_name)

num_trials = 20
num_experiments = 5
experiment_failing_ratio = 0.2 # Percentage of the time an experiment fails for a given trial

trial_names = [f"trial_{i}" for i in range(num_trials)]
experiment_names = [f"exp_{i}" for i in range(num_experiments)]

for trial_name in trial_names:
    for experiment_name in experiment_names:
        if np.random.uniform(0,1) < experiment_failing_ratio:
            break
        
        syso_project.log(trial_name, experiment_name, value = np.random.uniform(1,2))

# Test with another table
syso_project.set_table_name("Table_2")
for k,trial_name in enumerate(trial_names):
    for j,experiment_name in enumerate(experiment_names):
        if np.random.uniform(0,1) < experiment_failing_ratio:
            break
        
        syso_project.log(trial_name, experiment_name, value = f"{k}-{j}")