import os
import pandas as pd
import numpy as np
from sysoproj import SysoProj

def setup(project_name, working_dir = None, table_name = "Table_0"):
    '''Setup a working directory or load an existing project, return class instance of SysoProj'''

    working_dir = os.path.abspath("./") if working_dir is None else working_dir
    # Create or load project folder
    project_exists = False
    if project_name in os.listdir(working_dir):
        if os.path.isdir(os.path.join(working_dir, project_name)):
            print("Load project")
            project = _load_project(working_dir, project_name, table_name = table_name)
            project_exists = True
    if not project_exists:
        print("Create project")
        project = _create_project(working_dir, project_name, table_name = table_name)
        
    return project

def remove_project(project_name, working_dir = None):
    '''remove project folder'''
    working_dir = os.path.abspath("./") if working_dir is None else working_dir
    if project_name in os.listdir(working_dir):
        if os.path.isdir(os.path.join(working_dir, project_name)):
            os.system(f"rm -r '{os.path.join(working_dir, project_name)}'")
            print(f"remove project {project_name}")

def _load_project(working_dir, project_name, table_name):
    '''Load existing project into SysoProj'''

    project_path = os.path.join(working_dir, project_name)
    project = SysoProj(project_path, table_name = table_name)
    return project

def _create_project(working_dir, project_name, table_name):
    '''Create the project folder and subfolders, returns SysoProject class instance'''
    
    # Create folders and subfolders
    project_path = os.path.join(working_dir, project_name)
    os.makedirs(project_path, exist_ok=True)
    
    project = SysoProj(project_path, table_name = table_name)
    
    return project