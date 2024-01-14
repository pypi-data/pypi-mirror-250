"""
.. module:: modularbuildingpy
   :synopsis: This file contains the main classes for ModularBuildingPy.

.. moduleauthor:: Mehmet Baris Batukan

This module was created on 2023-12-02. The units used in this module are meters (m), kilonewtons (kN), and Celsius (C).
"""

import os, sys, re, shutil, logging, psutil, functools, pkg_resources, warnings, json, time
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import openseespy.opensees as ops
import ipyparallel as ipp
import requests
import pymetis
from scipy.spatial import distance
from scipy import constants
from scipy.spatial import Voronoi
from shapely.geometry import Polygon, box
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon as mpl_polygon

if "utils.helper" in sys.modules.keys():
    del sys.modules["utils.helper"]

from .utils import helper

__version__ = "0.2.5.2"

class Model(object):
    """
    This is the main class for ModularBuildingPy. When it is initialized, it creates an instance of the following classes:

    - Analyze
    - Design (Not implemented yet!)
    - Generate
    - Material
    - PostProcess

    .. important::
        It is expected that the user will only instantiate this class. The user can access the instances of the :class:`_Analyze`, :class:`_Design`, :class:`_Generate`, :class:`_Material`, and :class:`_PostProcess` classes using the following methods:


    Methods:

        get_analyze():
            Returns the instance of the :class:`_Analyze` class.

        get_design():
            Returns the instance of the :class:`_Design` class.

        get_generate():
            Returns the instance of the :class:`_Generate` class.

        get_material():
            Returns the instance of the :class:`_Material` class.

        get_post_process():
            Returns the instance of the :class:`_PostProcess` class.

    Args:

        name (str): Name of the model.

        directory (str): Path to save the files and results of the model.

    Keyword Args:

        logger_kwargs (dict, optional): Keyword arguments for logger.

            Available keywords:

            - ``console``: Logging level for console. Default is ``"info"``.

                Available options are:

                    ``"debug"``, ``"info"``, ``"warning"``, ``"error"``, ``"critical"``


            - ``file``: Logging level for file.  Default is ``"debug"``.

                Available options are:

                    ``"debug"``, ``"info"``, ``"warning"``, ``"error"``, ``"critical"``

            - ``mode``: Mode for file logging. Default is ``"w"``.

                Available options are:

                    ``"w"`` for write, ``"a"`` for append

        generate_kwargs (dict, optional): Keyword arguments for Generate class.

            Available keywords:

                - ``nprocs`` (int): Number of processes to use for parallel computing.

                .. warning::
                    Currently, only ``nprocs = 1`` is supported. ``nprocs`` greater than 1 will be ignored.

        analyze_kwargs (dict, optional): Keyword arguments for Analyze class.

            Available keywords:

                - ``nprocs`` (int): Number of processes to use for parallel computing.

                .. warning::
                    Make sure that ``nprocs`` is not greater than the number of cores in your computer. Otherwise, it will raise an error.

        design_kwargs (dict, optional): Keyword arguments for Design class. Currently, this class is not implemented.

        post_process_kwargs (dict, optional): Keyword arguments for PostProcess class.

            Available keywords:

                - ``nprocs`` (int): Number of processes to use for parallel computing.

                .. warning::
                    Make sure that ``nprocs`` is not greater than the number of cores in your computer. Otherwise, it will raise an error.


    Returns:
        None

    Examples:

        Here is an example of how to initialize Model class:

        .. code-block:: python

            import modularbuildingpy as mbpy

            model = mbpy.Model(
                name="test",
                directory="/home/test",
                logger_kwargs={"console": "info", "file": "debug", "mode": "w"},
                generate_kwargs={"nprocs": 1},
                analyze_kwargs={"nprocs": 1},
                design_kwargs={"nprocs": 1},
                post_process_kwargs={"nprocs": 1},
            )

            analyze = model.get_analyze()
            design = model.get_design()
            generate = model.get_generate()
            material = model.get_material()
            post_process = model.get_post_process()



    """

    def __init__(self, name=None, directory=None, **kwargs):
        formatted_name = name.lower().replace(" ", "_")
        directory = directory
        logger_kwargs = kwargs.get("logger_kwargs", {})
        generate_kwargs = kwargs.get("generate_kwargs", {})
        analyze_kwargs = kwargs.get("analyze_kwargs", {})
        design_kwargs = kwargs.get("design_kwargs", {})
        post_process_kwargs = kwargs.get("post_process_kwargs", {})
        nprocs_generate = generate_kwargs.get("nprocs", 1)
        nprocs_analyze = analyze_kwargs.get("nprocs", 1)
        nprocs_design = design_kwargs.get("nprocs", 1)
        nprocs_post_process = post_process_kwargs.get("nprocs", 1)
        nprocs_max = psutil.cpu_count(logical=False)

        if name is None or not name[0].isalnum() or not re.search("[a-zA-Z]", name):
            raise ValueError(
                f"Please provide a name for the model. It should start with a letter or number and contain only letters, numbers, and underscores."
            )

        if directory is not None:
            if not os.path.exists(directory):
                os.makedirs(directory)
        else:
            raise ValueError(f"Please provide a path to save files.")

        for item in [
            nprocs_generate,
            nprocs_analyze,
            nprocs_design,
            nprocs_post_process,
        ]:
            if item > nprocs_max:
                raise ValueError(
                    f"Number of processes for {item = } cannot be greater than {nprocs_max}."
                )

        logger = _Logger(directory, **logger_kwargs)
        logger_object = logger.get()
        self.logger_file = logger.get_file()
        self.material = _Material()
        self.generate = _Generate(
            formatted_name,
            directory,
            logger_object,
            self.material,
            generate_kwargs=generate_kwargs,
            analyze_kwargs=analyze_kwargs,
            design_kwargs=design_kwargs,
            post_process_kwargs=post_process_kwargs,
        )
        self.analyze = _Analyze(
            formatted_name,
            directory,
            logger_object,
            self.material,
            self.generate,
            generate_kwargs=generate_kwargs,
            analyze_kwargs=analyze_kwargs,
            design_kwargs=design_kwargs,
            post_process_kwargs=post_process_kwargs,
        )
        self.design = _Design(
            formatted_name,
            directory,
            logger_object,
            self.material,
            self.generate,
            self.analyze,
            generate_kwargs=generate_kwargs,
            analyze_kwargs=analyze_kwargs,
            design_kwargs=design_kwargs,
            post_process_kwargs=post_process_kwargs,
        )

        self.post_process = _PostProcess(
            formatted_name,
            directory,
            logger_object,
            self.material,
            self.generate,
            self.analyze,
            self.design,
            generate_kwargs=generate_kwargs,
            analyze_kwargs=analyze_kwargs,
            design_kwargs=design_kwargs,
            post_process_kwargs=post_process_kwargs,
        )

        logger_object.info(
            f"Model is initialized. Now you can start building a numerical model for a Volumetric Modular Steel Building."
        )

    def get_material(self):
        return self.material

    def get_generate(self):
        return self.generate

    def get_analyze(self):
        return self.analyze

    def get_design(self):
        return self.design

    def get_post_process(self):
        return self.post_process


class OpenSeesPy(object):
    """
    This class is used to call OpenSeesPy methods. It is used as a wrapper for OpenSeesPy module. All methods of OpenSeesPy module can be called using this class. It also checks the version of OpenSeesPy and warns the user if it is not compatible with ModularBuildingPy.

    .. caution::
        Please do not use this class directly if ``nprocs`` keyword argument for :class:`_Analyze` class is greater than 1.

    Args:

        None

    Keyword Args:

        None

    Returns:

        None

    Examples:

        .. code-block:: python

            import modularbuildingpy as mbpy

            ops = mbpy.OpenSeesPy()

            ops.wipe()
            ops.model("basic", "-ndm", 3, "-ndf", 6)


    """

    def __init__(self):
        if self.check_internet_access():
            self.check_update()
        else:
            pass

    def __getattr__(self, attr):
        original_attr = getattr(ops, attr)

        if callable(original_attr):

            def new_attr(*args, **kwargs):
                return original_attr(*args, **kwargs)

            return new_attr
        else:
            return original_attr

    def check_internet_access(self) -> bool:
        """
        This method checks if there is an internet connection available. If there is no internet connection, it warns the user.

        Args:

            None

        Keyword Args:

            None

        Returns:

            bool
                True if there is an internet connection, False otherwise.

        """

        url = "http://www.google.com"
        timeout = 5
        try:
            _ = requests.get(url, timeout=timeout)
            return True
        except requests.ConnectionError:
            warnings.warn("No internet connection available.")
        return False

    def check_update(self) -> None:
        """
        This method checks if the version of OpenSeesPy is compatible with ModularBuildingPy. If it is not compatible, it warns the user.

        Args:

            None

        Keyword Args:

            None

        Returns:

            None

        """
        current_version = pkg_resources.get_distribution("openseespy").version

        response = requests.get(f"https://pypi.org/pypi/openseespy/json")
        data = json.loads(response.text)
        latest_version = data["info"]["version"]

        compatible_version = "3.5.1.12"

        if tuple(map(int, current_version.split("."))) < tuple(
            map(int, compatible_version.split("."))
        ):
            warnings.warn(
                "ModularBuildingPy is compatible with OpenSeesPy version 3.5.1.12 or higher. Please update OpenSeesPy."
            )
        elif tuple(map(int, current_version.split("."))) > tuple(
            map(int, compatible_version.split("."))
        ):
            warnings.warn(
                f"Your OpenSeesPy version ({current_version}) is higher than the version used for ModularBuildingPy ({compatible_version}). Please be aware of the possible incompatibilities."
            )
        else:
            pass

        return None


class _Design(object):
    """
    This class is used to design the model. When it is implemented, it will be able to design the model based on building codes.

    .. caution::
        This class is not meant to be used directly. Please use the ``get_design()`` method of :class:`Model` class to call methods and attributes.

    """

    def __init__(self, name, directory, logger, material, generate, analyze, **kwargs):
        self.name = name
        self.directory = directory
        self.logger = logger
        self.material = material
        self.generate = generate
        self.analyze = analyze
        self.nprocs = kwargs["design_kwargs"].get("nprocs", 1)

        self.logger.debug("Design class is initialized.")

        # TODO: change logging type to error
        self.logger.debug(f"Design class is not implemented yet...")


class _PostProcess(object):
    """
    This class is used to post-process the model. When it is implemented, it will be able to post-process the model based on user inputs.

    .. caution::
        This class is not meant to be used directly. Please use the ``get_post_process()`` method of :class:`Model` class to call methods and attributes.

    Parameters:
    -----------
    name: str
        Name of the model.
    directory: str
        Path to save files.
    logger: logging.Logger
        Logger object.
    material: _Material
        Material class.
    generate: _Generate
        Generate class.
    analyze: _Analyze
        Analyze class.
    design: _Design
        Design class.

    Returns:
    --------
    None

    """

    def __init__(
        self, name, directory, logger, material, generate, analyze, design, **kwargs
    ):
        self.name = name
        self.directory = directory
        self.logger = logger
        self.material = material
        self.generate = generate
        self.analyze = analyze
        self.design = design
        self.nprocs = kwargs["post_process_kwargs"].get("nprocs", 1)

        self.logger.debug("PostProcess class is initialized.")

        self.methods_called = {
            "_find": False,
        }

    def _find(self) -> None:
        self.methods_called["_find"] = True

        lst = os.listdir(f"{self.directory}")
        output_folders = list(filter(lambda x: x.endswith("output"), lst))
        self.output_items = [item.split("_") for item in output_folders]
        self.analysis_names = [sublist[-2] for sublist in self.output_items]

        return None

    def print_available(self) -> None:
        if not self.methods_called["_find"]:
            self._find()

        for item in self.analysis_names:
            self.logger.info(f"'{item}' analysis results are available.")


class _Analyze(object):
    """
    This class is used to analyze the model which was created using Generate class. It has methods to create nodes, diaphragms, elements, sections, materials, and geometric transformations for OpenSeesPy. It also has methods to add mass and gravity loads to the model. When the Model class is initialized, user can define nprocs keyword argument to use multiple cores to perform static or dynamic analysis. If nprocs is greater than 1, then the analysis will be performed using ipyparallel (externally). If nprocs is equal to 1, then the analysis will be performed using the current kernel.

    .. caution::
        This class is not meant to be used directly. Please use the ``get_analyze()`` method of :class:`Model` class to call methods and attributes.


    Parameters:
    -----------
    name: str
        Name of the model.
    directory: str
        Path to save files.
    logger: logging.Logger
        Logger object.
    material: _Material
        Material class.
    generate: _Generate
        Generate class.
    generate_kwargs: dict
        Keyword arguments for Generate class.

    Returns:
    --------
    None

    """

    _name = None
    _directory = None
    _generate = None

    def __init__(self, name, directory, logger, material, generate, **kwargs):
        self.name = name
        self.directory = directory
        self.logger = logger
        self.material = material
        self.generate = generate
        self.nprocs = kwargs["analyze_kwargs"].get("nprocs", 1)
        self.save_model = kwargs["analyze_kwargs"].get("save_model", False)
        _Analyze._name = name
        _Analyze._directory = directory
        _Analyze._generate = generate

        self.methods_called = {
            "initialize_ops": False,
            "declare_global_var": False,
            "assign_section_material": False,
            "assign_geo_transf": False,
            "assign_node": False,
            "assign_diaphragm": False,
            "assign_element": {
                "assign_column": False,
                "assign_brace": False,
                "assign_floor_beam": False,
                "assign_ceiling_beam": False,
                "assign_ver_con": False,
                "assign_hor_con": False,
            },
        }

    def timer(self, **kwargs):
        start = time.time()
        while True:
            time_passed = time.time() - start
            reset = yield time_passed
            if reset:
                start = time.time()

    @helper.log_time_memory
    def initialize_ops(self, **kwargs) -> None:
        self.methods_called["initialize_ops"] = True

        self.section_tags, self.material_tags = [], []
        self.create_column_hinge.cache_clear()
        self.create_beam_hinge.cache_clear()
        self.hss_section.cache_clear()
        self.w_section.cache_clear()
        self.create_steel01_material.cache_clear()
        self.create_fatigue_material.cache_clear()

        ops.wipe()
        ops.model("basic", "-ndm", 3, "-ndf", 6)
        self.logger.info("OpenSeesPy initialized.")
        self.logger.info("BE AWARE! Only following units (m, kN, C, etc.) are used!")

        return None

    def declare_global_var(self, **kwargs) -> None:
        self.methods_called["declare_global_var"] = True

        self.elastic_ceiling_beam = kwargs.get("elastic_ceiling_beam", False)
        self.elastic_floor_beam = kwargs.get("elastic_floor_beam", False)
        self.elastic_column = kwargs.get("elastic_column", False)
        self.elastic_brace = kwargs.get("elastic_brace", False)
        self.elastic_ver_con = kwargs.get("elastic_ver_con", False)
        self.elastic_hor_con = kwargs.get("elastic_hor_con", True)
        self.include_fatigue = kwargs.get("include_fatigue", False)
        self.include_element_mass = kwargs.get("include_element_mass", False)

        self.list_recorder = []
        self.list_mass = []
        self.list_bilin_params = []
        self.defined_recorders = []

        return None

    @helper.log_time_memory
    def assign_section_material(self, **kwargs) -> None:
        self.methods_called["assign_section_material"] = True

        for func in self.generate._command_section_material["func"]:
            method_name = func["type"]
            if hasattr(ops, method_name):
                method = getattr(ops, method_name)
                if isinstance(func["tag"], list):
                    tags = [
                        item["value"]
                        for tag in func["tag"]
                        for item in self.generate._command_section_material["tag"]
                        if item["name"] == tag
                    ]
                    if tags:
                        method(func["option"], *tags, *func["args"])
                else:
                    tag = next(
                        (
                            item["value"]
                            for item in self.generate._command_section_material["tag"]
                            if item["name"] == func["tag"]
                        ),
                        None,
                    )
                    if tag is not None:
                        method(func["option"], tag, *func["args"])
            else:
                self.logger.error(f"{method_name} is not a method of {ops.__name__}")

            if "uniaxialMaterial" in method_name:
                self.material_tags.append(tag)
            elif "section" in method_name:
                self.section_tags.append(tag)

        self.logger.info("Sections and materials have been assigned.")
        return None

    @helper.log_time_memory
    def assign_geo_transf(self, **kwargs) -> None:
        self.methods_called["assign_geo_transf"] = True

        for func in self.generate._command_geo_transf["func"]:
            method_name = func["type"]
            if hasattr(ops, method_name):
                method = getattr(ops, method_name)
                tag = next(
                    (
                        item["value"]
                        for item in self.generate._command_geo_transf["tag"]
                        if item["name"] == func["tag"]
                    ),
                    None,
                )
                if tag is not None:
                    method(func["option"], tag, *func["args"])
            else:
                self.logger.error(f"{method_name} is not a method of {ops.__name__}")

        self.logger.info("Geometric transformation has been assigned.")
        return None

    @helper.log_time_memory
    def assign_node(self, **kwargs) -> None:
        self.methods_called["assign_node"] = True

        pid = kwargs.get("pid", 0)
        plot_kwargs = kwargs.get("plot_kwargs", {})

        df_melted = self.generate.df_partition.melt(
            id_vars=["pid"],
            value_vars=["i_node", "j_node", "mid_node"],
            value_name="node",
        )

        df_node = self.generate.df_global_nodes[
            self.generate.df_global_nodes["node"].isin(
                df_melted[df_melted["pid"] == pid].node.unique()
            )
        ]

        if not df_node.empty:
            for row in df_node.itertuples(index=False):
                ops.node(
                    row.node,
                    row.X,
                    row.Y,
                    row.Z,
                )

        df_fix = self.generate.df_global_nodes_fix[
            self.generate.df_global_nodes_fix["node"].isin(df_node.node)
        ]

        if not df_fix.empty:
            for row in df_fix.itertuples(index=False):
                ops.fix(
                    row.node,
                    row.UX,
                    row.UY,
                    row.UZ,
                    row.RX,
                    row.RY,
                    row.RZ,
                )

        node_tags = ops.getNodeTags()
        self.logger.info(f"{len(node_tags)} global nodes have been created.")

        if plot_kwargs.get("show", False):
            fig, ax = helper.plot_nodes_3D(self.generate.df_global_nodes, plot_kwargs)
            fig.show()

        return None

    @helper.log_time_memory
    def assign_diaphragm(self, **kwargs):
        self.methods_called["assign_diaphragm"] = True

        pid = kwargs.get("pid", 0)
        ceiling, floor = kwargs.get("ceiling", True), kwargs.get("floor", True)
        self.diaphragm_created = {"ceiling": ceiling, "floor": floor}

        df_ceiling = self.generate.df_diaphragms[
            self.generate.df_diaphragms["type"] == "ceiling"
        ]
        df_floor = self.generate.df_diaphragms[
            self.generate.df_diaphragms["type"] == "floor"
        ]

        node_tags_local = ops.getNodeTags()

        if self.nprocs > 1:
            df_ceiling = df_ceiling[
                [
                    any(node in node_tags_local for node in slaves)
                    for slaves in df_ceiling["slaves"]
                ]
            ]
            df_floor = df_floor[
                [
                    any(node in node_tags_local for node in slaves)
                    for slaves in df_floor["slaves"]
                ]
            ]

            df_ceiling["pid"] = pid
            df_floor["pid"] = pid

            nodes_to_def_ceiling = [
                item
                for sublist in df_ceiling["slaves"].tolist()
                for item in sublist
                if item not in node_tags_local
            ]
            nodes_to_def_floor = [
                item
                for sublist in df_floor["slaves"].tolist()
                for item in sublist
                if item not in node_tags_local
            ]

            nodes_to_def = list(set(nodes_to_def_ceiling + nodes_to_def_floor))

            if nodes_to_def:
                df_nodes = self.generate.df_global_nodes[
                    self.generate.df_global_nodes["node"].isin(nodes_to_def)
                ]

                for row in df_nodes.itertuples(index=False):
                    ops.node(
                        row.node,
                        row.X,
                        row.Y,
                        row.Z,
                    )

                df_nodes_fix = self.generate.df_global_nodes_fix[
                    self.generate.df_global_nodes_fix["node"].isin(df_nodes.node)
                ]

                for row in df_nodes_fix.itertuples(index=False):
                    ops.fix(
                        row.node,
                        row.UX,
                        row.UY,
                        row.UZ,
                        row.RX,
                        row.RY,
                        row.RZ,
                    )

        if ceiling:
            for row in df_ceiling.itertuples(index=False):
                ops.node(row.master, *row.master_coord)
                ops.fix(row.master, *[0, 0, 1, 1, 1, 0])
                ops.rigidDiaphragm(3, row.master, *row.slaves)

        if floor:
            for row in df_floor.itertuples(index=False):
                ops.node(row.master, *row.master_coord)
                ops.fix(row.master, *[0, 0, 1, 1, 1, 0])
                ops.rigidDiaphragm(3, row.master, *row.slaves)

        self.logger.info(
            f"{len(self.generate.df_diaphragms)} diaphragms have been created."
        )

        if self.nprocs > 1:
            return (df_ceiling, df_floor)

        else:
            return None

    @helper.log_time_memory
    def assign_element(self, **kwargs) -> None:
        pid = kwargs.get("pid", 0)
        plot_kwargs = kwargs.get("plot_kwargs", {})
        column_kwargs = kwargs.get("column_kwargs", {})
        brace_kwargs = kwargs.get("brace_kwargs", {})
        floor_beam_kwargs = kwargs.get("floor_beam_kwargs", {})
        ceiling_beam_kwargs = kwargs.get("ceiling_beam_kwargs", {})
        ver_con_kwargs = kwargs.get("ver_con_kwargs", {})
        hor_con_kwargs = kwargs.get("hor_con_kwargs", {})

        kwargs_dict = {
            "assign_column": column_kwargs,
            "assign_brace": brace_kwargs,
            "assign_floor_beam": floor_beam_kwargs,
            "assign_ceiling_beam": ceiling_beam_kwargs,
            "assign_ver_con": ver_con_kwargs,
            "assign_hor_con": hor_con_kwargs,
        }

        items = [
            "assign_column",
            "assign_brace",
            "assign_floor_beam",
            "assign_ceiling_beam",
            "assign_ver_con",
            "assign_hor_con",
        ]

        node_tags_all_old = np.array(ops.getNodeTags())
        ele_tags_all_old = np.array(ops.getEleTags())

        for item in items:
            self.methods_called["assign_element"][item] = True
            method = getattr(self, item)
            method_kwargs = kwargs_dict.get(item, {})
            method(pid=pid, **method_kwargs)

            node_tags_all = np.array(ops.getNodeTags())
            ele_tags_all = np.array(ops.getEleTags())

            self.logger.debug(
                f"{item} nodes: {node_tags_all.size - node_tags_all_old.size}"
            )
            self.logger.debug(
                f"{item} elements: {ele_tags_all.size - ele_tags_all_old.size}"
            )

            node_tags_all_old = node_tags_all
            ele_tags_all_old = ele_tags_all

        if plot_kwargs.get("show", False):
            node_tags = ops.getNodeTags()
            node_data = [[node_tag, *ops.nodeCoord(node_tag)] for node_tag in node_tags]
            ele_tags = ops.getEleTags()
            ele_data = [[ele_tag, *ops.eleNodes(ele_tag)] for ele_tag in ele_tags]
            fig, ax = helper.plot_elements_3D(node_data, ele_data, plot_kwargs)
            fig.show()

        self.logger.info(
            f"There are {len(ops.getEleTags())} elements and {len(ops.getNodeTags())} nodes in the model."
        )

        return None

    def add_mass(self, **kwargs) -> None:
        self.methods_called["add_mass"] = True
        pid = kwargs.get("pid", 0)

        factor_dl = kwargs.get("factor_dl", 1.0)
        factor_ll = kwargs.get("factor_ll", 0.0)
        factor_sl = kwargs.get("factor_sl", 0.0)
        factor_sdl = kwargs.get("factor_sdl", 1.0)

        df_mass_element = pd.DataFrame(
            self.list_mass,
            columns=["name", "ele_info", "ele_number", "i_node", "j_node", "mass"],
        )

        # Combine 'iNode' and 'jNode' columns
        node_numbers = pd.concat(
            [df_mass_element["i_node"], df_mass_element["j_node"]], ignore_index=True
        )

        # Create a new DataFrame with 'node_number' and 'mass' columns
        df_mass_member_nodal = pd.DataFrame(
            {
                "node": node_numbers,
                "mass": pd.concat(
                    [0.5 * df_mass_element["mass"], 0.5 * df_mass_element["mass"]],
                    ignore_index=True,
                ),
            }
        )

        self.df_mass_member_grouped = (
            df_mass_member_nodal.groupby("node").sum().reset_index()
        )

        self.logger.info(
            f"Total member mass in the model is {self.df_mass_member_grouped['mass'].sum():.2f} tons."
        )

        ceiling, floor = (
            self.diaphragm_created["ceiling"],
            self.diaphragm_created["floor"],
        )
        df_ceiling = self.generate.df_diaphragms[
            self.generate.df_diaphragms["type"] == "ceiling"
        ]
        df_floor = self.generate.df_diaphragms[
            self.generate.df_diaphragms["type"] == "floor"
        ]

        if self.nprocs > 1:
            self.df_mass_member_grouped["pid"] = pid
            self.df_mass_member_grouped.to_pickle(
                f"{self.directory}/tmp/df_mass_member_grouped_{pid}.pkl"
            )

            ops.barrier()
            if pid == 0:
                df_mass_member_grouped = pd.DataFrame()
                for i in range(self.nprocs):
                    df_mass_member_grouped = pd.concat(
                        [
                            df_mass_member_grouped,
                            pd.read_pickle(
                                f"{self.directory}/tmp/df_mass_member_grouped_{i}.pkl"
                            ),
                        ]
                    )
                df_mass_member_grouped = (
                    df_mass_member_grouped.groupby("node")
                    .agg({"mass": "sum", "pid": "first"})
                    .reset_index()
                )
                df_mass_member_grouped.to_pickle(
                    f"{self.directory}/tmp/df_mass_member_grouped.pkl"
                )

            ops.barrier()
            df_mass_member_grouped = pd.read_pickle(
                f"{self.directory}/tmp/df_mass_member_grouped.pkl"
            )
            df_ceiling = pd.read_pickle(f"{self.directory}/tmp/df_ceiling.pkl")
            df_floor = pd.read_pickle(f"{self.directory}/tmp/df_floor.pkl")

            df_mass_member_grouped = df_mass_member_grouped[
                df_mass_member_grouped["pid"] == pid
            ]
            df_ceiling = df_ceiling[df_ceiling["pid"] == pid]
            df_floor = df_floor[df_floor["pid"] == pid]

        mass_diaphragm = []
        for row in df_ceiling.itertuples():
            (
                dead,
                live,
                snow,
                superimposed_dead,
                _,
            ) = self.generate.df_ceiling_loads.loc[row.Index].values

            _load_XY = (
                factor_dl * dead
                + factor_sdl * superimposed_dead
                + factor_ll * live
                + factor_sl * snow
            ) / constants.g
            _load_MZ = (1 / 12) * _load_XY * (row.we_dir**2 + row.sn_dir**2)

            if ceiling:
                ops.mass(
                    row.master,
                    *[_load_XY, _load_XY, 0.0, 0.0, 0.0, _load_MZ],
                )

                mass_diaphragm.append(
                    ["ceiling", row.master, _load_XY, _load_XY, 0.0, 0.0, 0.0, _load_MZ]
                )

            else:
                len_slaves = len(row.slaves)
                _load_XY = _load_XY / len_slaves
                for slave in row.slaves:
                    ops.mass(
                        slave,
                        *[_load_XY, _load_XY, 0.0, 0.0, 0.0, 0.0],
                    )

                    mass_diaphragm.append(
                        ["ceiling", slave, _load_XY, _load_XY, 0.0, 0.0, 0.0, 0.0]
                    )

        if ceiling:
            self.logger.info(f"Celing diaphragm mass added to the model.")

        for row in df_floor.itertuples():
            (
                dead,
                live,
                snow,
                superimposed_dead,
                _,
            ) = self.generate.df_floor_loads.loc[row.Index].values

            _load_XY = (
                factor_dl * dead
                + factor_sdl * superimposed_dead
                + factor_ll * live
                + factor_sl * snow
            ) / constants.g

            _load_MZ = (1 / 12) * _load_XY * (row.we_dir**2 + row.sn_dir**2)

            if floor:
                ops.mass(
                    row.master,
                    *[_load_XY, _load_XY, 0.0, 0.0, 0.0, _load_MZ],
                )

                mass_diaphragm.append(
                    ["floor", row.master, _load_XY, _load_XY, 0.0, 0.0, 0.0, _load_MZ]
                )

            else:
                len_slaves = len(row.slaves)
                _load_XY = _load_XY / len_slaves
                for slave in row.slaves:
                    ops.mass(
                        slave,
                        *[_load_XY, _load_XY, 0.0, 0.0, 0.0, 0.0],
                    )

                    mass_diaphragm.append(
                        ["floor", slave, _load_XY, _load_XY, 0.0, 0.0, 0.0, 0.0]
                    )

        if floor:
            self.logger.info(f"Floor diaphragm mass added to the model.")

        self.df_mass_diaphragm = pd.DataFrame(
            mass_diaphragm,
            columns=["type", "node", "MX", "MY", "MZ", "MRX", "MRY", "MRZ"],
        )

        if not self.include_element_mass and ceiling and floor:
            for row in self.df_mass_member_grouped.itertuples(index=False):
                ops.mass(
                    row.node,
                    *[factor_dl * row.mass, factor_dl * row.mass, 0.0, 0.0, 0.0, 0.0],
                )

            self.logger.info(f"Element mass manually added to the model.")

        elif not self.include_element_mass and not ceiling and not floor:
            self.df_mass_member_diaphragm_grouped = (
                pd.concat(
                    [
                        self.df_mass_member_grouped,
                        self.df_mass_diaphragm[["node", "MX"]].rename(
                            columns={"MX": "mass"}
                        ),
                    ]
                )
                .reset_index(drop=True)
                .groupby("node")
                .sum()
                .reset_index()
            )

            for row in self.df_mass_member_diaphragm_grouped.itertuples(index=False):
                ops.mass(
                    row.node,
                    *[factor_dl * row.mass, factor_dl * row.mass, 0.0, 0.0, 0.0, 0.0],
                )

            self.logger.info(f"Diaphragm and element mass manually added to the model.")

        elif self.include_element_mass and not ceiling and not floor:
            self.df_mass_diaphragm_grouped = (
                self.df_mass_diaphragm[["node", "MX"]]
                .rename(columns={"MX": "mass"})
                .reset_index(drop=True)
                .groupby("node")
                .sum()
                .reset_index()
            )

            for row in self.df_mass_member_grouped.itertuples(index=False):
                ops.mass(
                    row.node,
                    *[factor_dl * row.mass, factor_dl * row.mass, 0.0, 0.0, 0.0, 0.0],
                )

            self.logger.info(f"Ceiling and floor mass manually added to the model.")

        elif self.include_element_mass and ceiling and not floor:
            self.df_mass_diaphragm_grouped = (
                self.df_mass_diaphragm[self.df_mass_diaphragm["type"] == "floor"][
                    ["node", "MX"]
                ]
                .rename(columns={"MX": "mass"})
                .reset_index(drop=True)
                .groupby("node")
                .sum()
                .reset_index()
            )

            for row in self.df_mass_member_grouped.itertuples(index=False):
                ops.mass(
                    row.node,
                    *[factor_dl * row.mass, factor_dl * row.mass, 0.0, 0.0, 0.0, 0.0],
                )

            self.logger.info(f"Floor mass manually added to the model.")

        elif self.include_element_mass and not ceiling and floor:
            self.df_mass_diaphragm_grouped = (
                self.df_mass_diaphragm[self.df_mass_diaphragm["type"] == "ceiling"][
                    ["node", "MX"]
                ]
                .rename(columns={"MX": "mass"})
                .reset_index(drop=True)
                .groupby("node")
                .sum()
                .reset_index()
            )

            for row in self.df_mass_member_grouped.itertuples(index=False):
                ops.mass(
                    row.node,
                    *[factor_dl * row.mass, factor_dl * row.mass, 0.0, 0.0, 0.0, 0.0],
                )

            self.logger.info(f"Ceiling mass manually added to the model.")

        elif self.include_element_mass and ceiling and floor:
            self.logger.info(
                f"Diaphragm and element mass is already included in the model."
            )

        self.logger.info(
            f"Total diaphragm mass in the west-east direction is {self.df_mass_diaphragm['MX'].sum():.2f} tons."
        )
        self.logger.info(
            f"Total diaphragm mass in the south-north direction is {self.df_mass_diaphragm['MY'].sum():.2f} tons."
        )
        self.logger.info(
            f"Total diaphragm mass in the torsional direction is {self.df_mass_diaphragm['MRZ'].sum():.2f} tons-m2."
        )

        return None

    def add_gravity_load(self, **kwargs) -> None:
        self.methods_called["add_gravity_load"] = True

        pid = kwargs.get("pid", 0)
        num_steps = kwargs.get("num_steps", 10)

        """
        NOTE: FEMA P695 - Eq. 6.1
        In all cases, modeling parameters, including the seismic mass and imposed gravity loads, should represent the median values of the structure and its components. The gravity loads for analysis are different from design gravity loads, and are given by the following load combination:
        1.05D + 0.25L
        """
        factor_dl = kwargs.get("factor_gravity_dl", 1.05)
        factor_ll = kwargs.get("factor_gravity_ll", 0.25)
        factor_sl = kwargs.get("factor_gravity_sl", 0.0)
        factor_sdl = kwargs.get("factor_gravity_sdl", 1.05)

        df_mass_element = pd.DataFrame(
            self.list_mass,
            columns=["name", "ele_info", "ele_number", "i_node", "j_node", "mass"],
        )

        # Combine 'iNode' and 'jNode' columns
        node_numbers = pd.concat(
            [df_mass_element["i_node"], df_mass_element["j_node"]], ignore_index=True
        )

        # Create a new DataFrame with 'node_number' and 'mass' columns
        df_mass_member_nodal = pd.DataFrame(
            {
                "node": node_numbers,
                "mass": pd.concat(
                    [0.5 * df_mass_element["mass"], 0.5 * df_mass_element["mass"]],
                    ignore_index=True,
                ),
            }
        )

        df_mass_member_grouped = (
            df_mass_member_nodal.groupby("node").sum().reset_index()
        )

        self.df_weight_member_grouped = df_mass_member_grouped.copy()
        self.df_weight_member_grouped = self.df_weight_member_grouped.rename(
            columns={"mass": "weight"}
        )
        self.df_weight_member_grouped["weight"] *= constants.g

        self.logger.info(
            f"Total member self-weight in the model is {self.df_weight_member_grouped['weight'].sum():.2f} kN."
        )

        ceiling, floor = (
            self.diaphragm_created["ceiling"],
            self.diaphragm_created["floor"],
        )
        df_ceiling = self.generate.df_diaphragms[
            self.generate.df_diaphragms["type"] == "ceiling"
        ]
        df_floor = self.generate.df_diaphragms[
            self.generate.df_diaphragms["type"] == "floor"
        ]

        if self.nprocs > 1:
            df_ceiling = pd.read_pickle(f"{self.directory}/tmp/df_ceiling.pkl")
            df_floor = pd.read_pickle(f"{self.directory}/tmp/df_floor.pkl")

            df_ceiling = df_ceiling[df_ceiling["pid"] == pid]
            df_floor = df_floor[df_floor["pid"] == pid]

        weight_diaphragm = []
        for row in df_ceiling.itertuples():
            (
                dead,
                live,
                snow,
                superimposed_dead,
                _,
            ) = self.generate.df_ceiling_loads.loc[row.Index].values

            _load_Z = (
                factor_dl * dead
                + factor_sdl * superimposed_dead
                + factor_ll * live
                + factor_sl * snow
            )

            if ceiling:
                weight_diaphragm.append(
                    ["ceiling", row.master, 0.0, 0.0, -_load_Z, 0.0, 0.0, 0.0]
                )

            else:
                len_slaves = len(row.slaves)
                _load_Z = _load_Z / len_slaves
                for slave in row.slaves:
                    weight_diaphragm.append(
                        ["ceiling", slave, 0.0, 0.0, -_load_Z, 0.0, 0.0, 0.0]
                    )

        for row in df_floor.itertuples():
            (
                dead,
                live,
                snow,
                superimposed_dead,
                _,
            ) = self.generate.df_floor_loads.loc[row.Index].values

            _load_Z = (
                factor_dl * dead
                + factor_sdl * superimposed_dead
                + factor_ll * live
                + factor_sl * snow
            )

            if floor:
                weight_diaphragm.append(
                    ["floor", row.master, 0.0, 0.0, -_load_Z, 0.0, 0.0, 0.0]
                )

            else:
                len_slaves = len(row.slaves)
                _load_Z = _load_Z / len_slaves
                for slave in row.slaves:
                    weight_diaphragm.append(
                        ["floor", slave, 0.0, 0.0, -_load_Z, 0.0, 0.0, 0.0]
                    )

        self.df_weight_diaphragm = pd.DataFrame(
            weight_diaphragm,
            columns=["type", "node", "WX", "WY", "WZ", "WRX", "WRY", "WRZ"],
        )

        ops.timeSeries("Linear", 1)
        ops.pattern("Plain", 1, 1)

        for row in self.df_weight_member_grouped.itertuples(index=False):
            ops.load(
                row.node,
                *[0.0, 0.0, -row.weight, 0.0, 0.0, 0.0],
            )

        for row in self.df_weight_diaphragm.itertuples(index=False):
            ops.load(
                row.node,
                *[row.WX, row.WY, row.WZ, row.WRX, row.WRY, row.WRZ],
            )

        self.logger.info(
            f"Total ceiling and floor weight in the model is {self.df_weight_diaphragm['WZ'].sum() * -1:.2f} kN."
        )

        if self.nprocs == 1:
            ops.wipeAnalysis()

            system = kwargs.get("system", "Mumps")
            ops.system(system)

            numberer = kwargs.get("numberer", "RCM")
            ops.numberer(numberer)

            constraints = kwargs.get("constraints", "Transformation")
            ops.constraints(constraints)

            test = kwargs.get("test", ("NormDispIncr", 1e-12, 200, 0))
            ops.test(*test)

            algorithm = kwargs.get("algorithm", "KrylovNewton")
            ops.algorithm(algorithm)

            integrator = kwargs.get("integrator", ("LoadControl", 1 / num_steps))
            ops.integrator(*integrator)

            analysis = kwargs.get("analysis", "Static")
            ops.analysis(analysis)

        else:
            ops.wipeAnalysis()
            system = kwargs.get("system", "Mumps")
            ops.system(system)

            numberer = kwargs.get("numberer", "ParallelRCM")
            ops.numberer(numberer)

            constraints = kwargs.get("constraints", "Transformation")
            ops.constraints(constraints)

            test = kwargs.get("test", ("NormDispIncr", 1e-12, 200, 0))
            ops.test(*test)

            algorithm = kwargs.get("algorithm", "KrylovNewton")
            ops.algorithm(algorithm)

            integrator = kwargs.get("integrator", ("LoadControl", 1 / num_steps))
            ops.integrator(*integrator)

            analysis = kwargs.get("analysis", "Static")
            ops.analysis(analysis)

        return None

    def add_rayleigh_damping(self, **kwargs):
        self.methods_called["add_rayleigh_damping"] = True

        pid = kwargs.get("pid", 0)

        damping_ratio = kwargs.get("damping_ratio", 0.03)
        period_first = kwargs.get("period_first", None)
        period_second = kwargs.get("period_second", None)

        if period_first is None or period_second is None:
            raise ValueError(
                f"Please provide two periods for Rayleigh damping. {period_first = } and {period_second = } must be provided."
            )

        mass_prop_switch = kwargs.get("mass_prop_switch", 1.0)
        stiff_init_switch = kwargs.get("stiff_init_switch", 1.0)
        stiff_curr_switch = kwargs.get("stiff_curr_switch", 0.0)
        stiff_comm_switch = kwargs.get("stiff_comm_switch", 0.0)

        omega_i = (2 * np.pi) / period_first
        omega_j = (2 * np.pi) / period_second

        # M-prop
        alpha_mass = (
            mass_prop_switch
            * damping_ratio
            * (2 * omega_i * omega_j)
            / (omega_i + omega_j)
        )
        # initial-K
        beta_stiff_init = stiff_init_switch * 2.0 * damping_ratio / (omega_i + omega_j)
        # current-K
        beta_stiff_curr = stiff_curr_switch * 2.0 * damping_ratio / (omega_i + omega_j)
        # last-committed K
        beta_stiff_comm = stiff_comm_switch * 2.0 * damping_ratio / (omega_i + omega_j)

        ops.rayleigh(alpha_mass, beta_stiff_curr, beta_stiff_init, beta_stiff_comm)

        return None

    def add_uniform_excitation(self, **kwargs) -> tuple:
        self.methods_called["add_uniform_excitation"] = True

        input_dict = kwargs.get("input_dict", {})
        if input_dict is None:
            raise ValueError(f"Please provide a dictionary of input parameters.")

        filename = input_dict.get("filename", [])
        direction = input_dict.get("direction", [])
        factor = input_dict.get("factor", [])

        if (
            len(filename) != len(direction) != len(factor)
            or not filename
            or not direction
            or not factor
        ):
            raise ValueError(
                f"Please provide the same number of filename, direction, and factor, and ensure none of them are empty."
            )
        elif not filename or not direction or not factor:
            raise ValueError(
                f"The lists of filename, direction, and factor cannot be empty."
            )

        data_dict = {}
        for item in filename:
            data_dict[item] = helper.peer_to_2D_array(
                os.path.join(self.directory, item)
            )

        dt, values = [], []
        for _, val in data_dict.items():
            self.logger.debug(f"Processed ground motion data for: {val[0]}")
            dt.append(val[1][1, 0] - val[1][0, 0])
            values.append(val[1][:, 1])

        for i in range(len(filename)):
            ops.timeSeries(
                "Path",
                int(10 + i),
                "-dt",
                dt[i],
                "-values",
                *values[i].tolist(),
                "-factor",
                factor[i] * constants.g,
            )

            ops.pattern(
                "UniformExcitation",
                int(10 + i),
                helper.get_dir(direction[i]),
                "-accel",
                int(10 + i),
            )

        if self.nprocs == 1:
            ops.wipeAnalysis()

            system = kwargs.get("system", "UmfPack")
            ops.system(system)

            numberer = kwargs.get("numberer", "RCM")
            ops.numberer(numberer)

            constraints = kwargs.get("constraints", "Transformation")
            ops.constraints(constraints)

            alpha = kwargs.get("alpha", 0.85)
            beta = kwargs.get("beta", 1.5 - alpha)
            gamma = kwargs.get("gamma", (2 - alpha) ** 2 / 4)
            ops.integrator("HHT", alpha, beta, gamma)

            tol = kwargs.get("tol", 1e-6)
            maxNumIter = kwargs.get("maxNumIter", 100)
            printFlag = kwargs.get("printFlag", 0)
            normType = kwargs.get("normType", "EnergyIncr")
            ops.test(normType, tol, maxNumIter, printFlag)

            algorithm = kwargs.get("algorithm", "KrylovNewton")
            ops.algorithm(algorithm)

            analysis = kwargs.get("analysis", "Transient")
            ops.analysis(analysis)

        else:
            ops.wipeAnalysis()
            system = kwargs.get("system", "Mumps")
            ops.system(system)

            numberer = kwargs.get("numberer", "ParallelRCM")
            ops.numberer(numberer)

            constraints = kwargs.get("constraints", "Transformation")
            ops.constraints(constraints)

            alpha = kwargs.get("alpha", 0.85)
            beta = kwargs.get("beta", 1.5 - alpha)
            gamma = kwargs.get("gamma", (2 - alpha) ** 2 / 4)
            ops.integrator("HHT", alpha, beta, gamma)

            tol = kwargs.get("tol", 1e-6)
            maxNumIter = kwargs.get("maxNumIter", 100)
            printFlag = kwargs.get("printFlag", 0)
            normType = kwargs.get("normType", "EnergyIncr")
            ops.test(normType, tol, maxNumIter, printFlag)

            algorithm = kwargs.get("algorithm", "KrylovNewton")
            ops.algorithm(algorithm)

            analysis = kwargs.get("analysis", "Transient")
            ops.analysis(analysis)

        return (dt, values)

    def add_wind_load(self, **kwargs):
        self.methods_called["add_wind_load"] = True

        return None

    def add_pushover_load(self, **kwargs) -> None:
        self.methods_called["pushover"] = True
        return None

    def add_recorder(
        self, kind=None, analysis_name=None, analysis_type=None, location=None, **kwargs
    ) -> None:
        self.methods_called["add_recorder"] = True

        if kind is None:
            raise ValueError(f"Please provide a recorder type.")

        if analysis_name is None:
            raise ValueError(f"Please provide an analysis name.")

        if analysis_type is None:
            raise ValueError(f"Please provide an analysis type.")

        pid = kwargs.get("pid", 0)
        jobid = kwargs.get("jobid", "")
        close_on_write = kwargs.get("close_on_write", False)
        dt_record = kwargs.get("dt_record", None)
        _result_type = kwargs.get("result_type", None)

        recorder_args = ["-precision", kwargs.get("precision", 10), "-time"]
        if dt_record is not None:
            if isinstance(dt_record, float):
                recorder_args.append("-dT")
                recorder_args.append(dt_record)
            else:
                raise ValueError(f"Please provide a float value for dt_record.")

        if close_on_write:
            recorder_args.append("-closeOnWrite")

        data_dir = f"{self.directory}/{jobid}_{self.name}_{analysis_name}_{analysis_type}_output"

        if not os.path.exists(data_dir) and pid == 0:
            os.makedirs(data_dir)

        if self.nprocs > 1:
            ops.barrier()

        if kind == "node":
            dof = kwargs.get("dof", [1, 2, 3, 4, 5, 6])

            if location is None:
                raise ValueError(
                    f"Please provide a location for the recorder. Available options are: 'base', 'roof', 'global', 'diaphragm', 'all', or 'node_tags'."
                )

            if _result_type is None:
                raise ValueError(
                    f"Please provide a result type for the recorder. Available options are: 'disp', 'vel', 'accel', or 'reaction'"
                )

            if not isinstance(dof, list):
                raise ValueError(f"Please provide a list of degrees of freedom.")

            base_elevation = self.generate.df_global_nodes.Z.min()
            roof_elevation = self.generate.df_global_nodes.Z.max()

            if location == "base":
                node_tags = self.generate.df_global_nodes[
                    self.generate.df_global_nodes.Z == base_elevation
                ].node.tolist()

            elif location == "roof":
                node_tags = self.generate.df_global_nodes[
                    self.generate.df_global_nodes.Z == roof_elevation
                ].node.tolist()

            elif location == "global":
                node_tags = self.generate.df_global_nodes.node.tolist()

            elif location == "diaphragm":
                node_tags = self.generate.df_diaphragms.master.tolist()

            elif location == "all":
                node_tags = ops.getNodeTags()

            elif location == "node_tags":
                node_tags = kwargs.get("node_tags", [])
                if not node_tags:
                    raise ValueError(f"Please provide a list of node tags.")

            else:
                raise ValueError(
                    f"Please provide a valid location. Available options are: 'base', 'roof', 'global', 'diaphragm', 'all', or 'node_tags'."
                )

            node_tags = [
                node_tag for node_tag in node_tags if node_tag in ops.getNodeTags()
            ]

            if _result_type == "disp":
                values = ["D1", "D2", "D3", "D4", "D5", "D6"]

            elif _result_type == "vel":
                values = ["V1", "V2", "V3", "V4", "V5", "V6"]

            elif _result_type == "accel":
                values = ["A1", "A2", "A3", "A4", "A5", "A6"]

            elif _result_type == "reaction":
                values = ["R1", "R2", "R3", "R4", "R5", "R6"]

            filename = f"{kind}_{_result_type}_{location}_{pid}"
            if node_tags:
                if filename not in self.defined_recorders:
                    ops.recorder(
                        "Node",
                        "-file",
                        f"{data_dir}/{filename}.out",
                        *recorder_args,
                        "-node",
                        *node_tags,
                        "-dof",
                        *dof,
                        *[_result_type],
                    )

                    self.defined_recorders.append(filename)

                    data_json = {
                        "info": f"This file contains the results of {analysis_name}-{analysis_type} analysis.",
                        "model_name": f"{self.name}",
                        "jobid": jobid,
                        "nprocs": self.nprocs,
                        "pid": pid,
                        "time": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "filename": f"{filename}.out",
                        "analysis_name": analysis_name,
                        "analysis_type": analysis_type,
                        "kind": kind,
                        "args": _result_type,
                        "values": values,
                        "location": location,
                        "dof": dof,
                        "time_col": True,
                        "dt_record": dt_record,
                        "num_cols": len(dof) * len(node_tags) + 1,
                        "num_rows": "num_steps",
                        "node_size": len(node_tags),
                        "node_info_columns": ["node_tag", "x", "y", "z"],
                        "node_info": [
                            [node_tag, *ops.nodeCoord(node_tag)]
                            for node_tag in node_tags
                        ],
                    }

                    with open(f"{data_dir}/{filename}.json", "w") as f:
                        json.dump(data_json, f, indent=4)

                else:
                    raise ValueError(
                        f"Recorder with the same name has already been defined."
                    )

        elif kind == "element":
            if location is None:
                raise ValueError(
                    f"Please provide a location for the recorder. Available options are: 'column', 'brace', 'floor_beam', 'ceiling_beam', 'ver_con', 'hor_con', 'all', or 'ele_tags'."
                )

            df = pd.DataFrame(self.list_recorder)

            if len(df.columns) == 4:
                df.columns = ["location", "ele_info", "tag", "result_type"]
            elif len(df.columns) == 5:
                df.columns = ["location", "ele_info", "tag", "result_type", "section"]

            parameters = [
                {
                    "location": "column",
                    "element_types": ["column_element", "column_hinge"],
                    "result_types": [
                        [["localForce"], ["globalForce"]],
                        [["force"], ["deformation"]],
                    ],
                    "suffixes": ["elastic", "hinge"],
                    "num_cols_multipliers": [[12, 12], [12, 2]],
                },
                {
                    "location": "brace",
                    "element_types": ["brace_element", "brace_spring", "brace_element"],
                    "result_types": [
                        [["basicDeformation"], ["localForce"]],
                        [["force"], ["deformation"]],
                        [
                            ["section_force"],
                            ["section_deformation"],
                            ["section_stiffness"],
                            ["section_fiber_top"],
                            ["section_fiber_bottom"],
                            ["section_fiber_left"],
                            ["section_fiber_right"],
                        ],
                    ],
                    "suffixes": ["inelastic", "spring", "section"],
                    "num_cols_multipliers": [
                        [6, 12],
                        [12, 1],
                        [4, 1, 4, 2, 2, 2, 2],
                    ],
                },
                {
                    "location": "floor_beam",
                    "element_types": ["floor_beam_element", "floor_beam_hinge"],
                    "result_types": [
                        [["localForce"], ["globalForce"]],
                        [["force"], ["deformation"]],
                    ],
                    "suffixes": ["elastic", "hinge"],
                    "num_cols_multipliers": [[12, 12], [12, 1]],
                },
                {
                    "location": "ceiling_beam",
                    "element_types": ["ceiling_beam_element", "ceiling_beam_hinge"],
                    "result_types": [
                        [["localForce"], ["globalForce"]],
                        [["force"], ["deformation"]],
                    ],
                    "suffixes": ["elastic", "hinge"],
                    "num_cols_multipliers": [[12, 12], [12, 1]],
                },
                {
                    "location": "ver_con",
                    "element_types": ["ver_con_element"],
                    "result_types": [[["basicDeformation"], ["localForce"]]],
                    "suffixes": ["inelastic"],
                    "num_cols_multipliers": [[6, 12]],
                },
                {
                    "location": "hor_con",
                    "element_types": ["hor_con_element"],
                    "result_types": [[["localForce"], ["globalForce"]]],
                    "suffixes": ["elastic"],
                    "num_cols_multipliers": [[12, 12]],
                },
            ]

            for param in parameters:
                if location == param["location"]:
                    for element_type, result_types, suffix, num_cols_multiplier in zip(
                        param["element_types"],
                        param["result_types"],
                        param["suffixes"],
                        param["num_cols_multipliers"],
                    ):
                        elements = df[df["location"] == element_type].tag.tolist()
                        ele_info = df[df["location"] == element_type].ele_info.tolist()

                        if location == "brace":
                            result_types_flatten = [
                                item for sublist in result_types for item in sublist
                            ]

                        for i_result_type, result_type in enumerate(result_types):
                            if (
                                location == "brace"
                                and result_type[0].startswith("section")
                                and _result_type is not None
                            ):
                                if "section" in df.columns:
                                    df["section"] = df["section"].apply(
                                        lambda x: tuple(round(i, 6) for i in x)
                                        if x is not None
                                        else None
                                    )

                                    df_section = (
                                        df[df["location"] == "brace_element"]
                                        .groupby("section")
                                        .agg({"tag": list})
                                    ).reset_index(drop=False)

                                if _result_type not in result_types_flatten:
                                    raise ValueError(
                                        f"Please provide a result type for the recorder. Available options are: {result_types_flatten}."
                                    )
                                elif _result_type == "section_force":
                                    result_type = ["section", "3", "force"]
                                    filename = f"{kind}_{location}_{_result_type}_{pid}"
                                    values = ["P", "Mz", "My", "T"]

                                elif _result_type == "section_deformation":
                                    result_type = ["section", "3", "deformation"]
                                    filename = f"{kind}_{location}_{_result_type}_{pid}"
                                    values = ["eps", "kappaZ", "kappaY", "theta"]

                                elif _result_type == "section_stiffness":
                                    result_type = ["section", "3", "stiffness"]
                                    filename = f"{kind}_{location}_{_result_type}_{pid}"
                                    values = ["K"]

                                elif (
                                    _result_type
                                    in [
                                        "section_fiber_top",
                                        "section_fiber_bottom",
                                        "section_fiber_left",
                                        "section_fiber_right",
                                    ]
                                    and not df_section.empty
                                ):
                                    for row in df_section.itertuples():
                                        sec_D, sec_B = row.section
                                        elements = row.tag
                                        if _result_type == "section_fiber_top":
                                            result_type = [
                                                "section",
                                                "3",
                                                "fiber",
                                                f"{sec_D*0.5}",
                                                f"0.0",
                                                "stressStrain",
                                            ]
                                            position = [
                                                "top-center",
                                                {
                                                    "y": f"{sec_D*0.5}",
                                                    "z": f"0.0",
                                                },
                                            ]
                                        elif _result_type == "section_fiber_bottom":
                                            result_type = [
                                                "section",
                                                "3",
                                                "fiber",
                                                f"{-sec_D*0.5}",
                                                f"0.0",
                                                "stressStrain",
                                            ]
                                            position = [
                                                "bottom-center",
                                                {
                                                    "y": f"{-sec_D*0.5}",
                                                    "z": f"0.0",
                                                },
                                            ]
                                        elif _result_type == "section_fiber_left":
                                            result_type = [
                                                "section",
                                                "3",
                                                "fiber",
                                                f"0.0",
                                                f"{-sec_B*0.5}",
                                                "stressStrain",
                                            ]
                                            position = [
                                                "left-center",
                                                {
                                                    "y": f"0.0",
                                                    "z": f"{-sec_B*0.5}",
                                                },
                                            ]
                                        elif _result_type == "section_fiber_right":
                                            result_type = [
                                                "section",
                                                "3",
                                                "fiber",
                                                f"0.0",
                                                f"{sec_B*0.5}",
                                                "stressStrain",
                                            ]
                                            position = [
                                                "right-center",
                                                {
                                                    "y": f"0.0",
                                                    "z": f"{sec_B*0.5}",
                                                },
                                            ]

                                        filename = f"{kind}_{location}_{_result_type}_stressStrain_idx{row.Index}_{pid}"

                                        if filename not in self.defined_recorders:
                                            ops.recorder(
                                                "Element",
                                                "-file",
                                                f"{data_dir}/{filename}.out",
                                                *recorder_args,
                                                "-ele",
                                                *elements,
                                                *result_type,
                                            )

                                            self.defined_recorders.append(
                                                f"{filename}.out"
                                            )

                                            data_json = {
                                                "info": f"This file contains the results of {analysis_name}-{analysis_type} analysis.",
                                                "model_name": f"{self.name}",
                                                "jobid": jobid,
                                                "nprocs": self.nprocs,
                                                "pid": pid,
                                                "time": pd.Timestamp.now().strftime(
                                                    "%Y-%m-%d %H:%M:%S"
                                                ),
                                                "filename": f"{filename}.out",
                                                "analysis_name": analysis_name,
                                                "analysis_type": analysis_type,
                                                "kind": kind,
                                                "result_type": _result_type,
                                                "args": result_type,
                                                "values": ["sig11", "eps11"],
                                                "location": location,
                                                "position": position,
                                                "sec_D": sec_D,
                                                "sec_B": sec_B,
                                                "dof": None,
                                                "time_col": True,
                                                "dt_record": dt_record,
                                                "num_cols": len(elements)
                                                * num_cols_multiplier[i_result_type]
                                                + 1,
                                                "num_rows": "num_steps",
                                                "ele_size": len(elements),
                                                "ele_info": ele_info,
                                                "ele_tags": elements,
                                                "ele_nodes": [
                                                    ops.eleNodes(item)
                                                    for item in elements
                                                ],
                                            }

                                            with open(
                                                f"{data_dir}/{filename}.json", "w"
                                            ) as f:
                                                json.dump(data_json, f, indent=4)

                                        else:
                                            raise ValueError(
                                                f"Recorder with the same name has already been defined."
                                            )

                                    break

                                if filename not in self.defined_recorders:
                                    ops.recorder(
                                        "Element",
                                        "-file",
                                        f"{data_dir}/{filename}.out",
                                        *recorder_args,
                                        "-ele",
                                        *elements,
                                        *result_type,
                                    )

                                    self.defined_recorders.append(filename)

                                    data_json = {
                                        "info": f"This file contains the results of {analysis_name}-{analysis_type} analysis.",
                                        "model_name": f"{self.name}",
                                        "jobid": jobid,
                                        "nprocs": self.nprocs,
                                        "pid": pid,
                                        "time": pd.Timestamp.now().strftime(
                                            "%Y-%m-%d %H:%M:%S"
                                        ),
                                        "filename": f"{filename}.out",
                                        "analysis_name": analysis_name,
                                        "analysis_type": analysis_type,
                                        "kind": kind,
                                        "args": result_type,
                                        "values": values,
                                        "location": location,
                                        "dof": None,
                                        "time_col": True,
                                        "dt_record": dt_record,
                                        "num_cols": len(elements)
                                        * num_cols_multiplier[i_result_type]
                                        + 1,
                                        "num_rows": "num_steps",
                                        "ele_size": len(elements),
                                        "ele_info": ele_info,
                                        "ele_tags": elements,
                                        "ele_nodes": [
                                            ops.eleNodes(item) for item in elements
                                        ],
                                    }

                                    with open(f"{data_dir}/{filename}.json", "w") as f:
                                        json.dump(data_json, f, indent=4)

                            if _result_type is None:
                                if not result_type[0].startswith("section"):
                                    filename = f"{kind}_{location}_{result_type[0]}_{suffix}_{pid}"

                                if result_type[0] == "basicDeformation":
                                    values = [
                                        "eps",
                                        "thetaZ_1",
                                        "thetaZ_2",
                                        "thetaY_1",
                                        "thetaY_2",
                                        "thetaX",
                                    ]

                                elif result_type[0] == "localForce":
                                    values = [
                                        "N_1",
                                        "Vy_1",
                                        "Vz_1",
                                        "T_1",
                                        "My_1",
                                        "Mz_1",
                                        "N_2",
                                        "Vy_2",
                                        "Vz_2",
                                        "T_2",
                                        "My_2",
                                        "Mz_2",
                                    ]

                                elif result_type[0] == "globalForce":
                                    values = [
                                        "Px_1",
                                        "Py_1",
                                        "Pz_1",
                                        "Mx_1",
                                        "My_1",
                                        "Mz_1",
                                        "Px_2",
                                        "Py_2",
                                        "Pz_2",
                                        "Mx_2",
                                        "My_2",
                                        "Mz_2",
                                    ]

                                elif result_type[0] == "deformation":
                                    if num_cols_multiplier[i_result_type] == 1:
                                        values = ["e1"]
                                    elif num_cols_multiplier[i_result_type] == 2:
                                        values = ["e1", "e2"]

                                elif result_type[0] == "force":
                                    values = [
                                        "P1_1",
                                        "P1_2",
                                        "P1_3",
                                        "P1_4",
                                        "P1_5",
                                        "P1_6",
                                        "P2_1",
                                        "P2_2",
                                        "P2_3",
                                        "P2_4",
                                        "P2_5",
                                        "P2_6",
                                    ]

                                if filename not in self.defined_recorders:
                                    ops.recorder(
                                        "Element",
                                        "-file",
                                        f"{data_dir}/{filename}.out",
                                        *recorder_args,
                                        "-ele",
                                        *elements,
                                        *result_type,
                                    )

                                    self.defined_recorders.append(filename)

                                    data_json = {
                                        "info": f"This file contains the results of {analysis_name}-{analysis_type} analysis.",
                                        "model_name": f"{self.name}",
                                        "jobid": jobid,
                                        "nprocs": self.nprocs,
                                        "pid": pid,
                                        "time": pd.Timestamp.now().strftime(
                                            "%Y-%m-%d %H:%M:%S"
                                        ),
                                        "filename": f"{filename}.out",
                                        "analysis_name": analysis_name,
                                        "analysis_type": analysis_type,
                                        "kind": kind,
                                        "args": result_type,
                                        "values": values,
                                        "location": location,
                                        "dof": None,
                                        "time_col": True,
                                        "dt_record": dt_record,
                                        "num_cols": len(elements)
                                        * num_cols_multiplier[i_result_type]
                                        + 1,
                                        "num_rows": "num_steps",
                                        "ele_size": len(elements),
                                        "ele_info": ele_info,
                                        "ele_tags": elements,
                                        "ele_nodes": [
                                            ops.eleNodes(item) for item in elements
                                        ],
                                    }

                                    with open(f"{data_dir}/{filename}.json", "w") as f:
                                        json.dump(data_json, f, indent=4)

        return None

    def remove_recorder(self, **kwargs) -> None:
        self.methods_called["remove_recorder"] = True
        self.defined_recorders = []
        ops.remove("recorders")
        return None

    def _save_model(self, **kwargs) -> None:
        self.methods_called["save_model"] = True

        pid = kwargs.get("pid", 0)
        jobid = kwargs.get("jobid", "")

        data_json = {
            "info": f"This file contains the model information.",
            "model_name": f"{self.name}",
            "jobid": jobid,
            "nprocs": self.nprocs,
            "time": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "node_tags": ops.getNodeTags(),
            "element_tags": ops.getEleTags(),
            "node_tags_global": self.generate.df_global_nodes.to_dict(orient="records"),
            "df_brace_elements": self.generate.df_brace_elements.to_dict(
                orient="records"
            ),
            "df_brace_positions": self.generate.df_brace_positions.to_dict(
                orient="records"
            ),
            "df_brace_sections": self.generate.df_brace_sections.to_dict(
                orient="records"
            ),
            "df_ceiling_beam_elements": self.generate.df_ceiling_beam_elements.to_dict(
                orient="records"
            ),
            "df_ceiling_braced_sections": self.generate.df_ceiling_braced_sections.to_dict(
                orient="records"
            ),
            "df_ceiling_loads": self.generate.df_ceiling_loads.to_dict(
                orient="records"
            ),
            "df_ceiling_regular_sections": self.generate.df_ceiling_regular_sections.to_dict(
                orient="records"
            ),
            "df_column_elements": self.generate.df_column_elements.to_dict(
                orient="records"
            ),
            "df_column_sections": self.generate.df_column_sections.to_dict(
                orient="records"
            ),
            "df_corner_neighbors": self.generate.df_corner_neighbors.to_dict(
                orient="records"
            ),
            "df_diaphragms": self.generate.df_diaphragms.to_dict(orient="records"),
            "df_floor_beam_elements": self.generate.df_floor_beam_elements.to_dict(
                orient="records"
            ),
            "df_floor_braced_sections": self.generate.df_floor_braced_sections.to_dict(
                orient="records"
            ),
            "df_floor_loads": self.generate.df_floor_loads.to_dict(orient="records"),
            "df_floor_regular_sections": self.generate.df_floor_regular_sections.to_dict(
                orient="records"
            ),
            "df_geo_transf": self.generate.df_geo_transf.to_dict(orient="records"),
            "df_global_nodes": self.generate.df_global_nodes.to_dict(orient="records"),
            "df_global_nodes_fix": self.generate.df_global_nodes_fix.to_dict(
                orient="records"
            ),
            "df_grid_x": self.generate.df_grid_x.to_dict(orient="records"),
            "df_grid_y": self.generate.df_grid_y.to_dict(orient="records"),
            "df_height": self.generate.df_height.to_dict(orient="records"),
            "df_hor_con_elements": self.generate.df_hor_con_elements.to_dict(
                orient="records"
            ),
            "df_hor_con_elements_filtered": self.generate.df_hor_con_elements_filtered.to_dict(
                orient="records"
            ),
            "df_inter_braced": self.generate.df_inter_braced.to_dict(orient="records"),
            "df_inter_unbraced": self.generate.df_inter_unbraced.to_dict(
                orient="records"
            ),
            "df_intra_braced": self.generate.df_intra_braced.to_dict(orient="records"),
            "df_intra_unbraced": self.generate.df_intra_unbraced.to_dict(
                orient="records"
            ),
            "df_load_factors": self.generate.df_load_factors.to_dict(orient="records"),
            "df_module_coords": self.generate.df_module_coords.to_dict(
                orient="records"
            ),
            "df_module_mid_nodes": self.generate.df_module_mid_nodes.to_dict(
                orient="records"
            ),
            # FIXME: df_modules causes error in json.dump that's why it's commented out
            # "df_modules": self.generate.df_modules.to_dict(orient="records"),
            "df_partition": self.generate.df_partition.to_dict(orient="records"),
            "df_point_neighbors": self.generate.df_point_neighbors.to_dict(
                orient="records"
            ),
            "df_section_material": self.generate.df_section_material.to_dict(
                orient="records"
            ),
            "df_self_weight_diaphragms": self.generate.df_self_weight_diaphragms.to_dict(
                orient="records"
            ),
            "df_self_weight_elements": self.generate.df_self_weight_elements.to_dict(
                orient="records"
            ),
            "df_steel_HSS": self.generate.df_steel_HSS.to_dict(orient="records"),
            "df_steel_W": self.generate.df_steel_W.to_dict(orient="records"),
            "df_ver_con_elements": self.generate.df_ver_con_elements.to_dict(
                orient="records"
            ),
            "masses": self.list_mass,
            "recorders": self.defined_recorders,
            "elastic_ceiling_beam": self.elastic_ceiling_beam,
            "elastic_floor_beam": self.elastic_floor_beam,
            "elastic_column": self.elastic_column,
            "elastic_brace": self.elastic_brace,
            "elastic_ver_con": self.elastic_ver_con,
            "elastic_hor_con": self.elastic_hor_con,
            "include_fatigue": self.include_fatigue,
            "include_element_mass": self.include_element_mass,
        }

        with open(f"{self.directory}/{jobid}_{self.name}_model_{pid}.json", "w") as f:
            json.dump(data_json, f, indent=4, cls=_CustomEncoder)

        return None

    def eigenvalue(self, num_values=None, **kwargs):
        self.methods_called["eigenvalue"] = True

        if num_values is None:
            raise ValueError(f"Please provide a number of eigenvalues.")

        if self.nprocs > 1:
            raise ValueError(f"Eigenvalue analysis is not supported in parallel mode.")

        _print = kwargs.get("print", False)
        save = kwargs.get("save", True)
        return_values = kwargs.get("return_values", False)

        ops.system("UmfPack")
        eigvalues = ops.eigen("-genBandArpack", num_values)

        if save and _print:
            ops.modalProperties(
                "-print",
                "-file",
                f"{self.directory}/{self.name}_modal_report.txt",
                "-unorm",
            )

            self.logger.info(f"Modal report is saved to the given directory.")

        elif save and not _print:
            ops.modalProperties(
                "-file", f"{self.directory}/{self.name}_modal_report.txt", "-unorm"
            )

            self.logger.info(f"Modal report is saved to the given directory.")

        elif not save and _print:
            ops.modalProperties("-print", "-unorm")

        else:
            ops.modalProperties("-unorm")

        if return_values:
            return eigvalues
        else:
            return None

        # list_eigenvalues = []

        # for row in df_rigid_diaphragms_merged.iterrows():
        #     for mode, dof in zip([1, 2], [2, 1]):
        #         list_eigenvalues.append([int(row[1].master), mode, dof, ops.nodeEigenvector(int(row[1].master), mode, dof)])

        # df_eigenvectors = pd.DataFrame(list_eigenvalues, columns=["node", "mode", "dof", "eigenvector"])

    def _test(self) -> None:
        ops.start()
        # truss model
        # 8 nodes and 13 elements
        #     6    8    7
        #     -----------
        #    /|\   |   /|\
        #   / | \  |  / | \
        #  /  |  \ | /  |  \
        # /   |   \|/   |   \
        # -------------------
        # 1   2    3    4   5

        # auto_partition = True
        auto_partition = False

        pid = ops.getPID()
        logger = _Logger(
            self.directory,
            filename=f"mbp_parallel_{pid}",
            mode="w",
            console="critical",
            file="debug",
        ).get()

        ops.wipe()
        ops.model("basic", "-ndm", 2, "-ndf", 2)
        ops.uniaxialMaterial("Elastic", 1, 3000.0)

        if auto_partition:
            if pid == 0:
                logger.debug(f"AUTO PARTITIONING")

            ops.node(1, 0.0, 0.0)
            ops.node(2, 72.0, 0.0)
            ops.node(3, 144.0, 0.0)
            ops.node(6, 72.0, 96.0)
            ops.node(8, 144.0, 96.0)

            ops.fix(1, 1, 1)

            ops.element("Truss", 1, 1, 6, 10.0, 1)
            ops.element("Truss", 2, 1, 2, 10.0, 1)
            ops.element("Truss", 3, 2, 6, 10.0, 1)
            ops.element("Truss", 4, 2, 3, 10.0, 1)
            ops.element("Truss", 5, 3, 6, 10.0, 1)
            ops.element("Truss", 6, 3, 8, 10.0, 1)
            ops.element("Truss", 12, 6, 8, 10.0, 1)

            ops.node(4, 216.0, 0.0)
            ops.node(5, 288.0, 0.0)
            ops.node(7, 216.0, 96.0)

            ops.fix(5, 1, 1)

            ops.element("Truss", 7, 3, 7, 5.0, 1)
            ops.element("Truss", 8, 4, 7, 5.0, 1)
            ops.element("Truss", 9, 5, 7, 5.0, 1)
            ops.element("Truss", 10, 3, 4, 5.0, 1)
            ops.element("Truss", 11, 4, 5, 5.0, 1)
            ops.element("Truss", 13, 7, 8, 5.0, 1)

            ops.timeSeries(
                "Path",
                1,
                "-time",
                *np.arange(0.1, 1.1, 0.1).tolist(),
                "-values",
                *np.arange(1, 11, 1).astype(float).tolist(),
                "-factor",
                10.0,
            )
            ops.pattern("Plain", 1, 1)
            ops.load(8, *[1.0, 0.0])

            ops.partition("-ncuts", 10, "-niter", 100, "-ufactor", 3)

        else:  # User defined partitioning
            if pid == 0:
                logger.debug(f"USER DEFINED PARTITIONING")
                ops.node(1, 0.0, 0.0)
                ops.node(2, 72.0, 0.0)
                ops.node(3, 144.0, 0.0)
                ops.node(6, 72.0, 96.0)
                ops.node(8, 144.0, 96.0)

                ops.fix(1, 1, 1)

                ops.element("Truss", 1, 1, 6, 10.0, 1)
                ops.element("Truss", 2, 1, 2, 10.0, 1)
                ops.element("Truss", 3, 2, 6, 10.0, 1)
                ops.element("Truss", 4, 2, 3, 10.0, 1)
                ops.element("Truss", 5, 3, 6, 10.0, 1)
                ops.element("Truss", 6, 3, 8, 10.0, 1)
                ops.element("Truss", 12, 6, 8, 10.0, 1)
                ops.timeSeries(
                    "Path",
                    1,
                    "-time",
                    *np.arange(0.1, 1.1, 0.1).tolist(),
                    "-values",
                    *np.arange(1, 11, 1).astype(float).tolist(),
                    "-factor",
                    10.0,
                )
                ops.pattern("Plain", 1, 1)
                ops.load(8, *[1.0, 0.0])

            # common nodes (This is necessary!)
            if pid == 1 or np == 1:
                if pid == 1:
                    ops.node(3, 144.0, 0.0)
                    ops.node(8, 144.0, 96.0)

                ops.node(4, 216.0, 0.0)
                ops.node(5, 288.0, 0.0)
                ops.node(7, 216.0, 96.0)

                ops.fix(5, 1, 1)

                ops.element("Truss", 7, 3, 7, 5.0, 1)
                ops.element("Truss", 8, 4, 7, 5.0, 1)
                ops.element("Truss", 9, 5, 7, 5.0, 1)
                ops.element("Truss", 10, 3, 4, 5.0, 1)
                ops.element("Truss", 11, 4, 5, 5.0, 1)
                ops.element("Truss", 13, 7, 8, 5.0, 1)

        nodes = ops.getNodeTags()
        eles = ops.getEleTags()

        if pid == 0:
            test_message = "Hello from master"
            ops.send("-pid", 1, *[test_message])
            logger.debug(f"{pid = } {test_message = }")
        else:
            test_message = ops.recv("-pid", 0)
            logger.debug(f"{pid = } {test_message = }")

        logger.debug(f"Partition {pid}")
        logger.debug(f"{nodes =}")
        logger.debug(f"{eles =}")

        ops.recorder(
            "Node",
            "-file",
            f"{self.directory}/node_disp_{pid}.out",
            "-time",
            "-node",
            *nodes,
            "-dof",
            *[1, 2, 3, 4, 5, 6],
            "disp",
        )

        np.savetxt(f"{self.directory}/node_disp_tags_{pid}.out", nodes, fmt="%d")

        ops.barrier()
        ops.wipeAnalysis()
        ops.system("Mumps")
        ops.numberer("ParallelRCM")
        ops.constraints("Transformation")
        ops.test("NormDispIncr", 1e-12, 200, 0)
        ops.algorithm("KrylovNewton")
        ops.integrator("Newmark", 0.5, 0.25)
        ops.analysis("Transient")

        for _ in range(10):
            ops.analyze(1, 0.1)
            if pid == 0:
                # pass
                # logger.debug('Node 8: ', [ops.nodeCoord(8), ops.nodeDisp(8)])
                logger.debug(f"Node 8: {ops.nodeCoord(8), ops.nodeDisp(8)}")
                # Node 8:  [[144.0, 96.0], [0.6766666666666666, -0.29833333333333334]]
        ops.stop()
        return None
        # return "DONE!"

    def _serial_model(self, **kwargs) -> None:
        analysis_name = kwargs.get("analysis_name", "")
        time_analyze = kwargs.get("time_analyze", None)
        dt_analyze = kwargs.get("dt_analyze", None)
        time_job = kwargs.get("time_job", 1e9)
        free_vibration = kwargs.get("free_vibration", 0.0)

        time_gen = self.timer()
        next(time_gen)

        jobid = os.environ.get("SLURM_JOB_ID", "")
        if not jobid:
            jobid = 1_000_001

        self.initialize_ops()
        self.declare_global_var()
        self.assign_section_material()
        self.assign_geo_transf()
        self.assign_node()
        self.assign_diaphragm()
        self.assign_element()
        self.add_mass()
        num_steps = 10
        self.add_gravity_load(num_steps=num_steps)

        self.logger.debug(f"Model generation took {next(time_gen):.2f} seconds.")

        self.logger.info(
            f"Now, gravity analysis having {num_steps} steps is just started."
        )

        analysis_type = "gravity"

        for item, result_type in zip(
            [
                "base",
                "roof",
                "global",
                "global",
                "global",
                "diaphragm",
                "diaphragm",
                "diaphragm",
            ],
            ["reaction", "disp", "disp", "vel", "accel", "disp", "vel", "accel"],
        ):
            self.add_recorder(
                kind="node",
                analysis_name=analysis_name,
                analysis_type=analysis_type,
                location=item,
                result_type=result_type,
                jobid=jobid,
                pid=0,
            )

        for item in [
            "column",
            "ver_con",
            "floor_beam",
            "ceiling_beam",
            "hor_con",
            "brace",
        ]:
            self.add_recorder(
                kind="element",
                analysis_name=analysis_name,
                analysis_type=analysis_type,
                location=item,
                jobid=jobid,
                pid=0,
            )

        for item in [
            "section_force",
            "section_deformation",
            "section_stiffness",
            "section_fiber_top",
            "section_fiber_bottom",
            "section_fiber_left",
            "section_fiber_right",
        ]:
            self.add_recorder(
                kind="element",
                analysis_name=analysis_name,
                analysis_type=analysis_type,
                location="brace",
                result_type=item,
                jobid=jobid,
                pid=0,
            )

        if self.save_model:
            self._save_model(pid=0, jobid=jobid)

        for i in range(num_steps):
            ops.analyze(1)
            self.logger.info(f"Step {i + 1} is completed.")
            sys.stdout.flush()
            if i == 0:
                break

        df = pd.DataFrame(self.list_recorder)
        if len(df.columns) == 4:
            df.columns = ["location", "ele_info", "ele_number", "ele_type"]
        elif len(df.columns) == 5:
            df.columns = ["location", "ele_info", "ele_number", "ele_type", "section"]

        col_ele = df[df["location"] == "column_element"].ele_number.tolist()
        df_column_gravity = pd.DataFrame(
            [[item, -ops.basicForce(item)[0]] for item in col_ele],
            columns=["ele_number", "axial_force"],
        ).set_index("ele_number")

        df_column_gravity.to_pickle(
            f"{self.directory}/{self.name}_df_column_gravity.pkl"
        )

        ops.loadConst("-time", 0.0)

        self.logger.info(f"Gravity loads succesfully are added to the model.")
        self.logger.info(f"Gravity analysis took {next(time_gen):.2f} seconds.")

        self.remove_recorder()
        analysis_type = "timehistory"

        for item, result_type in zip(
            [
                "base",
                "roof",
                "global",
                "global",
                "global",
                "diaphragm",
                "diaphragm",
                "diaphragm",
            ],
            ["reaction", "disp", "disp", "vel", "accel", "disp", "vel", "accel"],
        ):
            self.add_recorder(
                kind="node",
                analysis_name=analysis_name,
                analysis_type=analysis_type,
                location=item,
                result_type=result_type,
                jobid=jobid,
                pid=0,
            )

        for item in [
            "column",
            "ver_con",
            "floor_beam",
            "ceiling_beam",
            "hor_con",
            "brace",
        ]:
            self.add_recorder(
                kind="element",
                analysis_name=analysis_name,
                analysis_type=analysis_type,
                location=item,
                jobid=jobid,
                pid=0,
            )

        for item in [
            "section_force",
            "section_deformation",
            "section_stiffness",
            "section_fiber_top",
            "section_fiber_bottom",
            "section_fiber_left",
            "section_fiber_right",
        ]:
            self.add_recorder(
                kind="element",
                analysis_name=analysis_name,
                analysis_type=analysis_type,
                location="brace",
                result_type=item,
                jobid=jobid,
                pid=0,
            )

        self.add_rayleigh_damping(
            damping_ratio=0.03, period_first=5.12, period_second=1.012
        )
        dt, values = self.add_uniform_excitation(
            input_dict={
                "filename": [
                    "data/RSN165_IMPVALL.H_H-CHI012.AT2",
                    "data/RSN165_IMPVALL.H_H-CHI282.AT2",
                ],
                "direction": [1, 2],
                "factor": [1.0, 1.0],
            }
        )
        if dt_analyze is None:
            dt_analyze = dt[0]
            self.logger.debug(f"dt_analyze is set to {dt_analyze} seconds.")

        if time_analyze is None:
            time_analyze = dt_analyze * len(values[0])

        dt_initial = dt_analyze
        t_current = ops.getTime()
        t_end_analysis = time_analyze + free_vibration
        t_end_time_history = dt_analyze * len(values[0])

        status = 0
        count_success = 0
        count_failure = 0

        self.logger.info(f"Total number of steps = {int(t_end_analysis / dt_initial)}")
        self.logger.info(
            f"Total time for analysis including {free_vibration} sec free vibration phase = {t_end_analysis} sec\n"
        )
        self.logger.info(
            f"Time history analysis is started. Time increment = {dt_initial} sec"
        )

        self.logger.info(
            f"The total job time is set to {time_job} sec (Real-time). The analysis will be terminated after {time_job} sec."
        )

        start_time = time.time()
        while t_current < t_end_analysis:
            status = ops.analyze(1, dt_analyze)

            if status == 0 and t_current < t_end_time_history and count_failure == 0:
                count_success += 1
                count_failure = 0
                t_current = ops.getTime()
                t_nextstep = t_current + dt_initial

                self.logger.info(
                    f"current time = {t_current:.6f} sec | remaining time = {t_end_analysis - t_current:.6f} sec | progress = {t_current / t_end_analysis * 100:.2f}%"
                )

            if status == 0 and t_current < t_end_time_history and count_failure != 0:
                t_current = ops.getTime()
                dt = np.min([dt * 1.2, t_nextstep - t_current])

                if dt < 1e-6:
                    count_failure = 0
                    dt = dt_initial

                self.logger.debug(
                    f"Recovering from failure... Current time increment = {dt:.6f} sec and t_current = {t_current:.6f} sec"
                )

            if status == 0 and t_current >= t_end_time_history and count_failure == 0:
                count_success += 1
                count_failure = 0

                t_current = ops.getTime()
                t_nextstep = t_current + dt_initial

                self.logger.debug(
                    f"Free vibration phase is running. Remaining time = {t_end_analysis - t_current:.2f} sec | remaining steps = {int((t_end_analysis - t_current) / dt)} | progress = {t_current / t_end_analysis * 100:.2f}%"
                )

            if status != 0:
                dt *= 0.5
                count_success = 0
                count_failure += 1

                self.logger.debug(
                    f"Failure #{int(count_failure)} -> Time increment has been halved! Current time increment = {dt:.6f} sec and remaining time = {t_end_analysis - t_current:.2f} sec"
                )

            sys.stdout.flush()
            current_time = time.time()
            if current_time - start_time > time_job:
                self.logger.info(
                    f"Time limit ({time_job} sec) is reached. The analysis is terminated."
                )
                break

        return None

    def _parallel_model(self, **kwargs) -> None:
        analysis_name = kwargs.get("analysis_name", "")
        time_analyze = kwargs.get("time_analyze", None)
        dt_analyze = kwargs.get("dt_analyze", None)
        time_job = kwargs.get("time_job", 1e9)
        free_vibration = kwargs.get("free_vibration", 0.0)

        time_gen = self.timer()
        next(time_gen)

        jobid = os.environ.get("SLURM_JOB_ID", "")
        if not jobid:
            jobid = 1_000_001

        pid = ops.getPID()
        nprocs = ops.getNP()
        tmp = f"{self.directory}/tmp"
        if pid == 0:
            if os.path.exists(f"{tmp}") and os.path.isdir(f"{tmp}"):
                shutil.rmtree(f"{tmp}")
                os.makedirs(f"{tmp}")
            else:
                os.makedirs(f"{tmp}")

        ops.barrier()

        logger = _Logger(
            self.directory,
            filename=f"mbp_parallel_{pid}",
            mode="w",
            console="critical",
            file="debug",
        ).get()

        logger.debug(f"The number of processes: {nprocs} ({nprocs = })")
        logger.debug(f"Process id: {pid} ({pid = })")
        logger.debug(f"Model name: {self.name}")
        logger.debug(f"Python version: {sys.version}")
        logger.debug(
            f"Analysis start date and time: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        logger.debug(f"Job id: {jobid}")

        self.initialize_ops()
        self.declare_global_var()
        self.assign_section_material()
        self.assign_geo_transf()
        self.assign_node(pid=pid)

        df_ceiling, df_floor = self.assign_diaphragm(pid=pid)
        df_ceiling.to_pickle(f"{tmp}/df_ceiling_{pid}.pkl")
        df_floor.to_pickle(f"{tmp}/df_floor_{pid}.pkl")

        ops.barrier()

        if pid == 0:
            dataframes = {"df_ceiling": pd.DataFrame(), "df_floor": pd.DataFrame()}

            for df_name in dataframes.keys():
                for i in range(self.nprocs):
                    dataframes[df_name] = pd.concat(
                        [
                            dataframes[df_name],
                            pd.read_pickle(f"{tmp}/{df_name}_{i}.pkl"),
                        ],
                        ignore_index=False,
                    )

                dataframes[df_name] = dataframes[df_name][
                    ~dataframes[df_name].index.duplicated(keep="first")
                ]
                dataframes[df_name] = dataframes[df_name].sort_index()
                dataframes[df_name].to_pickle(f"{tmp}/{df_name}.pkl")

        ops.barrier()

        df_ceiling = pd.read_pickle(f"{tmp}/df_ceiling.pkl")
        df_floor = pd.read_pickle(f"{tmp}/df_floor.pkl")

        df_global_nodes_local = pd.DataFrame(ops.getNodeTags(), columns=["node"])
        df_global_nodes_local["pid"] = pid
        df_global_nodes_local.to_pickle(f"{tmp}/df_global_nodes_local_{pid}.pkl")

        ops.barrier()
        if pid == 0:
            df_global_nodes_local = pd.DataFrame()
            for i in range(self.nprocs):
                df_global_nodes_local = pd.concat(
                    [
                        df_global_nodes_local,
                        pd.read_pickle(f"{tmp}/df_global_nodes_local_{i}.pkl"),
                    ],
                    ignore_index=False,
                )

            df_global_nodes_local = df_global_nodes_local.reset_index(drop=True)
            df_global_nodes_local = df_global_nodes_local.sort_values(
                by=["pid", "node"]
            )
            df_global_nodes_local.to_pickle(f"{tmp}/df_global_nodes_local.pkl")

        ops.barrier()

        df_global_nodes_local = pd.read_pickle(f"{tmp}/df_global_nodes_local.pkl")

        self.assign_element(pid=pid)
        self.add_mass(pid=pid)

        ops.barrier()
        df_node_mass_local = pd.DataFrame(
            [[item, *ops.nodeMass(item)] for item in ops.getNodeTags()],
            columns=["node", "MX", "MY", "MZ", "MRX", "MRY", "MRZ"],
        )
        df_node_mass_local.to_pickle(f"{tmp}/df_node_mass_local_{pid}.pkl")

        ops.barrier()
        if pid == 0:
            df_node_mass_local = pd.DataFrame()
            for i in range(self.nprocs):
                df_node_mass_local = pd.concat(
                    [
                        df_node_mass_local,
                        pd.read_pickle(f"{tmp}/df_node_mass_local_{i}.pkl"),
                    ],
                    ignore_index=False,
                )

            df_node_mass_local = df_node_mass_local.reset_index(drop=True).sum()
            for item in ["MX", "MY"]:
                logger.debug(
                    f"Total mass in {item}: {df_node_mass_local[item]:.2f} tons"
                )
            for item in ["MRZ"]:
                logger.debug(
                    f"Total mass in {item}: {df_node_mass_local[item]:.2f} tons-m2"
                )

        ops.barrier()

        elements = ops.getEleTags()
        nodes = ops.getNodeTags()
        logger.debug(f"The number of nodes: {len(nodes)}")
        logger.debug(f"The number of elements: {len(elements)}")
        logger.debug(f"Model generation took {next(time_gen):.2f} seconds.")

        analysis_type = "gravity"

        for item, result_type in zip(
            [
                "base",
                "roof",
                "global",
                "global",
                "global",
                "diaphragm",
                "diaphragm",
                "diaphragm",
            ],
            ["reaction", "disp", "disp", "vel", "accel", "disp", "vel", "accel"],
        ):
            self.add_recorder(
                kind="node",
                analysis_name=analysis_name,
                analysis_type=analysis_type,
                location=item,
                result_type=result_type,
                jobid=jobid,
                pid=pid,
            )

        for item in [
            "column",
            "ver_con",
            "floor_beam",
            "ceiling_beam",
            "hor_con",
            "brace",
        ]:
            self.add_recorder(
                kind="element",
                analysis_name=analysis_name,
                analysis_type=analysis_type,
                location=item,
                jobid=jobid,
                pid=pid,
            )

        for item in [
            "section_force",
            "section_deformation",
            "section_stiffness",
            "section_fiber_top",
            "section_fiber_bottom",
            "section_fiber_left",
            "section_fiber_right",
        ]:
            self.add_recorder(
                kind="element",
                analysis_name=analysis_name,
                analysis_type=analysis_type,
                location="brace",
                result_type=item,
                jobid=jobid,
                pid=pid,
            )

        if self.save_model:
            self._save_model(pid=pid, jobid=jobid)

        ops.barrier()

        logger.debug(f"Recorders for gravity analysis are added to the model.")
        logger.debug(f"Adding recorders took about {next(time_gen):.2f} seconds.")

        num_steps = 10
        self.add_gravity_load(pid=pid, num_steps=num_steps)
        logger.debug(f"Now, gravity analysis having {num_steps} steps is just started.")

        for i in range(num_steps):
            ops.analyze(1)
            logger.debug(f"Step {i + 1} is completed.")

        ops.loadConst("-time", 0.0)

        df = pd.DataFrame(self.list_recorder)
        if len(df.columns) == 4:
            df.columns = ["location", "ele_info", "ele_number", "ele_type"]
        elif len(df.columns) == 5:
            df.columns = ["location", "ele_info", "ele_number", "ele_type", "section"]

        col_ele = df[df["location"] == "column_element"].ele_number.tolist()
        df_column_gravity = pd.DataFrame(
            [[item, -ops.basicForce(item)[0]] for item in col_ele],
            columns=["ele_number", "axial_force"],
        )

        df_column_gravity.to_pickle(f"{tmp}/df_column_gravity_{pid}.pkl")
        ops.barrier()
        if pid == 0:
            df_column_gravity = pd.DataFrame()
            for i in range(self.nprocs):
                df_column_gravity = pd.concat(
                    [
                        df_column_gravity,
                        pd.read_pickle(f"{tmp}/df_column_gravity_{i}.pkl"),
                    ],
                    ignore_index=False,
                )

            df_column_gravity = df_column_gravity.reset_index(drop=True)
            df_column_gravity = df_column_gravity.drop_duplicates(
                subset=["ele_number"], keep="first"
            ).set_index("ele_number")
            df_column_gravity.to_pickle(
                f"{self.directory}/{self.name}_df_column_gravity.pkl"
            )

        ops.barrier()

        # if 5564 in ops.getNodeTags():
        #     logger.debug(f"Node (5564) Disp: {ops.nodeDisp(5564)}")

        # elif 431 in ops.getNodeTags():
        #     logger.debug(f"Node (431) Disp: {ops.nodeDisp(431)}")

        logger.debug(f"Gravity analysis took about {next(time_gen):.2f} seconds.")
        ops.barrier()

        self.remove_recorder()
        analysis_type = "timehistory"

        for item, result_type in zip(
            [
                "base",
                "roof",
                "global",
                "global",
                "global",
                "diaphragm",
                "diaphragm",
                "diaphragm",
            ],
            ["reaction", "disp", "disp", "vel", "accel", "disp", "vel", "accel"],
        ):
            self.add_recorder(
                kind="node",
                analysis_name=analysis_name,
                analysis_type=analysis_type,
                location=item,
                result_type=result_type,
                jobid=jobid,
                pid=pid,
            )

        for item in [
            "column",
            "ver_con",
            "floor_beam",
            "ceiling_beam",
            "hor_con",
            "brace",
        ]:
            self.add_recorder(
                kind="element",
                analysis_name=analysis_name,
                analysis_type=analysis_type,
                location=item,
                jobid=jobid,
                pid=pid,
            )

        for item in [
            "section_force",
            "section_deformation",
            "section_stiffness",
            "section_fiber_top",
            "section_fiber_bottom",
            "section_fiber_left",
            "section_fiber_right",
        ]:
            self.add_recorder(
                kind="element",
                analysis_name=analysis_name,
                analysis_type=analysis_type,
                location="brace",
                result_type=item,
                jobid=jobid,
                pid=pid,
            )

        self.add_rayleigh_damping(
            damping_ratio=0.03, period_first=5.12, period_second=1.012
        )
        dt, values = self.add_uniform_excitation(
            input_dict={
                "filename": [
                    "data/RSN165_IMPVALL.H_H-CHI012.AT2",
                    "data/RSN165_IMPVALL.H_H-CHI282.AT2",
                ],
                "direction": [1, 2],
                "factor": [1.0, 1.0],
            }
        )
        if dt_analyze is None:
            dt_analyze = dt[0]
            self.logger.debug(f"dt_analyze is set to {dt_analyze} seconds.")

        if time_analyze is None:
            time_analyze = dt_analyze * len(values[0])

        dt_initial = dt_analyze
        t_current = ops.getTime()
        t_end_analysis = time_analyze + free_vibration
        t_end_time_history = dt_analyze * len(values[0])

        status = 0
        count_success = 0
        count_failure = 0

        logger.info(f"Total number of steps = {int(t_end_analysis / dt_initial)}")
        logger.info(
            f"Total time for analysis including {free_vibration} sec free vibration phase = {t_end_analysis} sec\n"
        )
        logger.info(
            f"Time history analysis is started. Time increment = {dt_initial} sec"
        )

        logger.info(
            f"The total job time is set to {time_job} sec (real-time). The analysis will be terminated after {time_job} sec."
        )

        ops.barrier()
        start_time = time.time()
        while t_current < t_end_analysis:
            status = ops.analyze(1, dt_analyze)

            if status == 0 and t_current < t_end_time_history and count_failure == 0:
                count_success += 1
                count_failure = 0
                t_current = ops.getTime()
                t_nextstep = t_current + dt_initial

                logger.info(
                    f"current time = {t_current:.6f} sec | remaining time = {t_end_analysis - t_current:.6f} sec | progress = {t_current / t_end_analysis * 100:.2f}%"
                )

            if status == 0 and t_current < t_end_time_history and count_failure != 0:
                t_current = ops.getTime()
                dt = np.min([dt * 1.2, t_nextstep - t_current])

                if dt < 1e-6:
                    count_failure = 0
                    dt = dt_initial

                logger.debug(
                    f"Recovering from failure... Current time increment = {dt:.6f} sec and t_current = {t_current:.6f} sec"
                )

            if status == 0 and t_current >= t_end_time_history and count_failure == 0:
                count_success += 1
                count_failure = 0

                t_current = ops.getTime()
                t_nextstep = t_current + dt_initial

                logger.debug(
                    f"Free vibration phase is running. Remaining time = {t_end_analysis - t_current:.2f} sec | remaining steps = {int((t_end_analysis - t_current) / dt)} | progress = {t_current / t_end_analysis * 100:.2f}%"
                )

            if status != 0:
                dt *= 0.5
                count_success = 0
                count_failure += 1

                logger.debug(
                    f"Failure #{int(count_failure)} -> Time increment has been halved! Current time increment = {dt:.6f} sec and remaining time = {t_end_analysis - t_current:.2f} sec"
                )

            sys.stdout.flush()
            current_time = time.time()
            if current_time - start_time > time_job:
                logger.info(
                    f"Time limit ({time_job} sec) is reached. The analysis is terminated."
                )
                break

        if pid == 0:
            shutil.rmtree(f"{tmp}")

        return None

    def __run_parallel(self, **kwargs):
        self.logger.info(
            f"Parallel processing is just started with {self.nprocs} cores."
        )
        self.logger.warning(
            "It will not print anything to the console until the analysis is completed."
        )
        self.logger.warning(
            "In order to monitor analysis, please look at the log file (logs/mbp_parallel_{pid}.log)."
        )

        with ipp.Cluster(engines="mpi", n=self.nprocs) as rc:
            view = rc.broadcast_view()
            ar = view.apply_async(self._parallel_model, **kwargs)
            ar.wait()
            ar.get()
            return (ar.stdout, ar.stderr)

    def __run_serial(self, **kwargs) -> None:
        self._serial_model(**kwargs)
        return None

    def run(self, **kwargs):
        analysis_name = kwargs.get("analysis_name", None)

        if (
            analysis_name is None
            or not analysis_name[0].isalnum()
            or not re.search("[a-zA-Z]", analysis_name)
        ):
            raise ValueError(
                f"Please provide an analysis name. It should start with a letter and contain only letters and numbers."
            )

        if self.nprocs > 1:
            out = self.__run_parallel(**kwargs)
        else:
            out = self.__run_serial(**kwargs)

        return out

    @functools.lru_cache(maxsize=None, typed=False)
    def hss_section(self, **kwargs) -> int:
        mat_tag = kwargs.get("mat_tag", None)
        num_subdiv_len = kwargs.get("num_subdiv_len", None)
        num_subdiv_thick = kwargs.get("num_subdiv_thick", None)
        num_subdiv_corner_len = kwargs.get("num_subdiv_corner_len", None)
        num_subdiv_corner_thick = kwargs.get("num_subdiv_corner_thick", None)
        z_axis = kwargs.get("D", None)
        y_axis = kwargs.get("B", None)
        thickness = kwargs.get("T", None)
        J = kwargs.get("J", None)
        G = kwargs.get("G", None)

        if self.section_tags:
            section_tag = self.section_tags[-1] + 1
        else:
            section_tag = 1

        self.section_tags.append(section_tag)

        ops.section("Fiber", section_tag, "-GJ", G * J)

        ops.patch(
            "circ",
            mat_tag,
            *[num_subdiv_corner_len, num_subdiv_corner_thick],
            *[y_axis / 2 - 2 * thickness, z_axis / 2 - 2 * thickness],
            *[thickness, 2 * thickness],
            *[0.0, 90.0],
        )
        ops.patch(
            "circ",
            mat_tag,
            *[num_subdiv_corner_len, num_subdiv_corner_thick],
            *[y_axis / 2 - 2 * thickness, -z_axis / 2 + 2 * thickness],
            *[thickness, 2 * thickness],
            *[90.0, 180.0],
        )
        ops.patch(
            "circ",
            mat_tag,
            *[num_subdiv_corner_len, num_subdiv_corner_thick],
            *[-y_axis / 2 + 2 * thickness, -z_axis / 2 + 2 * thickness],
            *[thickness, 2 * thickness],
            *[180.0, 270.0],
        )
        ops.patch(
            "circ",
            mat_tag,
            *[num_subdiv_corner_len, num_subdiv_corner_thick],
            *[-y_axis / 2 + 2 * thickness, z_axis / 2 - 2 * thickness],
            *[thickness, 2 * thickness],
            *[270.0, 360.0],
        )
        ops.patch(
            "quad",
            mat_tag,
            *[num_subdiv_len, num_subdiv_thick],
            *[y_axis / 2 - thickness, z_axis / 2 - 2 * thickness],
            *[y_axis / 2 - thickness, -z_axis / 2 + 2 * thickness],
            *[y_axis / 2, -z_axis / 2 + 2 * thickness],
            *[y_axis / 2, z_axis / 2 - 2 * thickness],
        )
        ops.patch(
            "quad",
            mat_tag,
            *[num_subdiv_len, num_subdiv_thick],
            *[y_axis / 2 - 2 * thickness, -z_axis / 2 + thickness],
            *[-y_axis / 2 + 2 * thickness, -z_axis / 2 + thickness],
            *[-y_axis / 2 + 2 * thickness, -z_axis / 2],
            *[y_axis / 2 - 2 * thickness, -z_axis / 2],
        )
        ops.patch(
            "quad",
            mat_tag,
            *[num_subdiv_len, num_subdiv_thick],
            *[-y_axis / 2 + thickness, -z_axis / 2 + 2 * thickness],
            *[-y_axis / 2 + thickness, z_axis / 2 - 2 * thickness],
            *[-y_axis / 2, z_axis / 2 - 2 * thickness],
            *[-y_axis / 2, -z_axis / 2 + 2 * thickness],
        )
        ops.patch(
            "quad",
            mat_tag,
            *[num_subdiv_len, num_subdiv_thick],
            *[-y_axis / 2 + 2 * thickness, z_axis / 2 - thickness],
            *[y_axis / 2 - 2 * thickness, z_axis / 2 - thickness],
            *[y_axis / 2 - 2 * thickness, z_axis / 2],
            *[-y_axis / 2 + 2 * thickness, z_axis / 2],
        )

        return section_tag

    @functools.lru_cache(maxsize=None, typed=False)
    def w_section(self, **kwargs) -> int:
        mat_tag = kwargs.get("mat_tag", None)
        nfdw = kwargs.get("nfdw", None)
        nftw = kwargs.get("nftw", None)
        nfbf = kwargs.get("nfbf", None)
        nftf = kwargs.get("nftf", None)
        D = kwargs.get("D", None)
        B = kwargs.get("B", None)
        T = kwargs.get("T", None)
        W = kwargs.get("W", None)
        J = kwargs.get("J", None)
        G = kwargs.get("G", None)

        if self.section_tags:
            section_tag = self.section_tags[-1] + 1
        else:
            section_tag = 1

        self.section_tags.append(section_tag)

        Dw = D - 2 * T
        y1, y2, y3, y4 = -D / 2, -Dw / 2, Dw / 2, D / 2
        z1, z2, z3, z4 = -B / 2, -W / 2, W / 2, B / 2

        ops.section("Fiber", section_tag, "-GJ", G * J)
        ops.patch(
            "quad", mat_tag, nfbf, nftf, *[y1, z4], *[y1, z1], *[y2, z1], *[y2, z4]
        )
        ops.patch(
            "quad", mat_tag, nftw, nfdw, *[y2, z3], *[y2, z2], *[y3, z2], *[y3, z3]
        )
        ops.patch(
            "quad", mat_tag, nfbf, nftf, *[y3, z4], *[y3, z1], *[y4, z1], *[y4, z4]
        )

        return section_tag

    @functools.lru_cache(maxsize=None, typed=False)
    def create_beam_hinge(self, **kwargs) -> tuple:
        beam_length = kwargs.get("beam_length", None)
        beam_length_braced = kwargs.get("beam_length_braced", None)
        young_modulus = kwargs.get("YoungModulus", None)
        fy_beam = kwargs.get("Fy_beam", None)
        sec_McMy = kwargs.get("McMy", None)
        sec_D = kwargs.get("D", None)
        sec_B = kwargs.get("B", None)
        sec_T = kwargs.get("T", None)
        sec_W = kwargs.get("W", None)
        sec_Ix = kwargs.get("Ix", None)
        sec_Zx = kwargs.get("Zx", None)
        sec_Ry = kwargs.get("Ry", None)
        n_cons = kwargs.get("n_cons", None)

        Ke = (6 * young_modulus * sec_Ix) / beam_length
        My_Plus = fy_beam * sec_Zx * 1.1
        My_Neg = -fy_beam * sec_Zx * 1.1

        beam_length = beam_length * 1e3
        beam_length_braced = beam_length_braced * 1e3
        young_modulus = young_modulus * 1e-3
        fy_beam = fy_beam * 1e-3
        sec_D, sec_B, sec_T, sec_W = sec_D * 1e3, sec_B * 1e3, sec_T * 1e3, sec_W * 1e3
        sec_Ix, sec_Zx, sec_Ry = sec_Ix * 1e12, sec_Zx * 1e9, sec_Ry * 1e3
        c_unit1, c_unit2 = 1.0, 1.0

        ThetaU = 0.06
        cyc_det = 1.0
        rate_cyc_det = 1.0

        if sec_D < 533:
            ThetaP = (
                0.0865
                * ((sec_D - 2 * sec_T) / sec_W) ** (-0.365)
                * (sec_B / (sec_T * 2)) ** (-0.140)
                * (beam_length / sec_D) ** (0.340)
                * ((c_unit1 * sec_D) / 533) ** (-0.721)
                * ((c_unit2 * fy_beam) / 355) ** (-0.230)
            )

            ThetaPc = (
                5.63
                * ((sec_D - 2 * sec_T) / sec_W) ** (-0.565)
                * (sec_B / (sec_T * 2)) ** (-0.800)
                * ((c_unit1 * sec_D) / 533) ** (-0.280)
                * ((c_unit2 * fy_beam) / 355) ** (-0.430)
            )

            Lambda = (
                495
                * ((sec_D - 2 * sec_T) / sec_W) ** (-1.34)
                * (sec_B / (sec_T * 2)) ** (-0.595)
                * ((c_unit2 * fy_beam) / 355) ** (-0.36)
            )

        if sec_D >= 533:
            ThetaP = (
                0.318
                * ((sec_D - 2 * sec_T) / sec_W) ** (-0.550)
                * (sec_B / (sec_T * 2)) ** (-0.345)
                * (beam_length_braced / sec_Ry) ** (-0.0230)
                * (beam_length / sec_D) ** (0.090)
                * ((c_unit1 * sec_D) / 533) ** (-0.330)
                * ((c_unit2 * fy_beam) / 355) ** (-0.130)
            )

            ThetaPc = (
                7.50
                * ((sec_D - 2 * sec_T) / sec_W) ** (-0.610)
                * (sec_B / (sec_T * 2)) ** (-0.710)
                * (beam_length_braced / sec_Ry) ** (-0.110)
                * ((c_unit1 * sec_D) / 533) ** (-0.161)
                * ((c_unit2 * fy_beam) / 355) ** (-0.320)
            )

            Lambda = (
                536
                * ((sec_D - 2 * sec_T) / sec_W) ** (-1.26)
                * (sec_B / (sec_T * 2)) ** (-0.525)
                * (beam_length_braced / sec_Ry) ** (-0.130)
                * ((c_unit2 * fy_beam) / 355) ** (-0.291)
            )

        strain_harden_mem = (
            (n_cons + 1.0) * (My_Plus * (sec_McMy - 1.0)) / (Ke * n_cons * ThetaP)
        )
        strain_harden = strain_harden_mem / (1.0 + n_cons * (1.0 - strain_harden_mem))

        bilin_params = {
            "Ke": Ke,
            "as_Plus": strain_harden,
            "as_Neg": strain_harden,
            "My_Plus": My_Plus,
            "My_Neg": My_Neg,
            "Lambda_S": Lambda + self.material.steel_beam["Lambda_UQ"],
            "Lambda_C": Lambda + self.material.steel_beam["Lambda_UQ"],
            "Lambda_A": Lambda + self.material.steel_beam["Lambda_UQ"],
            "Lambda_K": Lambda + self.material.steel_beam["Lambda_UQ"],
            "c_S": cyc_det,
            "c_C": cyc_det,
            "c_A": cyc_det,
            "c_K": cyc_det,
            "theta_p_Plus": ThetaP + self.material.steel_beam["ThetaP_UQ"],
            "theta_p_Neg": ThetaP + self.material.steel_beam["ThetaP_UQ"],
            "theta_pc_Plus": ThetaPc + self.material.steel_beam["ThetaPc_UQ"],
            "theta_pc_Neg": ThetaPc + self.material.steel_beam["ThetaPc_UQ"],
            "Res_Pos": 0.0,
            "Res_Neg": 0.0,
            "theta_u_Plus": ThetaU,
            "theta_u_Neg": ThetaU,
            "D_Plus": rate_cyc_det,
            "D_Neg": rate_cyc_det,
            "n_cons": n_cons,
        }

        mat_tag_bilin = self.material_tags[-1] + 1
        self.material_tags.append(mat_tag_bilin)

        ops.uniaxialMaterial("Bilin", mat_tag_bilin, *bilin_params.values())

        return (mat_tag_bilin, bilin_params)

    @functools.lru_cache(maxsize=None, typed=False)
    def create_column_hinge(self, **kwargs) -> tuple:
        load_axial = kwargs.get("load_axial", None)
        column_length = kwargs.get("column_length", None)
        young_modulus = kwargs.get("YoungModulus", None)
        fy_column = kwargs.get("Fy_column", None)
        sec_McMy = kwargs.get("McMy", None)
        sec_D = kwargs.get("D", None)
        sec_T = kwargs.get("T", None)
        sec_A = kwargs.get("A", None)
        sec_Ix = kwargs.get("Ix", None)
        sec_Zx = kwargs.get("Zx", None)
        n_cons = kwargs.get("n_cons", None)

        Ke = (6 * young_modulus * sec_Ix) / column_length
        My_Plus = fy_column * sec_Zx * 1.1
        My_Neg = -fy_column * sec_Zx * 1.1

        D_over_T = sec_D / sec_T
        load_axial_over_load_yield = load_axial / (0.9 * sec_A * fy_column)
        fy_column = fy_column * 1e-3
        c_unit2 = 0.145

        ThetaU = 0.06
        cyc_det = 1.0
        rate_cyc_det = 1.0

        ThetaP = (
            0.572
            * (D_over_T) ** (-1.0)
            * (1 - load_axial_over_load_yield) ** (1.210)
            * ((c_unit2 * fy_column) / 50) ** (-0.838)
        )

        ThetaPc = (
            14.51
            * (D_over_T) ** (-1.217)
            * (1 - load_axial_over_load_yield) ** (3.035)
            * ((c_unit2 * fy_column) / 50) ** (-0.498)
        )

        Lambda = (
            3800
            * (D_over_T) ** (-2.492)
            * (1 - load_axial_over_load_yield) ** (3.501)
            * ((c_unit2 * fy_column) / 50) ** (-2.391)
        )

        strain_harden_mem = (
            (n_cons + 1.0) * (My_Plus * (sec_McMy - 1.0)) / (Ke * n_cons * ThetaP)
        )
        strain_harden = strain_harden_mem / (1.0 + n_cons * (1.0 - strain_harden_mem))

        bilin_params = {
            "Ke": Ke,
            "as_Plus": strain_harden,
            "as_Neg": strain_harden,
            "My_Plus": My_Plus,
            "My_Neg": My_Neg,
            "Lambda_S": Lambda + self.material.steel_column["Lambda_UQ"],
            "Lambda_C": Lambda + self.material.steel_column["Lambda_UQ"],
            "Lambda_A": Lambda + self.material.steel_column["Lambda_UQ"],
            "Lambda_K": Lambda + self.material.steel_column["Lambda_UQ"],
            "c_S": cyc_det,
            "c_C": cyc_det,
            "c_A": cyc_det,
            "c_K": cyc_det,
            "theta_p_Plus": ThetaP + self.material.steel_column["ThetaP_UQ"],
            "theta_p_Neg": ThetaP + self.material.steel_column["ThetaP_UQ"],
            "theta_pc_Plus": ThetaPc + self.material.steel_column["ThetaPc_UQ"],
            "theta_pc_Neg": ThetaPc + self.material.steel_column["ThetaPc_UQ"],
            "Res_Pos": 0.0,
            "Res_Neg": 0.0,
            "theta_u_Plus": ThetaU,
            "theta_u_Neg": ThetaU,
            "D_Plus": rate_cyc_det,
            "D_Neg": rate_cyc_det,
            "n_cons": n_cons,
        }

        mat_tag_bilin = self.material_tags[-1] + 1
        self.material_tags.append(mat_tag_bilin)

        ops.uniaxialMaterial("Bilin", mat_tag_bilin, *bilin_params.values())

        return (mat_tag_bilin, bilin_params)

    @functools.lru_cache(maxsize=None, typed=False)
    def create_steel01_material(self, **kwargs) -> int:
        elastic_stiff = kwargs.get("elastic_stiff", None)
        yield_strength = kwargs.get("yield_strength", None)
        hardening_ratio = kwargs.get("hardening_ratio", 0.01)

        mat_tag = self.material_tags[-1] + 1
        self.material_tags.append(mat_tag)

        ops.uniaxialMaterial(
            "Steel01", mat_tag, yield_strength, elastic_stiff, hardening_ratio
        )

        return mat_tag

    @functools.lru_cache(maxsize=None, typed=False)
    def create_fatigue_material(self, **kwargs) -> int:
        brace_steel_tag = kwargs.get("brace_steel", None)
        fatigue_E0 = kwargs.get("fatigue_E0", None)
        _m = kwargs.get("m", -0.458)
        _min = kwargs.get("min", -1e16)
        _max = kwargs.get("max", 1e16)

        mat_tag = self.material_tags[-1] + 1
        self.material_tags.append(mat_tag)

        ops.uniaxialMaterial(
            "Fatigue",
            *[mat_tag, brace_steel_tag],
            "-E0",
            fatigue_E0,
            "-m",
            _m,
            "-min",
            _min,
            "-max",
            _max,
        )

        return mat_tag

    def discretize_member(self, **kwargs) -> None:
        i_node = kwargs.get("i_node", None)
        j_node = kwargs.get("j_node", None)
        number_element = kwargs.get("number_element", None)
        element_type = kwargs.get("element_type", None)
        integration_tag = kwargs.get("integration_tag", None)
        transfer_tag = kwargs.get("transfer_tag", None)
        start_node = kwargs.get("start_node", None)
        start_ele = kwargs.get("start_ele", None)
        direction = kwargs.get("direction", None)
        mass = kwargs.get("mass", None)
        imperfection = kwargs.get("imperfection", None)
        kind = kwargs.get("kind", None)
        sec_D = kwargs.get("sec_D", None)
        sec_B = kwargs.get("sec_B", None)
        info = kwargs.get("info", None)
        # brace_location = kwargs.get("brace_location", None)

        if number_element % 2 != 0:
            raise ValueError("Number of elements must be even number!")

        xi, yi, zi = ops.nodeCoord(i_node)
        xj, yj, zj = ops.nodeCoord(j_node)

        number_point = number_element + 1

        if direction in ["west-east", "east-west"]:
            len_br_all = np.sqrt((xj - xi) ** 2 + (zj - zi) ** 2)
            x = np.concatenate(
                (
                    np.linspace(xi, 0.5 * (xi + xj), 1, endpoint=False),
                    np.linspace(0.5 * (xi + xj), xj, 2, endpoint=True),
                )
            )
            y = np.concatenate(
                (
                    np.linspace(yi, yi + imperfection * len_br_all, 1, endpoint=False),
                    np.linspace(yi + imperfection * len_br_all, yj, 2, endpoint=True),
                )
            )
            p = np.polyfit(x, y, 2)
            all_xyz = np.stack(
                (
                    np.linspace(xi, xj, number_point),
                    np.polyval(p, np.linspace(xi, xj, number_point)),
                    np.linspace(zi, zj, number_point),
                ),
                axis=1,
            )

        if direction in ["south-north", "north-south"]:
            len_br_all = np.sqrt((yj - yi) ** 2 + (zj - zi) ** 2)
            x = np.concatenate(
                (
                    np.linspace(yi, 0.5 * (yi + yj), 1, endpoint=False),
                    np.linspace(0.5 * (yi + yj), yj, 2, endpoint=True),
                )
            )
            y = np.concatenate(
                (
                    np.linspace(xi, xi + imperfection * len_br_all, 1, endpoint=False),
                    np.linspace(xi + imperfection * len_br_all, xj, 2, endpoint=True),
                )
            )
            p = np.polyfit(x, y, 2)
            all_xyz = np.stack(
                (
                    np.polyval(p, np.linspace(yi, yj, number_point)),
                    np.linspace(yi, yj, number_point),
                    np.linspace(zi, zj, number_point),
                ),
                axis=1,
            )

        node_num = []
        for i, node in enumerate(all_xyz):
            if (i != 0) and (i != all_xyz.shape[0] - 1):
                ops.node(start_node + i - 1, *node.tolist())

            node_num.append(start_node + i)

        ops.element(
            element_type,
            start_ele,
            *[i_node, node_num[0]],
            transfer_tag,
            integration_tag,
            "-mass",
            mass,
        )

        self.list_recorder.append(
            [
                "brace_element",
                info,
                start_ele,
                element_type,
                [sec_D, sec_B],
            ]
        )

        for i in range(len(node_num) - 2):
            if element_type == "dispBeamColumn":
                ops.element(
                    element_type,
                    start_ele + i + 1,
                    *[node_num[i], node_num[i + 1]],
                    transfer_tag,
                    integration_tag,
                    "-mass",
                    mass,
                )
                self.list_recorder.append(
                    [
                        "brace_element",
                        info,
                        start_ele + i + 1,
                        "dispBeamColumn",
                        [sec_D, sec_B],
                    ]
                )

            elif element_type == "forceBeamColumn":
                ops.element(
                    element_type,
                    start_ele + i + 1,
                    *[node_num[i], node_num[i + 1]],
                    transfer_tag,
                    integration_tag,
                    "-iter",
                    1000,
                    1e-12,
                    "-mass",
                    mass,
                )
                self.list_recorder.append(
                    [
                        "brace_element",
                        info,
                        start_ele + i + 1,
                        "forceBeamColumn",
                        [sec_D, sec_B],
                    ]
                )

        return None

    @helper.log_time_memory
    def assign_brace(self, **kwargs) -> None:
        self.methods_called["assign_element"]["assign_brace"] = True

        pid = kwargs.get("pid", 0)
        use_tnom = kwargs.get("use_tnom", False)
        indep_sec = kwargs.get("indep_sec", False)
        indep_mat = kwargs.get("indep_mat", False)

        if self.elastic_brace:
            self.logger.warning("Elastic brace has been selected!!!")

        brace_steel = int(self.generate.df_section_material.loc["brace_steel", "value"])

        make_rigid = 10.0

        for row in self.generate.df_brace_elements[
            self.generate.df_brace_elements["pid"] == pid
        ].itertuples(index=False):
            i_node, j_node = row.i_node, row.j_node
            element_number = row.ele_number
            brace_sec_props, len_brace = row.section_props, row.length
            direction, side, position = (
                row.direction,
                row.side,
                row.position,
            )
            info = {
                "story": row.story,
                "module": row.module,
                "side": side,
                "length": len_brace,
                "type": row.type,
                "position": position,
                "section": row.section,
                "direction": direction,
                "element_number": element_number,
            }

            sec_D, sec_B, sec_T, sec_A, sec_Ix, sec_Iy, sec_J, mass = (
                brace_sec_props["Ht"],
                brace_sec_props["B"],
                brace_sec_props["tnom"] if use_tnom else brace_sec_props["tdes"],
                brace_sec_props["A"],
                brace_sec_props["Ix"],
                brace_sec_props["Iy"],
                brace_sec_props["J"],
                brace_sec_props["W"],
            )

            transfer_tag = int(
                self.generate.df_geo_transf.loc["brace_we", "value"]
                if side in ["south", "north"]
                else self.generate.df_geo_transf.loc["brace_sn", "value"]
                if side in ["east", "west"]
                else None
            )

            # TODO: fix end offset
            end_offset = 300 * 1e-3

            # Hsiao et al. HSS modelling parameters
            # num_subdiv_len, num_subdiv_thick = 10, 4
            imperfection, nip = self.material.steel_brace["imperfection"], 5

            number_element = 10
            number_element_total = number_element + 4
            element_type = "dispBeamColumn"
            # element_type = "forceBeamColumn"

            l_rigid, l_avg, withm_w, t_gusset = (
                end_offset,
                200 * 1e-3,
                300 * 1e-3,
                16 * 1e-3,
            )

            young_modulus_0_rot = (
                self.material.steel_plate["YoungModulus"] / l_avg
            ) * ((withm_w * t_gusset**3) / 12)
            fy_rot = self.material.steel_plate["Fy"] * ((withm_w * t_gusset**2) / 6)

            if indep_mat:
                self.create_steel01_material.cache_clear()

            steel01_tag = self.create_steel01_material(
                elastic_stiff=young_modulus_0_rot,
                yield_strength=fy_rot,
            )

            if self.include_fatigue:
                if indep_mat:
                    self.create_fatigue_material.cache_clear()

                brace_steel = self.create_fatigue_material(
                    brace_steel=brace_steel,
                    fatigue_E0=self.material.steel_brace["FatigueE0"],
                )

            if indep_sec:
                self.hss_section.cache_clear()

            section_tag = self.hss_section(
                mat_tag=brace_steel,
                num_subdiv_len=10,
                num_subdiv_thick=4,
                num_subdiv_corner_len=4,
                num_subdiv_corner_thick=4,
                D=round(sec_D, 6),
                B=round(sec_B, 6),
                T=round(sec_T, 6),
                J=round(sec_J, 6),
                G=self.material.steel_brace["ShearModulus"],
            )

            ops.beamIntegration("Lobatto", element_number, section_tag, nip)

            xi, yi, zi = ops.nodeCoord(i_node)
            xj, yj, zj = ops.nodeCoord(j_node)

            release_z, release_y = 0, 0

            i_node_new1 = element_number + 0
            i_node_new2 = element_number + 1
            j_node_new1 = element_number + number_element_total - 2
            j_node_new2 = element_number + number_element_total - 3

            if direction in ["south-north", "north-south"]:
                if position == "up":
                    self.list_mass.append(
                        [
                            "brace_element",
                            info,
                            element_number,
                            i_node,
                            j_node,
                            len_brace * mass,
                        ]
                    )

                    angle = np.arctan((zj - zi) / (yj - yi))

                    ops.node(
                        i_node_new1,
                        xi,
                        yi + l_rigid * np.cos(angle),
                        zi + l_rigid * np.sin(angle),
                    )
                    ops.node(
                        j_node_new1,
                        xi,
                        yj - l_rigid * np.cos(angle),
                        zj - l_rigid * np.sin(angle),
                    )

                    if not self.elastic_brace:
                        ops.node(
                            i_node_new2,
                            xi,
                            yi + l_rigid * np.cos(angle),
                            zi + l_rigid * np.sin(angle),
                        )
                        ops.node(
                            j_node_new2,
                            xi,
                            yj - l_rigid * np.cos(angle),
                            zj - l_rigid * np.sin(angle),
                        )

                elif position == "down":
                    self.list_mass.append(
                        [
                            "brace_element",
                            info,
                            element_number,
                            i_node,
                            j_node,
                            len_brace * mass,
                        ]
                    )

                    angle = np.arctan((zi - zj) / (yj - yi))

                    ops.node(
                        i_node_new1,
                        xi,
                        yi + l_rigid * np.cos(angle),
                        zi - l_rigid * np.sin(angle),
                    )
                    ops.node(
                        j_node_new1,
                        xi,
                        yj - l_rigid * np.cos(angle),
                        zj + l_rigid * np.sin(angle),
                    )
                    if not self.elastic_brace:
                        ops.node(
                            i_node_new2,
                            xi,
                            yi + l_rigid * np.cos(angle),
                            zi - l_rigid * np.sin(angle),
                        )
                        ops.node(
                            j_node_new2,
                            xi,
                            yj - l_rigid * np.cos(angle),
                            zj + l_rigid * np.sin(angle),
                        )
            elif direction in ["west-east", "east-west"]:
                if position == "up":
                    self.list_mass.append(
                        [
                            "brace_element",
                            info,
                            element_number,
                            i_node,
                            j_node,
                            len_brace * mass,
                        ]
                    )

                    angle = np.arctan((zj - zi) / (xj - xi))

                    ops.node(
                        i_node_new1,
                        xi + l_rigid * np.cos(angle),
                        yi,
                        zi + l_rigid * np.sin(angle),
                    )
                    ops.node(
                        j_node_new1,
                        xj - l_rigid * np.cos(angle),
                        yi,
                        zj - l_rigid * np.sin(angle),
                    )
                    if not self.elastic_brace:
                        ops.node(
                            i_node_new2,
                            xi + l_rigid * np.cos(angle),
                            yi,
                            zi + l_rigid * np.sin(angle),
                        )
                        ops.node(
                            j_node_new2,
                            xj - l_rigid * np.cos(angle),
                            yi,
                            zj - l_rigid * np.sin(angle),
                        )

                elif position == "down":
                    self.list_mass.append(
                        [
                            "brace_element",
                            info,
                            element_number,
                            i_node,
                            j_node,
                            len_brace * mass,
                        ]
                    )

                    angle = np.arctan((zi - zj) / (xj - xi))

                    ops.node(
                        i_node_new1,
                        xi + l_rigid * np.cos(angle),
                        yi,
                        zi - l_rigid * np.sin(angle),
                    )
                    ops.node(
                        j_node_new1,
                        xj - l_rigid * np.cos(angle),
                        yi,
                        zj + l_rigid * np.sin(angle),
                    )
                    if not self.elastic_brace:
                        ops.node(
                            i_node_new2,
                            xi + l_rigid * np.cos(angle),
                            yi,
                            zi - l_rigid * np.sin(angle),
                        )
                        ops.node(
                            j_node_new2,
                            xj - l_rigid * np.cos(angle),
                            yi,
                            zj + l_rigid * np.sin(angle),
                        )

            if self.include_element_mass:
                pass
            else:
                mass = 0.0

            ops.element(
                "elasticBeamColumn",
                element_number + 0,
                *[i_node, i_node_new1],
                sec_A * make_rigid,
                self.material.steel_brace["YoungModulus"],
                self.material.steel_brace["ShearModulus"],
                sec_J * make_rigid,
                sec_Iy * make_rigid,
                sec_Ix * make_rigid,
                transfer_tag,
                "-mass",
                mass,
                "-releasez",
                0,
                "-releasey",
                0,
            )
            self.list_recorder.append(
                [
                    "brace_rigid_element",
                    info,
                    element_number + 0,
                    "elasticBeamColumn",
                ]
            )

            ops.element(
                "elasticBeamColumn",
                element_number + number_element_total - 1,
                *[j_node_new1, j_node],
                sec_A * make_rigid,
                self.material.steel_brace["YoungModulus"],
                self.material.steel_brace["ShearModulus"],
                sec_J * make_rigid,
                sec_Iy * make_rigid,
                sec_Ix * make_rigid,
                transfer_tag,
                "-mass",
                mass,
                "-releasez",
                0,
                "-releasey",
                0,
            )
            self.list_recorder.append(
                [
                    "brace_rigid_element",
                    info,
                    element_number + number_element_total - 1,
                    "elasticBeamColumn",
                ]
            )

            if self.elastic_brace:
                release_z, release_y = 3, 3
                ops.element(
                    "elasticBeamColumn",
                    element_number + 1,
                    *[i_node_new1, j_node_new1],
                    sec_A,
                    self.material.steel_brace["YoungModulus"],
                    self.material.steel_brace["ShearModulus"],
                    sec_J,
                    sec_Iy,
                    sec_Ix,
                    transfer_tag,
                    "-mass",
                    mass,
                    "-releasez",
                    release_z,
                    "-releasey",
                    release_y,
                )
                self.list_recorder.append(
                    [
                        "brace_elastic_element",
                        info,
                        element_number + 1,
                        "elasticBeamColumn",
                        sec_D,
                    ]
                )

            else:
                self.discretize_member(
                    i_node=i_node_new2,
                    j_node=j_node_new2,
                    number_element=number_element,
                    element_type=element_type,
                    integration_tag=element_number,
                    transfer_tag=transfer_tag,
                    start_node=element_number + 2,
                    start_ele=element_number + 2,
                    direction=direction,
                    mass=mass,
                    imperfection=imperfection,
                    kind="quadratic",
                    sec_D=sec_D,
                    sec_B=sec_B,
                    info=info,
                    # braceLocation=brace_location,
                )

                if direction in ["south-north", "north-south"]:
                    ops.element(
                        "zeroLength",
                        element_number + 1,
                        *[i_node_new1, i_node_new2],
                        "-mat",
                        *[steel01_tag],
                        "-dir",
                        *[6],
                        "-orient",
                        *[0.0, np.cos(angle), np.sin(angle), -1.0, 0.0, 0.0],
                    )
                    ops.equalDOF(i_node_new1, i_node_new2, *[1, 2, 3, 4, 5])
                    ops.element(
                        "zeroLength",
                        element_number + number_element_total - 2,
                        *[j_node_new2, j_node_new1],
                        "-mat",
                        *[steel01_tag],
                        "-dir",
                        *[6],
                        "-orient",
                        *[0.0, np.cos(angle), np.sin(angle), -1.0, 0.0, 0.0],
                    )
                    ops.equalDOF(j_node_new1, j_node_new2, *[1, 2, 3, 4, 5])

                elif direction in ["west-east", "east-west"]:
                    ops.element(
                        "zeroLength",
                        element_number + 1,
                        *[i_node_new1, i_node_new2],
                        "-mat",
                        *[steel01_tag],
                        "-dir",
                        *[6],
                        "-orient",
                        *[np.cos(angle), 0.0, np.sin(angle), 0.0, -1.0, 0.0],
                    )
                    ops.equalDOF(i_node_new1, i_node_new2, *[1, 2, 3, 4, 5])
                    ops.element(
                        "zeroLength",
                        element_number + number_element_total - 2,
                        *[j_node_new2, j_node_new1],
                        "-mat",
                        *[steel01_tag],
                        "-dir",
                        *[6],
                        "-orient",
                        *[np.cos(angle), 0.0, np.sin(angle), 0.0, -1.0, 0.0],
                    )
                    ops.equalDOF(j_node_new1, j_node_new2, *[1, 2, 3, 4, 5])

                self.list_recorder.append(
                    [
                        "brace_spring",
                        info,
                        element_number + 1,
                        "zeroLength",
                    ]
                )
                self.list_recorder.append(
                    [
                        "brace_spring",
                        info,
                        element_number + number_element_total - 2,
                        "zeroLength",
                    ]
                )

        self.logger.info("Brace elements have been assigned.")

        return None

    @helper.log_time_memory
    def assign_ceiling_beam(self, **kwargs) -> None:
        self.methods_called["assign_element"]["assign_ceiling_beam"] = True

        pid = kwargs.get("pid", 0)
        indep_sec = kwargs.get("indep_sec", False)
        indep_mat = kwargs.get("indep_mat", False)

        if self.elastic_ceiling_beam:
            self.logger.warning("Elastic ceiling beam has been selected!!!")

        make_rigid = 10.0

        for row in self.generate.df_ceiling_beam_elements[
            self.generate.df_ceiling_beam_elements["pid"] == pid
        ].itertuples(index=False):
            i_node, j_node = row.i_node, row.j_node
            braced, brace_type, side, len_beam = (
                row.braced,
                row.brace_type,
                row.side,
                row.length,
            )
            sec_props = row.section_props
            element_number = row.ele_number
            (
                sec_B,
                sec_D,
                sec_T,
                sec_W,
                sec_A,
                sec_J,
                sec_Iy,
                sec_Ix,
                sec_Zx,
                sec_Ry,
                mass,
            ) = (
                sec_props["bf"],
                sec_props["d"],
                sec_props["tf"],
                sec_props["tw"],
                sec_props["A"],
                sec_props["J"],
                sec_props["Iy"],
                sec_props["Ix"],
                sec_props["Zx"],
                sec_props["ry"],
                sec_props["W"],
            )
            info = {
                "story": row.story,
                "module": row.module,
                "braced": braced,
                "brace_type": brace_type,
                "side": side,
                "length": len_beam,
                "section": row.section,
                "direction": row.direction,
                "element_number": element_number,
            }

            transfer_tag = int(
                self.generate.df_geo_transf.loc["beam_we", "value"]
                if side in ["south", "north"]
                else self.generate.df_geo_transf.loc["beam_sn", "value"]
                if side in ["east", "west"]
                else None
            )

            # TODO: Fix end offset and end moment release
            end_offset = 300 * 1e-3
            end_moment_release = True

            xi, yi, zi = ops.nodeCoord(i_node)
            xj, yj, zj = ops.nodeCoord(j_node)

            self.list_mass.append(
                [
                    "ceiling_beam_element",
                    info,
                    element_number,
                    i_node,
                    j_node,
                    len_beam * mass,
                ]
            )

            if self.include_element_mass:
                pass
            else:
                mass = 0.0

            if not braced:
                i_node_new1 = element_number
                j_node_new1 = element_number + 2

                if side in ["west", "east"]:
                    ops.node(i_node_new1, xi, yi + end_offset, zi)
                    ops.node(j_node_new1, xj, yj - end_offset, zj)

                elif side in ["south", "north"]:
                    ops.node(i_node_new1, xi + end_offset, yi, zi)
                    ops.node(j_node_new1, xj - end_offset, yj, zj)

                if end_moment_release:
                    moment_release_z = 3
                    moment_release_y = 0
                else:
                    # TODO: Fix this constraint
                    moment_release_z = 0
                    moment_release_y = 0

                ops.element(
                    "elasticBeamColumn",
                    element_number + 0,
                    *[i_node, i_node_new1],
                    sec_A * make_rigid,
                    self.material.steel_beam["YoungModulus"],
                    self.material.steel_beam["ShearModulus"],
                    sec_J,
                    sec_Iy * make_rigid,
                    sec_Ix * make_rigid,
                    transfer_tag,
                    "-mass",
                    mass,
                    "-releasez",
                    0,
                    "-releasey",
                    0,
                )
                self.list_recorder.append(
                    [
                        "ceiling_beam_rigid_element",
                        info,
                        element_number + 0,
                        "elasticBeamColumn",
                    ]
                )

                ops.element(
                    "elasticBeamColumn",
                    element_number + 2,
                    *[j_node_new1, j_node],
                    sec_A * make_rigid,
                    self.material.steel_beam["YoungModulus"],
                    self.material.steel_beam["ShearModulus"],
                    sec_J,
                    sec_Iy * make_rigid,
                    sec_Ix * make_rigid,
                    transfer_tag,
                    "-mass",
                    mass,
                    "-releasez",
                    0,
                    "-releasey",
                    0,
                )
                self.list_recorder.append(
                    [
                        "ceiling_beam_rigid_element",
                        info,
                        element_number + 2,
                        "elasticBeamColumn",
                    ]
                )

                # middle element
                ops.element(
                    "elasticBeamColumn",
                    element_number + 1,
                    *[i_node_new1, j_node_new1],
                    sec_A,
                    self.material.steel_beam["YoungModulus"],
                    self.material.steel_beam["ShearModulus"],
                    sec_J,
                    sec_Iy,
                    sec_Ix,
                    transfer_tag,
                    "-mass",
                    mass,
                    "-releasez",
                    moment_release_z,
                    "-releasey",
                    moment_release_y,
                )

                self.list_recorder.append(
                    [
                        "ceiling_beam_element",
                        info,
                        element_number + 1,
                        "elasticBeamColumn",
                    ]
                )

            elif braced and brace_type == "Chevron":
                mid_node = row.mid_node

                xmid, ymid, zmid = ops.nodeCoord(mid_node)

                # TODO: FIX THIS
                """
                # NOTE: length of the rigid element is assumed to be 300 mm
                """
                mid_rigid = 300 * 1e-3

                i_node_new1 = element_number + 0
                i_node_new2 = element_number + 1
                i_node_new3 = element_number + 2
                i_node_new4 = element_number + 3
                j_node_new1 = element_number + 4
                j_node_new2 = element_number + 5
                j_node_new3 = element_number + 6
                j_node_new4 = element_number + 7

                if side in ["west", "east"]:
                    beam_length = (yj - yi - mid_rigid) * 0.5
                    ops.node(i_node_new1, xi, yi + end_offset, zi)
                    ops.node(j_node_new1, xmid, ymid - 0.5 * mid_rigid, zmid)
                    ops.node(i_node_new3, xmid, ymid + 0.5 * mid_rigid, zmid)
                    ops.node(j_node_new3, xj, yj - end_offset, zj)

                    if not self.elastic_ceiling_beam:
                        ops.node(i_node_new2, xi, yi + end_offset, zi)
                        ops.node(j_node_new2, xmid, ymid - 0.5 * mid_rigid, zmid)
                        ops.node(i_node_new4, xmid, ymid + 0.5 * mid_rigid, zmid)
                        ops.node(j_node_new4, xj, yj - end_offset, zj)
                        dir_zero_length = 4

                elif side in ["south", "north"]:
                    beam_length = (xj - xi - mid_rigid) * 0.5
                    ops.node(i_node_new1, xi + end_offset, yi, zi)
                    ops.node(j_node_new1, xmid - 0.5 * mid_rigid, ymid, zmid)
                    ops.node(i_node_new3, xmid + 0.5 * mid_rigid, ymid, zmid)
                    ops.node(j_node_new3, xj - end_offset, yj, zj)

                    if not self.elastic_ceiling_beam:
                        ops.node(i_node_new2, xi + end_offset, yi, zi)
                        ops.node(j_node_new2, xmid - 0.5 * mid_rigid, ymid, zmid)
                        ops.node(i_node_new4, xmid + 0.5 * mid_rigid, ymid, zmid)
                        ops.node(j_node_new4, xj - end_offset, yj, zj)
                        dir_zero_length = 5

                if end_moment_release:
                    # TODO: fix this constraint
                    moment_release_zi = 0
                    moment_release_zj = 0
                    moment_release_yi = 0
                    moment_release_yj = 0

                else:
                    moment_release_zi = 0
                    moment_release_zj = 0
                    moment_release_yi = 0
                    moment_release_yj = 0

                if not self.elastic_ceiling_beam:
                    if indep_mat:
                        self.create_beam_hinge.cache_clear()

                    n_cons = 10
                    mat_tag_bilin, bilin_params = self.create_beam_hinge(
                        beam_length=beam_length,
                        beam_length_braced=beam_length,
                        YoungModulus=self.material.steel_beam["YoungModulus"],
                        Fy_beam=self.material.steel_beam["Fy"],
                        McMy=self.material.steel_beam["McMy"],
                        D=sec_D,
                        B=sec_B,
                        T=sec_T,
                        W=sec_W,
                        Ix=sec_Ix,
                        Zx=sec_Zx,
                        Ry=sec_Ry,
                        n_cons=n_cons,
                    )
                    self.list_bilin_params.append(
                        ["beam_ceiling", element_number, sec_D, bilin_params]
                    )

                    # First hinge element
                    ops.element(
                        "zeroLength",
                        element_number + 1,
                        *[i_node_new1, i_node_new2],
                        "-mat",
                        *[mat_tag_bilin],
                        "-dir",
                        *[dir_zero_length],
                    )
                    ops.equalDOF(
                        i_node_new1,
                        i_node_new2,
                        *[item for item in range(1, 7) if not item == dir_zero_length],
                    )
                    self.list_recorder.append(
                        [
                            "ceiling_beam_hinge",
                            info,
                            element_number + 1,
                            "zeroLength",
                        ]
                    )

                    # First middle element
                    ops.element(
                        "elasticBeamColumn",
                        element_number + 2,
                        *[i_node_new2, j_node_new2],
                        sec_A,
                        self.material.steel_beam["YoungModulus"],
                        self.material.steel_beam["ShearModulus"],
                        sec_J * ((n_cons + 1.0) / n_cons),
                        sec_Iy * ((n_cons + 1.0) / n_cons),
                        sec_Ix * ((n_cons + 1.0) / n_cons),
                        transfer_tag,
                        "-mass",
                        mass,
                        "-releasez",
                        moment_release_zi,
                        "-releasey",
                        moment_release_yi,
                    )
                    self.list_recorder.append(
                        [
                            "ceiling_beam_element",
                            info,
                            element_number + 2,
                            "elasticBeamColumn",
                        ]
                    )

                    # Second hinge element
                    ops.element(
                        "zeroLength",
                        element_number + 3,
                        *[j_node_new2, j_node_new1],
                        "-mat",
                        *[mat_tag_bilin],
                        "-dir",
                        *[dir_zero_length],
                    )
                    ops.equalDOF(
                        j_node_new2,
                        j_node_new1,
                        *[item for item in range(1, 7) if not item == dir_zero_length],
                    )
                    self.list_recorder.append(
                        [
                            "ceiling_beam_hinge",
                            info,
                            element_number + 3,
                            "zeroLength",
                        ]
                    )

                    # Third hinge element
                    ops.element(
                        "zeroLength",
                        element_number + 6,
                        *[i_node_new3, i_node_new4],
                        "-mat",
                        *[mat_tag_bilin],
                        "-dir",
                        *[dir_zero_length],
                    )
                    ops.equalDOF(
                        i_node_new3,
                        i_node_new4,
                        *[item for item in range(1, 7) if not item == dir_zero_length],
                    )
                    self.list_recorder.append(
                        [
                            "ceiling_beam_hinge",
                            info,
                            element_number + 6,
                            "zeroLength",
                        ]
                    )

                    # Second middle element
                    ops.element(
                        "elasticBeamColumn",
                        element_number + 7,
                        *[i_node_new4, j_node_new4],
                        sec_A,
                        self.material.steel_beam["YoungModulus"],
                        self.material.steel_beam["ShearModulus"],
                        sec_J * ((n_cons + 1.0) / n_cons),
                        sec_Iy * ((n_cons + 1.0) / n_cons),
                        sec_Ix * ((n_cons + 1.0) / n_cons),
                        transfer_tag,
                        "-mass",
                        mass,
                        "-releasez",
                        moment_release_zj,
                        "-releasey",
                        moment_release_yj,
                    )
                    self.list_recorder.append(
                        [
                            "ceiling_beam_element",
                            info,
                            element_number + 7,
                            "elasticBeamColumn",
                        ]
                    )

                    # Fourth hinge element
                    ops.element(
                        "zeroLength",
                        element_number + 8,
                        *[j_node_new4, j_node_new3],
                        "-mat",
                        *[mat_tag_bilin],
                        "-dir",
                        *[dir_zero_length],
                    )
                    ops.equalDOF(
                        j_node_new4,
                        j_node_new3,
                        *[item for item in range(1, 7) if not item == dir_zero_length],
                    )
                    self.list_recorder.append(
                        [
                            "ceiling_beam_hinge",
                            info,
                            element_number + 8,
                            "zeroLength",
                        ]
                    )

                if self.elastic_ceiling_beam:
                    # First middle element
                    ops.element(
                        "elasticBeamColumn",
                        element_number + 2,
                        *[i_node_new1, j_node_new1],
                        sec_A,
                        self.material.steel_beam["YoungModulus"],
                        self.material.steel_beam["ShearModulus"],
                        sec_J,
                        sec_Iy,
                        sec_Ix,
                        transfer_tag,
                        "-mass",
                        mass,
                        "-releasez",
                        moment_release_zi,
                        "-releasey",
                        moment_release_yi,
                    )
                    self.list_recorder.append(
                        [
                            "ceiling_beam_braced_elastic_element",
                            info,
                            element_number + 2,
                            "elasticBeamColumn",
                        ]
                    )

                    # Second middle element
                    ops.element(
                        "elasticBeamColumn",
                        element_number + 7,
                        *[i_node_new3, j_node_new3],
                        sec_A,
                        self.material.steel_beam["YoungModulus"],
                        self.material.steel_beam["ShearModulus"],
                        sec_J,
                        sec_Iy,
                        sec_Ix,
                        transfer_tag,
                        "-mass",
                        mass,
                        "-releasez",
                        moment_release_zj,
                        "-releasey",
                        moment_release_yj,
                    )
                    self.list_recorder.append(
                        [
                            "ceiling_beam_braced_elastic_element",
                            info,
                            element_number + 7,
                            "elasticBeamColumn",
                        ]
                    )

                # First rigid element
                ops.element(
                    "elasticBeamColumn",
                    element_number + 0,
                    *[i_node, i_node_new1],
                    sec_A * make_rigid,
                    self.material.steel_beam["YoungModulus"],
                    self.material.steel_beam["ShearModulus"],
                    sec_J,
                    sec_Iy * make_rigid,
                    sec_Ix * make_rigid,
                    transfer_tag,
                    "-mass",
                    mass,
                    "-releasez",
                    0,
                    "-releasey",
                    0,
                )
                self.list_recorder.append(
                    [
                        "ceiling_beam_rigid_element",
                        info,
                        element_number + 0,
                        "elasticBeamColumn",
                    ]
                )

                # First middle rigid element
                ops.element(
                    "elasticBeamColumn",
                    element_number + 4,
                    *[j_node_new1, mid_node],
                    sec_A * make_rigid,
                    self.material.steel_beam["YoungModulus"],
                    self.material.steel_beam["ShearModulus"],
                    sec_J,
                    sec_Iy * make_rigid,
                    sec_Ix * make_rigid,
                    transfer_tag,
                    "-mass",
                    mass,
                    "-releasez",
                    0,
                    "-releasey",
                    0,
                )
                self.list_recorder.append(
                    [
                        "ceiling_beam_rigid_element",
                        info,
                        element_number + 4,
                        "elasticBeamColumn",
                    ]
                )

                # Second middle rigid element
                ops.element(
                    "elasticBeamColumn",
                    element_number + 5,
                    *[mid_node, i_node_new3],
                    sec_A * make_rigid,
                    self.material.steel_beam["YoungModulus"],
                    self.material.steel_beam["ShearModulus"],
                    sec_J,
                    sec_Iy * make_rigid,
                    sec_Ix * make_rigid,
                    transfer_tag,
                    "-mass",
                    mass,
                    "-releasez",
                    0,
                    "-releasey",
                    0,
                )
                self.list_recorder.append(
                    [
                        "ceiling_beam_rigid_element",
                        info,
                        element_number + 5,
                        "elasticBeamColumn",
                    ]
                )

                # Last rigid element
                ops.element(
                    "elasticBeamColumn",
                    element_number + 9,
                    *[j_node_new3, j_node],
                    sec_A * make_rigid,
                    self.material.steel_beam["YoungModulus"],
                    self.material.steel_beam["ShearModulus"],
                    sec_J,
                    sec_Iy * make_rigid,
                    sec_Ix * make_rigid,
                    transfer_tag,
                    "-mass",
                    mass,
                    "-releasez",
                    0,
                    "-releasey",
                    0,
                )
                self.list_recorder.append(
                    [
                        "ceiling_beam_rigid_element",
                        info,
                        element_number + 9,
                        "elasticBeamColumn",
                    ]
                )

            elif braced and brace_type == "X":
                i_node_new1 = element_number + 0
                i_node_new2 = element_number + 1
                j_node_new1 = element_number + 2
                j_node_new2 = element_number + 3

                if side in ["west", "east"]:
                    beam_length = (yj - yi) * 0.5
                    ops.node(i_node_new1, xi, yi + end_offset, zi)
                    ops.node(j_node_new1, xj, yj - end_offset, zj)

                    if not self.elastic_ceiling_beam:
                        ops.node(i_node_new2, xi, yi + end_offset, zi)
                        ops.node(j_node_new2, xj, yj - end_offset, zj)
                        dir_zero_length = 4

                elif side in ["south", "north"]:
                    beam_length = (xj - xi) * 0.5
                    ops.node(i_node_new1, xi + end_offset, yi, zi)
                    ops.node(j_node_new1, xj - end_offset, yj, zj)

                    if not self.elastic_ceiling_beam:
                        ops.node(i_node_new2, xi + end_offset, yi, zi)
                        ops.node(j_node_new2, xj - end_offset, yj, zj)
                        dir_zero_length = 5

                if end_moment_release:
                    # TODO: fix this constraint
                    moment_release_zi = 0
                    moment_release_zj = 0
                    moment_release_yi = 0
                    moment_release_yj = 0

                else:
                    moment_release_zi = 0
                    moment_release_zj = 0
                    moment_release_yi = 0
                    moment_release_yj = 0

                if self.elastic_ceiling_beam:
                    # Middle element
                    ops.element(
                        "elasticBeamColumn",
                        element_number + 2,
                        *[i_node_new1, j_node_new1],
                        sec_A,
                        self.material.steel_beam["YoungModulus"],
                        self.material.steel_beam["ShearModulus"],
                        sec_J,
                        sec_Iy,
                        sec_Ix,
                        transfer_tag,
                        "-mass",
                        mass,
                        "-releasez",
                        moment_release_zi,
                        "-releasey",
                        moment_release_yi,
                    )
                    self.list_recorder.append(
                        [
                            "ceiling_beam_braced_elastic_element",
                            info,
                            element_number + 2,
                            "elasticBeamColumn",
                        ]
                    )

                else:
                    if indep_mat:
                        self.create_beam_hinge.cache_clear()

                    n_cons = 10
                    mat_tag_bilin, bilin_params = self.create_beam_hinge(
                        beam_length=beam_length,
                        beam_length_braced=beam_length,
                        YoungModulus=self.material.steel_beam["YoungModulus"],
                        Fy_beam=self.material.steel_beam["Fy"],
                        McMy=self.material.steel_beam["McMy"],
                        D=sec_D,
                        B=sec_B,
                        T=sec_T,
                        W=sec_W,
                        Ix=sec_Ix,
                        Zx=sec_Zx,
                        Ry=sec_Ry,
                        n_cons=n_cons,
                    )
                    self.list_bilin_params.append(
                        ["beam_ceiling", element_number, sec_D, bilin_params]
                    )

                    # First hinge element
                    ops.element(
                        "zeroLength",
                        element_number + 1,
                        *[i_node_new1, i_node_new2],
                        "-mat",
                        *[mat_tag_bilin],
                        "-dir",
                        *[dir_zero_length],
                    )
                    ops.equalDOF(
                        i_node_new1,
                        i_node_new2,
                        *[item for item in range(1, 7) if not item == dir_zero_length],
                    )
                    self.list_recorder.append(
                        [
                            "ceiling_beam_hinge",
                            info,
                            element_number + 1,
                            "zeroLength",
                        ]
                    )

                    # Middle element
                    ops.element(
                        "elasticBeamColumn",
                        element_number + 2,
                        *[i_node_new2, j_node_new2],
                        sec_A,
                        self.material.steel_beam["YoungModulus"],
                        self.material.steel_beam["ShearModulus"],
                        sec_J * ((n_cons + 1.0) / n_cons),
                        sec_Iy * ((n_cons + 1.0) / n_cons),
                        sec_Ix * ((n_cons + 1.0) / n_cons),
                        transfer_tag,
                        "-mass",
                        mass,
                        "-releasez",
                        moment_release_zi,
                        "-releasey",
                        moment_release_yi,
                    )
                    self.list_recorder.append(
                        [
                            "ceiling_beam_element",
                            info,
                            element_number + 2,
                            "elasticBeamColumn",
                        ]
                    )

                    # Second hinge element
                    ops.element(
                        "zeroLength",
                        element_number + 3,
                        *[j_node_new2, j_node_new1],
                        "-mat",
                        *[mat_tag_bilin],
                        "-dir",
                        *[dir_zero_length],
                    )
                    ops.equalDOF(
                        j_node_new2,
                        j_node_new1,
                        *[item for item in range(1, 7) if not item == dir_zero_length],
                    )
                    self.list_recorder.append(
                        [
                            "ceiling_beam_hinge",
                            info,
                            element_number + 3,
                            "zeroLength",
                        ]
                    )

                # First rigid element
                ops.element(
                    "elasticBeamColumn",
                    element_number + 0,
                    *[i_node, i_node_new1],
                    sec_A * make_rigid,
                    self.material.steel_beam["YoungModulus"],
                    self.material.steel_beam["ShearModulus"],
                    sec_J,
                    sec_Iy * make_rigid,
                    sec_Ix * make_rigid,
                    transfer_tag,
                    "-mass",
                    mass,
                    "-releasez",
                    0,
                    "-releasey",
                    0,
                )
                self.list_recorder.append(
                    [
                        "ceiling_beam_rigid_element",
                        info,
                        element_number + 0,
                        "elasticBeamColumn",
                    ]
                )

                # Last rigid element
                ops.element(
                    "elasticBeamColumn",
                    element_number + 4,
                    *[j_node_new1, j_node],
                    sec_A * make_rigid,
                    self.material.steel_beam["YoungModulus"],
                    self.material.steel_beam["ShearModulus"],
                    sec_J,
                    sec_Iy * make_rigid,
                    sec_Ix * make_rigid,
                    transfer_tag,
                    "-mass",
                    mass,
                    "-releasez",
                    0,
                    "-releasey",
                    0,
                )
                self.list_recorder.append(
                    [
                        "ceiling_beam_rigid_element",
                        info,
                        element_number + 9,
                        "elasticBeamColumn",
                    ]
                )

            else:
                raise ValueError(
                    "Ceiling beam should be either braced (type = Chevron or X) or unbraced!"
                )

        self.logger.info("Ceiling beam elements have been assigned.")

        return None

    @helper.log_time_memory
    def assign_floor_beam(self, **kwargs) -> None:
        self.methods_called["assign_element"]["assign_floor_beam"] = True

        pid = kwargs.get("pid", 0)
        indep_sec = kwargs.get("indep_sec", False)
        indep_mat = kwargs.get("indep_mat", False)

        if self.elastic_floor_beam:
            self.logger.warning("Elastic floor beam has been selected!!!")

        make_rigid = 10.0

        for row in self.generate.df_floor_beam_elements[
            self.generate.df_floor_beam_elements["pid"] == pid
        ].itertuples(index=False):
            i_node, j_node = row.i_node, row.j_node
            braced, brace_type, side, len_beam = (
                row.braced,
                row.brace_type,
                row.side,
                row.length,
            )
            sec_props = row.section_props
            element_number = row.ele_number
            (
                sec_B,
                sec_D,
                sec_T,
                sec_W,
                sec_A,
                sec_J,
                sec_Iy,
                sec_Ix,
                sec_Zx,
                sec_Ry,
                mass,
            ) = (
                sec_props["bf"],
                sec_props["d"],
                sec_props["tf"],
                sec_props["tw"],
                sec_props["A"],
                sec_props["J"],
                sec_props["Iy"],
                sec_props["Ix"],
                sec_props["Zx"],
                sec_props["ry"],
                sec_props["W"],
            )
            info = {
                "story": row.story,
                "module": row.module,
                "braced": braced,
                "brace_type": brace_type,
                "side": side,
                "length": len_beam,
                "section": row.section,
                "direction": row.direction,
                "element_number": element_number,
            }

            transfer_tag = int(
                self.generate.df_geo_transf.loc["beam_we", "value"]
                if side in ["south", "north"]
                else self.generate.df_geo_transf.loc["beam_sn", "value"]
                if side in ["east", "west"]
                else None
            )

            # TODO: Fix end offset and end moment release
            end_offset = 300 * 1e-3
            end_moment_release = True

            xi, yi, zi = ops.nodeCoord(i_node)
            xj, yj, zj = ops.nodeCoord(j_node)

            self.list_mass.append(
                [
                    "floor_beam_element",
                    info,
                    element_number,
                    i_node,
                    j_node,
                    len_beam * mass,
                ]
            )

            if self.include_element_mass:
                pass
            else:
                mass = 0.0

            if not braced:
                i_node_new1 = element_number
                j_node_new1 = element_number + 2

                if side in ["west", "east"]:
                    ops.node(i_node_new1, xi, yi + end_offset, zi)
                    ops.node(j_node_new1, xj, yj - end_offset, zj)

                elif side in ["south", "north"]:
                    ops.node(i_node_new1, xi + end_offset, yi, zi)
                    ops.node(j_node_new1, xj - end_offset, yj, zj)

                if end_moment_release:
                    moment_release_z = 3
                    moment_release_y = 0
                else:
                    moment_release_z = 0
                    moment_release_y = 0

                # 1st rigid element
                ops.element(
                    "elasticBeamColumn",
                    element_number + 0,
                    *[i_node, i_node_new1],
                    sec_A * make_rigid,
                    self.material.steel_beam["YoungModulus"],
                    self.material.steel_beam["ShearModulus"],
                    sec_J,
                    sec_Iy * make_rigid,
                    sec_Ix * make_rigid,
                    transfer_tag,
                    "-mass",
                    mass,
                    "-releasez",
                    0,
                    "-releasey",
                    0,
                )
                self.list_recorder.append(
                    [
                        "floor_beam_rigid_element",
                        info,
                        element_number + 0,
                        "elasticBeamColumn",
                    ]
                )

                # 2nd rigid element
                ops.element(
                    "elasticBeamColumn",
                    element_number + 2,
                    *[j_node_new1, j_node],
                    sec_A * make_rigid,
                    self.material.steel_beam["YoungModulus"],
                    self.material.steel_beam["ShearModulus"],
                    sec_J,
                    sec_Iy * make_rigid,
                    sec_Ix * make_rigid,
                    transfer_tag,
                    "-mass",
                    mass,
                    "-releasez",
                    0,
                    "-releasey",
                    0,
                )
                self.list_recorder.append(
                    [
                        "floor_beam_rigid_element",
                        info,
                        element_number + 2,
                        "elasticBeamColumn",
                    ]
                )

                # middle element
                ops.element(
                    "elasticBeamColumn",
                    element_number + 1,
                    *[i_node_new1, j_node_new1],
                    sec_A,
                    self.material.steel_beam["YoungModulus"],
                    self.material.steel_beam["ShearModulus"],
                    sec_J,
                    sec_Iy,
                    sec_Ix,
                    transfer_tag,
                    "-mass",
                    mass,
                    "-releasez",
                    moment_release_z,
                    "-releasey",
                    moment_release_y,
                )

                self.list_recorder.append(
                    [
                        "floor_beam_element",
                        info,
                        element_number + 1,
                        "elasticBeamColumn",
                    ]
                )
            elif braced and brace_type in ["Chevron", "X"]:
                i_node_new1 = element_number + 0
                i_node_new2 = element_number + 1
                j_node_new1 = element_number + 2
                j_node_new2 = element_number + 3

                if side in ["west", "east"]:
                    # beam_length = yj - yi
                    ops.node(i_node_new1, xi, yi + end_offset, zi)
                    ops.node(j_node_new1, xj, yj - end_offset, zj)
                    if not self.elastic_floor_beam:
                        ops.node(i_node_new2, xi, yi + end_offset, zi)
                        ops.node(j_node_new2, xj, yj - end_offset, zj)
                        dir_zero_length = 4

                elif side in ["south", "north"]:
                    # beam_length = xj - xi
                    ops.node(i_node_new1, xi + end_offset, yi, zi)
                    ops.node(j_node_new1, xj - end_offset, yj, zj)
                    if not self.elastic_floor_beam:
                        ops.node(i_node_new2, xi + end_offset, yi, zi)
                        ops.node(j_node_new2, xj - end_offset, yj, zj)
                        dir_zero_length = 5

                # TODO: Fix this constraint
                if end_moment_release:
                    moment_release_z = 0
                    moment_release_y = 0

                else:
                    moment_release_z = 0
                    moment_release_y = 0

                if self.elastic_floor_beam:
                    ops.element(
                        "elasticBeamColumn",
                        element_number + 1,
                        *[i_node_new1, j_node_new1],
                        sec_A,
                        self.material.steel_beam["YoungModulus"],
                        self.material.steel_beam["ShearModulus"],
                        sec_J,
                        sec_Iy,
                        sec_Ix,
                        transfer_tag,
                        "-mass",
                        mass,
                        "-releasez",
                        moment_release_z,
                        "-releasey",
                        moment_release_y,
                    )
                    self.list_recorder.append(
                        [
                            "floor_beam_element",
                            info,
                            element_number + 1,
                            "elasticBeamColumn",
                        ]
                    )

                else:
                    if indep_mat:
                        self.create_beam_hinge.cache_clear()

                    n_cons = 10
                    mat_tag_bilin, bilin_params = self.create_beam_hinge(
                        beam_length=len_beam,
                        beam_length_braced=len_beam,
                        YoungModulus=self.material.steel_beam["YoungModulus"],
                        Fy_beam=self.material.steel_beam["Fy"],
                        McMy=self.material.steel_beam["McMy"],
                        D=sec_D,
                        B=sec_B,
                        T=sec_T,
                        W=sec_W,
                        Ix=sec_Ix,
                        Zx=sec_Zx,
                        Ry=sec_Ry,
                        n_cons=n_cons,
                    )
                    self.list_bilin_params.append(
                        ["beam_floor", element_number, sec_D, bilin_params]
                    )

                    # first hinge element
                    ops.element(
                        "zeroLength",
                        element_number + 1,
                        *[i_node_new1, i_node_new2],
                        "-mat",
                        *[mat_tag_bilin],
                        "-dir",
                        *[dir_zero_length],
                    )
                    ops.equalDOF(
                        i_node_new1,
                        i_node_new2,
                        *[item for item in range(1, 7) if not item == dir_zero_length],
                    )
                    self.list_recorder.append(
                        [
                            "floor_beam_hinge",
                            info,
                            element_number + 1,
                            "zeroLength",
                        ]
                    )

                    # middle element
                    ops.element(
                        "elasticBeamColumn",
                        element_number + 2,
                        *[i_node_new2, j_node_new2],
                        sec_A,
                        self.material.steel_beam["YoungModulus"],
                        self.material.steel_beam["ShearModulus"],
                        sec_J * ((n_cons + 1.0) / n_cons),
                        sec_Iy * ((n_cons + 1.0) / n_cons),
                        sec_Ix * ((n_cons + 1.0) / n_cons),
                        transfer_tag,
                        "-mass",
                        mass,
                        "-releasez",
                        moment_release_z,
                        "-releasey",
                        moment_release_y,
                    )
                    self.list_recorder.append(
                        [
                            "floor_beam_element",
                            info,
                            element_number + 2,
                            "elasticBeamColumn",
                        ]
                    )

                    # second hinge element
                    ops.element(
                        "zeroLength",
                        element_number + 3,
                        *[j_node_new2, j_node_new1],
                        "-mat",
                        *[mat_tag_bilin],
                        "-dir",
                        *[dir_zero_length],
                    )
                    ops.equalDOF(
                        j_node_new2,
                        j_node_new1,
                        *[item for item in range(1, 7) if not item == dir_zero_length],
                    )
                    self.list_recorder.append(
                        [
                            "floor_beam_hinge",
                            info,
                            element_number + 3,
                            "zeroLength",
                        ]
                    )

                # 1st rigid element
                ops.element(
                    "elasticBeamColumn",
                    element_number + 0,
                    *[i_node, i_node_new1],
                    sec_A * make_rigid,
                    self.material.steel_beam["YoungModulus"],
                    self.material.steel_beam["ShearModulus"],
                    sec_J,
                    sec_Iy * make_rigid,
                    sec_Ix * make_rigid,
                    transfer_tag,
                    "-mass",
                    mass,
                    "-releasez",
                    0,
                    "-releasey",
                    0,
                )
                self.list_recorder.append(
                    [
                        "floor_beam_rigid_element",
                        info,
                        element_number + 0,
                        "elasticBeamColumn",
                    ]
                )

                # last rigid element
                ops.element(
                    "elasticBeamColumn",
                    element_number + 4,
                    *[j_node_new1, j_node],
                    sec_A * make_rigid,
                    self.material.steel_beam["YoungModulus"],
                    self.material.steel_beam["ShearModulus"],
                    sec_J,
                    sec_Iy * make_rigid,
                    sec_Ix * make_rigid,
                    transfer_tag,
                    "-mass",
                    mass,
                    "-releasez",
                    0,
                    "-releasey",
                    0,
                )
                self.list_recorder.append(
                    [
                        "floor_beam_rigid_element",
                        info,
                        element_number + 4,
                        "elasticBeamColumn",
                    ]
                )

            else:
                raise ValueError(
                    "Floor beam should be either braced (type = Chevron or X) or unbraced!"
                )

        self.logger.info("Floor beam elements have been assigned!")

        return None

    @helper.log_time_memory
    def assign_column(self, **kwargs) -> None:
        self.methods_called["assign_element"]["assign_column"] = True

        pid = kwargs.get("pid", 0)
        use_tnom = kwargs.get("use_tnom", False)
        indep_sec = kwargs.get("indep_sec", False)
        indep_mat = kwargs.get("indep_mat", False)

        if self.elastic_column:
            self.logger.warning("Elastic column has been selected!!!")

        make_rigid = 10.0
        count_warning = 0

        for row in self.generate.df_column_elements[
            self.generate.df_column_elements["pid"] == pid
        ].itertuples(index=False):
            i_node, j_node = row.i_node, row.j_node
            element_number = row.ele_number
            col_sec_props = row.section_props
            brace_side, len_column = row.brace_side, row.length
            num_of_columns = int(row.multi) if not pd.isna(row.multi) else 1
            info = {
                "story": row.story,
                "module": row.module,
                "braced": row.braced,
                "brace_side": row.brace_side,
                "num_of_columns": num_of_columns,
                "point": row.point,
                "length": row.length,
                "section": row.section,
                "element_number": element_number,
            }

            transfer_tag = int(
                self.generate.df_geo_transf.loc["column_we", "value"]
                if brace_side in ["south", "north"]
                else self.generate.df_geo_transf.loc["column_sn", "value"]
                if brace_side in ["east", "west"]
                else self.generate.df_geo_transf.loc["column_we", "value"]
            )
            # column_location = [df.story, df.module, df.point]

            sec_Ht, sec_T, sec_A, sec_Ix, sec_Iy, sec_J, sec_Zx, mass = (
                col_sec_props["Ht"],
                col_sec_props["tnom"] if use_tnom else col_sec_props["tdes"],
                col_sec_props["A"],
                col_sec_props["Ix"],
                col_sec_props["Iy"],
                col_sec_props["J"],
                col_sec_props["Zx"],
                col_sec_props["W"],
            )

            xi, yi, zi = ops.nodeCoord(i_node)
            xj, yj, zj = ops.nodeCoord(j_node)

            self.list_mass.append(
                [
                    "column_element",
                    info,
                    element_number,
                    i_node,
                    j_node,
                    len_column * mass * num_of_columns,
                ]
            )

            if self.include_element_mass:
                pass
            else:
                mass = 0.0

            i_node2 = element_number + 1
            j_node2 = element_number + 3

            # TODO: CHANGE THESE VALUES
            d_bottom = 0.1
            d_top = 0.1

            ops.node(i_node2, xi, yi, zi + d_bottom * 0.5)
            ops.node(j_node2, xj, yj, zj - d_top * 0.5)

            if row.braced and not self.elastic_column:
                i_node3 = element_number + 2
                j_node3 = element_number + 4
                ops.node(i_node3, xi, yi, zi + d_bottom * 0.5)
                ops.node(j_node3, xj, yj, zj - d_top * 0.5)

                try:
                    df_column_gravity = pd.read_pickle(
                        f"{self.directory}/{self.name}_df_column_gravity.pkl"
                    )
                    load_axial = df_column_gravity.loc[
                        int(element_number + 1), "axial_force"
                    ]
                except:
                    load_axial = 1.0
                    count_warning += 1
                    if count_warning == 1 and pid == 0:
                        self.logger.error(
                            "The axial force of the column could not be found."
                        )
                        self.logger.critical(
                            f"Please run the gravity analysis once before performing any type of nonlinear analysis."
                        )

                len_column = len_column - d_top * 0.5 - d_bottom * 0.5

                if indep_mat:
                    self.create_column_hinge.cache_clear()

                n_cons = 10.0
                mat_tag_bilin, bilin_params = self.create_column_hinge(
                    load_axial=load_axial,
                    column_length=len_column,
                    YoungModulus=self.material.steel_column["YoungModulus"],
                    Fy_column=self.material.steel_column["Fy"],
                    McMy=self.material.steel_column["McMy"],
                    D=sec_Ht,
                    T=sec_T,
                    A=sec_A,
                    Ix=sec_Ix,
                    Zx=sec_Zx,
                    n_cons=n_cons,
                )

            for i in range(num_of_columns):
                if row.braced and not self.elastic_column:
                    self.list_bilin_params.append(
                        ["column", element_number, sec_Ht, bilin_params]
                    )

                    ops.element(
                        "zeroLength",
                        element_number + (i * 5) + 3,
                        *[i_node2, i_node3],
                        "-mat",
                        *[mat_tag_bilin, mat_tag_bilin],
                        "-dir",
                        *[4, 5],
                    )
                    ops.equalDOF(i_node2, i_node3, *[1, 2, 3, 6])
                    self.list_recorder.append(
                        [
                            "column_hinge",
                            info,
                            element_number + (i * 5) + 3,
                            "zeroLength",
                        ]
                    )

                    ops.element(
                        "zeroLength",
                        element_number + (i * 5) + 4,
                        *[j_node3, j_node2],
                        "-mat",
                        *[mat_tag_bilin, mat_tag_bilin],
                        "-dir",
                        *[4, 5],
                    )
                    ops.equalDOF(j_node2, j_node3, *[1, 2, 3, 6])
                    self.list_recorder.append(
                        [
                            "column_hinge",
                            info,
                            element_number + (i * 5) + 4,
                            "zeroLength",
                        ]
                    )

                    # middle element
                    ops.element(
                        "elasticBeamColumn",
                        element_number + (i * 5) + 1,
                        *[i_node3, j_node3],
                        sec_A,
                        self.material.steel_column["YoungModulus"],
                        self.material.steel_column["ShearModulus"],
                        sec_J * ((n_cons + 1.0) / n_cons),
                        sec_Iy * ((n_cons + 1.0) / n_cons),
                        sec_Ix * ((n_cons + 1.0) / n_cons),
                        transfer_tag,
                        "-mass",
                        mass,
                        "-releasez",
                        0,
                        "-releasey",
                        0,
                    )
                    self.list_recorder.append(
                        [
                            "column_element",
                            info,
                            element_number + (i * 5) + 1,
                            "elasticBeamColumn",
                        ]
                    )

                else:
                    ops.element(
                        "elasticBeamColumn",
                        element_number + (i * 5) + 1,
                        *[i_node2, j_node2],
                        sec_A,
                        self.material.steel_column["YoungModulus"],
                        self.material.steel_column["ShearModulus"],
                        sec_J,
                        sec_Iy,
                        sec_Ix,
                        transfer_tag,
                        "-mass",
                        mass,
                        "-releasez",
                        0,
                        "-releasey",
                        0,
                    )
                    self.list_recorder.append(
                        [
                            "column_element",
                            info,
                            element_number + (i * 5) + 1,
                            "elasticBeamColumn",
                        ]
                    )

                ops.element(
                    "elasticBeamColumn",
                    element_number + (i * 5) + 0,
                    *[i_node, i_node2],
                    sec_A,
                    self.material.steel_column["YoungModulus"],
                    self.material.steel_column["ShearModulus"],
                    make_rigid * sec_J,
                    make_rigid * sec_Iy,
                    make_rigid * sec_Ix,
                    transfer_tag,
                    "-mass",
                    mass,
                    "-releasez",
                    0,
                    "-releasey",
                    0,
                )
                self.list_recorder.append(
                    [
                        "column_rigid_element",
                        info,
                        element_number + (i * 5),
                        "elasticBeamColumn",
                    ]
                )

                ops.element(
                    "elasticBeamColumn",
                    element_number + (i * 5) + 2,
                    *[j_node2, j_node],
                    sec_A,
                    self.material.steel_column["YoungModulus"],
                    self.material.steel_column["ShearModulus"],
                    make_rigid * sec_J,
                    make_rigid * sec_Iy,
                    make_rigid * sec_Ix,
                    transfer_tag,
                    "-mass",
                    mass,
                    "-releasez",
                    0,
                    "-releasey",
                    0,
                )
                self.list_recorder.append(
                    [
                        "column_rigid_element",
                        info,
                        element_number + (i * 5) + 2,
                        "elasticBeamColumn",
                    ]
                )

        self.logger.info("Column elements have been assigned.")

        return None

    @helper.log_time_memory
    def assign_ver_con(self, **kwargs) -> None:
        self.methods_called["assign_element"]["assign_ver_con"] = True

        pid = kwargs.get("pid", 0)
        use_tnom = kwargs.get("use_tnom", False)
        indep_sec = kwargs.get("indep_sec", False)
        indep_mat = kwargs.get("indep_mat", False)
        extend_multi = kwargs.get("extend_multi", False)

        ver_con_steel = int(
            self.generate.df_section_material.loc["ver_con_steel", "value"]
        )

        if self.elastic_ver_con:
            self.logger.warning("Elastic vertical connection has been selected!!!")

        make_rigid = 10.0

        for row in self.generate.df_ver_con_elements[
            self.generate.df_ver_con_elements["pid"] == pid
        ].itertuples(index=False):
            i_node, j_node = row.i_node, row.j_node
            element_number = row.ele_number
            col_sec_props = row.section_props
            len_column = row.length
            story, module, point = row.story, row.module, row.point
            num_of_columns = int(row.multi) if not pd.isna(row.multi) else 1
            info = {
                "story": story,
                "module": module,
                "braced": row.braced,
                "brace_side": row.brace_side,
                "num_of_columns": num_of_columns,
                "point": point,
                "length": row.length,
                "section": row.section,
                "element_number": element_number,
            }
            if story > 1 and extend_multi:
                num_of_columns_lower = (
                    int(
                        self.generate.df_ver_con_elements[
                            (self.generate.df_ver_con_elements["story"] == story - 1)
                            & (self.generate.df_ver_con_elements["module"] == module)
                            & (self.generate.df_ver_con_elements["point"] == point)
                        ]["multi"].values[0]
                    )
                    if not pd.isna(
                        self.generate.df_ver_con_elements[
                            (self.generate.df_ver_con_elements["story"] == story - 1)
                            & (self.generate.df_ver_con_elements["module"] == module)
                            & (self.generate.df_ver_con_elements["point"] == point)
                        ]["multi"].values[0]
                    )
                    else 1
                )

                if num_of_columns_lower - num_of_columns > 0:
                    num_of_columns = num_of_columns_lower

            transfer_tag = int(
                self.generate.df_geo_transf.loc["column_we", "value"]
                if row.brace_side in ["south", "north"]
                else self.generate.df_geo_transf.loc["column_sn", "value"]
                if row.brace_side in ["east", "west"]
                else self.generate.df_geo_transf.loc["column_we", "value"]
            )

            sec_Ht, sec_B, sec_T, sec_A, sec_Ix, sec_Iy, sec_J, mass = (
                col_sec_props["Ht"],
                col_sec_props["B"],
                col_sec_props["tnom"] if use_tnom else col_sec_props["tdes"],
                col_sec_props["A"],
                col_sec_props["Ix"],
                col_sec_props["Iy"],
                col_sec_props["J"],
                col_sec_props["W"],
            )

            xi, yi, zi = ops.nodeCoord(i_node)
            xj, yj, zj = ops.nodeCoord(j_node)

            self.list_mass.append(
                [
                    "ver_con_element",
                    info,
                    element_number,
                    i_node,
                    j_node,
                    len_column * mass * num_of_columns,
                ]
            )

            if self.include_element_mass:
                pass
            else:
                mass = 0.0

            i_node_new1 = element_number + 0
            j_node_new1 = element_number + 1

            # TODO: CHANGE THESE VALUES
            d_bottom, d_top = 0.1, 0.1

            ops.node(i_node_new1, xi, yi, zi + d_bottom * 0.5)
            ops.node(j_node_new1, xj, yj, zj - d_top * 0.5)

            if story == 1:
                release_z, release_y = 0, 0
            else:
                release_z, release_y = 1, 1

            if not self.elastic_ver_con:
                if indep_sec:
                    self.hss_section.cache_clear()

                section_tag = self.hss_section(
                    mat_tag=ver_con_steel,
                    num_subdiv_len=10,
                    num_subdiv_thick=4,
                    num_subdiv_corner_len=4,
                    num_subdiv_corner_thick=4,
                    D=round(sec_Ht, 6),
                    B=round(sec_B, 6),
                    T=round(sec_T, 6),
                    J=round(sec_J, 6),
                    G=self.material.steel_column["ShearModulus"],
                )

                nip = 5
                ops.beamIntegration("Lobatto", element_number, section_tag, nip)

            for i in range(num_of_columns):
                # first rigid element
                ops.element(
                    "elasticBeamColumn",
                    element_number + (i * 5) + 0,
                    *[i_node, i_node_new1],
                    sec_A,
                    self.material.steel_column["YoungModulus"],
                    self.material.steel_column["ShearModulus"],
                    make_rigid * sec_J,
                    make_rigid * sec_Iy,
                    make_rigid * sec_Ix,
                    transfer_tag,
                    "-mass",
                    mass,
                    "-releasez",
                    0,
                    "-releasey",
                    0,
                )
                self.list_recorder.append(
                    [
                        "ver_con_rigid_element",
                        info,
                        element_number + (i * 5),
                        "elasticBeamColumn",
                    ]
                )
                # second rigid element
                ops.element(
                    "elasticBeamColumn",
                    element_number + (i * 5) + 2,
                    *[j_node_new1, j_node],
                    sec_A,
                    self.material.steel_column["YoungModulus"],
                    self.material.steel_column["ShearModulus"],
                    make_rigid * sec_J,
                    make_rigid * sec_Iy,
                    make_rigid * sec_Ix,
                    transfer_tag,
                    "-mass",
                    mass,
                    "-releasez",
                    release_z,
                    "-releasey",
                    release_y,
                )
                self.list_recorder.append(
                    [
                        "ver_con_rigid_element",
                        info,
                        element_number + (i * 5) + 2,
                        "elasticBeamColumn",
                    ]
                )

                if self.elastic_ver_con:
                    ops.element(
                        "elasticBeamColumn",
                        element_number + (i * 5) + 1,
                        *[i_node_new1, j_node_new1],
                        sec_A,
                        self.material.steel_column["YoungModulus"],
                        self.material.steel_column["ShearModulus"],
                        sec_J,
                        sec_Iy,
                        sec_Ix,
                        transfer_tag,
                        "-mass",
                        mass,
                        "-releasez",
                        0,
                        "-releasey",
                        0,
                    )
                    self.list_recorder.append(
                        [
                            "ver_con_elastic_element",
                            info,
                            element_number + (i * 5) + 1,
                            "elasticBeamColumn",
                        ]
                    )
                else:
                    ops.element(
                        "dispBeamColumn",
                        element_number + (i * 5) + 1,
                        *[i_node_new1, j_node_new1],
                        transfer_tag,
                        element_number,
                        "-mass",
                        mass,
                    )
                    self.list_recorder.append(
                        [
                            "ver_con_element",
                            info,
                            element_number + (i * 5) + 1,
                            "dispBeamColumn",
                        ]
                    )

        self.logger.info("Vertical connection elements has been assigned.")

        return None

    def assign_hor_con(self, **kwargs) -> None:
        self.methods_called["assign_element"]["assign_hor_con"] = True

        pid = kwargs.get("pid", 0)
        indep_sec = kwargs.get("indep_sec", False)
        indep_mat = kwargs.get("indep_mat", False)

        if not self.elastic_hor_con:
            raise ValueError(
                f"Horizontal connection must be elastic!!!, given that {self.elastic_hor_con = }"
            )

        make_rigid = 1.3

        for row in self.generate.df_hor_con_elements_filtered[
            self.generate.df_hor_con_elements_filtered["pid"] == pid
        ].itertuples(index=False):
            model = row.model
            if model != "Annan2009":
                raise ValueError(
                    f"Currently, only Annan2009 model is supported for horizontal connection, given that {model = }"
                )

            i_node, j_node = row.i_node, row.j_node
            element_number = row.ele_number
            direction, len_beam = (row.direction, row.length)
            sec_props = row.section_props

            (
                sec_A,
                sec_J,
                sec_Iy,
                sec_Ix,
                mass,
            ) = (
                sec_props["A"],
                sec_props["J"],
                sec_props["Iy"],
                sec_props["Ix"],
                sec_props["W"],
            )
            info = {
                "story": row.story,
                "direction": direction,
                "braced": row.braced,
                "i_node": i_node,
                "j_node": j_node,
                "length": len_beam,
                "element_number": element_number,
                "model": model,
            }

            transfer_tag = int(
                self.generate.df_geo_transf.loc["beam_we", "value"]
                if direction in ["west-east", "east-west"]
                else self.generate.df_geo_transf.loc["beam_sn", "value"]
                if direction in ["south-north", "north-south"]
                else None
            )

            """
            This is unnecessary but will be handy when incorporating other models for horizontal connection.
            """

            if row.braced:
                self.list_mass.append(
                    [
                        "hor_con_element",
                        info,
                        element_number,
                        i_node,
                        j_node,
                        len_beam * mass,
                    ]
                )

                if self.include_element_mass:
                    pass
                else:
                    mass = 0.0

                ops.element(
                    "elasticBeamColumn",
                    element_number,
                    *[i_node, j_node],
                    sec_A * make_rigid,
                    self.material.steel_beam["YoungModulus"],
                    self.material.steel_beam["ShearModulus"],
                    sec_J * make_rigid,
                    sec_Iy * make_rigid,
                    sec_Ix * make_rigid,
                    transfer_tag,
                    "-mass",
                    mass,
                    "-releasez",
                    0,
                    "-releasey",
                    0,
                )
                self.list_recorder.append(
                    [
                        "hor_con_element",
                        info,
                        element_number,
                        "elasticBeamColumn",
                    ]
                )

            elif not row.braced:
                self.list_mass.append(
                    [
                        "hor_con_element",
                        info,
                        element_number,
                        i_node,
                        j_node,
                        len_beam * mass,
                    ]
                )

                if self.include_element_mass:
                    pass
                else:
                    mass = 0.0

                ops.element(
                    "elasticBeamColumn",
                    element_number,
                    *[i_node, j_node],
                    sec_A * make_rigid,
                    self.material.steel_beam["YoungModulus"],
                    self.material.steel_beam["ShearModulus"],
                    sec_J * make_rigid,
                    sec_Iy * make_rigid,
                    sec_Ix * make_rigid,
                    transfer_tag,
                    "-mass",
                    mass,
                    "-releasez",
                    0,
                    "-releasey",
                    0,
                )
                self.list_recorder.append(
                    [
                        "hor_con_element",
                        info,
                        element_number,
                        "elasticBeamColumn",
                    ]
                )

            else:
                raise ValueError(
                    "Horizontal connection should be either braced or unbraced!"
                )

        self.logger.info("Horizontal connection elements have been assigned.")

        return None

    def plot_elements_3D(self, plot_kwargs={}, **kwargs) -> tuple:
        node_tags = ops.getNodeTags()
        node_data = [[node_tag, *ops.nodeCoord(node_tag)] for node_tag in node_tags]
        ele_tags = ops.getEleTags()
        ele_data = [[ele_tag, *ops.eleNodes(ele_tag)] for ele_tag in ele_tags]
        fig, ax = helper.plot_elements_3D(node_data, ele_data, plot_kwargs)
        fig.show()
        return fig, ax


class _Generate(object):
    """
    This class is used to generate the model.

    .. caution::
        This class is not meant to be used directly. Please use the ``get_generate()`` method of :class:`Model` class to call methods and attributes.

    """

    def __init__(self, name, directory, logger, material, **kwargs):
        self.name = name
        self.directory = directory
        self.logger = logger
        self.material = material
        self.nprocs = kwargs["generate_kwargs"].get("nprocs", 1)
        metric_label = kwargs["generate_kwargs"].get("metric_label", True)
        self.nprocs_analyze = kwargs["analyze_kwargs"].get("nprocs", 1)

        if self.nprocs > 1:
            self.nprocs = 1
            self.logger.warning(
                f"Currently, parallel processing for the model generation is not supported. The number of processors is set to 1."
            )

        data_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "data/aisc-shapes-database-v16.0.xlsx",
        )
        df = pd.read_excel(data_path, sheet_name="Database v16.0").set_index("Type")

        if not metric_label:
            labels = df["AISC_Manual_Label"]

        df = df.filter(regex="\.1$")
        df.columns = df.columns.str.rstrip(".1")

        if not metric_label:
            df["AISC_Manual_Label"] = labels

        columns_W = [
            "AISC_Manual_Label",
            "W",
            "A",
            "d",
            "bf",
            "tw",
            "tf",
            "Ix",
            "Zx",
            "Sx",
            "rx",
            "Iy",
            "Zy",
            "Sy",
            "ry",
            "J",
            "T",
        ]
        columns_HSS = [
            "AISC_Manual_Label",
            "W",
            "A",
            "Ht",
            "B",
            "tnom",
            "tdes",
            "Ix",
            "Zx",
            "Sx",
            "rx",
            "Iy",
            "Zy",
            "Sy",
            "ry",
            "J",
        ]
        self.df_steel_W = (
            df.loc["W", columns_W]
            .set_index("AISC_Manual_Label")
            .replace("–", 0)
            .astype(float)
        )
        self.df_steel_HSS = (
            df.loc["HSS", columns_HSS]
            .set_index("AISC_Manual_Label")
            .replace("–", 0)
            .astype(float)
        )

        for df in [self.df_steel_W, self.df_steel_HSS]:
            for col in df.columns:
                if col in [
                    "W",
                    "d",
                    "bf",
                    "tw",
                    "tf",
                    "Ht",
                    "B",
                    "tnom",
                    "tdes",
                    "T",
                    "rx",
                    "ry",
                ]:
                    df[col] = df[col] * 1e-3
                elif col in ["A"]:
                    df[col] = df[col] * 1e-6
                elif col in ["Sx", "Sy", "Zx", "Zy"]:
                    df[col] = df[col] * 1e-9 * 1e3
                elif col in ["Ix", "Iy"]:
                    df[col] = df[col] * 1e-12 * 1e6
                elif col in ["J"]:
                    df[col] = df[col] * 1e-12 * 1e3
                else:
                    pass

        self._modules = None
        self.methods_called = {
            "layout": False,
            "height": False,
            "diaphragm": False,
            "node": False,
            "geo_transf": False,
            "section_material": False,
            "element": False,
            "connection": False,
            "load": False,
            "partition": False,
        }

    @property
    def modules(self):
        return self._modules

    @modules.setter
    def modules(self, value):
        self._modules = value

    @helper.log_time_memory
    def layout(self, layout=None, horizontal_spacing=None, **kwargs) -> None:
        """
        This method is used to define the layout of the model. The layout is defined by the modules dictionary. The modules dictionary is a nested dictionary with the following structure:

        Here's an example of a dictionary:

        .. code-block:: python

            layouts = {
                "1-3": {
                    1: {
                        "we-dir": 3.5,
                        "sn-dir": 12,
                        "location": "south-west",
                        "brace": [
                            {"side": "west", "range": "entire", "type": "Chevron"},
                        ],
                        "sw-coord": [0.0, 0.0],
                    },
                    2: {
                        "we-dir": 3.5,
                        "sn-dir": 10.4,
                        "location": "north-1",
                        "brace": [
                            {"side": "west", "range": "entire", "type": "Chevron"},
                        ],
                        "sw-coord": [0.0, 12 + 0.35],
                    },
            }

        The key of the first level of the dictionary is the story number. In this case this layout is defined for stories 1 to 3 (inclusive).

        The key of the second level of the dictionary is the module number. Make sure you number the modules in the order you want them to be generated.

        The value of the second level of the dictionary is a dictionary with the following keys:

        - ``we-dir``: The width of the module in the west-east direction.
        - ``sn-dir``: The width of the module in the south-north direction.
        - ``location``: The location of the module in the story. The location can be one of the following: ``south-west``, ``north-1``, ``north-2``, ``north-3``, ``north-4``, ``east-1``, ``east-2``, ``east-3``, ``east-4``.
        - ``brace``: The bracing configuration of the module. The bracing configuration is a list of dictionaries. Each dictionary in the list represents a bracing configuration. The dictionary has the following keys:
            - ``side``: The side of the module that is braced. The side can be one of the following: ``south``, ``north``, ``east``, ``west``.
            - ``range``: The range of the bracing. The range can be one of the following: ``entire``, ``all``, ``full``, ``start-end``. If the range is ``start-end``, then the bracing is applied from the start of the module to the end of the module. If the range is ``entire``, ``all``, or ``full``, then the bracing is applied from the start of the module to the end of the module.
            - ``type``: The type of the bracing. The type can be one of the following: ``Chevron``, ``X``.
        - ``sw-coord``: The south-west coordinate of the module. The south-west coordinate is a list with two elements. The first element is the x-coordinate and the second element is the y-coordinate.

        Args:
            layout (dict): The layout dictionary. Defaults to None.

            horizontal_spacing (float): The horizontal spacing between the modules. Defaults to None.

        Keyword Args:
            plot_kwargs (dict, optional): The plot_kwargs dictionary. Defaults to {}.


        Raises:
            ValueError: If layout or horizontal_spacing is not provided.

        Returns:
            None

        Examples:

            .. code-block:: python

                generate.layout(
                    layout=input_layout,
                    horizontal_spacing=0.5,
                )

        """
        self.methods_called["layout"] = True

        self.modules = layout
        if self.modules is None or not isinstance(self.modules, dict):
            raise ValueError("Modules dictionary is not provided.")

        if horizontal_spacing is None or not isinstance(horizontal_spacing, float):
            raise ValueError("Horizontal spacing is not provided.")

        plot_kwargs = kwargs.get("plot_kwargs", {})

        positions = {}
        corners = {}
        brace_positions = {}
        x, y = 0.0, 0.0  # Starting positions

        for story, submodules in self.modules.items():
            for module_number, module in submodules.items():
                if module.get("sw-coord"):
                    x = module["sw-coord"][0]
                    y = module["sw-coord"][1]

                    if (
                        module["location"] == "south-west"
                        or module["location"] == "0.0"
                    ):
                        module["west-spacing"] = 0.0 if x == 0.0 else x
                        module["south-spacing"] = 0.0 if y == 0.0 else y
                    elif module["location"] == "north-1":
                        module["west-spacing"] = 0.0 if x == 0.0 else x
                        module["south-spacing"] = module.get(
                            "south-spacing", horizontal_spacing
                        )
                    elif module["location"].split("-")[0] == "east":
                        module["west-spacing"] = module.get(
                            "west-spacing", horizontal_spacing
                        )
                        module["south-spacing"] = 0.0 if y == 0.0 else y
                    else:
                        module["west-spacing"] = module.get(
                            "west-spacing", horizontal_spacing
                        )
                        module["south-spacing"] = module.get(
                            "south-spacing", horizontal_spacing
                        )

                else:
                    if (
                        module["location"] == "south-west"
                        or module["location"] == "0.0"
                    ):
                        x += module.get("west-spacing", 0.0)
                        y += module.get("south-spacing", 0.0)

                        module["west-spacing"] = 0.0 if x == 0.0 else x
                        module["south-spacing"] = 0.0 if y == 0.0 else y
                    else:
                        # Get the module number from the location
                        relative_module_number = int(module["location"].split("-")[1])
                        relative_module = self.modules[story][relative_module_number]

                        if "north" in module["location"]:
                            x = (
                                positions[relative_module_number][0]
                                - horizontal_spacing
                                + module.get("west-spacing", horizontal_spacing)
                            )
                            y = (
                                positions[relative_module_number][1]
                                + relative_module["sn-dir"]
                                + module.get("south-spacing", horizontal_spacing)
                            )
                        elif "east" in module["location"]:
                            x = (
                                positions[relative_module_number][0]
                                + relative_module["we-dir"]
                                + module.get("west-spacing", horizontal_spacing)
                            )
                            y = (
                                positions[relative_module_number][1]
                                - horizontal_spacing
                                + module.get("south-spacing", horizontal_spacing)
                            )

                        if module["location"] == "north-1":
                            module["west-spacing"] = 0.0 if x == 0.0 else x
                            module["south-spacing"] = module.get(
                                "south-spacing", horizontal_spacing
                            )
                        elif module["location"].split("-")[0] == "east":
                            module["west-spacing"] = module.get(
                                "west-spacing", horizontal_spacing
                            )
                            module["south-spacing"] = 0.0 if y == 0.0 else y
                        else:
                            module["west-spacing"] = module.get(
                                "west-spacing", horizontal_spacing
                            )
                            module["south-spacing"] = module.get(
                                "south-spacing", horizontal_spacing
                            )

                positions[module_number] = (x, y)
                module["sw-coord"] = (x, y)

                if module.get("brace"):
                    brace_positions[module_number] = {}
                    for brace in module["brace"]:
                        # side, range_, type_brace = brace
                        side = brace["side"]
                        range_ = brace["range"]
                        type_brace = brace["type"]

                        if range_ == "entire" or range_ == "all" or range_ == "full":
                            if side in ["south"]:
                                start_x, end_x = 0.0, module["we-dir"]
                                start_y, end_y = 0.0, 0.0
                            elif side in ["north"]:
                                start_x, end_x = 0.0, module["we-dir"]
                                start_y, end_y = module["sn-dir"], module["sn-dir"]
                            elif side in ["east"]:
                                start_y, end_y = 0.0, module["sn-dir"]
                                start_x, end_x = module["we-dir"], module["we-dir"]
                            elif side in ["west"]:
                                start_y, end_y = 0.0, module["sn-dir"]
                                start_x, end_x = 0.0, 0.0
                        else:
                            if side in ["south"]:
                                split_range = range_.split("-")
                                if split_range[0] == "start":
                                    start = 0.0
                                else:
                                    start = float(split_range[0])
                                if split_range[1] == "end":
                                    end = module["we-dir"]
                                else:
                                    end = float(split_range[1])

                                start_x, end_x = start, end
                                start_y, end_y = 0.0, 0.0
                            elif side in ["north"]:
                                split_range = range_.split("-")
                                if split_range[0] == "start":
                                    start = 0.0
                                else:
                                    start = float(split_range[0])
                                if split_range[1] == "end":
                                    end = module["we-dir"]
                                else:
                                    end = float(split_range[1])

                                start_x, end_x = start, end
                                start_y, end_y = module["sn-dir"], module["sn-dir"]
                            elif side in ["east"]:
                                split_range = range_.split("-")
                                if split_range[0] == "start":
                                    start = 0.0
                                else:
                                    start = float(split_range[0])
                                if split_range[1] == "end":
                                    end = module["sn-dir"]
                                else:
                                    end = float(split_range[1])

                                start_y, end_y = start, end
                                start_x, end_x = module["we-dir"], module["we-dir"]
                            elif side in ["west"]:
                                split_range = range_.split("-")
                                if split_range[0] == "start":
                                    start = 0.0
                                else:
                                    start = float(split_range[0])
                                if split_range[1] == "end":
                                    end = module["sn-dir"]
                                else:
                                    end = float(split_range[1])
                                start_y, end_y = start, end
                                start_x, end_x = 0.0, 0.0

                        # Calculate the global start and end points
                        global_start_x = start_x + x
                        global_end_x = end_x + x
                        global_start_y = start_y + y
                        global_end_y = end_y + y

                        # Calculate the middle point if the type is "Chevron"
                        if (
                            type_brace == "Chevron"
                            or type_brace == "chevron"
                            or type_brace == "^"
                            or type_brace == "inv-v"
                            or type_brace == "V-shape"
                            or type_brace == "inverted-V"
                        ):
                            type_brace = "Chevron"
                            middle_x = (start_x + end_x) / 2
                            middle_y = (start_y + end_y) / 2
                            global_middle_x = (global_start_x + global_end_x) / 2
                            global_middle_y = (global_start_y + global_end_y) / 2
                            brace_positions[module_number][(side, type_brace)] = {
                                "relative": (
                                    (round(start_x, 6), round(start_y, 6)),
                                    (round(middle_x, 6), round(middle_y, 6)),
                                    (round(end_x, 6), round(end_y, 6)),
                                ),
                                "global": (
                                    (
                                        round(global_start_x, 6),
                                        round(global_start_y, 6),
                                    ),
                                    (
                                        round(global_middle_x, 6),
                                        round(global_middle_y, 6),
                                    ),
                                    (round(global_end_x, 6), round(global_end_y, 6)),
                                ),
                                "range": range_,
                            }
                            module["brace_positions"] = brace_positions[module_number]

                        elif (
                            type_brace == "X"
                            or type_brace == "x"
                            or "cross" in type_brace
                            or type_brace == "Cross"
                            or "cross-brace" in type_brace
                        ):
                            type_brace = "X"
                            brace_positions[module_number][(side, type_brace)] = {
                                "relative": (
                                    (round(start_x, 6), round(start_y, 6)),
                                    (round(end_x, 6), round(end_y, 6)),
                                ),
                                "global": (
                                    (
                                        round(global_start_x, 6),
                                        round(global_start_y, 6),
                                    ),
                                    (round(global_end_x, 6), round(global_end_y, 6)),
                                ),
                                "range": range_,
                            }
                            module["brace_positions"] = brace_positions[module_number]
                        else:
                            raise ValueError(
                                f"Please provide a valid brace type. {type_brace} is not valid."
                            )

                        corners[module_number] = [
                            (x, y),
                            (x + module["we-dir"], y),
                            (x + module["we-dir"], y + module["sn-dir"]),
                            (x, y + module["sn-dir"]),
                        ]
                        module["corners"] = corners[module_number]
                        module["points"] = [
                            (x, y),
                            (x + module["we-dir"], y),
                            (x + module["we-dir"], y + module["sn-dir"]),
                            (x, y + module["sn-dir"]),
                            (global_start_x, global_start_y),
                            (global_end_x, global_end_y),
                        ]

                else:
                    brace_positions[module_number] = None
                    corners[module_number] = [
                        (x, y),
                        (x + module["we-dir"], y),
                        (x + module["we-dir"], y + module["sn-dir"]),
                        (x, y + module["sn-dir"]),
                    ]
                    module["corners"] = corners[module_number]
                    module["points"] = corners[module_number]
                    module["brace_positions"] = None

        for story, submodules in self.modules.items():
            for module_number, module in submodules.items():
                for key in ["points", "corners"]:
                    module[key] = [
                        tuple(round(num, 6) for num in item) for item in module[key]
                    ]

        # sort the points and corners of each module:  sw corner --> ccw
        for story, submodules in self.modules.items():
            for module_number, module in submodules.items():
                for key in ["points", "corners"]:
                    # items = np.unique(np.array(module[key]), axis=0)
                    # sw_idx = np.argmin(np.sum(items, axis=1))
                    # sw_corner = items[sw_idx]
                    # items = np.delete(items, sw_idx, axis=0)
                    # angles = np.arctan2(
                    #     items[:, 1] - sw_corner[1], items[:, 0] - sw_corner[0]
                    # )
                    # sorted_items = items[np.argsort(angles)]
                    # sorted_items = np.vstack([sw_corner, sorted_items])
                    # module[key] = sorted_items

                    items = np.unique(np.array(module[key]), axis=0)
                    sw_idx = np.argmin(np.sum(items, axis=1))
                    sw_corner = items[sw_idx]
                    items = np.delete(items, sw_idx, axis=0)

                    # Calculate polar angles from the southwest corner
                    angles = np.arctan2(items[:, 1] - sw_corner[1], items[:, 0] - sw_corner[0])

                    # Calculate distances from the southwest corner
                    distances = np.sqrt((items[:, 0] - sw_corner[0])**2 + (items[:, 1] - sw_corner[1])**2)

                    # Identify unique angles and their indices
                    unique_angles, unique_indices = np.unique(angles, return_index=True)

                    # For each unique angle, sort the points with that angle by distance (farthest first)
                    sorted_items = []
                    for angle, index in zip(unique_angles, unique_indices):
                        same_angle_items = items[angles == angle]
                        if len(same_angle_items) > 1:
                            same_angle_distances = distances[angles == angle]
                            sorted_indices = np.argsort(same_angle_distances)[::-1]  # Reverse the order
                            sorted_same_angle_items = same_angle_items[sorted_indices]
                            sorted_items.extend(sorted_same_angle_items)
                        else:
                            sorted_items.append(items[index])

                    sorted_items = np.vstack([sw_corner, sorted_items])
                    module[key] = sorted_items

        spacing_info = {}

        for story, submodules in self.modules.items():
            for module_number, module in submodules.items():
                spacing_info[(story, module_number)] = {
                    "west-spacing": module["west-spacing"],
                    "south-spacing": module["south-spacing"],
                }

        edge_modules = {}

        for story, submodules in self.modules.items():
            edge_modules[story] = []
            for module_number, module in submodules.items():
                for point in module["points"]:
                    if -1e-6 <= point[0] <= 1e-6 or -1e-6 <= point[1] <= 1e-6:
                        edge_modules[story].append(module_number)
                        break

        df_spacing = (
            pd.DataFrame.from_dict(spacing_info, orient="index")
            .reset_index(drop=False)
            .rename({"level_0": "story", "level_1": "ID"}, axis=1)
        )

        for key, items in edge_modules.items():
            df_spacing_edge = df_spacing[
                (df_spacing["ID"].isin(edge_modules[key]))
                & (df_spacing["story"] == key)
            ]
            df_spacing_not_edge = df_spacing[
                (~df_spacing["ID"].isin(edge_modules[key]))
                & (df_spacing["story"] == key)
            ]

            for search_key in ["west", "south"]:
                output = helper.check_horizontal_distance(
                    df_spacing_edge, horizontal_spacing, search_key=search_key
                )
                for dummy in output:
                    if not dummy.empty:
                        self.logger.debug(
                            f"Make sure that the following modules are located at the {search_key}-edge of the building: {', '.join(f'{int(row.ID)}' for row in dummy.itertuples(index=False))} for story: {key}\n"
                        )

                output = helper.check_horizontal_distance(
                    df_spacing_not_edge, horizontal_spacing, search_key=search_key
                )
                for dummy in output:
                    if not dummy.empty:
                        self.logger.warning(
                            f"Horizontal spacing is different than {horizontal_spacing} m for the following modules: {', '.join(f'{int(row.ID)}' for row in dummy.itertuples(index=False))} for story: {key}\nIt might overlap with the adjacent modules.\n"
                        )

        self.df_module_coords = pd.concat(
            [
                pd.DataFrame(module["points"], columns=["X", "Y"])
                .assign(ID=module_number)
                .assign(story=story)
                .drop_duplicates()
                for story, submodules in self.modules.items()
                for module_number, module in submodules.items()
            ]
        )

        self.df_module_coords = (
            self.df_module_coords.groupby(["ID", "story"])
            .agg({"X": list, "Y": list})
            .reset_index()
        )

        data = []
        for story, submodules in self.modules.items():
            for module_number, module in submodules.items():
                if module["brace_positions"]:
                    for key, value in module["brace_positions"].items():
                        # for (side, type_brace), _, global_coords in module[
                        #     "brace_positions"
                        # ]:
                        if value.get("global") and key[1] == "Chevron":
                            data.append(
                                {
                                    "story": story,
                                    "ID": module_number,
                                    "X": value["global"][1][0],
                                    "Y": value["global"][1][1],
                                }
                            )

        self.df_module_mid_nodes = pd.DataFrame(data)

        unique_nodes = {}
        if not self.df_module_mid_nodes.empty:
            for story, _ in self.modules.items():
                unique_x = np.unique(
                    pd.concat(
                        [
                            self.df_module_coords[self.df_module_coords.story == story][
                                "X"
                            ]
                            .explode()
                            .astype(float),
                            self.df_module_mid_nodes[
                                self.df_module_mid_nodes.story == story
                            ]["X"],
                        ]
                    )
                )

                unique_y = np.unique(
                    pd.concat(
                        [
                            self.df_module_coords[self.df_module_coords.story == story][
                                "Y"
                            ]
                            .explode()
                            .astype(float),
                            self.df_module_mid_nodes[
                                self.df_module_mid_nodes.story == story
                            ]["Y"],
                        ]
                    )
                )

                unique_nodes[story] = (unique_x, unique_y)
        else:
            for story, _ in self.modules.items():
                unique_x = np.unique(
                    self.df_module_coords[self.df_module_coords.story == story]["X"]
                    .explode()
                    .astype(float)
                )

                unique_y = np.unique(
                    self.df_module_coords[self.df_module_coords.story == story]["Y"]
                    .explode()
                    .astype(float)
                )

                unique_nodes[story] = (unique_x, unique_y)

        unique_x_all = set()
        unique_y_all = set()

        for x_values, y_values in unique_nodes.values():
            unique_x_all.update(x_values)
            unique_y_all.update(y_values)

        self.df_grid_x = pd.DataFrame(
            unique_x_all, columns=["X"], index=np.arange(11, len(unique_x_all) + 11)
        )
        self.df_grid_y = pd.DataFrame(
            unique_y_all, columns=["Y"], index=np.arange(11, len(unique_y_all) + 11)
        )

        self.nodes_floor = {}
        for story, _ in self.modules.items():
            self.nodes_floor[story] = (
                pd.DataFrame(
                    np.column_stack(
                        (
                            self.df_module_coords[self.df_module_coords.story == story][
                                "X"
                            ].explode(),
                            self.df_module_coords[self.df_module_coords.story == story][
                                "Y"
                            ].explode(),
                        )
                    ),
                    columns=["X", "Y"],
                )
                .drop_duplicates(subset=["X", "Y"])
                .reset_index(drop=True)
            )

        self.nodes_ceiling = {}
        if not self.df_module_mid_nodes.empty:
            for story, _ in self.modules.items():
                self.nodes_ceiling[story] = (
                    pd.DataFrame(
                        np.column_stack(
                            (
                                np.hstack(
                                    (
                                        self.df_module_coords[
                                            self.df_module_coords.story == story
                                        ]["X"].explode(),
                                        self.df_module_mid_nodes[
                                            self.df_module_mid_nodes.story == story
                                        ]["X"],
                                    )
                                ),
                                np.hstack(
                                    (
                                        self.df_module_coords[
                                            self.df_module_coords.story == story
                                        ]["Y"].explode(),
                                        self.df_module_mid_nodes[
                                            self.df_module_mid_nodes.story == story
                                        ]["Y"],
                                    )
                                ),
                            )
                        ),
                        columns=["X", "Y"],
                    )
                    .drop_duplicates(subset=["X", "Y"])
                    .reset_index(drop=True)
                )
        else:
            for story, _ in self.modules.items():
                self.nodes_ceiling[story] = (
                    pd.DataFrame(
                        np.column_stack(
                            (
                                self.df_module_coords[
                                    self.df_module_coords.story == story
                                ]["X"].explode(),
                                self.df_module_coords[
                                    self.df_module_coords.story == story
                                ]["Y"].explode(),
                            )
                        ),
                        columns=["X", "Y"],
                    )
                    .drop_duplicates(subset=["X", "Y"])
                    .reset_index(drop=True)
                )

        for story, _ in self.modules.items():
            self.nodes_floor[story]["X_ID"] = self.nodes_floor[story]["X"].map(
                self.df_grid_x.reset_index().set_index("X")["index"]
            )
            self.nodes_floor[story]["Y_ID"] = self.nodes_floor[story]["Y"].map(
                self.df_grid_y.reset_index().set_index("Y")["index"]
            )

            self.nodes_ceiling[story]["X_ID"] = self.nodes_ceiling[story]["X"].map(
                self.df_grid_x.reset_index().set_index("X")["index"]
            )
            self.nodes_ceiling[story]["Y_ID"] = self.nodes_ceiling[story]["Y"].map(
                self.df_grid_y.reset_index().set_index("Y")["index"]
            )

        if not self.df_module_mid_nodes.empty:
            self.df_module_mid_nodes["X_ID"] = self.df_module_mid_nodes["X"].map(
                self.df_grid_x.reset_index().set_index("X")["index"]
            )
            self.df_module_mid_nodes["Y_ID"] = self.df_module_mid_nodes["Y"].map(
                self.df_grid_y.reset_index().set_index("Y")["index"]
            )

        self.df_module_coords["X_ID"] = [
            [self.df_grid_x.reset_index().set_index("X")["index"].get(x) for x in lst]
            for lst in self.df_module_coords["X"]
        ]

        self.df_module_coords["Y_ID"] = [
            [self.df_grid_y.reset_index().set_index("Y")["index"].get(y) for y in lst]
            for lst in self.df_module_coords["Y"]
        ]

        for story, submodules in self.modules.items():
            for module_number, module in submodules.items():
                module["points_ID"] = [
                    (
                        self.df_grid_x.reset_index().set_index("X")["index"].get(x),
                        self.df_grid_y.reset_index().set_index("Y")["index"].get(y),
                    )
                    for x, y in module["points"]
                ]

        for story, submodules in self.modules.items():
            for module_number, module in submodules.items():
                module["corners_ID"] = [
                    (
                        self.df_grid_x.reset_index().set_index("X")["index"].get(x),
                        self.df_grid_y.reset_index().set_index("Y")["index"].get(y),
                    )
                    for x, y in module["corners"]
                ]

        brace_global_ID = {}
        for story, submodules in self.modules.items():
            for module_number, module in submodules.items():
                if module.get("brace"):
                    for key, value in module["brace_positions"].items():
                        brace_global_ID[key] = []
                        for i in range(len(value["global"])):
                            brace_global_ID[key].append(
                                (
                                    self.df_grid_x.reset_index()
                                    .set_index("X")["index"]
                                    .get(value["global"][i][0]),
                                    self.df_grid_y.reset_index()
                                    .set_index("Y")["index"]
                                    .get(value["global"][i][1]),
                                ),
                            )
                        module["brace_positions"][key]["global_ID"] = brace_global_ID[
                            key
                        ]

        flattened_data1, flattened_data2 = [], []
        for story, submodules in self.modules.items():
            story_range = helper.convert_to_range(story)
            for story_num in story_range:
                for key1, values1 in submodules.items():
                    values1_copy = values1.copy()
                    values1_copy["module"] = key1
                    values1_copy["story"] = story_num
                    flattened_data1.append(values1_copy)
                for module_number, module in submodules.items():
                    if module.get("brace_positions"):
                        for key2, values2 in module["brace_positions"].items():
                            side, type_brace = key2
                            flattened_data2.append(
                                {
                                    "story": story_num,
                                    "module": module_number,
                                    "side": side,
                                    "type_brace": type_brace,
                                    "relative_coords": values2["relative"],
                                    "global_coords": values2["global"],
                                    "global_ID": values2["global_ID"],
                                }
                            )

        self.df_modules = (
            pd.DataFrame(flattened_data1)
            .set_index(["story", "module"])
            .rename({"we-dir": "we_dir", "sn-dir": "sn_dir"}, axis=1)
        )
        self.df_brace_positions = pd.DataFrame(flattened_data2).set_index(
            ["story", "module"]
        )

        point_neighbors = self.__find_neighbors(
            threshold=horizontal_spacing, search_key="points"
        )

        corner_neighbors = self.__find_neighbors(
            threshold=horizontal_spacing, search_key="corners"
        )

        data = [
            {"story": key[0], "point": key[1], "neighbors": value}
            for key, value in point_neighbors.items()
        ]

        self.df_point_neighbors = pd.DataFrame(data)
        self.df_point_neighbors[["module", "point"]] = pd.DataFrame(
            self.df_point_neighbors["point"].tolist(),
            index=self.df_point_neighbors.index,
        )
        self.df_point_neighbors["story"] = self.df_point_neighbors["story"].apply(
            helper.convert_to_range
        )

        data = [
            {"story": key[0], "corner": key[1], "neighbors": value}
            for key, value in corner_neighbors.items()
        ]

        self.df_corner_neighbors = pd.DataFrame(data)
        self.df_corner_neighbors[["module", "corner"]] = pd.DataFrame(
            self.df_corner_neighbors["corner"].tolist(),
            index=self.df_corner_neighbors.index,
        )
        self.df_corner_neighbors["story"] = self.df_corner_neighbors["story"].apply(
            helper.convert_to_range
        )

        for story, submodules in self.modules.items():
            for item in submodules.items():
                for key, value in item[1].items():
                    self.logger.debug(
                        f"{key} of the module {item[0]} ({story}): \n{value}\n"
                    )

        for key, value in point_neighbors.items():
            self.logger.debug(f"Neighbors of the (module, point) {key}: \n{value}\n")

        for key, value in corner_neighbors.items():
            self.logger.debug(f"Neighbors of the (module, corner) {key}: \n{value}\n")

        if plot_kwargs.get("show", False):
            figs_axs = self.__plot_module_2D(plot_kwargs)
            for fig, ax in figs_axs:
                fig.show()

        return None

    @helper.log_time_memory
    def height(self, height=None, **kwargs) -> None:
        """
        This method is used to define the height of the building. The height is defined by the height dictionary. The height dictionary is a nested dictionary with the following structure:

        Here's an example of a dictionary:

        .. code-block:: python

            height = {
                "ground_level": 0.0,
                "1": {
                    "module": 3.5 + 0.6,
                    "vert_con": 0.6,
                },
                "2-3": {"module": 3.5 + 0.45, "vert_con": 0.45},
            }

        The key of the first level of the dictionary is the story number. In this case this height is defined for stories 1 to 3 (inclusive). You can also define the ground level by using the key ``ground_level`` (Default: 0.0).

        The value of the first level of the dictionary is a dictionary with the following keys:

            - ``module``: The height of the module.
            - ``vert_con``: The height of the vertical connector.

        Args:

            height (dict): The height dictionary. Defaults to None.

        Keyword Args:

            plot_kwargs (dict, optional): The plot_kwargs dictionary. Defaults to {}.

        Raises:

            ValueError: If height is not provided.

        Returns:

            None

        Examples:

            .. code-block:: python

                generate.height(
                    height=input_height,
                )

        .. note::
            This method must be called after the layout method. Otherwise, it will raise a ValueError.

        """
        self.methods_called["height"] = True
        if self.methods_called["layout"] is False:
            raise ValueError("Please call the layout method first.")

        plot_kwargs = kwargs.get("plot_kwargs", {})

        if height is None:
            raise ValueError("Please provide a height dictionary.")

        # Initialize an empty dictionary to store the module data
        self.building_height = {}

        alternative_keys = [
            "ground_level",
            "base_height",
            "start_height",
            "origin_altitude",
            "initial_altitude",
        ]

        base_height = 0.0
        for key in alternative_keys:
            if key in height:
                base_height = height[key]
                break

        for key, value in height.items():
            # Skip the ground level
            if key in alternative_keys:
                continue

            for story in helper.convert_to_range(key):
                self.building_height[story] = {
                    "module": value["module"],
                    "ver_con": value["vert_con"],
                    "clearance": value["module"] - value["vert_con"],
                    "base": base_height,
                }
                base_height += value["module"]

        self.df_height = pd.DataFrame.from_dict(self.building_height, orient="index")
        total_height = (
            self.df_height.iloc[-1]["base"] + self.df_height.iloc[-1]["module"]
        )
        self.logger.info(f"Total height of the building is {total_height:.4f} m.")

        self.df_height["story_ID"] = self.df_height.index.to_series().apply(
            lambda x: [9 + 2 * x, 10 + 2 * x, 11 + 2 * x]
        )

        for key, value in self.building_height.items():
            self.logger.debug(f"Story {key}: \n{value}\n")

        if plot_kwargs.get("show", False):
            fig, ax = self.__plot_elevation_2D(total_height, plot_kwargs)
            fig.show()

        return None

    @helper.log_time_memory
    def node(self, **kwargs) -> None:
        self.methods_called["node"] = True
        if (
            self.methods_called["height"] is False
            or self.methods_called["layout"] is False
        ):
            raise ValueError("Please call the height and layout methods first.")

        base_constraint = kwargs.get("base_constraint", [1, 1, 1, 0, 0, 1])
        if base_constraint.lower() == "fixed":
            self.logger.info(f"Base of the building is fixed in all directions.")

            base_constraint = [1, 1, 1, 1, 1, 1]

        elif base_constraint.lower() == "pinned":
            self.logger.info(f"Base of the building is pinned in all directions.")

            base_constraint = [1, 1, 1, 0, 0, 1]
        elif isinstance(base_constraint, list):
            if len(base_constraint) == 6:
                self.logger.info(
                    f"User-defined base constraint is used: {base_constraint}."
                )
            else:
                raise ValueError(
                    f"Length of {base_constraint = } is not 6. Please provide a valid base constraint."
                )
        else:
            raise ValueError(
                f"Please provide a valid base constraint. {base_constraint = } is not valid."
            )

        global_nodes = {"node": [], "fix": [], "mass": []}

        for story, height in self.df_height.iterrows():
            for story_key, values in self.nodes_floor.items():
                if story in helper.convert_to_range(story_key):
                    for row in values.itertuples(index=False):
                        if story == self.df_height.index[0]:
                            for i in [0, 1]:
                                global_nodes["node"].append(
                                    [
                                        int(
                                            f"{height['story_ID'][i]}{row.X_ID}{row.Y_ID}"
                                        ),
                                        float(f"{row.X}"),
                                        float(f"{row.Y}"),
                                        float(f"{height['base']}")
                                        if i == 0
                                        else float(
                                            f"{height['base'] + height['ver_con']}"
                                        ),
                                    ]
                                )
                            global_nodes["fix"].append(
                                [
                                    int(f"{height['story_ID'][0]}{row.X_ID}{row.Y_ID}"),
                                    *base_constraint,
                                ]
                            )
                        else:
                            global_nodes["node"].append(
                                [
                                    int(f"{height['story_ID'][1]}{row.X_ID}{row.Y_ID}"),
                                    float(f"{row.X}"),
                                    float(f"{row.Y}"),
                                    float(f"{height['base'] + height['ver_con']}"),
                                ]
                            )
            for story_key, values in self.nodes_ceiling.items():
                if story in helper.convert_to_range(story_key):
                    for row in values.itertuples(index=False):
                        global_nodes["node"].append(
                            [
                                int(f"{height['story_ID'][2]}{row.X_ID}{row.Y_ID}"),
                                float(f"{row.X}"),
                                float(f"{row.Y}"),
                                float(f"{height['base'] + height['module']}"),
                            ]
                        )

        self.df_global_nodes = pd.DataFrame(
            global_nodes["node"], columns=["node", "X", "Y", "Z"]
        )
        self.df_global_nodes["node_renum"] = self.df_global_nodes.index
        self.df_global_nodes = self.df_global_nodes.rename(
            columns={"node": "node_old", "node_renum": "node"}
        )
        self.df_global_nodes_fix = pd.DataFrame(
            global_nodes["fix"],
            columns=["node_old", "UX", "UY", "UZ", "RX", "RY", "RZ"],
        )
        self.__map_dict_node = dict(
            zip(self.df_global_nodes["node_old"], self.df_global_nodes["node"])
        )
        self.df_global_nodes_fix["node"] = self.df_global_nodes_fix["node_old"].map(
            self.__map_dict_node
        )

        self.logger.debug(f"Total number of nodes is {len(self.df_global_nodes):,}.\n")

        self.logger.debug(
            f"Total number of fixed nodes is {len(self.df_global_nodes_fix):,}.\n"
        )

        return None

    @helper.log_time_memory
    def diaphragm(self, **kwargs) -> None:
        self.methods_called["diaphragm"] = True
        if (
            self.methods_called["layout"] is False
            or self.methods_called["height"] is False
            or self.methods_called["node"] is False
        ):
            raise ValueError("Please call the layout, height, and node methods first.")

        remove_ceiling = kwargs.get("remove_ceiling", [])
        remove_floor = kwargs.get("remove_floor", [])

        if isinstance(remove_ceiling, int):
            remove_ceiling = [remove_ceiling]
        elif isinstance(remove_ceiling, list):
            pass
        else:
            raise ValueError(
                f"Please provide a valid module number or list of modules. {remove_ceiling = } is not valid."
            )

        if isinstance(remove_floor, int):
            remove_floor = [remove_floor]
        elif isinstance(remove_floor, list):
            pass
        else:
            raise ValueError(
                f"Please provide a valid module number or list of modules. {remove_floor = } is not valid."
            )

        diaphragm = []

        for story, row_height in self.df_height.iterrows():
            master_num = 0
            for module in self.df_modules.xs(story, level="story").itertuples():
                if module.brace is None:
                    if module.Index not in remove_floor:
                        master_coord = np.append(
                            module.points.mean(axis=0),
                            row_height["base"] + row_height["ver_con"],
                        )
                        diaphragm.append(
                            {
                                "story": story,
                                "module": module.Index,
                                "type": "floor",
                                "we_dir": module.we_dir,
                                "sn_dir": module.sn_dir,
                                "master": int(
                                    f"{row_height['story_ID'][1]}{master_num:03d}"
                                ),
                                "master_coord": master_coord,
                                "slaves": [
                                    int(
                                        f"{row_height['story_ID'][1]}{item[0]}{item[1]}"
                                    )
                                    for item in module.points_ID
                                ],
                            }
                        )

                    if module.Index not in remove_ceiling:
                        master_coord = np.append(
                            module.points.mean(axis=0),
                            row_height["base"] + row_height["module"],
                        )

                        diaphragm.append(
                            {
                                "story": story,
                                "module": module.Index,
                                "type": "ceiling",
                                "we_dir": module.we_dir,
                                "sn_dir": module.sn_dir,
                                "master": int(
                                    f"{row_height['story_ID'][2]}{master_num:03d}"
                                ),
                                "master_coord": master_coord,
                                "slaves": [
                                    int(
                                        f"{row_height['story_ID'][2]}{item[0]}{item[1]}"
                                    )
                                    for item in module.points_ID
                                ],
                            }
                        )

                    master_num += 1

                else:
                    if module.Index not in remove_floor:
                        points = module.points
                        points_ID = module.points_ID
                        master_coord = np.append(
                            points.mean(axis=0),
                            row_height["base"] + row_height["ver_con"],
                        )

                        diaphragm.append(
                            {
                                "story": story,
                                "module": module.Index,
                                "type": "floor",
                                "we_dir": module.we_dir,
                                "sn_dir": module.sn_dir,
                                "master": int(
                                    f"{row_height['story_ID'][1]}{master_num:03d}"
                                ),
                                "master_coord": master_coord,
                                "slaves": [
                                    int(
                                        f"{row_height['story_ID'][1]}{item[0]}{item[1]}"
                                    )
                                    for item in points_ID
                                ],
                            }
                        )

                    if module.Index not in remove_ceiling:
                        for _key, brace in module.brace_positions.items():
                            if _key[-1] == "Chevron":
                                mid_point_coord = brace["global"][1]
                                mid_point_id = brace["global_ID"][1]
                                _points = np.append(points, [mid_point_coord], axis=0)
                                _points_ID = np.append(
                                    points_ID, [mid_point_id], axis=0
                                )
                            elif _key[-1] == "X":
                                _points = points
                                _points_ID = points_ID

                        master_coord = np.append(
                            _points.mean(axis=0),
                            row_height["base"] + row_height["module"],
                        )

                        diaphragm.append(
                            {
                                "story": story,
                                "module": module.Index,
                                "type": "ceiling",
                                "we_dir": module.we_dir,
                                "sn_dir": module.sn_dir,
                                "master": int(
                                    f"{row_height['story_ID'][2]}{master_num:03d}"
                                ),
                                "master_coord": master_coord,
                                "slaves": [
                                    int(
                                        f"{row_height['story_ID'][2]}{item[0]}{item[1]}"
                                    )
                                    for item in _points_ID
                                ],
                            }
                        )
                    master_num += 1

        self.df_diaphragms = pd.DataFrame(
            diaphragm,
            columns=[
                "story",
                "module",
                "type",
                "we_dir",
                "sn_dir",
                "master",
                "slaves",
                "master_coord",
            ],
        )

        self.df_diaphragms = self.df_diaphragms.rename(
            columns={"master": "master_old", "slaves": "slaves_old"}
        )

        self.df_diaphragms["master"] = range(
            self.df_global_nodes.node.iloc[-1] + 1,
            self.df_global_nodes.node.iloc[-1] + 1 + len(self.df_diaphragms),
        )

        self.df_diaphragms["slaves"] = self.df_diaphragms["slaves_old"].apply(
            lambda x: helper.map_list(self.__map_dict_node, x)
        )
        self.df_diaphragms = self.df_diaphragms.set_index(["story", "module"])

        return None

    @helper.log_time_memory
    def geo_transf(self, **kwargs) -> None:
        self.methods_called["geo_transf"] = True

        beam_option = kwargs.get("beam_option", "PDelta")
        brace_option = kwargs.get("brace_option", "Corotational")
        column_option = kwargs.get("column_option", "PDelta")

        if beam_option not in ["Linear", "PDelta", "Corotational"]:
            raise ValueError(
                f"Please provide a valid beam option. {beam_option} is not valid. Valid options are 'Linear', 'PDelta', and 'Corotational'."
            )

        if brace_option not in ["Linear", "PDelta", "Corotational"]:
            raise ValueError(
                f"Please provide a valid brace option. {brace_option} is not valid. Valid options are 'Linear', 'PDelta', and 'Corotational'."
            )

        if column_option not in ["Linear", "PDelta", "Corotational"]:
            raise ValueError(
                f"Please provide a valid column option. {column_option} is not valid. Valid options are 'Linear', 'PDelta', and 'Corotational'."
            )

        self._command_geo_transf = {
            "tag": [
                {
                    "name": "column_we",
                    "value": 1,
                    "description": "columns in west-east direction",
                },
                {
                    "name": "beam_we",
                    "value": 2,
                    "description": "beams in west-east direction",
                },
                {
                    "name": "brace_we",
                    "value": 3,
                    "description": "braces in west-east direction",
                },
                {
                    "name": "column_sn",
                    "value": 4,
                    "description": "columns in south-north direction",
                },
                {
                    "name": "beam_sn",
                    "value": 5,
                    "description": "beams in south-north direction",
                },
                {
                    "name": "brace_sn",
                    "value": 6,
                    "description": "braces in south-north direction",
                },
            ],
            "func": [
                {
                    "type": "geomTransf",
                    "option": column_option,
                    "tag": "column_we",
                    "args": [0.0, 1.0, 0.0],
                },
                {
                    "type": "geomTransf",
                    "option": beam_option,
                    "tag": "beam_we",
                    "args": [0.0, 1.0, 0.0],
                },
                {
                    "type": "geomTransf",
                    "option": brace_option,
                    "tag": "brace_we",
                    "args": [0.0, 1.0, 0.0],
                },
                {
                    "type": "geomTransf",
                    "option": column_option,
                    "tag": "column_sn",
                    "args": [1.0, 0.0, 0.0],
                },
                {
                    "type": "geomTransf",
                    "option": beam_option,
                    "tag": "beam_sn",
                    "args": [1.0, 0.0, 0.0],
                },
                {
                    "type": "geomTransf",
                    "option": brace_option,
                    "tag": "brace_sn",
                    "args": [1.0, 0.0, 0.0],
                },
            ],
        }

        self.df_geo_transf = (
            pd.DataFrame(self._command_geo_transf["tag"])
            .set_index("name")
            .astype({"value": int})
        )

        self.logger.info("Geometric transformations have been created.")
        self.logger.debug(f"{column_option} transformation was used for columns.")
        self.logger.debug(f"{beam_option} transformation was used for beams.")
        self.logger.debug(f"{brace_option} transformation was used for braces.")

        return None

    @helper.log_time_memory
    def section_material(self, **kwargs) -> None:
        self.methods_called["section_material"] = True

        self._command_section_material = {
            "tag": [
                {
                    "name": "pinned",
                    "value": 1,
                    "description": "UniaxialMaterial for pinned elements",
                },
                {
                    "name": "rigid",
                    "value": 2,
                    "description": "UniaxialMaterial for rigid elements",
                },
                {
                    "name": "torsion",
                    "value": 3,
                    "description": "UniaxialMaterial for torsional elements",
                },
                {
                    "name": "brace_steel",
                    "value": 4,
                    "description": "UniaxialMaterial for steel brace elements",
                },
                {
                    "name": "ver_con_steel",
                    "value": 5,
                    "description": "UniaxialMaterial for steel vertical connection elements",
                },
            ],
            "func": [
                {
                    "type": "uniaxialMaterial",
                    "option": "Elastic",
                    "tag": "pinned",
                    "args": [1e-9],
                },
                {
                    "type": "uniaxialMaterial",
                    "option": "Elastic",
                    "tag": "rigid",
                    "args": [1e20],
                },
                {
                    "type": "uniaxialMaterial",
                    "option": "Elastic",
                    "tag": "torsion",
                    "args": [1.0],
                },
                {
                    "type": "uniaxialMaterial",
                    "option": "Steel02",
                    "tag": "brace_steel",
                    "args": [
                        self.material.steel_brace["Fy"],
                        self.material.steel_brace["YoungModulus"],
                        self.material.steel_brace["b"],
                        *[
                            self.material.steel_brace["R0"],
                            self.material.steel_brace["cR1"],
                            self.material.steel_brace["cR2"],
                        ],
                        self.material.steel_brace["a1"],
                        self.material.steel_brace["a2"],
                        self.material.steel_brace["a3"],
                        self.material.steel_brace["a4"],
                    ],
                },
                {
                    "type": "uniaxialMaterial",
                    "option": "Steel02",
                    "tag": "ver_con_steel",
                    "args": [
                        self.material.steel_column["Fy"],
                        self.material.steel_column["YoungModulus"],
                        self.material.steel_column["b"],
                        *[
                            self.material.steel_column["R0"],
                            self.material.steel_column["cR1"],
                            self.material.steel_column["cR2"],
                        ],
                        self.material.steel_column["a1"],
                        self.material.steel_column["a2"],
                        self.material.steel_column["a3"],
                        self.material.steel_column["a4"],
                    ],
                },
            ],
        }
        self.df_section_material = (
            pd.DataFrame(self._command_section_material["tag"])
            .set_index("name")
            .astype({"value": int})
        )

        self.logger.info("Sections and materials have been created.")

        return None

    @helper.log_time_memory
    def element(self, **kwargs) -> None:
        self.methods_called["element"] = True
        if (
            self.methods_called["layout"] is False
            or self.methods_called["height"] is False
            or self.methods_called["node"] is False
        ):
            raise ValueError("Please call the layout, height, and node methods first.")
        self.sections = kwargs.get("section", None)
        if self.sections is None:
            raise ValueError("Please provide a dictionary of sections.")

        element_list = [
            "column",
            "brace",
            "floor_beam",
            "ceiling_beam",
        ]

        for ele in element_list:
            if ele not in self.sections.keys():
                raise ValueError(
                    f"Please provide a section for {ele}. {ele} is not found in the section dictionary."
                )

        self.__parse_column_section()
        self.__parse_brace_section()
        self.__parse_beam_section()

        element_dict = {
            "floor_beam": [],
            "ceiling_beam": [],
            "column": [],
            "brace": [],
            "horizontal_connection": [],
        }

        for story, row_height in self.df_height.iterrows():
            for _mod_id, row_module in self.df_modules.xs(
                story, level="story"
            ).iterrows():
                points = row_module["points"]
                corner_sw, corner_se, corner_ne, corner_nw = row_module["corners"]
                corner_sw_ID, corner_se_ID, corner_ne_ID, corner_nw_ID = row_module[
                    "corners_ID"
                ]

                # braced modules
                if row_module.brace:
                    _story_id = row_height["story_ID"]
                    _row_brace_section = self.df_brace_sections.loc[story]
                    _row_col_section = self.df_column_sections.loc[(story, _mod_id)]
                    _row_floor_braced_section = self.df_floor_braced_sections.loc[story]
                    _row_floor_regular_section = self.df_floor_regular_sections.loc[
                        story
                    ]
                    _row_ceiling_braced_section = self.df_ceiling_braced_sections.loc[
                        story
                    ]
                    _row_ceiling_regular_section = self.df_ceiling_regular_sections.loc[
                        story
                    ]
                    _col_points, _floor_points, _ceiling_points = [], [], []
                    _col_section = _row_col_section.section
                    _col_multi = pd.DataFrame(_row_col_section.multi)

                    for _row_brace_pos in self.df_brace_positions.loc[
                        [(story, _mod_id)]
                    ].itertuples(index=False):
                        side, type_brace = (
                            _row_brace_pos.side,
                            _row_brace_pos.type_brace,
                        )
                        global_id = _row_brace_pos.global_ID
                        global_coords = _row_brace_pos.global_coords
                        _len_brace, _len_floor_beam, _len_ceiling_beam = 0, 0, 0

                        if side in ["west", "east"]:
                            _len_brace = np.sqrt(
                                (global_coords[0][1] - global_coords[1][1]) ** 2
                                + (row_height["clearance"]) ** 2
                            )
                            _len_floor_beam = global_coords[-1][1] - global_coords[0][1]
                            if type_brace in ["Chevron", "X"]:
                                _len_ceiling_beam = (
                                    global_coords[-1][1] - global_coords[0][1]
                                )

                        elif side in ["south", "north"]:
                            _len_brace = np.sqrt(
                                (global_coords[0][0] - global_coords[1][0]) ** 2
                                + (row_height["clearance"]) ** 2
                            )
                            _len_floor_beam = global_coords[-1][0] - global_coords[0][0]
                            if type_brace in ["Chevron", "X"]:
                                _len_ceiling_beam = (
                                    global_coords[-1][0] - global_coords[0][0]
                                )
                        else:
                            raise ValueError(f"{side} is not valid.")

                        for __length, __section, __dir in zip(
                            _row_floor_braced_section["length"],
                            _row_floor_braced_section["section"],
                            _row_floor_braced_section["direction"],
                        ):
                            if not isinstance(__length, list) and __dir == "all":
                                _floor_section = __section
                                break
                            elif (
                                not isinstance(__length, list)
                                and __dir == "south-north"
                                and side in ["east", "west"]
                            ):
                                _floor_section = __section
                                break
                            elif (
                                not isinstance(__length, list)
                                and __dir == "west-east"
                                and side in ["south", "north"]
                            ):
                                _floor_section = __section
                                break
                            elif (
                                isinstance(__length, list)
                                and __length[0] <= _len_floor_beam <= __length[1]
                                and __dir == "all"
                            ):
                                _floor_section = __section
                                break
                            elif (
                                isinstance(__length, list)
                                and __length[0] <= _len_floor_beam <= __length[1]
                                and __dir == "south-north"
                                and side in ["east", "west"]
                            ):
                                _floor_section = __section
                                break
                            elif (
                                isinstance(__length, list)
                                and __length[0] <= _len_floor_beam <= __length[1]
                                and __dir == "west-east"
                                and side in ["south", "north"]
                            ):
                                _floor_section = __section
                                break

                        for __length, __section, __dir in zip(
                            _row_ceiling_braced_section["length"],
                            _row_ceiling_braced_section["section"],
                            _row_ceiling_braced_section["direction"],
                        ):
                            if not isinstance(__length, list) and __dir == "all":
                                _ceiling_section = __section
                                break
                            elif (
                                not isinstance(__length, list)
                                and __dir == "south-north"
                                and side in ["east", "west"]
                            ):
                                _ceiling_section = __section
                                break
                            elif (
                                not isinstance(__length, list)
                                and __dir == "west-east"
                                and side in ["south", "north"]
                            ):
                                _ceiling_section = __section
                                break
                            elif (
                                isinstance(__length, list)
                                and __length[0] <= _len_ceiling_beam <= __length[1]
                                and __dir == "all"
                            ):
                                _ceiling_section = __section
                                break
                            elif (
                                isinstance(__length, list)
                                and __length[0] <= _len_ceiling_beam <= __length[1]
                                and __dir == "south-north"
                                and side in ["east", "west"]
                            ):
                                _ceiling_section = __section
                                break
                            elif (
                                isinstance(__length, list)
                                and __length[0] <= _len_ceiling_beam <= __length[1]
                                and __dir == "west-east"
                                and side in ["south", "north"]
                            ):
                                _ceiling_section = __section
                                break

                        __i_node_floor = (
                            f"{_story_id[1]}{global_id[0][0]}{global_id[0][1]}"
                        )
                        __j_node_floor = (
                            f"{_story_id[1]}{global_id[-1][0]}{global_id[-1][1]}"
                        )
                        _floor_points.append([global_id[0], global_id[-1]])

                        if type_brace == "Chevron":
                            __i_node_ceiling = (
                                f"{_story_id[2]}{global_id[0][0]}{global_id[0][1]}"
                            )
                            __mid_node_ceiling = (
                                f"{_story_id[2]}{global_id[1][0]}{global_id[1][1]}"
                            )
                            __j_node_ceiling = (
                                f"{_story_id[2]}{global_id[2][0]}{global_id[2][1]}"
                            )
                            _ceiling_points.append(
                                [
                                    [global_id[0], global_id[1]],
                                    [global_id[1], global_id[2]],
                                ],
                            )

                        elif type_brace == "X":
                            __i_node_ceiling = (
                                f"{_story_id[2]}{global_id[0][0]}{global_id[0][1]}"
                            )
                            __mid_node_ceiling = np.nan
                            __j_node_ceiling = (
                                f"{_story_id[2]}{global_id[-1][0]}{global_id[-1][1]}"
                            )
                            _ceiling_points.append([global_id[0], global_id[-1]])
                        else:
                            raise ValueError(
                                f"Please provide a valid brace type. {type_brace} is not valid."
                            )

                        element_dict["floor_beam"].append(
                            {
                                "story": story,
                                "module": _mod_id,
                                "braced": True,
                                "brace_type": type_brace,
                                "side": side,
                                "length": _len_floor_beam,
                                "direction": "south-north"
                                if side in ["east", "west"]
                                else "west-east",
                                "i_node": __i_node_floor,
                                "j_node": __j_node_floor,
                                "ele_number": np.nan,
                                "section": _floor_section,
                                "section_props": self.__get_section_props(
                                    _floor_section
                                ),
                            }
                        )
                        element_dict["ceiling_beam"].append(
                            {
                                "story": story,
                                "module": _mod_id,
                                "braced": True,
                                "brace_type": type_brace,
                                "side": side,
                                "length": _len_ceiling_beam,
                                "direction": "south-north"
                                if side in ["east", "west"]
                                else "west-east",
                                "i_node": __i_node_ceiling,
                                "mid_node": __mid_node_ceiling,
                                "j_node": __j_node_ceiling,
                                "ele_number": np.nan,
                                "section": _ceiling_section,
                                "section_props": self.__get_section_props(
                                    _ceiling_section
                                ),
                            }
                        )

                        for section, direction in zip(
                            _row_brace_section["section"],
                            _row_brace_section["location"],
                        ):
                            if (
                                side in ["west", "east"]
                                and type_brace == "Chevron"
                                and direction in ["south-north", "all"]
                            ):
                                element_dict["brace"].append(
                                    {
                                        "story": story,
                                        "module": _mod_id,
                                        "side": side,
                                        "length": _len_brace,
                                        "type": type_brace,
                                        "position": "up",
                                        "section": section,
                                        "section_props": self.__get_section_props(
                                            section
                                        ),
                                        "direction": "south-north",
                                        "i_node": f"{_story_id[1]}{global_id[0][0]}{global_id[0][1]}",
                                        "j_node": f"{_story_id[2]}{global_id[1][0]}{global_id[1][1]}",
                                        "ele_number": np.nan,
                                        "floor_section": _floor_section,
                                        "floor_section_props": self.__get_section_props(
                                            _floor_section
                                        ),
                                        "ceiling_section": _ceiling_section,
                                        "ceiling_section_props": self.__get_section_props(
                                            _ceiling_section
                                        ),
                                    }
                                )

                                element_dict["brace"].append(
                                    {
                                        "story": story,
                                        "module": _mod_id,
                                        "side": side,
                                        "length": _len_brace,
                                        "type": type_brace,
                                        "position": "down",
                                        "section": section,
                                        "section_props": self.__get_section_props(
                                            section
                                        ),
                                        "direction": "south-north",
                                        "i_node": f"{_story_id[2]}{global_id[1][0]}{global_id[1][1]}",
                                        "j_node": f"{_story_id[1]}{global_id[2][0]}{global_id[2][1]}",
                                        "ele_number": np.nan,
                                        "floor_section": _floor_section,
                                        "floor_section_props": self.__get_section_props(
                                            _floor_section
                                        ),
                                        "ceiling_section": _ceiling_section,
                                        "ceiling_section_props": self.__get_section_props(
                                            _ceiling_section
                                        ),
                                    }
                                )

                            elif (
                                side in ["west", "east"]
                                and type_brace == "X"
                                and direction in ["south-north", "all"]
                            ):
                                element_dict["brace"].append(
                                    {
                                        "story": story,
                                        "module": _mod_id,
                                        "side": side,
                                        "length": _len_brace,
                                        "type": type_brace,
                                        "position": "up",
                                        "section": section,
                                        "section_props": self.__get_section_props(
                                            section
                                        ),
                                        "direction": "south-north",
                                        "i_node": f"{_story_id[1]}{global_id[0][0]}{global_id[0][1]}",
                                        "j_node": f"{_story_id[2]}{global_id[1][0]}{global_id[1][1]}",
                                        "ele_number": np.nan,
                                        "floor_section": _floor_section,
                                        "floor_section_props": self.__get_section_props(
                                            _floor_section
                                        ),
                                        "ceiling_section": _ceiling_section,
                                        "ceiling_section_props": self.__get_section_props(
                                            _ceiling_section
                                        ),
                                    }
                                )

                                element_dict["brace"].append(
                                    {
                                        "story": story,
                                        "module": _mod_id,
                                        "side": side,
                                        "length": _len_brace,
                                        "type": type_brace,
                                        "position": "down",
                                        "section": section,
                                        "section_props": self.__get_section_props(
                                            section
                                        ),
                                        "direction": "south-north",
                                        "i_node": f"{_story_id[2]}{global_id[0][0]}{global_id[0][1]}",
                                        "j_node": f"{_story_id[1]}{global_id[1][0]}{global_id[1][1]}",
                                        "ele_number": np.nan,
                                        "floor_section": _floor_section,
                                        "floor_section_props": self.__get_section_props(
                                            _floor_section
                                        ),
                                        "ceiling_section": _ceiling_section,
                                        "ceiling_section_props": self.__get_section_props(
                                            _ceiling_section
                                        ),
                                    }
                                )
                            elif (
                                side in ["south", "north"]
                                and type_brace == "Chevron"
                                and direction in ["west-east", "all"]
                            ):
                                element_dict["brace"].append(
                                    {
                                        "story": story,
                                        "module": _mod_id,
                                        "side": side,
                                        "length": _len_brace,
                                        "type": type_brace,
                                        "position": "up",
                                        "section": section,
                                        "section_props": self.__get_section_props(
                                            section
                                        ),
                                        "direction": "west-east",
                                        "i_node": f"{_story_id[1]}{global_id[0][0]}{global_id[0][1]}",
                                        "j_node": f"{_story_id[2]}{global_id[1][0]}{global_id[1][1]}",
                                        "ele_number": np.nan,
                                        "floor_section": _floor_section,
                                        "floor_section_props": self.__get_section_props(
                                            _floor_section
                                        ),
                                        "ceiling_section": _ceiling_section,
                                        "ceiling_section_props": self.__get_section_props(
                                            _ceiling_section
                                        ),
                                    }
                                )

                                element_dict["brace"].append(
                                    {
                                        "story": story,
                                        "module": _mod_id,
                                        "side": side,
                                        "length": _len_brace,
                                        "type": type_brace,
                                        "position": "down",
                                        "section": section,
                                        "section_props": self.__get_section_props(
                                            section
                                        ),
                                        "direction": "west-east",
                                        "i_node": f"{_story_id[2]}{global_id[1][0]}{global_id[1][1]}",
                                        "j_node": f"{_story_id[1]}{global_id[2][0]}{global_id[2][1]}",
                                        "ele_number": np.nan,
                                        "floor_section": _floor_section,
                                        "floor_section_props": self.__get_section_props(
                                            _floor_section
                                        ),
                                        "ceiling_section": _ceiling_section,
                                        "ceiling_section_props": self.__get_section_props(
                                            _ceiling_section
                                        ),
                                    }
                                )

                            elif (
                                side in ["south", "north"]
                                and type_brace == "X"
                                and direction in ["west-east", "all"]
                            ):
                                element_dict["brace"].append(
                                    {
                                        "story": story,
                                        "module": _mod_id,
                                        "side": side,
                                        "length": _len_brace,
                                        "type": type_brace,
                                        "position": "up",
                                        "section": section,
                                        "section_props": self.__get_section_props(
                                            section
                                        ),
                                        "direction": "west-east",
                                        "i_node": f"{_story_id[1]}{global_id[0][0]}{global_id[0][1]}",
                                        "j_node": f"{_story_id[2]}{global_id[1][0]}{global_id[1][1]}",
                                        "ele_number": np.nan,
                                        "floor_section": _floor_section,
                                        "floor_section_props": self.__get_section_props(
                                            _floor_section
                                        ),
                                        "ceiling_section": _ceiling_section,
                                        "ceiling_section_props": self.__get_section_props(
                                            _ceiling_section
                                        ),
                                    }
                                )

                                element_dict["brace"].append(
                                    {
                                        "story": story,
                                        "module": _mod_id,
                                        "side": side,
                                        "length": _len_brace,
                                        "type": type_brace,
                                        "position": "down",
                                        "section": section,
                                        "section_props": self.__get_section_props(
                                            section
                                        ),
                                        "direction": "west-east",
                                        "i_node": f"{_story_id[2]}{global_id[0][0]}{global_id[0][1]}",
                                        "j_node": f"{_story_id[1]}{global_id[1][0]}{global_id[1][1]}",
                                        "ele_number": np.nan,
                                        "floor_section": _floor_section,
                                        "floor_section_props": self.__get_section_props(
                                            _floor_section
                                        ),
                                        "ceiling_section": _ceiling_section,
                                        "ceiling_section_props": self.__get_section_props(
                                            _ceiling_section
                                        ),
                                    }
                                )

                        if not _col_multi.empty:
                            if "brace" in _col_multi.columns:
                                for __row in _col_multi.itertuples():
                                    __side_col, __pos_col = __row.Index.split("-")
                                    __num_col = __row.brace
                                    if __side_col == side:
                                        if __pos_col == "start":
                                            _col_points.append(global_id[0])
                                            element_dict["column"].append(
                                                {
                                                    "story": story,
                                                    "module": _mod_id,
                                                    "braced": True,
                                                    "brace_side": side,
                                                    "multi": __num_col,
                                                    "section": _col_section,
                                                    "point": "sw"
                                                    if np.array_equal(
                                                        global_id[0], corner_sw_ID
                                                    )
                                                    else "se"
                                                    if np.array_equal(
                                                        global_id[0], corner_se_ID
                                                    )
                                                    else "ne"
                                                    if np.array_equal(
                                                        global_id[0], corner_ne_ID
                                                    )
                                                    else "nw"
                                                    if np.array_equal(
                                                        global_id[0], corner_nw_ID
                                                    )
                                                    else f"middle-{side}",
                                                    "length": row_height["clearance"],
                                                    "len_ver_con": row_height[
                                                        "ver_con"
                                                    ],
                                                    "i_node": f"{_story_id[1]}{global_id[0][0]}{global_id[0][1]}",
                                                    "j_node": f"{_story_id[2]}{global_id[0][0]}{global_id[0][1]}",
                                                    "ele_number": np.nan,
                                                    "section_props": self.__get_section_props(
                                                        _col_section
                                                    ),
                                                    "brace_section": section,
                                                    "brace_section_props": self.__get_section_props(
                                                        section
                                                    ),
                                                }
                                            )
                                        elif __pos_col == "end":
                                            _col_points.append(global_id[-1])
                                            element_dict["column"].append(
                                                {
                                                    "story": story,
                                                    "module": _mod_id,
                                                    "braced": True,
                                                    "brace_side": side,
                                                    "multi": __num_col,
                                                    "section": _col_section,
                                                    "point": "sw"
                                                    if np.array_equal(
                                                        global_id[-1], corner_sw_ID
                                                    )
                                                    else "se"
                                                    if np.array_equal(
                                                        global_id[-1], corner_se_ID
                                                    )
                                                    else "ne"
                                                    if np.array_equal(
                                                        global_id[-1], corner_ne_ID
                                                    )
                                                    else "nw"
                                                    if np.array_equal(
                                                        global_id[-1], corner_nw_ID
                                                    )
                                                    else f"middle-{side}",
                                                    "length": row_height["clearance"],
                                                    "len_ver_con": row_height[
                                                        "ver_con"
                                                    ],
                                                    "i_node": f"{_story_id[1]}{global_id[-1][0]}{global_id[-1][1]}",
                                                    "j_node": f"{_story_id[2]}{global_id[-1][0]}{global_id[-1][1]}",
                                                    "ele_number": np.nan,
                                                    "section_props": self.__get_section_props(
                                                        _col_section
                                                    ),
                                                    "brace_section": section,
                                                    "brace_section_props": self.__get_section_props(
                                                        section
                                                    ),
                                                }
                                            )
                                        else:
                                            raise NotImplementedError(
                                                f"Please provide a valid position. {__pos_col} is not valid."
                                            )
                        elif _col_multi.empty:
                            for point_id in row_module["points_ID"]:
                                if np.array_equal(point_id, global_id[0]):
                                    _col_points.append(point_id)
                                    element_dict["column"].append(
                                        {
                                            "story": story,
                                            "module": _mod_id,
                                            "braced": True,
                                            "brace_side": side,
                                            "multi": None,
                                            "section": _col_section,
                                            "point": "sw"
                                            if np.array_equal(point_id, corner_sw_ID)
                                            else "se"
                                            if np.array_equal(point_id, corner_se_ID)
                                            else "ne"
                                            if np.array_equal(point_id, corner_ne_ID)
                                            else "nw"
                                            if np.array_equal(point_id, corner_nw_ID)
                                            else f"middle-{side}",
                                            "length": row_height["clearance"],
                                            "len_ver_con": row_height["ver_con"],
                                            "i_node": f"{_story_id[1]}{point_id[0]}{point_id[1]}",
                                            "j_node": f"{_story_id[2]}{point_id[0]}{point_id[1]}",
                                            "ele_number": np.nan,
                                            "section_props": self.__get_section_props(
                                                _col_section
                                            ),
                                            "brace_section": section,
                                            "brace_section_props": self.__get_section_props(
                                                section
                                            ),
                                        }
                                    )
                                elif np.array_equal(point_id, global_id[-1]):
                                    _col_points.append(point_id)
                                    element_dict["column"].append(
                                        {
                                            "story": story,
                                            "module": _mod_id,
                                            "braced": True,
                                            "brace_side": side,
                                            "multi": None,
                                            "section": _col_section,
                                            "point": "sw"
                                            if np.array_equal(point_id, corner_sw_ID)
                                            else "se"
                                            if np.array_equal(point_id, corner_se_ID)
                                            else "ne"
                                            if np.array_equal(point_id, corner_ne_ID)
                                            else "nw"
                                            if np.array_equal(point_id, corner_nw_ID)
                                            else f"middle-{side}",
                                            "length": row_height["clearance"],
                                            "len_ver_con": row_height["ver_con"],
                                            "i_node": f"{_story_id[1]}{point_id[0]}{point_id[1]}",
                                            "j_node": f"{_story_id[2]}{point_id[0]}{point_id[1]}",
                                            "ele_number": np.nan,
                                            "section_props": self.__get_section_props(
                                                _col_section
                                            ),
                                            "brace_section": section,
                                            "brace_section_props": self.__get_section_props(
                                                section
                                            ),
                                        }
                                    )
                                else:
                                    pass

                        else:
                            raise ValueError(
                                "Dataframe is neither empty nor have some values."
                            )

                    for point_id in row_module["points_ID"]:
                        if point_id not in _col_points:
                            element_dict["column"].append(
                                {
                                    "story": story,
                                    "module": _mod_id,
                                    "braced": False,
                                    "brace_side": None,
                                    "multi": None,
                                    "section": _col_section,
                                    "point": "sw"
                                    if np.array_equal(point_id, corner_sw_ID)
                                    else "se"
                                    if np.array_equal(point_id, corner_se_ID)
                                    else "ne"
                                    if np.array_equal(point_id, corner_ne_ID)
                                    else "nw"
                                    if np.array_equal(point_id, corner_nw_ID)
                                    else "middle",
                                    "length": row_height["clearance"],
                                    "len_ver_con": row_height["ver_con"],
                                    "i_node": f"{_story_id[1]}{point_id[0]}{point_id[1]}",
                                    "j_node": f"{_story_id[2]}{point_id[0]}{point_id[1]}",
                                    "ele_number": np.nan,
                                    "section_props": self.__get_section_props(
                                        _col_section
                                    ),
                                    "brace_section": None,
                                    "brace_section_props": None,
                                }
                            )

                    for i in range(len(row_module["points"])):
                        if i == len(row_module["points"]) - 1:
                            __point1, __point2 = (
                                row_module["points"][i],
                                row_module["points"][0],
                            )
                            __point1_id, __point2_id = (
                                row_module["points_ID"][i],
                                row_module["points_ID"][0],
                            )
                        else:
                            __point1, __point2 = (
                                row_module["points"][i],
                                row_module["points"][i + 1],
                            )
                            __point1_id, __point2_id = (
                                row_module["points_ID"][i],
                                row_module["points_ID"][i + 1],
                            )

                        corners = [
                            (corner_sw, corner_se, "south", "west-east"),
                            (corner_se, corner_ne, "east", "south-north"),
                            (corner_ne, corner_nw, "north", "west-east"),
                            (corner_nw, corner_sw, "west", "south-north"),
                        ]

                        __side, __dir = None, None

                        for corner1, corner2, side, direction in corners:
                            p3, p4 = helper.check_points_on_line(
                                tuple(corner1),
                                tuple(corner2),
                                tuple(__point1),
                                tuple(__point2),
                            )
                            if p3 and p4:
                                __side, __dir = side, direction
                                if side in ["north", "west"]:
                                    __point1, __point2 = __point2, __point1
                                    __point1_id, __point2_id = __point2_id, __point1_id

                                if direction in ["west-east", "east-west"]:
                                    _len_floor_beam = __point2[0] - __point1[0]
                                    _len_ceiling_beam = __point2[0] - __point1[0]
                                elif direction in ["south-north", "north-south"]:
                                    _len_floor_beam = __point2[1] - __point1[1]
                                    _len_ceiling_beam = __point2[1] - __point1[1]
                                break

                        for __length, __section, __dir in zip(
                            _row_floor_regular_section["length"],
                            _row_floor_regular_section["section"],
                            _row_floor_regular_section["direction"],
                        ):
                            if not isinstance(__length, list) and __dir == "all":
                                _floor_section = __section
                                break
                            elif (
                                not isinstance(__length, list)
                                and __dir == "south-north"
                                and side in ["east", "west"]
                            ):
                                _floor_section = __section
                                break
                            elif (
                                not isinstance(__length, list)
                                and __dir == "west-east"
                                and side in ["south", "north"]
                            ):
                                _floor_section = __section
                                break
                            elif (
                                isinstance(__length, list)
                                and __length[0] <= _len_floor_beam <= __length[1]
                                and __dir == "all"
                            ):
                                _floor_section = __section
                                break
                            elif (
                                isinstance(__length, list)
                                and __length[0] <= _len_floor_beam <= __length[1]
                                and __dir == "south-north"
                                and side in ["east", "west"]
                            ):
                                _floor_section = __section
                                break
                            elif (
                                isinstance(__length, list)
                                and __length[0] <= _len_floor_beam <= __length[1]
                                and __dir == "west-east"
                                and side in ["south", "north"]
                            ):
                                _floor_section = __section
                                break

                        for __length, __section, __dir in zip(
                            _row_ceiling_regular_section["length"],
                            _row_ceiling_regular_section["section"],
                            _row_ceiling_regular_section["direction"],
                        ):
                            if not isinstance(__length, list) and __dir == "all":
                                _ceiling_section = __section
                                break
                            elif (
                                not isinstance(__length, list)
                                and __dir == "south-north"
                                and side in ["east", "west"]
                            ):
                                _ceiling_section = __section
                                break
                            elif (
                                not isinstance(__length, list)
                                and __dir == "west-east"
                                and side in ["south", "north"]
                            ):
                                _ceiling_section = __section
                                break
                            elif (
                                isinstance(__length, list)
                                and __length[0] <= _len_ceiling_beam <= __length[1]
                                and __dir == "all"
                            ):
                                _ceiling_section = __section
                                break
                            elif (
                                isinstance(__length, list)
                                and __length[0] <= _len_ceiling_beam <= __length[1]
                                and __dir == "south-north"
                                and side in ["east", "west"]
                            ):
                                _ceiling_section = __section
                                break
                            elif (
                                isinstance(__length, list)
                                and __length[0] <= _len_ceiling_beam <= __length[1]
                                and __dir == "west-east"
                                and side in ["south", "north"]
                            ):
                                _ceiling_section = __section
                                break

                        if not any(
                            [__point1_id, __point2_id] == sublist
                            for sublist in _floor_points
                        ):
                            element_dict["floor_beam"].append(
                                {
                                    "story": story,
                                    "module": _mod_id,
                                    "braced": False,
                                    "brace_type": np.nan,
                                    "side": __side,
                                    "length": _len_floor_beam,
                                    "direction": __dir,
                                    "i_node": f"{_story_id[1]}{__point1_id[0]}{__point1_id[1]}",
                                    "j_node": f"{_story_id[1]}{__point2_id[0]}{__point2_id[1]}",
                                    "ele_number": np.nan,
                                    "section": _floor_section,
                                    "section_props": self.__get_section_props(
                                        _floor_section
                                    ),
                                }
                            )
                        _defined = []
                        for item in _ceiling_points:
                            if isinstance(item[0], list):
                                if np.array_equal(
                                    item[0][0], __point1_id
                                ) and np.array_equal(item[-1][-1], __point2_id):
                                    _defined.append([__point1_id, __point2_id])
                            else:
                                if np.array_equal(
                                    item[0], __point1_id
                                ) and np.array_equal(item[1], __point2_id):
                                    _defined.append([__point1_id, __point2_id])

                        if not _defined:
                            element_dict["ceiling_beam"].append(
                                {
                                    "story": story,
                                    "module": _mod_id,
                                    "braced": False,
                                    "brace_type": np.nan,
                                    "side": __side,
                                    "length": _len_ceiling_beam,
                                    "direction": __dir,
                                    "i_node": f"{_story_id[2]}{__point1_id[0]}{__point1_id[1]}",
                                    "j_node": f"{_story_id[2]}{__point2_id[0]}{__point2_id[1]}",
                                    "ele_number": np.nan,
                                    "section": _ceiling_section,
                                    "section_props": self.__get_section_props(
                                        _ceiling_section
                                    ),
                                }
                            )

                # regular modules (not braced)
                elif row_module.brace is None:
                    # process columns first
                    _story_id = row_height["story_ID"]
                    _row = self.df_column_sections.loc[(story, _mod_id)]
                    _col_section = _row["section"]
                    _multi = _row["multi"]
                    for point_id in row_module["points_ID"]:
                        element_dict["column"].append(
                            {
                                "story": story,
                                "module": _mod_id,
                                "braced": False,
                                "multi": _multi,
                                "section": _col_section,
                                "point": "sw"
                                if np.array_equal(point_id, corner_sw_ID)
                                else "se"
                                if np.array_equal(point_id, corner_se_ID)
                                else "ne"
                                if np.array_equal(point_id, corner_ne_ID)
                                else "nw",
                                "length": row_height["clearance"],
                                "len_ver_con": row_height["ver_con"],
                                "i_node": f"{_story_id[1]}{point_id[0]}{point_id[1]}",
                                "j_node": f"{_story_id[2]}{point_id[0]}{point_id[1]}",
                                "ele_number": np.nan,
                                "section_props": self.__get_section_props(_col_section),
                                "brace_section": None,
                                "brace_section_props": None,
                            }
                        )

                    # Process floor beams second
                    len_beam_sw_se = corner_se[0] - corner_sw[0]
                    len_beam_nw_ne = corner_ne[0] - corner_nw[0]
                    len_beam_se_ne = corner_ne[1] - corner_se[1]
                    len_beam_sw_nw = corner_nw[1] - corner_sw[1]

                    beam_types = ["floor_beam", "ceiling_beam"]
                    for beam_type in beam_types:
                        if beam_type == "floor_beam":
                            _row = self.df_floor_regular_sections.loc[story]
                            _story_id = row_height["story_ID"][1]
                        elif beam_type == "ceiling_beam":
                            _row = self.df_ceiling_regular_sections.loc[story]
                            _story_id = row_height["story_ID"][2]

                        for length, section in zip(
                            _row["length"],
                            _row["section"],
                        ):
                            if length[0] <= len_beam_sw_se <= length[1]:
                                section = section
                                element_dict[beam_type].append(
                                    {
                                        "story": story,
                                        "module": _mod_id,
                                        "braced": False,
                                        "side": "south",
                                        "length": len_beam_sw_se,
                                        "direction": "west-east",
                                        "i_node": f"{_story_id}{corner_sw_ID[0]}{corner_sw_ID[1]}",
                                        "j_node": f"{_story_id}{corner_se_ID[0]}{corner_se_ID[1]}",
                                        "ele_number": np.nan,
                                        "section": section,
                                        "section_props": self.__get_section_props(
                                            section
                                        ),
                                    }
                                )

                            if length[0] <= len_beam_nw_ne <= length[1]:
                                element_dict[beam_type].append(
                                    {
                                        "story": story,
                                        "module": _mod_id,
                                        "braced": False,
                                        "side": "north",
                                        "length": len_beam_nw_ne,
                                        "direction": "west-east",
                                        "i_node": f"{_story_id}{corner_nw_ID[0]}{corner_nw_ID[1]}",
                                        "j_node": f"{_story_id}{corner_ne_ID[0]}{corner_ne_ID[1]}",
                                        "ele_number": np.nan,
                                        "section": section,
                                        "section_props": self.__get_section_props(
                                            section
                                        ),
                                    }
                                )

                            if length[0] <= len_beam_se_ne <= length[1]:
                                section = section
                                element_dict[beam_type].append(
                                    {
                                        "story": story,
                                        "module": _mod_id,
                                        "braced": False,
                                        "side": "east",
                                        "length": len_beam_se_ne,
                                        "direction": "south-north",
                                        "i_node": f"{_story_id}{corner_se_ID[0]}{corner_se_ID[1]}",
                                        "j_node": f"{_story_id}{corner_ne_ID[0]}{corner_ne_ID[1]}",
                                        "ele_number": np.nan,
                                        "section": section,
                                        "section_props": self.__get_section_props(
                                            section
                                        ),
                                    }
                                )

                            if length[0] <= len_beam_sw_nw <= length[1]:
                                section = section
                                element_dict[beam_type].append(
                                    {
                                        "story": story,
                                        "module": _mod_id,
                                        "braced": False,
                                        "side": "west",
                                        "length": len_beam_sw_nw,
                                        "direction": "south-north",
                                        "i_node": f"{_story_id}{corner_sw_ID[0]}{corner_sw_ID[1]}",
                                        "j_node": f"{_story_id}{corner_nw_ID[0]}{corner_nw_ID[1]}",
                                        "ele_number": np.nan,
                                        "section": section,
                                        "section_props": self.__get_section_props(
                                            section
                                        ),
                                    }
                                )

                # these are neither braced nor regular modules (hard to know what are those)
                else:
                    raise ValueError("These modules should not exist!")

        # self.element_dict = element_dict
        self.df_brace_elements = pd.DataFrame(element_dict["brace"]).astype(
            {"i_node": int, "j_node": int}
        )
        self.df_column_elements = pd.DataFrame(element_dict["column"]).astype(
            {"i_node": int, "j_node": int}
        )
        # drop duplicated values due to overlapping modules
        self.df_column_elements = self.df_column_elements.drop_duplicates(
            subset=["i_node", "j_node"]
        ).reset_index(drop=True)

        self.df_floor_beam_elements = pd.DataFrame(element_dict["floor_beam"]).astype(
            {"i_node": int, "j_node": int}
        )
        self.df_floor_beam_elements = self.df_floor_beam_elements.drop_duplicates(
            subset=["i_node", "j_node"]
        ).reset_index(drop=True)
        self.df_ceiling_beam_elements = pd.DataFrame(
            element_dict["ceiling_beam"]
        ).astype({"i_node": int, "j_node": int})
        self.df_ceiling_beam_elements["mid_node"] = (
            self.df_ceiling_beam_elements["mid_node"].fillna(-1).astype(int)
        )
        self.df_ceiling_beam_elements = self.df_ceiling_beam_elements.drop_duplicates(
            subset=["i_node", "j_node"]
        ).reset_index(drop=True)

        # Define the mappings
        mappings = [
            ("i_col_section", "section"),
            ("i_col_section_props", "section_props"),
            ("j_col_section", "section"),
            ("j_col_section_props", "section_props"),
            ("i_col_multi", "multi"),
            ("j_col_multi", "multi"),
        ]

        # Apply the mappings to df_floor_beam_elements
        for col, prop in mappings:
            if col.startswith("i"):
                self.df_floor_beam_elements[col] = self.df_floor_beam_elements[
                    "i_node"
                ].map(self.df_column_elements.set_index("i_node")[prop])
            elif col.startswith("j"):
                self.df_floor_beam_elements[col] = self.df_floor_beam_elements[
                    "j_node"
                ].map(self.df_column_elements.set_index("i_node")[prop])

        # Apply the mappings to df_ceiling_beam_elements
        for col, prop in mappings:
            if col.startswith("i"):
                self.df_ceiling_beam_elements[col] = self.df_ceiling_beam_elements[
                    "i_node"
                ].map(self.df_column_elements.set_index("j_node")[prop])
            elif col.startswith("j"):
                self.df_ceiling_beam_elements[col] = self.df_ceiling_beam_elements[
                    "j_node"
                ].map(self.df_column_elements.set_index("j_node")[prop])

        self.df_ver_con_elements = self.df_column_elements.copy()
        self.df_column_elements = self.df_column_elements.drop(columns=["len_ver_con"])
        self.df_ver_con_elements = self.df_ver_con_elements.drop(
            columns=["length"]
        ).rename({"len_ver_con": "length"}, axis=1)
        self.df_ver_con_elements = self.df_ver_con_elements
        self.df_ver_con_elements[["i_node", "j_node"]] = (
            self.df_ver_con_elements[["i_node", "j_node"]] - 10000
        )

        # Define the id_vars and value_vars
        id_vars = ["section", "section_props", "side"]
        value_vars = ["i_node", "j_node"]

        # Use melt to unpivot the dataframe
        df_melt_floor = pd.melt(
            self.df_floor_beam_elements,
            id_vars=id_vars,
            value_vars=value_vars,
            var_name="node_type",
            value_name="node",
        )
        df_melt_ceiling = pd.melt(
            self.df_ceiling_beam_elements,
            id_vars=id_vars,
            value_vars=value_vars,
            var_name="node_type",
            value_name="node",
        )

        df_melt_floor_grouped = (
            df_melt_floor.groupby("node")[["section", "section_props", "side"]]
            .agg(list)
            .reset_index()
        )
        df_melt_ceiling_grouped = (
            df_melt_ceiling.groupby("node")[["section", "section_props", "side"]]
            .agg(list)
            .reset_index()
        )

        df_melt_floor_side_ew = df_melt_floor[
            (df_melt_floor["side"] == "west") | (df_melt_floor["side"] == "east")
        ]
        df_melt_floor_side_sn = df_melt_floor[
            (df_melt_floor["side"] == "south") | (df_melt_floor["side"] == "north")
        ]

        df_melt_ceiling_side_ew = df_melt_ceiling[
            (df_melt_ceiling["side"] == "west") | (df_melt_ceiling["side"] == "east")
        ]
        df_melt_ceiling_side_sn = df_melt_ceiling[
            (df_melt_ceiling["side"] == "south") | (df_melt_ceiling["side"] == "north")
        ]

        df_melt_floor_side_ew = (
            df_melt_floor_side_ew.groupby("node")[["section", "section_props", "side"]]
            .agg(list)
            .reset_index()
        )
        df_melt_floor_side_sn = (
            df_melt_floor_side_sn.groupby("node")[["section", "section_props", "side"]]
            .agg(list)
            .reset_index()
        )

        df_melt_ceiling_side_ew = (
            df_melt_ceiling_side_ew.groupby("node")[
                ["section", "section_props", "side"]
            ]
            .agg(list)
            .reset_index()
        )
        df_melt_ceiling_side_sn = (
            df_melt_ceiling_side_sn.groupby("node")[
                ["section", "section_props", "side"]
            ]
            .agg(list)
            .reset_index()
        )

        df_column_elements_ij = self.df_column_elements[["i_node", "j_node"]]

        merged_floor = pd.merge(
            df_column_elements_ij,
            df_melt_floor_grouped,
            left_on="i_node",
            right_on="node",
            how="left",
        )
        merged_ceiling = pd.merge(
            df_column_elements_ij,
            df_melt_ceiling_grouped,
            left_on="j_node",
            right_on="node",
            how="left",
        )

        self.df_column_elements["i_node_beams"] = merged_floor[
            ["section", "section_props", "side"]
        ].values.tolist()

        self.df_column_elements["j_node_beams"] = merged_ceiling[
            ["section", "section_props", "side"]
        ].values.tolist()

        df_ver_con_elements_ij = self.df_ver_con_elements[["i_node", "j_node"]]

        merged_floor = pd.merge(
            df_ver_con_elements_ij,
            df_melt_floor_grouped,
            left_on="j_node",
            right_on="node",
            how="left",
        )
        merged_ceiling = pd.merge(
            df_ver_con_elements_ij,
            df_melt_ceiling_grouped,
            left_on="i_node",
            right_on="node",
            how="left",
        )

        self.df_ver_con_elements["i_node_beams"] = merged_ceiling[
            ["section", "section_props", "side"]
        ].values.tolist()

        self.df_ver_con_elements["j_node_beams"] = merged_floor[
            ["section", "section_props", "side"]
        ].values.tolist()

        # create element numbers
        start_number = 10000
        increment = 20

        self.df_column_elements["multi_value"] = self.df_column_elements.apply(
            lambda row: increment
            if pd.isnull(row["multi"])
            else (row["multi"] * increment),
            axis=1,
        )
        self.df_column_elements.loc[0, "multi_value"] = 0
        self.df_column_elements["ele_number"] = (
            start_number + self.df_column_elements["multi_value"].cumsum()
        ).astype(int)
        self.df_column_elements = self.df_column_elements.drop(columns=["multi_value"])

        end_number = (
            self.df_column_elements["ele_number"].iloc[-1]
            + increment * self.df_column_elements["multi"].iloc[-1]
            if not pd.isnull(self.df_column_elements["multi"].iloc[-1])
            else self.df_column_elements["ele_number"].iloc[-1] + increment
        )

        self.df_ver_con_elements["multi_value"] = self.df_ver_con_elements.apply(
            lambda row: increment
            if pd.isnull(row["multi"])
            else (row["multi"] * increment),
            axis=1,
        )
        self.df_ver_con_elements.loc[0, "multi_value"] = 0
        self.df_ver_con_elements["ele_number"] = (
            end_number + self.df_ver_con_elements["multi_value"].cumsum()
        ).astype(int)
        self.df_ver_con_elements = self.df_ver_con_elements.drop(
            columns=["multi_value"]
        )

        end_number = (
            self.df_ver_con_elements["ele_number"].iloc[-1]
            + increment * self.df_ver_con_elements["multi"].iloc[-1]
            if not pd.isnull(self.df_ver_con_elements["multi"].iloc[-1])
            else self.df_ver_con_elements["ele_number"].iloc[-1] + increment
        )

        self.df_brace_elements["ele_number"] = range(
            end_number, end_number + increment * len(self.df_brace_elements), increment
        )

        end_number = self.df_brace_elements["ele_number"].iloc[-1] + increment

        self.df_floor_beam_elements["ele_number"] = range(
            end_number,
            end_number + increment * len(self.df_floor_beam_elements),
            increment,
        )

        end_number = self.df_floor_beam_elements["ele_number"].iloc[-1] + increment

        self.df_ceiling_beam_elements["ele_number"] = range(
            end_number,
            end_number + increment * len(self.df_ceiling_beam_elements),
            increment,
        )

        # map new node numbers
        self.df_column_elements = self.df_column_elements.rename(
            columns={"i_node": "i_node_old", "j_node": "j_node_old"}
        )
        self.df_column_elements[["i_node", "j_node"]] = self.df_column_elements[
            ["i_node_old", "j_node_old"]
        ].map(self.__map_dict_node.get)

        self.df_ver_con_elements = self.df_ver_con_elements.rename(
            columns={"i_node": "i_node_old", "j_node": "j_node_old"}
        )
        self.df_ver_con_elements[["i_node", "j_node"]] = self.df_ver_con_elements[
            ["i_node_old", "j_node_old"]
        ].map(self.__map_dict_node.get)

        self.df_brace_elements = self.df_brace_elements.rename(
            columns={"i_node": "i_node_old", "j_node": "j_node_old"}
        )
        self.df_brace_elements[["i_node", "j_node"]] = self.df_brace_elements[
            ["i_node_old", "j_node_old"]
        ].map(self.__map_dict_node.get)

        self.df_floor_beam_elements = self.df_floor_beam_elements.rename(
            columns={"i_node": "i_node_old", "j_node": "j_node_old"}
        )
        self.df_floor_beam_elements[["i_node", "j_node"]] = self.df_floor_beam_elements[
            ["i_node_old", "j_node_old"]
        ].map(self.__map_dict_node.get)

        self.df_ceiling_beam_elements = self.df_ceiling_beam_elements.rename(
            columns={
                "i_node": "i_node_old",
                "mid_node": "mid_node_old",
                "j_node": "j_node_old",
            }
        )
        self.df_ceiling_beam_elements[["i_node", "mid_node", "j_node"]] = (
            self.df_ceiling_beam_elements[["i_node_old", "mid_node_old", "j_node_old"]]
            .map(self.__map_dict_node.get)
            .fillna(-1)
            .astype(int)
        )

        # Add member self weight to the dataframes
        self.df_column_elements["self_weight"] = (
            self.df_column_elements["length"]
            * self.df_column_elements["section_props"].apply(lambda x: x["W"])
            * np.where(
                pd.notnull(self.df_column_elements["multi"]),
                self.df_column_elements["multi"],
                1,
            )
        )

        self.df_ver_con_elements["self_weight"] = (
            self.df_ver_con_elements["length"]
            * self.df_ver_con_elements["section_props"].apply(lambda x: x["W"])
            * np.where(
                pd.notnull(self.df_ver_con_elements["multi"]),
                self.df_ver_con_elements["multi"],
                1,
            )
        )

        self.df_brace_elements["self_weight"] = self.df_brace_elements[
            "length"
        ] * self.df_brace_elements["section_props"].apply(lambda x: x["W"])

        self.df_floor_beam_elements["self_weight"] = self.df_floor_beam_elements[
            "length"
        ] * self.df_floor_beam_elements["section_props"].apply(lambda x: x["W"])

        self.df_ceiling_beam_elements["self_weight"] = self.df_ceiling_beam_elements[
            "length"
        ] * self.df_ceiling_beam_elements["section_props"].apply(lambda x: x["W"])

        return None

    def __parse_brace_section(self) -> None:
        data_dict = self.sections["brace"]

        data_list = []
        for _, section_info in data_dict.items():
            row_dict = {}
            story = section_info["story"]
            location = "all"
            if isinstance(story, list) and len(story) >= 2:
                story = range(story[0], story[-1] + 1)
            if isinstance(section_info["section"], dict):
                for location, section in section_info["section"].items():
                    new_row_dict = row_dict.copy()
                    new_row_dict.update(
                        {"location": location, "section": section, "story": story}
                    )
                    data_list.append(new_row_dict)
            else:
                row_dict.update(
                    {
                        "section": section_info["section"],
                        "story": story,
                        "location": location,
                    }
                )
                data_list.append(row_dict)

        self.df_brace_sections = pd.DataFrame(data_list)
        self.df_brace_sections = self.df_brace_sections.explode("story")
        self.df_brace_sections = self.df_brace_sections.groupby("story").agg(list)

        return None

    def __parse_beam_section(self) -> None:
        keys = ["ceiling_beam", "floor_beam"]
        df_dict = {}

        for key in keys:
            data_list_regular = []
            data_list_braced = []
            data_dict = self.sections[key]
            for section_type, sections in data_dict.items():
                for section_id, section_info in sections.items():
                    row_dict = {}
                    story = section_info["story"]
                    direction = "all"
                    length = section_info["length"]

                    if isinstance(story, list) and len(story) >= 2:
                        story = range(story[0], story[-1] + 1)
                    elif section_info["story"] == "all":
                        story = self.df_height.index.to_list()
                    if isinstance(section_info["section"], dict):
                        for direction, section in section_info["section"].items():
                            new_row_dict = row_dict.copy()
                            new_row_dict.update(
                                {
                                    "direction": direction,
                                    "section": section,
                                    "story": story,
                                    "length": length,
                                }
                            )
                            if section_type == "braced":
                                data_list_braced.append(new_row_dict)
                            else:
                                data_list_regular.append(new_row_dict)
                    else:
                        row_dict.update(section_info)
                        row_dict.update(
                            {"story": story, "direction": direction, "length": length}
                        )
                        if section_type == "braced":
                            data_list_braced.append(row_dict)
                        else:
                            data_list_regular.append(row_dict)

            df_dict[key + "_regular"] = pd.DataFrame(data_list_regular)
            df_dict[key + "_braced"] = pd.DataFrame(data_list_braced)

        self.df_ceiling_braced_sections = pd.DataFrame(df_dict["ceiling_beam_braced"])
        self.df_ceiling_regular_sections = pd.DataFrame(df_dict["ceiling_beam_regular"])
        self.df_floor_braced_sections = pd.DataFrame(df_dict["floor_beam_braced"])
        self.df_floor_regular_sections = pd.DataFrame(df_dict["floor_beam_regular"])

        self.df_ceiling_braced_sections = self.df_ceiling_braced_sections.explode(
            "story"
        )
        self.df_ceiling_braced_sections = self.df_ceiling_braced_sections.groupby(
            "story"
        ).agg(list)

        self.df_ceiling_regular_sections = self.df_ceiling_regular_sections.explode(
            "story"
        )
        self.df_ceiling_regular_sections = self.df_ceiling_regular_sections.groupby(
            "story"
        ).agg(list)

        self.df_floor_braced_sections = self.df_floor_braced_sections.explode("story")
        self.df_floor_braced_sections = self.df_floor_braced_sections.groupby(
            "story"
        ).agg(list)

        self.df_floor_regular_sections = self.df_floor_regular_sections.explode("story")
        self.df_floor_regular_sections = self.df_floor_regular_sections.groupby(
            "story"
        ).agg(list)

        return None

    def __parse_column_section(self) -> None:
        data = []

        for _, values in self.sections["column"].items():
            section = values["section"]
            for story in range(values["story"][0], values["story"][1] + 1):
                for key1 in self.modules.keys():
                    # start, end = map(int, key1.split("-"))
                    # if start <= story <= end:
                    if story in helper.convert_to_range(key1):
                        for module_num in self.modules[key1].keys():
                            if (
                                values.get("multi")
                                and module_num in values["multi"].keys()
                            ):
                                data.append(
                                    {
                                        "story": story,
                                        "module": module_num,
                                        "section": section,
                                        "multi": values["multi"][module_num],
                                    }
                                )
                            else:
                                data.append(
                                    {
                                        "story": story,
                                        "module": module_num,
                                        "section": section,
                                        "multi": None,
                                    }
                                )

        self.df_column_sections = pd.DataFrame(data).set_index(["story", "module"])
        self.logger.info("Column, brace, and beam sections have been created.")
        return None

    @helper.log_time_memory
    def connection(self, **kwargs) -> None:
        """Creates the connection dataframes."""
        self.methods_called["connection"] = True
        if (
            self.methods_called["layout"] is False
            or self.methods_called["height"] is False
            or self.methods_called["node"] is False
            or self.methods_called["element"] is False
        ):
            raise ValueError(
                "Please run the layout, height, node, and element methods first."
            )

        connection = kwargs.get("connection", None)
        if isinstance(connection, dict):
            self.__parse_connection(connection)
            self.__horizontal_connections()
            self.logger.info(
                "Connection dataframes and horizontal connections have been created."
            )
        else:
            raise ValueError("Please provide a connection dictionary.")

        return None

    def __parse_connection(self, connection) -> None:
        """Parses the connection information."""
        dict_inter_module, dict_intra_module = {}, {}
        for key1, val1 in connection.items():
            if key1 == "inter-module":
                for key2, val2 in val1.items():
                    if key2 == "braced_frame":
                        self.df_inter_braced = pd.DataFrame(val2)
                    elif key2 == "unbraced_frame":
                        self.df_inter_unbraced = pd.DataFrame(val2)
                    else:
                        raise ValueError(
                            f"Please provide a valid connection type. {key2 = } is not valid."
                        )
            elif key1 == "intra-module":
                for key2, val2 in val1.items():
                    if key2 == "braced_frame":
                        self.df_intra_braced = pd.DataFrame(val2)
                    elif key2 == "unbraced_frame":
                        self.df_intra_unbraced = pd.DataFrame(val2)
                    else:
                        raise ValueError(
                            f"Please provide a valid connection type. {key2 = } is not valid."
                        )
            else:
                raise ValueError(
                    f"Please provide a valid connection type. {key1 = } is not valid."
                )

        return None

    def __horizontal_connections(self) -> None:
        location = self.df_inter_braced["hor_con"]["location"]
        if not location in ["corner", "point"]:
            raise ValueError(
                f"Please provide a valid location. {location = } is not valid."
            )

        horizontal_connection = []
        if location == "corner":
            for height in self.df_height.itertuples():
                for row in self.df_corner_neighbors.itertuples():
                    if height.Index in row.story:
                        idx_corner = row.corner
                        sr_master_module = self.df_modules.loc[
                            (height.Index, row.module)
                        ]
                        corner_coord = sr_master_module["corners"][idx_corner]
                        corner_id = sr_master_module["corners_ID"][idx_corner]
                        master_sw, master_se, master_ne, master_nw = sr_master_module[
                            "corners"
                        ]
                        for neighbor in row.neighbors:
                            if neighbor:
                                neighbor_mod, neighbor_idx = neighbor
                                sr_neighbor_module = self.df_modules.loc[
                                    (height.Index, neighbor_mod)
                                ]
                                neighbor_coord = sr_neighbor_module["corners"][
                                    neighbor_idx
                                ]
                                neighbor_id = sr_neighbor_module["corners_ID"][
                                    neighbor_idx
                                ]
                                (
                                    neighbor_sw,
                                    neighbor_se,
                                    neighbor_ne,
                                    neighbor_nw,
                                ) = sr_neighbor_module["corners"]
                                if corner_coord[0] == neighbor_coord[0] and (
                                    corner_coord[1] - neighbor_coord[1] < 0
                                    or corner_coord[1] - neighbor_coord[1] > 0
                                ):
                                    horizontal_connection.append(
                                        {
                                            "corner_id": corner_id,
                                            "neighbor_id": neighbor_id,
                                            "i_node": f"{corner_id[0]}{corner_id[1]}",
                                            "j_node": f"{neighbor_id[0]}{neighbor_id[1]}",
                                            "module_id": row.module,
                                            "neighbor_module_id": neighbor_mod,
                                            "direction": "south-north",
                                            "length": abs(
                                                corner_coord[1] - neighbor_coord[1]
                                            ),
                                            "i_corner": "sw"
                                            if np.array_equal(corner_coord, master_sw)
                                            else "se"
                                            if np.array_equal(corner_coord, master_se)
                                            else "ne"
                                            if np.array_equal(corner_coord, master_ne)
                                            else "nw",
                                            "j_corner": "sw"
                                            if np.array_equal(
                                                neighbor_coord, neighbor_sw
                                            )
                                            else "se"
                                            if np.array_equal(
                                                neighbor_coord, neighbor_se
                                            )
                                            else "ne"
                                            if np.array_equal(
                                                neighbor_coord, neighbor_ne
                                            )
                                            else "nw",
                                            "story": height.Index,
                                            "story_id": height.story_ID,
                                            "corner_coord": corner_coord,
                                            "neighbor_coord": neighbor_coord,
                                        }
                                    )
                                elif corner_coord[1] == neighbor_coord[1] and (
                                    corner_coord[0] - neighbor_coord[0] < 0
                                    or corner_coord[0] - neighbor_coord[0] > 0
                                ):
                                    horizontal_connection.append(
                                        {
                                            "corner_id": corner_id,
                                            "neighbor_id": neighbor_id,
                                            "i_node": f"{corner_id[0]}{corner_id[1]}",
                                            "j_node": f"{neighbor_id[0]}{neighbor_id[1]}",
                                            "module_id": row.module,
                                            "neighbor_module_id": neighbor_mod,
                                            "direction": "west-east",
                                            "length": abs(
                                                corner_coord[0] - neighbor_coord[0]
                                            ),
                                            "i_corner": "sw"
                                            if np.array_equal(corner_coord, master_sw)
                                            else "se"
                                            if np.array_equal(corner_coord, master_se)
                                            else "ne"
                                            if np.array_equal(corner_coord, master_ne)
                                            else "nw",
                                            "j_corner": "sw"
                                            if np.array_equal(
                                                neighbor_coord, neighbor_sw
                                            )
                                            else "se"
                                            if np.array_equal(
                                                neighbor_coord, neighbor_se
                                            )
                                            else "ne"
                                            if np.array_equal(
                                                neighbor_coord, neighbor_ne
                                            )
                                            else "nw",
                                            "story": height.Index,
                                            "story_id": height.story_ID,
                                            "corner_coord": corner_coord,
                                            "neighbor_coord": neighbor_coord,
                                        }
                                    )

        elif location == "point":
            for height in self.df_height.itertuples():
                for row in self.df_point_neighbors.itertuples():
                    if height.Index in row.story:
                        idx_point = row.point
                        sr_master_module = self.df_modules.loc[
                            (height.Index, row.module)
                        ]
                        point_coord = sr_master_module["points"][idx_point]
                        point_id = sr_master_module["points_ID"][idx_point]
                        master_sw, master_se, master_ne, master_nw = sr_master_module[
                            "corners"
                        ]
                        for neighbor in row.neighbors:
                            if neighbor:
                                neighbor_mod, neighbor_idx = neighbor
                                sr_neighbor_module = self.df_modules.loc[
                                    (height.Index, neighbor_mod)
                                ]
                                neighbor_coord = sr_neighbor_module["points"][
                                    neighbor_idx
                                ]
                                neighbor_id = sr_neighbor_module["points_ID"][
                                    neighbor_idx
                                ]
                                (
                                    neighbor_sw,
                                    neighbor_se,
                                    neighbor_ne,
                                    neighbor_nw,
                                ) = sr_neighbor_module["corners"]
                                if point_coord[0] == neighbor_coord[0] and (
                                    point_coord[1] - neighbor_coord[1] < 0
                                    or point_coord[1] - neighbor_coord[1] > 0
                                ):
                                    horizontal_connection.append(
                                        {
                                            "point_id": point_id,
                                            "neighbor_id": neighbor_id,
                                            "i_node": f"{point_id[0]}{point_id[1]}",
                                            "j_node": f"{neighbor_id[0]}{neighbor_id[1]}",
                                            "module_id": row.module,
                                            "neighbor_module_id": neighbor_mod,
                                            "direction": "south-north",
                                            "length": abs(
                                                point_coord[1] - neighbor_coord[1]
                                            ),
                                            "i_point": "sw"
                                            if np.array_equal(point_coord, master_sw)
                                            else "se"
                                            if np.array_equal(point_coord, master_se)
                                            else "ne"
                                            if np.array_equal(point_coord, master_ne)
                                            else "nw"
                                            if np.array_equal(point_coord, master_nw)
                                            else "middle",
                                            "j_point": "sw"
                                            if np.array_equal(
                                                neighbor_coord, neighbor_sw
                                            )
                                            else "se"
                                            if np.array_equal(
                                                neighbor_coord, neighbor_se
                                            )
                                            else "ne"
                                            if np.array_equal(
                                                neighbor_coord, neighbor_ne
                                            )
                                            else "nw"
                                            if np.array_equal(
                                                neighbor_coord, neighbor_nw
                                            )
                                            else "middle",
                                            "story": height.Index,
                                            "story_id": height.story_ID,
                                            "point_coord": point_coord,
                                            "neighbor_coord": neighbor_coord,
                                        }
                                    )
                                elif point_coord[1] == neighbor_coord[1] and (
                                    point_coord[0] - neighbor_coord[0] < 0
                                    or point_coord[0] - neighbor_coord[0] > 0
                                ):
                                    horizontal_connection.append(
                                        {
                                            "point_id": point_id,
                                            "neighbor_id": neighbor_id,
                                            "i_node": f"{point_id[0]}{point_id[1]}",
                                            "j_node": f"{neighbor_id[0]}{neighbor_id[1]}",
                                            "module_id": row.module,
                                            "neighbor_module_id": neighbor_mod,
                                            "direction": "west-east",
                                            "length": abs(
                                                point_coord[0] - neighbor_coord[0]
                                            ),
                                            "i_point": "sw"
                                            if np.array_equal(point_coord, master_sw)
                                            else "se"
                                            if np.array_equal(point_coord, master_se)
                                            else "ne"
                                            if np.array_equal(point_coord, master_ne)
                                            else "nw"
                                            if np.array_equal(point_coord, master_nw)
                                            else "middle",
                                            "j_point": "sw"
                                            if np.array_equal(
                                                neighbor_coord, neighbor_sw
                                            )
                                            else "se"
                                            if np.array_equal(
                                                neighbor_coord, neighbor_se
                                            )
                                            else "ne"
                                            if np.array_equal(
                                                neighbor_coord, neighbor_ne
                                            )
                                            else "nw"
                                            if np.array_equal(
                                                neighbor_coord, neighbor_nw
                                            )
                                            else "middle",
                                            "story": height.Index,
                                            "story_id": height.story_ID,
                                            "point_coord": point_coord,
                                            "neighbor_coord": neighbor_coord,
                                        }
                                    )
        else:
            raise ValueError(
                f"Please provide a valid location. {location = } is not valid."
            )

        self.df_hor_con_elements = pd.DataFrame(horizontal_connection)

        self.df_hor_con_elements["couple"] = self.df_hor_con_elements.apply(
            lambda row: tuple(sorted([row["i_node"], row["j_node"]])), axis=1
        )

        self.df_hor_con_elements = self.df_hor_con_elements[
            ~self.df_hor_con_elements.duplicated(subset=["story", "couple"])
        ]

        self.df_hor_con_elements = self.df_hor_con_elements.drop(columns="couple")

        self.df_hor_con_elements["i_floor"] = self.df_hor_con_elements.apply(
            lambda row: str(row["story_id"][1]) + str(row["i_node"]), axis=1
        )
        self.df_hor_con_elements["j_floor"] = self.df_hor_con_elements.apply(
            lambda row: str(row["story_id"][1]) + str(row["j_node"]), axis=1
        )
        self.df_hor_con_elements["i_ceiling"] = self.df_hor_con_elements.apply(
            lambda row: str(row["story_id"][2]) + str(row["i_node"]), axis=1
        )
        self.df_hor_con_elements["j_ceiling"] = self.df_hor_con_elements.apply(
            lambda row: str(row["story_id"][2]) + str(row["j_node"]), axis=1
        )

        self.df_hor_con_elements = self.df_hor_con_elements.astype(
            {
                "i_node": int,
                "j_node": int,
                "i_floor": int,
                "j_floor": int,
                "i_ceiling": int,
                "j_ceiling": int,
            }
        )

        # Renumbering the nodes
        self.df_hor_con_elements = self.df_hor_con_elements.rename(
            {
                "i_floor": "i_floor_old",
                "j_floor": "j_floor_old",
                "i_ceiling": "i_ceiling_old",
                "j_ceiling": "j_ceiling_old",
            },
            axis=1,
        )
        self.df_hor_con_elements[
            ["i_floor", "j_floor", "i_ceiling", "j_ceiling"]
        ] = self.df_hor_con_elements[
            ["i_floor_old", "j_floor_old", "i_ceiling_old", "j_ceiling_old"]
        ].map(
            self.__map_dict_node.get
        )

        # Define the id_vars and value_vars
        id_vars = ["section", "section_props", "braced", "side"]
        value_vars = ["i_node", "j_node"]

        # Use melt to unpivot the dataframe
        df_melt_floor = pd.melt(
            self.df_floor_beam_elements,
            id_vars=id_vars,
            value_vars=value_vars,
            var_name="node_type",
            value_name="node",
        )
        df_melt_ceiling = pd.melt(
            self.df_ceiling_beam_elements,
            id_vars=id_vars,
            value_vars=value_vars,
            var_name="node_type",
            value_name="node",
        )

        df_melt_floor_side_ew = df_melt_floor[
            (df_melt_floor["side"] == "west") | (df_melt_floor["side"] == "east")
        ]
        df_melt_floor_side_sn = df_melt_floor[
            (df_melt_floor["side"] == "south") | (df_melt_floor["side"] == "north")
        ]

        df_melt_ceiling_side_ew = df_melt_ceiling[
            (df_melt_ceiling["side"] == "west") | (df_melt_ceiling["side"] == "east")
        ]
        df_melt_ceiling_side_sn = df_melt_ceiling[
            (df_melt_ceiling["side"] == "south") | (df_melt_ceiling["side"] == "north")
        ]

        df_melt_floor_side_ew = (
            df_melt_floor_side_ew.groupby("node")[
                ["section", "section_props", "braced", "side"]
            ]
            .agg(list)
            .reset_index()
        )
        df_melt_floor_side_sn = (
            df_melt_floor_side_sn.groupby("node")[
                ["section", "section_props", "braced", "side"]
            ]
            .agg(list)
            .reset_index()
        )

        df_melt_ceiling_side_ew = (
            df_melt_ceiling_side_ew.groupby("node")[
                ["section", "section_props", "braced", "side"]
            ]
            .agg(list)
            .reset_index()
        )
        df_melt_ceiling_side_sn = (
            df_melt_ceiling_side_sn.groupby("node")[
                ["section", "section_props", "braced", "side"]
            ]
            .agg(list)
            .reset_index()
        )

        operations = [
            {
                "df": df_melt_floor_side_sn,
                "direction": "west-east",
                "element": "floor",
            },
            {
                "df": df_melt_floor_side_ew,
                "direction": "south-north",
                "element": "floor",
            },
            {
                "df": df_melt_ceiling_side_ew,
                "direction": "west-east",
                "element": "ceiling",
            },
            {
                "df": df_melt_ceiling_side_sn,
                "direction": "south-north",
                "element": "ceiling",
            },
        ]

        for op in operations:
            mapping_dict1 = op["df"].set_index("node")["section"].to_dict()
            mapping_dict2 = op["df"].set_index("node")["section_props"].to_dict()
            mapping_dict3 = op["df"].set_index("node")["braced"].to_dict()

            self.df_hor_con_elements.loc[
                self.df_hor_con_elements.direction == op["direction"],
                f"i_{op['element']}_section",
            ] = self.df_hor_con_elements.loc[
                self.df_hor_con_elements.direction == op["direction"],
                f"i_{op['element']}",
            ].map(
                mapping_dict1
            )

            self.df_hor_con_elements.loc[
                self.df_hor_con_elements.direction == op["direction"],
                f"i_{op['element']}_section_props",
            ] = self.df_hor_con_elements.loc[
                self.df_hor_con_elements.direction == op["direction"],
                f"i_{op['element']}",
            ].map(
                mapping_dict2
            )

            self.df_hor_con_elements.loc[
                self.df_hor_con_elements.direction == op["direction"],
                f"i_{op['element']}_braced",
            ] = self.df_hor_con_elements.loc[
                self.df_hor_con_elements.direction == op["direction"],
                f"i_{op['element']}",
            ].map(
                mapping_dict3
            )

            self.df_hor_con_elements.loc[
                self.df_hor_con_elements.direction == op["direction"],
                f"j_{op['element']}_section",
            ] = self.df_hor_con_elements.loc[
                self.df_hor_con_elements.direction == op["direction"],
                f"j_{op['element']}",
            ].map(
                mapping_dict1
            )

            self.df_hor_con_elements.loc[
                self.df_hor_con_elements.direction == op["direction"],
                f"j_{op['element']}_section_props",
            ] = self.df_hor_con_elements.loc[
                self.df_hor_con_elements.direction == op["direction"],
                f"j_{op['element']}",
            ].map(
                mapping_dict2
            )

            self.df_hor_con_elements.loc[
                self.df_hor_con_elements.direction == op["direction"],
                f"j_{op['element']}_braced",
            ] = self.df_hor_con_elements.loc[
                self.df_hor_con_elements.direction == op["direction"],
                f"j_{op['element']}",
            ].map(
                mapping_dict3
            )

        # Add member self weight to the dataframe
        self.df_hor_con_elements["self_weight_ceiling"] = np.maximum(
            self.df_hor_con_elements["length"]
            * self.df_hor_con_elements["i_floor_section_props"].apply(
                lambda x: max(item["W"] for item in x) if isinstance(x, list) else 0
            ),
            self.df_hor_con_elements["length"]
            * self.df_hor_con_elements["j_floor_section_props"].apply(
                lambda x: max(item["W"] for item in x) if isinstance(x, list) else 0
            ),
        )
        self.df_hor_con_elements["self_weight_floor"] = np.maximum(
            self.df_hor_con_elements["length"]
            * self.df_hor_con_elements["i_ceiling_section_props"].apply(
                lambda x: max(item["W"] for item in x) if isinstance(x, list) else 0
            ),
            self.df_hor_con_elements["length"]
            * self.df_hor_con_elements["j_ceiling_section_props"].apply(
                lambda x: max(item["W"] for item in x) if isinstance(x, list) else 0
            ),
        )

        cols = [
            "story",
            "direction",
            "length",
            "i_ceiling",
            "j_ceiling",
            "i_ceiling_section",
            "i_ceiling_section_props",
            "i_ceiling_braced",
            "j_ceiling_section",
            "j_ceiling_section_props",
            "j_ceiling_braced",
        ]
        df_hor_con_ceiling = self.df_hor_con_elements[cols].copy()

        # Apply the lambda function to each row
        df_hor_con_ceiling["braced"] = df_hor_con_ceiling.apply(
            lambda row: True
            if row["i_ceiling_braced"] is True
            or (
                isinstance(row["i_ceiling_braced"], list)
                and True in row["i_ceiling_braced"]
            )
            or row["j_ceiling_braced"] is True
            or (
                isinstance(row["j_ceiling_braced"], list)
                and True in row["j_ceiling_braced"]
            )
            else False,
            axis=1,
        )

        df_hor_con_ceiling["section_props"] = df_hor_con_ceiling.apply(
            lambda row: max(
                max(row["i_ceiling_section_props"], key=lambda x: x.get("Ix", 0))
                if isinstance(row["i_ceiling_section_props"], list)
                else {"Ix": 0},
                max(row["j_ceiling_section_props"], key=lambda x: x.get("Ix", 0))
                if isinstance(row["j_ceiling_section_props"], list)
                else {"Ix": 0},
                key=lambda x: x.get("Ix", 0),
            ),
            axis=1,
        )

        cols = [
            "story",
            "direction",
            "length",
            "i_floor",
            "j_floor",
            "i_floor_section",
            "i_floor_section_props",
            "i_floor_braced",
            "j_floor_section",
            "j_floor_section_props",
            "j_floor_braced",
        ]
        df_hor_con_floor = self.df_hor_con_elements[cols].copy()

        # Apply the lambda function to each row
        df_hor_con_floor["braced"] = df_hor_con_floor.apply(
            lambda row: True
            if row["i_floor_braced"] is True
            or (
                isinstance(row["i_floor_braced"], list)
                and True in row["i_floor_braced"]
            )
            or row["j_floor_braced"] is True
            or (
                isinstance(row["j_floor_braced"], list)
                and True in row["j_floor_braced"]
            )
            else False,
            axis=1,
        )

        df_hor_con_floor["section_props"] = df_hor_con_floor.apply(
            lambda row: max(
                max(row["i_floor_section_props"], key=lambda x: x.get("Ix", 0))
                if isinstance(row["i_floor_section_props"], list)
                else {"Ix": 0},
                max(row["j_floor_section_props"], key=lambda x: x.get("Ix", 0))
                if isinstance(row["j_floor_section_props"], list)
                else {"Ix": 0},
                key=lambda x: x.get("Ix", 0),
            ),
            axis=1,
        )

        # Rename columns
        df_hor_con_floor = df_hor_con_floor.rename(
            columns={"i_floor": "i_node", "j_floor": "j_node"}
        )
        df_hor_con_ceiling = df_hor_con_ceiling.rename(
            columns={"i_ceiling": "i_node", "j_ceiling": "j_node"}
        )

        # Select required columns
        df_hor_con_floor = df_hor_con_floor[
            [
                "story",
                "direction",
                "length",
                "i_node",
                "j_node",
                "braced",
                "section_props",
            ]
        ]
        df_hor_con_ceiling = df_hor_con_ceiling[
            [
                "story",
                "direction",
                "length",
                "i_node",
                "j_node",
                "braced",
                "section_props",
            ]
        ]

        include_floor_braced, include_ceiling_braced = False, False
        include_floor_unbraced, include_ceiling_unbraced = False, False
        for item in self.df_inter_braced.loc["position", "hor_con"]:
            if item == "floor":
                include_floor_braced = True
                model_floor_braced = self.df_inter_braced.loc["model", "hor_con"]
            elif item == "ceiling":
                include_ceiling_braced = True
                model_ceiling_braced = self.df_inter_braced.loc["model", "hor_con"]
        for item in self.df_inter_unbraced.loc["position", "hor_con"]:
            if item == "floor":
                include_floor_unbraced = True
                model_floor_unbraced = self.df_inter_unbraced.loc["model", "hor_con"]
            elif item == "ceiling":
                include_ceiling_unbraced = True
                model_ceiling_unbraced = self.df_inter_unbraced.loc["model", "hor_con"]

        # Initialize the dataframes
        df_hor_con_floor_filtered = pd.DataFrame()
        df_hor_con_ceiling_filtered = pd.DataFrame()

        # Check the conditions for floor
        if include_floor_braced:
            df_hor_con_floor_filtered = pd.concat(
                [
                    df_hor_con_floor_filtered,
                    df_hor_con_floor[df_hor_con_floor["braced"] == True],
                ]
            )
            df_hor_con_floor_filtered["model"] = model_floor_braced
        if include_floor_unbraced:
            df_hor_con_floor_filtered = pd.concat(
                [
                    df_hor_con_floor_filtered,
                    df_hor_con_floor[df_hor_con_floor["braced"] == False],
                ]
            )
            df_hor_con_floor_filtered["model"] = model_floor_unbraced

        # Check the conditions for ceiling
        if include_ceiling_braced:
            df_hor_con_ceiling_filtered = pd.concat(
                [
                    df_hor_con_ceiling_filtered,
                    df_hor_con_ceiling[df_hor_con_ceiling["braced"] == True],
                ]
            )
            df_hor_con_ceiling_filtered["model"] = model_ceiling_braced

        if include_ceiling_unbraced:
            df_hor_con_ceiling_filtered = pd.concat(
                [
                    df_hor_con_ceiling_filtered,
                    df_hor_con_ceiling[df_hor_con_ceiling["braced"] == False],
                ]
            )
            df_hor_con_ceiling_filtered["model"] = model_ceiling_unbraced

        # Concatenate the filtered dataframes
        self.df_hor_con_elements_filtered = pd.concat(
            [df_hor_con_floor_filtered, df_hor_con_ceiling_filtered]
        ).reset_index(drop=True)

        increment = int(
            self.df_ceiling_beam_elements["ele_number"].iloc[-2:].diff().iloc[-1]
        )
        end_number = int(
            self.df_ceiling_beam_elements["ele_number"].iloc[-1] + increment
        )

        self.df_hor_con_elements_filtered["ele_number"] = range(
            end_number,
            end_number + increment * len(self.df_hor_con_elements_filtered),
            increment,
        )

        return None

    @helper.log_time_memory
    def load(self, **kwargs) -> None:
        """Loads the input files and parses the data."""
        self.methods_called["load"] = True

        load_and_factor = kwargs.get("load_and_factor", None)
        if isinstance(load_and_factor, dict):
            self.__parse_load_and_factor(load_and_factor)
        else:
            raise ValueError(
                "Please provide a dictionary with the load and factor information."
            )

        self.df_modules["area"] = np.nan
        area = self.df_modules["corners"].apply(lambda x: helper.poly_area(*zip(*x)))
        self.df_modules["area"] = area
        self.df_ceiling_loads["area"] = area
        self.df_floor_loads["area"] = area

        cols = [col for col in self.df_ceiling_loads.columns if col != "area"]

        self.df_ceiling_loads[cols] = self.df_ceiling_loads[cols].multiply(
            area, axis="index"
        )
        self.df_floor_loads[cols] = self.df_floor_loads[cols].multiply(
            area, axis="index"
        )

        self.df_ceiling_loads = self.df_ceiling_loads.loc[
            self.df_diaphragms[self.df_diaphragms["type"] == "ceiling"].index
        ]
        self.df_floor_loads = self.df_floor_loads.loc[
            self.df_diaphragms[self.df_diaphragms["type"] == "floor"].index
        ]

        self.__module_self_weight()
        self.logger.info("Load dataframes have been created.")
        return None

    def __parse_load_and_factor(self, load_and_factor) -> None:
        """Parses the load and factor information."""
        dict_ceiling, dict_floor = {}, {}
        for keys, values in load_and_factor.items():
            if keys == "load":
                for _keys, _values in values.items():
                    if _keys == "all":
                        for item, values in _values.items():
                            if item == "ceiling":
                                dict_ceiling.update(values)
                            elif item == "floor":
                                dict_floor.update(values)

                        self.df_ceiling_loads = pd.DataFrame(
                            index=self.df_modules.index
                        )
                        self.df_floor_loads = pd.DataFrame(index=self.df_modules.index)
                        for items in dict_ceiling.items():
                            self.df_ceiling_loads[items[0]] = items[1]
                        for items in dict_floor.items():
                            self.df_floor_loads[items[0]] = items[1]

                    elif _keys == "modify":
                        for _items in _values.items():
                            for story in helper.convert_to_range(_items[0]):
                                for item, values in _items[1].items():
                                    if item == "ceiling":
                                        for _mod_id, __value in values.items():
                                            if _mod_id == "all":
                                                for ___items in __value.items():
                                                    self.df_ceiling_loads.loc[
                                                        (story, slice(None)),
                                                        ___items[0],
                                                    ] = ___items[1]
                                            elif _mod_id != "all" and isinstance(
                                                _mod_id, str
                                            ):
                                                for __mod_id in helper.convert_to_range(
                                                    _mod_id
                                                ):
                                                    for ___items in __value.items():
                                                        self.df_ceiling_loads.loc[
                                                            (story, __mod_id),
                                                            ___items[0],
                                                        ] = ___items[1]
                                            elif isinstance(_mod_id, int):
                                                for ___items in __value.items():
                                                    self.df_ceiling_loads.loc[
                                                        (story, _mod_id), ___items[0]
                                                    ] = ___items[1]
                                            else:
                                                raise ValueError(
                                                    f"Please provide a valid module id. {_mod_id = } is not valid."
                                                )

                                    elif item == "floor":
                                        for _mod_id, __value in values.items():
                                            if _mod_id == "all":
                                                for ___items in __value.items():
                                                    self.df_floor_loads.loc[
                                                        (story, slice(None)),
                                                        ___items[0],
                                                    ] = ___items[1]
                                            elif _mod_id != "all" and isinstance(
                                                _mod_id, str
                                            ):
                                                for __mod_id in helper.convert_to_range(
                                                    _mod_id
                                                ):
                                                    for ___items in __value.items():
                                                        self.df_floor_loads.loc[
                                                            (story, __mod_id),
                                                            ___items[0],
                                                        ] = ___items[1]
                                            elif isinstance(_mod_id, int):
                                                for ___items in __value.items():
                                                    self.df_floor_loads.loc[
                                                        (story, _mod_id), ___items[0]
                                                    ] = ___items[1]
                                            else:
                                                raise ValueError(
                                                    f"Please provide a valid module id. {_mod_id = } is not valid."
                                                )

                                    else:
                                        raise ValueError(
                                            f"Please provide a valid load {item = }. Currently, 'ceiling' and 'floor' are supported."
                                        )
            elif keys == "factor":
                self.df_load_factors = pd.DataFrame(values)

                values = self.df_load_factors.to_numpy()
                values = np.insert(values, 0, 1, axis=0)

                self.df_load_factors = pd.DataFrame(
                    values, columns=self.df_load_factors.columns
                )

            else:
                raise ValueError(
                    f"Please provide a valid {keys = }. Currently, 'load' and 'factor' are supported."
                )

        return None

    def partition(self, niter=100, ufactor=3, ncuts=10, **kwargs) -> None:
        """Partitions the modules."""
        self.methods_called["partition"] = True

        ele_nodes = {}

        # For df_column_elements
        ele_nodes["i_node"] = self.df_column_elements["i_node"].tolist()
        ele_nodes["j_node"] = self.df_column_elements["j_node"].tolist()
        ele_nodes["mid_node"] = [-1] * len(ele_nodes["i_node"])

        # For df_ver_con_elements
        ele_nodes["i_node"] += self.df_ver_con_elements["i_node"].tolist()
        ele_nodes["j_node"] += self.df_ver_con_elements["j_node"].tolist()
        ele_nodes["mid_node"] += [-1] * len(self.df_ver_con_elements)

        # For df_brace_elements
        ele_nodes["i_node"] += self.df_brace_elements["i_node"].tolist()
        ele_nodes["j_node"] += self.df_brace_elements["j_node"].tolist()
        ele_nodes["mid_node"] += [-1] * len(self.df_brace_elements)

        # For df_floor_beam_elements
        ele_nodes["i_node"] += self.df_floor_beam_elements["i_node"].tolist()
        ele_nodes["j_node"] += self.df_floor_beam_elements["j_node"].tolist()
        ele_nodes["mid_node"] += [-1] * len(self.df_floor_beam_elements)

        # For df_ceiling_beam_elements
        ele_nodes["i_node"] += self.df_ceiling_beam_elements["i_node"].tolist()
        ele_nodes["j_node"] += self.df_ceiling_beam_elements["j_node"].tolist()
        ele_nodes["mid_node"] += self.df_ceiling_beam_elements["mid_node"].tolist()

        # For df_hor_con_elements
        ele_nodes["i_node"] += self.df_hor_con_elements_filtered["i_node"].tolist()
        ele_nodes["j_node"] += self.df_hor_con_elements_filtered["j_node"].tolist()
        ele_nodes["mid_node"] += [-1] * len(self.df_hor_con_elements_filtered)

        self.df_partition = pd.DataFrame(ele_nodes)

        if self.nprocs_analyze > 1:
            connectivity = self.df_partition[["i_node", "j_node"]].values.tolist()

            options = pymetis.Options()
            options.niter, options.ufactor, options.ncuts = niter, ufactor, ncuts
            _, epart, _ = pymetis.part_mesh(
                self.nprocs_analyze,
                connectivity,
                gtype=pymetis.GType.NODAL,
                options=options,
            )

            self.df_partition["pid"] = epart

            pid_mapping = self.df_partition.set_index(["i_node", "j_node"])[
                "pid"
            ].to_dict()

            dataframes = [
                self.df_column_elements,
                self.df_ver_con_elements,
                self.df_brace_elements,
                self.df_floor_beam_elements,
                self.df_ceiling_beam_elements,
                self.df_hor_con_elements_filtered,
            ]
            for df in dataframes:
                df["pid"] = list(
                    zip(
                        df["i_node"],
                        df["j_node"],
                    )
                )
                df["pid"] = df["pid"].map(pid_mapping)

            self.logger.info(
                f"Model has been partitioned into {self.nprocs_analyze} parts."
            )

        else:
            self.df_partition["pid"] = 0

            dataframes = [
                self.df_column_elements,
                self.df_ver_con_elements,
                self.df_brace_elements,
                self.df_floor_beam_elements,
                self.df_ceiling_beam_elements,
                self.df_hor_con_elements_filtered,
            ]
            for df in dataframes:
                df["pid"] = 0

            self.logger.info(
                f"Model has not been partitioned. The number of nprocs (provided = {self.nprocs_analyze}) must be greater than 1."
            )
        return None

    def print_module_load(self, **kwargs) -> None:
        """Prints the self-weight of the modules."""
        if self.methods_called["load"] is False:
            raise ValueError("Please run the load method first.")

        story = kwargs.get("story", None)
        module = kwargs.get("module", None)

        if story is None or module is None:
            raise ValueError("Please provide a story and module number.")

        df_sw_diaphragms = self.df_self_weight_diaphragms.loc[(story, module)]
        df_sw_elements = self.df_self_weight_elements.loc[(story, module)]

        for item in df_sw_diaphragms.items():
            if item[0].startswith("ceiling"):
                self.logger.info(
                    f"Ceiling ({item[0].split('_')[-1]}) weight at story {story} and module {module} is {item[1]:.2f} kN."
                )
            elif item[0].startswith("floor"):
                self.logger.info(
                    f"Floor ({item[0].split('_')[-1]}) weight at story {story} and module {module} is {item[1]:.2f} kN."
                )

        for item in df_sw_elements.items():
            if "column" in item[0]:
                self.logger.info(
                    f"Column self-weight at story {story} and module {module} is {item[1]:.2f} kN."
                )
            elif "floor_beam" in item[0]:
                self.logger.info(
                    f"Floor beam self-weight at story {story} and module {module} is {item[1]:.2f} kN."
                )
            elif "ceiling_beam" in item[0]:
                self.logger.info(
                    f"Ceiling beam self-weight at story {story} and module {module} is {item[1]:.2f} kN."
                )
            elif "brace" in item[0]:
                self.logger.info(
                    f"Brace self-weight at story {story} and module {module} is {item[1]:.2f} kN."
                )
            elif "ver_con" in item[0]:
                self.logger.info(
                    f"Vertical connection self-weight at story {story} and module {module} is {item[1]:.2f} kN."
                )
            elif "hor_con" in item[0]:
                self.logger.info(
                    f"Approximately horizontal connection (at {item[0].split('_')[-1]}) self-weight at story {story} and module {module} is {item[1]:.2f} kN."
                )

    def __module_self_weight(self, **kwargs) -> None:
        """Creates the module self-weight dataframe."""

        # Create a copy of the dataframes without the 'area' column
        df_ceiling_loads = self.df_ceiling_loads.drop(columns="area")
        df_floor_loads = self.df_floor_loads.drop(columns="area")

        # Add a prefix to each column name
        df_ceiling_loads.columns = "ceiling_" + df_ceiling_loads.columns
        df_floor_loads.columns = "floor_" + df_floor_loads.columns

        # Concatenate the dataframes along the columns axis
        self.df_self_weight_diaphragms = pd.concat(
            [df_ceiling_loads, df_floor_loads], axis=1
        )

        df_columns = self.df_column_elements[["story", "module", "self_weight"]].copy()
        df_columns = df_columns.groupby(["story", "module"]).sum()
        df_columns = df_columns.rename(columns={"self_weight": "column"})

        df_ver_cons = self.df_ver_con_elements[
            ["story", "module", "self_weight"]
        ].copy()
        df_ver_cons = df_ver_cons.groupby(["story", "module"]).sum()
        df_ver_cons = df_ver_cons.rename(columns={"self_weight": "ver_con"})

        df_floor_beams = self.df_floor_beam_elements[
            ["story", "module", "self_weight"]
        ].copy()
        df_floor_beams = df_floor_beams.groupby(["story", "module"]).sum()
        df_floor_beams = df_floor_beams.rename(columns={"self_weight": "floor_beam"})

        df_ceiling_beams = self.df_ceiling_beam_elements[
            ["story", "module", "self_weight"]
        ].copy()
        df_ceiling_beams = df_ceiling_beams.groupby(["story", "module"]).sum()
        df_ceiling_beams = df_ceiling_beams.rename(
            columns={"self_weight": "ceiling_beam"}
        )

        df_braces = self.df_brace_elements[["story", "module", "self_weight"]].copy()
        df_braces = df_braces.groupby(["story", "module"]).sum()
        df_braces = df_braces.rename(columns={"self_weight": "brace"})

        df_hor_cons = (
            self.df_hor_con_elements[
                ["story", "module_id", "self_weight_ceiling", "self_weight_floor"]
            ]
            .copy()
            .rename(columns={"module_id": "module"})
        )
        df_hor_cons = df_hor_cons.groupby(["story", "module"]).sum()
        df_hor_cons = df_hor_cons.rename(
            columns={
                "self_weight_ceiling": "hor_con_ceiling",
                "self_weight_floor": "hor_con_floor",
            }
        )

        self.df_self_weight_elements = (
            pd.concat(
                [
                    df_columns,
                    df_floor_beams,
                    df_ceiling_beams,
                    df_braces,
                    df_ver_cons,
                    df_hor_cons,
                ],
                axis=1,
            ).fillna(0)
            * constants.g
        )

        return None

    def __find_neighbors(self, threshold=None, search_key=None) -> dict:
        if threshold is None:
            raise ValueError("Please provide a threshold value.")
        else:
            threshold = threshold + 1e-6  # add a small value to avoid numerical errors

        # Create an empty dictionary to store the neighbor information
        neighbors = {}

        # Collect all points from all modules
        for story, submodules in self.modules.items():
            all_points = []
            for module_number, module in submodules.items():
                points = module[search_key]
                for i, point in enumerate(points):
                    all_points.append(((module_number, i), point))

            # Iterate over all points
            for i, (point_key, point) in enumerate(all_points):
                neighbors[(story, point_key)] = []
                # Iterate over all other points
                for j, (_, other_point) in enumerate(all_points):
                    if i != j:
                        # Calculate the Euclidean distance between the points
                        dist = distance.euclidean(point, other_point)
                        # If the distance is less than or equal to the threshold, the points are neighbors
                        if dist <= threshold:
                            neighbors[(story, point_key)].append(all_points[j][0])
        return neighbors

    def plot_neighbor(self, plot_kwargs={}, **kwargs) -> None:
        story = kwargs.get("story", None)
        module_number = kwargs.get("module", None)

        if module_number is None or story is None:
            raise ValueError(
                "Please provide a module number and story to plot the neighbors."
            )

        fig, ax = plt.subplots(figsize=plot_kwargs.get("figsize", (10, 6)))

        df_module = self.df_modules.loc[(story, module_number)]
        if df_module.empty:
            raise ValueError(
                f"Module {module_number} at story {story} could not be found."
            )

        # Iterate over all points in the module
        selected_modules = [module_number]
        colors = cm.get_cmap("tab20", 20).colors
        count_points = 0
        for i, point in enumerate(df_module["points"]):
            df_dummy = self.df_point_neighbors.query(f"ID == {module_number}")
            check = df_dummy["story"].apply(lambda x: story in x)
            df_dummy = df_dummy[check]
            neighbor_points = df_dummy["neighbors"].to_list()

            ax.scatter(
                point[0],
                point[1],
                marker="x",
                color="red",
                label="Module Points" if i == 0 else None,
            )
        neighbor_points = [item for sublist in neighbor_points for item in sublist]
        for neighbor_point in neighbor_points:
            neighbor_mod_num, neighbor_point_idx = neighbor_point
            df_module_neighbor = self.df_modules.loc[(story, neighbor_mod_num)]
            neighbor_point_coords = df_module_neighbor["points"][neighbor_point_idx]
            ax.scatter(
                neighbor_point_coords[0],
                neighbor_point_coords[1],
                marker="o",
                color=colors[count_points],
                label=f"Neighbor #{count_points+1}: M{neighbor_mod_num}-P{neighbor_point_idx}",
            )
            selected_modules.append(neighbor_mod_num)
            count_points += 1

        for i, item in enumerate(np.unique(selected_modules)):
            df_module = self.df_modules.loc[(story, item)]
            module_points = df_module["points"]
            module_corners = df_module["corners"]

            for j in range(len(module_points)):
                if j == len(module_points) - 1:
                    ax.plot(
                        [module_points[j][0], module_points[0][0]],
                        [module_points[j][1], module_points[0][1]],
                        color="green",
                        linestyle="-",
                        linewidth=1,
                    )
                else:
                    ax.plot(
                        [module_points[j][0], module_points[j + 1][0]],
                        [module_points[j][1], module_points[j + 1][1]],
                        color="green",
                        linestyle="-",
                        linewidth=1,
                        label=f"Module Perimeter" if i == 0 and j == 0 else None,
                    )

            # Add module number at the middle of the module
            mid_x = (module_corners[0][0] + module_corners[2][0]) / 2
            mid_y = (module_corners[0][1] + module_corners[2][1]) / 2
            ax.text(mid_x, mid_y, f"M{item}", ha="center", va="center")

        # Add a legend to the plot
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        ax.axis("equal")
        ax.set_xlabel("West-East (m)")
        ax.set_ylabel("South-North (m)")
        ax.set_title(f"Neighbors of M{module_number} for Story {story}", fontsize=12)
        fig.tight_layout()
        fig.show()

        return (fig, ax)

    def plot_module_3D(self, plot_kwargs={}, **kwargs) -> None:
        story = kwargs.get("story", None)
        module_number = kwargs.get("module", None)

        if module_number is None or story is None:
            raise ValueError(
                "Please provide a module number and story to plot the module."
            )

        if isinstance(module_number, int):
            modules_selected = [module_number]
        elif isinstance(module_number, list):
            modules_selected = module_number
            modules_selected.sort()
        else:
            raise ValueError(
                "Please provide a valid module number or list of module numbers."
            )

        if isinstance(story, int):
            stories_selected = [story]
        elif isinstance(story, list):
            stories_selected = story
            stories_selected.sort()
        else:
            raise ValueError("Please provide a valid story or list of stories.")

        fig, axs = plt.subplots(
            1,
            2,
            figsize=plot_kwargs.get("figsize", (10, 6)),
            subplot_kw={"projection": "3d"},
        )

        # Generate 20 colors using the tab20 colormap
        colors_array = cm.tab20(np.linspace(0, 1, 20))
        colors = iter(np.tile(colors_array, (10, 1)))

        for _story in stories_selected:
            for _module in modules_selected:
                df_height = self.df_height.loc[_story]
                df_module = self.df_modules.loc[(_story, _module)]
                if df_module.empty:
                    raise ValueError(
                        f"Module(s) {modules_selected} at story(s) {stories_selected} could not be found."
                    )

                points = df_module["points"]

                # Create lists to store the x, y, and z coordinates for each height
                coords = {
                    "base": {"x": [], "y": [], "z": []},
                    "ver_con": {"x": [], "y": [], "z": []},
                    "module": {"x": [], "y": [], "z": []},
                }

                for i, height in enumerate(["base", "ver_con", "module"]):
                    if i == 0:
                        i_color = next(colors)
                    for ii, point in enumerate(points):
                        # if ii == 0:
                        #     ii_color = next(colors)

                        coords[height]["x"].append(point[0])
                        coords[height]["y"].append(point[1])
                        coords[height]["z"].append(
                            df_height[height]
                            if height == "base"
                            else df_height[height] + df_height["base"]
                        )

                        axs[0].scatter(
                            point[0],
                            point[1],
                            coords[height]["z"][-1],
                            s=10,
                            marker="o",
                            color=i_color,
                            label=f"Points - M{_module}-S{_story}"
                            if (i == 0 and ii == 0)
                            else None,
                        )

                    # Append the first point to the end of the lists
                    coords[height]["x"].append(coords[height]["x"][0])
                    coords[height]["y"].append(coords[height]["y"][0])
                    coords[height]["z"].append(coords[height]["z"][0])

                    # Draw lines between the points
                    if height != "base":
                        axs[0].plot(
                            coords[height]["x"],
                            coords[height]["y"],
                            coords[height]["z"],
                            color=next(colors),
                            label=f"Ceiling Beams - M{_module}-S{_story}"
                            if height == "ver_con"
                            else f"Floor Beams - M{_module}-S{_story}",
                        )

                # Draw vertical lines between the corresponding points in each height
                for i in range(len(points)):
                    if i == 0:
                        color = next(colors)

                    axs[0].plot(
                        [
                            coords["base"]["x"][i],
                            coords["ver_con"]["x"][i],
                            coords["module"]["x"][i],
                        ],
                        [
                            coords["base"]["y"][i],
                            coords["ver_con"]["y"][i],
                            coords["module"]["y"][i],
                        ],
                        [
                            coords["base"]["z"][i],
                            coords["ver_con"]["z"][i],
                            coords["module"]["z"][i],
                        ],
                        color=color,
                        label=f"Columns - M{_module}-S{_story}" if i == 0 else None,
                    )

                if df_module["brace_positions"]:
                    brace_positions = df_module["brace_positions"]
                    for key, value in brace_positions.items():
                        if key[1] == "Chevron":
                            color = next(colors)
                            axs[0].plot(
                                [value["global"][0][0], value["global"][1][0]],
                                [value["global"][0][1], value["global"][1][1]],
                                [
                                    df_height["base"] + df_height["ver_con"],
                                    df_height["base"] + df_height["module"],
                                ],
                                color=color,
                                label=f"Chevron Braces - M{_module}-S{_story}",
                            )
                            axs[0].plot(
                                [value["global"][1][0], value["global"][2][0]],
                                [value["global"][1][1], value["global"][2][1]],
                                [
                                    df_height["base"] + df_height["module"],
                                    df_height["base"] + df_height["ver_con"],
                                ],
                                color=color,
                            )
                            axs[0].scatter(
                                value["global"][1][0],
                                value["global"][1][1],
                                df_height["base"] + df_height["module"],
                                s=10,
                                marker="o",
                                color=i_color,
                            )
                        elif key[1] == "X":
                            color = next(colors)
                            axs[0].plot(
                                [value["global"][0][0], value["global"][1][0]],
                                [value["global"][0][1], value["global"][1][1]],
                                [
                                    df_height["base"] + df_height["ver_con"],
                                    df_height["base"] + df_height["module"],
                                ],
                                color=color,
                                label=f"X Braces - M{_module}-S{_story}",
                            )
                            axs[0].plot(
                                [value["global"][0][0], value["global"][1][0]],
                                [value["global"][0][1], value["global"][1][1]],
                                [
                                    df_height["base"] + df_height["module"],
                                    df_height["base"] + df_height["ver_con"],
                                ],
                                color=color,
                            )

        column_elements = self.df_column_elements.query(
            f"module == {modules_selected[0]} & story == {stories_selected[0]}"
        )
        ceiling_elements = self.df_ceiling_beam_elements.query(
            f"module == {modules_selected[0]} & story == {stories_selected[0]}"
        )
        floor_elements = self.df_floor_beam_elements.query(
            f"module == {modules_selected[0]} & story == {stories_selected[0]}"
        )
        brace_elements = self.df_brace_elements.query(
            f"module == {modules_selected[0]} & story == {stories_selected[0]}"
        )

        df1 = column_elements[["section", "point", "multi"]].rename(
            columns={"section": "Columns", "point": "Location", "multi": "Multiple"}
        )
        df1["Location"] = df1["Location"].apply(
            lambda x: x.upper() if len(x) == 2 else x.capitalize()
        )
        df1["Multiple"] = df1["Multiple"].fillna(0).astype(int)
        if (df1["Multiple"] == 0).all():
            df1 = df1.drop(columns="Multiple")
        else:
            df1["Multiple"] = df1["Multiple"].replace(0, "N/A")

        df2 = (
            ceiling_elements[["section", "side", "braced"]]
            .rename(columns={"section": "Ceiling Beams"})
            .merge(
                floor_elements[["section", "side", "braced"]].rename(
                    columns={"section": "Floor Beams"}
                ),
                on=["side", "braced"],
                how="left",
            )
            .drop(columns="braced")
            .merge(
                brace_elements[["section", "side"]]
                .drop_duplicates("side")
                .set_index("side")
                .rename(columns={"section": "Braces"}),
                on=["side"],
                how="left",
            )
            .fillna("N/A")
            .sort_index(axis=1)
            .rename(columns={"side": "Location"})
        )
        df2["Location"] = df2["Location"].str.capitalize()

        dead_ceiling = self.df_self_weight_diaphragms.loc[
            (stories_selected[0], modules_selected[0])
        ][["ceiling_dead"]].sum()
        dead_floor = self.df_self_weight_diaphragms.loc[
            (stories_selected[0], modules_selected[0])
        ][["floor_dead"]].sum()

        dead_member = self.df_self_weight_elements.loc[
            (stories_selected[0], modules_selected[0])
        ].sum()

        df3 = (
            pd.DataFrame(
                [
                    [
                        dead_ceiling,
                        dead_floor,
                        dead_member,
                        dead_ceiling + dead_floor + dead_member,
                    ]
                ],
                columns=["Ceiling", "Floor", "Member", "Total"],
            )
            .div(constants.g)
            .round(2)
        )
        df3.insert(0, "Unit", "Tons")

        cols = ["Location"] + [col for col in df1.columns.tolist() if col != "Location"]
        df1 = df1[cols]

        cols = ["Location"] + [col for col in df2.columns.tolist() if col != "Location"]
        df2 = df2[cols]

        axs[1].clear()

        # Turn off the axis
        axs[1].axis("off")

        table1 = axs[1].table(
            cellText=df1.values.tolist(),
            colLabels=df1.columns.tolist(),
            cellLoc="center",
            loc="upper center",
            cellColours=None,
            colWidths=[0.2] * len(df1.columns),  # Adjust the width of the cells
        )
        table2 = axs[1].table(
            cellText=df2.values.tolist(),
            colLabels=df2.columns.tolist(),
            cellLoc="center",
            loc="lower center",
            cellColours=None,
            colWidths=[0.2] * len(df2.columns),  # Adjust the width of the cells
        )
        table3 = axs[1].table(
            cellText=df3.values.tolist(),
            colLabels=df3.columns.tolist(),
            cellLoc="center",
            loc="center",
            cellColours=None,
            colWidths=[0.2] * len(df3.columns),  # Adjust the width of the cells
        )

        axs[1].set_title(
            f"Self-Weight and Section Props of Module {modules_selected[0]} at Story {stories_selected[0]}",
        )

        plt.subplots_adjust(bottom=0.1, top=0.9)  # Adjust the subplot parameters

        # Adjust the font size
        table1.auto_set_font_size(False)
        table1.set_fontsize(10)

        # Adjust the cell padding
        table1.auto_set_column_width(col=list(range(len(df1.columns))))
        table1.scale(1, 1.5)  # The second argument is the row height

        # Adjust the font size
        table2.auto_set_font_size(False)
        table2.set_fontsize(10)

        # Adjust the cell padding
        table2.auto_set_column_width(col=list(range(len(df2.columns))))
        table2.scale(1, 1.5)  # The second argument is the row height

        # Adjust the font size
        table3.auto_set_font_size(False)
        table3.set_fontsize(10)

        # Adjust the cell padding
        table3.auto_set_column_width(col=list(range(len(df3.columns))))
        table3.scale(1, 1.5)  # The second argument is the row height

        axs[0].set_xlabel("West-East (m)")
        axs[0].set_ylabel("South-North (m)")
        axs[0].set_zlabel("Elevation (m)")
        legend_kwargs = plot_kwargs.get("legend_kwargs", {})
        if legend_kwargs.get("show", True):
            axs[0].legend(
                loc=legend_kwargs.get("loc", "upper left"), bbox_to_anchor=(1, 1)
            )
        axs[0].view_init(
            azim=plot_kwargs.get("azim", -60), elev=plot_kwargs.get("elev", 30)
        )

        if len(modules_selected) == 1 and len(stories_selected) == 1:
            axs[0].set_title(
                f"Module {', '.join(map(str, modules_selected))} at Story {', '.join(map(str, stories_selected))}"
            )
        elif len(modules_selected) > 1 and len(stories_selected) == 1:
            axs[0].set_title(
                f"Modules {', '.join(map(str, modules_selected))} at Story {', '.join(map(str, stories_selected))}"
            )
        elif len(modules_selected) == 1 and len(stories_selected) > 1:
            axs[0].set_title(
                f"Module {', '.join(map(str, modules_selected))} at Stories {', '.join(map(str, stories_selected))}"
            )
        else:
            axs[0].set_title(
                f"Modules {', '.join(map(str, modules_selected))} at Stories {', '.join(map(str, stories_selected))}"
            )

        helper.set_axes_equal(axs[0])
        fig.tight_layout()
        plt.show()

        return (fig, axs)

    def print_module_section(self, **kwargs) -> None:
        story = kwargs.get("story", None)
        module = kwargs.get("module", None)

        if module is None or story is None:
            raise ValueError(
                "Please provide a module number and story to print the section information."
            )

        column_elements = self.df_column_elements.query(
            f"module == {module} & story == {story}"
        )
        ceiling_elements = self.df_ceiling_beam_elements.query(
            f"module == {module} & story == {story}"
        )
        floor_elements = self.df_floor_beam_elements.query(
            f"module == {module} & story == {story}"
        )
        brace_elements = self.df_brace_elements.query(
            f"module == {module} & story == {story}"
        )

        for row in column_elements.itertuples():
            if row.multi != False:
                self.logger.info(
                    f"Column located at {row.story} story and {row.point} point of module #{row.module} has a section of {row.section} and it has {row.multi} multiple columns.\n"
                )
            else:
                self.logger.info(
                    f"Column located at {row.story} story and {row.point} point of module #{row.module} has a section of {row.section}.\n"
                )
        for row in ceiling_elements.itertuples():
            self.logger.info(
                f"Ceiling beam located at {row.story} story and {row.side} side of module #{row.module} has a section of {row.section}.\n"
            )
        for row in floor_elements.itertuples():
            self.logger.info(
                f"Floor beam located at {row.story} story and {row.side} side of module #{row.module} has a section of {row.section}.\n"
            )
        for row in brace_elements.itertuples():
            self.logger.info(
                f"Brace located at {row.story} story and {row.side} side of module #{row.module} has a section of {row.section}.\n"
            )
        return None

    def show_diaphragm_master(self, **kwargs) -> None:
        """Shows the diaphragm master nodes."""

        story = kwargs.get("story", None)
        if story is None:
            raise ValueError("Please provide a story number.")

        plot_kwargs = kwargs.get("plot", {"show": True})

        df_module = self.df_modules.xs(story, level="story")
        df_diaphragm = self.df_diaphragms.xs(story, level="story")

        fig, ax = plt.subplots(figsize=plot_kwargs.get("figsize", (10, 6)))
        for i, module in enumerate(df_module.itertuples()):
            ax.set_title(f"Diaphragm Master Nodes for Story {story}")

            for ii, point in enumerate(module.points):
                ax.scatter(
                    point[0],
                    point[1],
                    s=10,
                    marker="o",
                    color="purple",
                    label="Module Points" if i == 0 and ii == 0 else None,
                )

                ax.plot(
                    [module.points[ii][0], module.points[ii - 1][0]],
                    [module.points[ii][1], module.points[ii - 1][1]],
                    color="green",
                    linestyle="-",
                    linewidth=1,
                    label="Module Perimeter" if i == 0 and ii == 0 else None,
                )

        for i, diaphragm in enumerate(df_diaphragm.itertuples()):
            if diaphragm.type == "floor":
                ax.scatter(
                    diaphragm.master_coord[0],
                    diaphragm.master_coord[1],
                    s=50,
                    marker="x",
                    color="blue",
                    label="Floor Master Nodes" if i == 0 or i == 1 else None,
                )
            elif diaphragm.type == "ceiling":
                ax.scatter(
                    diaphragm.master_coord[0],
                    diaphragm.master_coord[1],
                    s=50,
                    marker="s",
                    color="red",
                    alpha=0.5,
                    label="Ceiling Master Nodes" if i == 0 or i == 1 else None,
                )

        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        ax.set_xlabel("West-East (m)")
        ax.set_ylabel("South-North (m)")
        ax.axis("equal")
        ax.grid(True, alpha=0.5)
        fig.tight_layout()
        fig.show()

        return (fig, ax)

    def calculate_tributary_area(self, **kwargs) -> None:
        self.methods_called["calculate_tributary_area"] = True
        ceiling = kwargs.get("ceiling", True)
        floor = kwargs.get("floor", False)
        keep_brace_midpoints = kwargs.get("keep_brace_midpoints", False)
        plot_kwargs = kwargs.get("plot_kwargs", {})

        if not keep_brace_midpoints and not self.df_module_mid_nodes.empty:
            mask = (
                self.df_global_nodes[["X", "Y"]]
                .apply(tuple, 1)
                .isin(self.df_module_mid_nodes[["X", "Y"]].apply(tuple, 1))
            )
            df_global_nodes_filtered = self.df_global_nodes.copy()
            df_global_nodes_filtered = df_global_nodes_filtered[~mask]
        else:
            df_global_nodes_filtered = self.df_global_nodes.copy()

        x_min, x_max = (
            df_global_nodes_filtered.X.min(),
            df_global_nodes_filtered.X.max(),
        )
        y_min, y_max = (
            df_global_nodes_filtered.Y.min(),
            df_global_nodes_filtered.Y.max(),
        )
        z_min, z_max = (
            df_global_nodes_filtered.Z.min(),
            df_global_nodes_filtered.Z.max(),
        )

        surface1 = df_global_nodes_filtered[
            (df_global_nodes_filtered.Y < y_min + 1e-6)
            & (df_global_nodes_filtered.Y > y_min - 1e-6)
        ]
        surface2 = df_global_nodes_filtered[
            (df_global_nodes_filtered.X < x_min + 1e-6)
            & (df_global_nodes_filtered.X > x_min - 1e-6)
        ]
        surface3 = df_global_nodes_filtered[
            (df_global_nodes_filtered.Y < y_max + 1e-6)
            & (df_global_nodes_filtered.Y > y_max - 1e-6)
        ]
        surface4 = df_global_nodes_filtered[
            (df_global_nodes_filtered.X < x_max + 1e-6)
            & (df_global_nodes_filtered.X > x_max - 1e-6)
        ]

        if ceiling and not floor:
            filtered_values1 = surface1[
                surface1["node_old"].apply(lambda x: int(str(x)[:2]) % 2 == 1)
            ].sort_values(by=["X", "Z"])
            filtered_values2 = surface2[
                surface2["node_old"].apply(lambda x: int(str(x)[:2]) % 2 == 1)
            ].sort_values(by=["Y", "Z"])
            filtered_values3 = surface3[
                surface3["node_old"].apply(lambda x: int(str(x)[:2]) % 2 == 1)
            ].sort_values(by=["X", "Z"])
            filtered_values4 = surface4[
                surface4["node_old"].apply(lambda x: int(str(x)[:2]) % 2 == 1)
            ].sort_values(by=["Y", "Z"])

        elif not ceiling and floor:
            filtered_values1 = surface1[
                surface1["node_old"].apply(lambda x: int(str(x)[:2]) % 2 == 0)
            ].sort_values(by=["X", "Z"])
            filtered_values2 = surface2[
                surface2["node_old"].apply(lambda x: int(str(x)[:2]) % 2 == 0)
            ].sort_values(by=["Y", "Z"])
            filtered_values3 = surface3[
                surface3["node_old"].apply(lambda x: int(str(x)[:2]) % 2 == 0)
            ].sort_values(by=["X", "Z"])
            filtered_values4 = surface4[
                surface4["node_old"].apply(lambda x: int(str(x)[:2]) % 2 == 0)
            ].sort_values(by=["Y", "Z"])

        elif ceiling and floor:
            filtered_values1 = surface1.sort_values(by=["X", "Z"])
            filtered_values2 = surface2.sort_values(by=["Y", "Z"])
            filtered_values3 = surface3.sort_values(by=["X", "Z"])
            filtered_values4 = surface4.sort_values(by=["Y", "Z"])

        else:
            raise ValueError(f"Please provide either {ceiling = } or {floor = }.")

        filtered_values1 = self.__compute_areas(
            filtered_values1, "X", "Z", plot_kwargs=plot_kwargs
        )
        filtered_values2 = self.__compute_areas(
            filtered_values2, "Y", "Z", plot_kwargs=plot_kwargs
        )
        filtered_values3 = self.__compute_areas(
            filtered_values3, "X", "Z", plot_kwargs=plot_kwargs
        )
        filtered_values4 = self.__compute_areas(
            filtered_values4, "Y", "Z", plot_kwargs=plot_kwargs
        )

        return None

    def __compute_areas(self, df, x_col, y_col, **kwargs):
        plot_kwargs = kwargs.get("plot_kwargs", {})
        # Generate the x and y coordinates
        x = df[x_col].unique()
        y = df[y_col].unique()

        num_points_x = len(x)
        num_points_y = len(y)

        x_min, x_max = (
            self.df_global_nodes[x_col].min(),
            self.df_global_nodes[x_col].max(),
        )
        y_min, y_max = (
            self.df_global_nodes[y_col].min(),
            self.df_global_nodes[y_col].max(),
        )

        # Create a rectangular grid
        xx, yy = np.meshgrid(x, y)

        # Flatten the grid coordinates and stack them into a (N, 2) array
        points = np.vstack([xx.ravel(), yy.ravel()]).T

        # Add a frame of points around the area of interest
        extend_frame = np.maximum(x_max, y_max)
        frame_points = np.vstack(
            [
                np.vstack(
                    [
                        np.linspace(
                            -extend_frame - x_min,
                            extend_frame + x_max,
                            4 * num_points_x,
                        ),
                        np.full(4 * num_points_x, -extend_frame - y_min),
                    ]
                ).T,
                np.vstack(
                    [
                        np.linspace(
                            -extend_frame - x_min,
                            extend_frame + x_max,
                            4 * num_points_x,
                        ),
                        np.full(4 * num_points_x, extend_frame + y_max),
                    ]
                ).T,
                np.vstack(
                    [
                        np.full(4 * num_points_y, -extend_frame - x_min),
                        np.linspace(
                            -extend_frame - y_min,
                            extend_frame + y_max,
                            4 * num_points_y,
                        ),
                    ]
                ).T,
                np.vstack(
                    [
                        np.full(4 * num_points_y, extend_frame + x_max),
                        np.linspace(
                            -extend_frame - y_min,
                            extend_frame + y_max,
                            4 * num_points_y,
                        ),
                    ]
                ).T,
            ]
        )

        points = np.vstack([points, frame_points])

        # Compute Voronoi tesselation
        vor = Voronoi(points)

        # Create a polygon for the area of interest
        area_of_interest = box(x_min, y_min, x_max, y_max)

        # Compute Voronoi polygons and intersect with area of interest
        polygons = []
        initial_points = []  # List to store the initial points of each polygon
        for i, region_index in enumerate(vor.point_region):
            region = vor.regions[region_index]
            if not -1 in region and len(region) > 0:
                polygon = Polygon([vor.vertices[i] for i in region])
                polygons.append(polygon.intersection(area_of_interest))
                initial_points.append(
                    vor.points[i]
                )  # Store the initial point of the polygon

        # Compute areas
        areas = [polygon.area for polygon in polygons if polygon.is_valid]

        df_areas = pd.DataFrame(initial_points, columns=[x_col, y_col])

        # Assuming areas is a list of area values
        df_areas["area"] = areas

        df = df.merge(df_areas, on=[x_col, y_col])

        self.logger.info(f"Total area calculated: {df.area.sum():.2f} m^2")
        self.logger.info(
            f"Total surface area: {(x_max - x_min) * (y_max - y_min):.2f} m^2"
        )

        if plot_kwargs.get("show", False):
            # Create figure and axes
            fig, ax = plt.subplots(figsize=plot_kwargs.get("figsize", (10, 10)))

            # Create a collection of matplotlib patches from the shapely polygons
            patches = [
                mpl_polygon(np.array(polygon.exterior.coords), closed=True)
                for polygon in polygons
                if polygon.is_valid and not polygon.is_empty
            ]

            # Create a colormap
            cmap = mpl.colormaps["viridis"]

            # Normalize to the range of areas
            norm = plt.Normalize(min(areas), max(areas))

            # Map areas to colors
            colors = cmap(norm(areas))

            # Create a patch collection with a specified color map
            p = PatchCollection(
                patches, facecolor=colors, edgecolor="k", linewidths=1, alpha=0.4
            )
            x_coords, y_coords = zip(*initial_points)

            # # Create a scatter plot of the points
            ax.scatter(x_coords, y_coords)

            # Add the collection to the axes
            ax.add_collection(p)

            # Add a colorbar that represents the colormap
            cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
            cbar.set_label("$Area\ (m^2)$", rotation=270, labelpad=15)

            # Set the limits of the plot to the limits of the area of interest
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)
            if x_col == "X":
                ax.set_xlabel("West-East (m)")
            else:
                ax.set_xlabel("South-North (m)")

            ax.set_ylabel("Elevation (m)")
            ax.set_title(
                f"Tributary Area for {x_col} = {x_min:.2f} to {x_max:.2f} and {y_col} = {y_min:.2f} to {y_max:.2f}"
            )

        return df

    def __plot_module_2D(
        self,
        plotting,
    ) -> list:
        figs_axs = []
        for story, submodules in self.modules.items():
            fig, ax = plt.subplots(figsize=plotting.get("figsize", (8, 8)))
            for i, (module_number, module) in enumerate(submodules.items()):
                for j in range(len(module["points"])):
                    if j == len(module["points"]) - 1:
                        ax.plot(
                            [module["points"][j][0], module["points"][0][0]],
                            [module["points"][j][1], module["points"][0][1]],
                            color="green",
                            linestyle="-",
                            linewidth=1,
                            label=f"Module Perimeter" if i == 0 and j == 0 else None,
                        )
                    else:
                        ax.plot(
                            [module["points"][j][0], module["points"][j + 1][0]],
                            [module["points"][j][1], module["points"][j + 1][1]],
                            color="green",
                            linestyle="-",
                            linewidth=1,
                            label=f"Module Perimeter" if i == 0 and j == 0 else None,
                        )

                # Add module number at the middle of the module
                mid_x = (module["corners"][0][0] + module["corners"][2][0]) / 2
                mid_y = (module["corners"][0][1] + module["corners"][2][1]) / 2
                ax.text(mid_x, mid_y, f"M{module_number}", ha="center", va="center")

            chevron_counter = 0
            other_counter = 0

            for module_number, module in submodules.items():
                if module.get("brace_positions"):
                    for _key, _values in module["brace_positions"].items():
                        _, type_brace = _key
                        global_coords = _values["global"]
                        if (
                            type_brace == "Chevron"
                            or type_brace == "chevron"
                            or type_brace == "V"
                            or type_brace == "v"
                        ):
                            (
                                (global_start_x, global_start_y),
                                (global_middle_x, global_middle_y),
                                (global_end_x, global_end_y),
                            ) = global_coords
                            ax.plot(
                                [global_start_x, global_middle_x, global_end_x],
                                [global_start_y, global_middle_y, global_end_y],
                                color="red",
                                linestyle="-",
                                linewidth=2,
                                label=f"{type_brace} Braces"
                                if chevron_counter == 0
                                else None,
                            )
                            chevron_counter += 1
                        elif type_brace == "X" or type_brace == "x":
                            (
                                (global_start_x, global_start_y),
                                (global_end_x, global_end_y),
                            ) = global_coords
                            ax.plot(
                                [global_start_x, global_end_x],
                                [global_start_y, global_end_y],
                                color="blue",
                                linestyle="-",
                                linewidth=2,
                                label=f"{type_brace} Braces"
                                if other_counter == 0
                                else None,
                            )
                            other_counter += 1
                        else:
                            raise ValueError(
                                f"Please provide a valid brace type. {type_brace} is not valid."
                            )

            save_xy = []
            for i, (module_number, module) in enumerate(submodules.items()):
                for ii, (x, y) in enumerate(module["points"]):
                    save_xy.append((round(x, 6), round(y, 6)))
                    ax.plot(
                        x,
                        y,
                        "o",
                        color="purple",
                        markersize=3,
                        label=f"Module Points" if i == 0 and ii == 0 else None,
                    )

            ax.set_title(f"Layout for Story {story}")
            ax.set_xlabel("West-East (m)")
            ax.set_ylabel("South-North (m)")
            ax.axis("equal")
            save_x = np.unique(np.array(save_xy)[:, 0])
            save_y = np.unique(np.array(save_xy)[:, 1])
            ax.set_xticks(np.r_[save_x[::2], save_x[-1]])
            ax.set_yticks(np.r_[save_y[::2], save_y[-1]])
            ax.grid(True, alpha=0.5)
            ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
            fig.tight_layout()
            figs_axs.append([fig, ax])

        return figs_axs

    def __plot_elevation_2D(self, total_height, plotting) -> tuple:
        self.logger.info("Plotting the building height...")

        # Get the stories, base heights, clearances, and vertical connection heights
        stories = list(self.building_height.keys())
        base_heights = [data["base"] for data in self.building_height.values()]
        clearances = [data["clearance"] for data in self.building_height.values()]
        vert_cons = [data["ver_con"] for data in self.building_height.values()]

        # plt.figure(figsize=))
        fig, ax = plt.subplots(figsize=plotting.get("figsize", (3, 10)))

        for i, (key, value) in enumerate(self.building_height.items()):
            if i == 0:
                ax.plot(
                    [0, 0],
                    [
                        value["base"],
                        value["base"] + value["ver_con"],
                    ],
                    color=plotting.get("color1", "blue"),
                    linewidth=plotting.get("linewidth1", 5),
                    label="Vertical Connection" if i == 0 else None,
                )
                ax.plot(
                    [0, 0],
                    [
                        value["base"] + value["ver_con"],
                        value["base"] + value["module"],
                    ],
                    color=plotting.get("color2", "orange"),
                    linewidth=plotting.get("linewidth2", 5),
                    label="Clearance" if i == 0 else None,
                )
            else:
                ax.plot(
                    [0, 0],
                    [
                        value["base"],
                        value["base"] + value["ver_con"],
                    ],
                    color=plotting.get("color1", "blue"),
                    linewidth=plotting.get("linewidth1", 5),
                )
                ax.plot(
                    [0, 0],
                    [
                        value["base"] + value["ver_con"],
                        value["base"] + value["module"],
                    ],
                    color=plotting.get("color2", "orange"),
                    linewidth=plotting.get("linewidth2", 5),
                )

        ax.set_ylabel("Elevation (m)")
        ax.set_title(f"Building Height = {total_height:.2f} m")
        ax.set_xticks([0.0])
        ax.set_yticks([*base_heights, total_height])
        ytick_labels = ["{:.2f}".format(tick) for tick in plt.gca().get_yticks()]

        # Set the y-tick labels
        ax.set_yticklabels(ytick_labels)

        # Calculate the heights for the center of the clearances
        center_clearances = [
            base + (vert_con + clearance) / 2
            for base, vert_con, clearance in zip(base_heights, vert_cons, clearances)
        ]

        # Add story labels to the right of the y-axis ticks
        for i in range(len(stories)):
            ax.text(
                0.01,
                center_clearances[i],
                f"Story {stories[i]}",
                horizontalalignment="left",
                verticalalignment="center",
            )

        ax.grid(True, alpha=0.5)
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

        return (fig, ax)

    @functools.lru_cache(maxsize=None, typed=False)
    def __get_section_props(self, section_name) -> dict:
        """Return the section properties of a given section.

        Parameters
        ----------
        section_name : str
            The name of the section whose properties are desired.

        Returns
        -------
        dict
            Dictionary of the section properties.
        """
        if section_name.startswith("W"):
            try:
                return self.df_steel_W.loc[section_name].to_dict()
            except KeyError:
                raise ValueError(
                    f"Please provide a valid section name. {section_name} is not valid."
                )
        elif section_name.startswith("HS"):
            try:
                return self.df_steel_HSS.loc[section_name].to_dict()
            except KeyError:
                raise ValueError(
                    f"Please provide a valid section name. {section_name} is not valid."
                )
        else:
            raise ValueError(
                f"Please provide a valid section name. {section_name} is not valid."
            )


class _Material(object):
    """
    This class contains the material properties for steel column, beam, brace, and plate.

    .. caution::
        This class is not meant to be used directly. Please use the ``get_material()`` method of :class:`Model` class to call methods and attributes.

    .. note::
        * All units are in the SI system.
        * Please use kN, m, and kPa for force, length, and stress, respectively.

    Attributes of _Material class are:

    Attributes:

        steel_column (dict):
            Dictionary of the steel column material properties.
            Default values are:

            - ``Fy``: 350e3
            - ``YoungModulus``: 2e8
            - ``ShearModulus``: 77e6
            - ``McMy``: 1.05
            - ``Lambda_UQ``: 0.0
            - ``ThetaP_UQ``: 0.0
            - ``ThetaPc_UQ``: 0.0
            - ``R0``: 20
            - ``cR1``: 0.925
            - ``cR2``: 0.15
            - ``b``: 0.10
            - ``a2``: 1.0
            - ``a1``: 1.0 * (350e3 / 2e8)
            - ``a4``: 1.0
            - ``a3``: 1.0 * (350e3 / 2e8)

        steel_beam (dict):
            Dictionary of the steel beam material properties.
            Default values are:

            - ``Fy``: 345e3
            - ``YoungModulus``: 2e8
            - ``ShearModulus``: 77e6
            - ``McMy``: 1.11
            - ``Lambda_UQ``: 0.0
            - ``ThetaP_UQ``: 0.0
            - ``ThetaPc_UQ``: 0.0

        steel_brace (dict):
            Dictionary of the steel brace material properties.
            Default values are:

            - ``Fy``: 350e3
            - ``YoungModulus``: 2e8
            - ``ShearModulus``: 77e6
            - ``R0``: 20
            - ``cR1``: 0.925
            - ``cR2``: 0.15
            - ``b``: 0.01
            - ``a2``: 1.0
            - ``a1``: 1.0 * (350e3 / 2e8)
            - ``a4``: 1.0
            - ``a3``: 1.0 * (350e3 / 2e8)
            - ``imperfection``: 0.002
            - ``fatigue_E0``: 0.01

        steel_plate (dict):
            Dictionary of the steel plate material properties.
            Default values are:

            - ``Fy``: 200e3
            - ``YoungModulus``: 2e8
            - ``ShearModulus``: 77e6
            - ``McMy``: 1.05

    Examples:

        Here is an example of how to modify the material properties of the steel column:

        .. code-block:: python

            import modularbuildingpy as mbpy

            model = mbpy.Model(name="test", directory="/home/test")

            material = model.get_material()
            material.steel_column["Fy"] = 400e3
            material.steel_column["YoungModulus"] = 2.1e8

        .. warning::
            Make sure you modify these properties before you generate the model.

    """

    def __init__(self, **kwargs) -> None:
        self.steel_column = {
            "Fy": 350e3,
            "YoungModulus": 2e8,
            "ShearModulus": 77e6,
            "McMy": 1.05,
            "Lambda_UQ": 0.0,
            "ThetaP_UQ": 0.0,
            "ThetaPc_UQ": 0.0,
            "R0": 20,
            "cR1": 0.925,
            "cR2": 0.15,
            "b": 0.10,
            "a2": 1.0,
            "a1": 1.0 * (350e3 / 2e8),
            "a4": 1.0,
            "a3": 1.0 * (350e3 / 2e8),
        }
        self.steel_beam = {
            "Fy": 345e3,
            "YoungModulus": 2e8,
            "ShearModulus": 77e6,
            "McMy": 1.11,
            "Lambda_UQ": 0.0,
            "ThetaP_UQ": 0.0,
            "ThetaPc_UQ": 0.0,
        }
        self.steel_brace = {
            "Fy": 350e3,
            "YoungModulus": 2e8,
            "ShearModulus": 77e6,
            "R0": 20,
            "cR1": 0.925,
            "cR2": 0.15,
            "b": 0.01,
            "a2": 1.0,
            "a1": 1.0 * (350e3 / 2e8),
            "a4": 1.0,
            "a3": 1.0 * (350e3 / 2e8),
            "imperfection": 0.002,
            "fatigue_E0": 0.01,
        }
        self.steel_plate = {
            "Fy": 200e3,
            "YoungModulus": 2e8,
            "ShearModulus": 77e6,
            "McMy": 1.05,
        }
        return None


# Class for logging
class _Logger(object):
    def __init__(self, directory, **kwargs):
        log_console = kwargs.get("console", "INFO").upper()
        log_file = kwargs.get("file", "DEBUG").upper()
        mode = kwargs.get("mode", "a").lower()

        if mode not in ["a", "w"]:
            raise ValueError(f"Please provide a valid mode. Options are: a, w.")

        if directory is not None:
            directory = f"{directory}/logs"
            if not os.path.exists(directory):
                os.makedirs(directory)
        else:
            raise ValueError(f"Please provide a path to read files.")

        self.directory = directory
        self.logger_name = kwargs.get("name", "ModularBuildingPy")
        self.logger_filename = kwargs.get("filename", "mbp_serial_0")
        self.logger = logging.getLogger(self.logger_name)
        while self.logger.hasHandlers():
            self.logger.removeHandler(self.logger.handlers[0])
        logging.Logger.manager.loggerDict.pop(self.logger_name)

        # Create a custom logger
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.DEBUG)

        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(
            f"{self.directory}/{self.logger_filename}.log", mode=mode
        )

        if log_console == "DEBUG":
            c_handler.setLevel(logging.DEBUG)
        elif log_console == "INFO":
            c_handler.setLevel(logging.INFO)
        elif log_console == "WARNING":
            c_handler.setLevel(logging.WARNING)
        elif log_console == "ERROR":
            c_handler.setLevel(logging.ERROR)
        elif log_console == "CRITICAL":
            c_handler.setLevel(logging.CRITICAL)
        else:
            raise ValueError(
                f"Please provide a valid log_console. Options are: DEBUG, INFO, WARNING, ERROR, CRITICAL."
            )

        if log_file == "DEBUG":
            f_handler.setLevel(logging.DEBUG)
        elif log_file == "INFO":
            f_handler.setLevel(logging.INFO)
        elif log_file == "WARNING":
            f_handler.setLevel(logging.WARNING)
        elif log_file == "ERROR":
            f_handler.setLevel(logging.ERROR)
        elif log_file == "CRITICAL":
            f_handler.setLevel(logging.CRITICAL)
        else:
            raise ValueError(
                f"Please provide a valid log_file. Options are: DEBUG, INFO, WARNING, ERROR, CRITICAL."
            )

        # Create formatters and add it to handlers
        c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        f_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        self.logger.addHandler(c_handler)
        self.logger.addHandler(f_handler)

        self.logger.debug(f"Logger has been initialized.")

    def get(self):
        return self.logger

    def get_file(self):
        return f"{self.directory}/{self.logger_name.lower()}.log"


class _CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, pd.DataFrame):
            return obj.values.tolist()
        elif isinstance(obj, range):
            return list(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {str(key): self.default(value) for key, value in obj.items()}
        elif isinstance(obj, tuple):
            return str(obj)
        else:
            return super(_CustomEncoder, self).default(obj)
