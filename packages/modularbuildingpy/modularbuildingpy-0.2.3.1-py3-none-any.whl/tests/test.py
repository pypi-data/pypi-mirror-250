# ml intel/2020u4 intelmpi/2020u4; source /home/w/wind/batukan/.virtualenvs/opensees311/bin/activate

import os, sys, importlib

home = os.environ["HOME"]
scratch = os.environ["SCRATCH"]
nnodes = int(os.environ["SLURM_JOB_NUM_NODES"])
nodelist = os.environ["SLURM_JOB_NODELIST"]
jobid = os.environ["SLURM_JOB_ID"]
os.environ["MPLCONFIGDIR"] = f"{scratch}/tmp/"
nprocs_per_node = 40

project_path = f"{home}/documents/github/ModularBuildingPy/src"
sys.path.append(project_path)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["figure.dpi"] = 600
plt.rcParams["savefig.dpi"] = 600

# Unload the module if it's already loaded
modules = ["modularbuildingpy"]
for module in modules:
    if module in sys.modules.keys():
        del sys.modules[module]

import modularbuildingpy as mbp

os.chdir(project_path)

# Create an instance of the class
# directory = f"{project_path}/tests/test_model"
directory = f"{scratch}/MSB/modularbuildingpy/case_study_32"

# logging options = "debug", "info", "warning", "error", "critical", mode = "w" or "a"
model = mbp.Model(
    name="Case Study 32",
    directory=directory,
    analyze_kwargs={"nprocs": nprocs_per_node},
    logger_kwargs={"console": "info", "file": "debug", "mode": "w"},
)
generate = model.get_generate()

# load the input dictionaries from a python file
spec = importlib.util.spec_from_file_location("input_file", f"./tests/input32.py")
input_file = importlib.util.module_from_spec(spec)
spec.loader.exec_module(input_file)

generate.layout(layout=input_file.layout,horizontal_spacing=0.35)
generate.height(height=input_file.height)
generate.node(base_constraint="pinned")
generate.diaphragm(remove_ceiling=9, remove_floor=9)
generate.geo_transf()
generate.section_material()
generate.element(section=input_file.sections)
generate.connection(connection=input_file.connections)
generate.load(load_and_factor=input_file.loads_and_factors)
generate.partition()

analyze = model.get_analyze()
stdout, stderr = analyze.run()
for i, (out, err) in enumerate(zip(stdout, stderr)):
    print(f"pid = {i} -> stdout: \n{out}")
    print(f"pid = {i} -> stderr: \n{err}")
