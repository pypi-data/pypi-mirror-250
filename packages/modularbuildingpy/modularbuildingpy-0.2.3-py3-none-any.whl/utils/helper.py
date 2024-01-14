"""
---------------------------------------------------------------------------------
Author: Mehmet Baris Batukan
Date: 2023-12-02
Description: This file contains the helper functions that are used in ModularBuildingPy.
---------------------------------------------------------------------------------
"""

import os, time, psutil, functools, subprocess, ctypes
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def log_time_memory(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process(os.getpid()).memory_info().rss

        result = func(self, *args, **kwargs)

        end_time = time.time()
        end_memory = psutil.Process(os.getpid()).memory_info().rss

        elapsed_time = end_time - start_time
        memory_usage = (end_memory - start_memory) / (
            1024 * 1024
        )  # Convert bytes to megabytes

        self.logger.debug(
            f"Method {func.__name__}: Elapsed time: {elapsed_time:.4f} sec"
        )
        self.logger.debug(
            f"Method {func.__name__}: Memory usage: {memory_usage:.2f} MB"
        )
        self.logger.debug(f"Total memory usage: {end_memory / (1024 * 1024):.2f} MB")

        return result

    return wrapper


def compile_cpp_code(directory, source_file, output_file) -> None:
    # Construct the full paths to the source file and the output file
    source_file_path = os.path.join(directory, source_file)
    output_file_path = os.path.join(directory, output_file)

    # Check if the output file already exists
    if os.path.exists(output_file_path):
        print(f"{output_file_path} already exists.")
        return

    # Load the Intel module
    command = ["/bin/bash", "-c", "module load intel/2020u4"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Error loading Intel module: {stderr.decode()}")
        return

    # Compile the C++ code
    command = ["icc", "-fPIC", "-shared", "-o", output_file_path, source_file_path]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Error compiling C++ code: {stderr.decode()}")
    else:
        pass

    return None


def save_list_to_file_py(directory, filename, given_list):
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, filename), "w") as f:
        for item in given_list:
            f.write("%s\n" % item)


def save_list_to_file_cpp(directory, filename, given_list) -> None:
    # Define the path to the shared library
    current_file_path = os.path.dirname(os.path.realpath(__file__))

    # Construct the lib_path relative to the current file path
    lib_path = os.path.join(current_file_path, "libs")

    input_file = "save_list_to_file.cpp"
    output_file = "save_list_to_file.so"

    # Check if the shared library exists
    if not os.path.exists(f"{lib_path}/{output_file}"):
        # If not, compile the C++ code into a shared library
        compile_cpp_code(lib_path, input_file, output_file)

    # Load the shared library
    lib = ctypes.CDLL(f"{lib_path}/{output_file}")

    # Define argument types and return type
    lib.save_list_to_file.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.POINTER(ctypes.c_char_p),
        ctypes.c_int,
    ]
    lib.save_list_to_file.restype = None

    # Convert directory and filename to bytes
    directory = directory.encode()
    filename = filename.encode()

    # Convert the given list to bytes
    byte_list = [item.encode() for item in given_list]
    list_size = len(byte_list)
    list_type = ctypes.c_char_p * list_size

    # Call the function
    lib.save_list_to_file(directory, filename, list_type(*byte_list), list_size)

    return None


def read_list_from_file(directory, filename):
    if not os.path.exists(os.path.join(directory, filename)):
        print(f"The file {filename} does not exist in the directory {directory}.")
        return
    with open(os.path.join(directory, filename), "r") as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def plot_nodes_3D(df, plot_kwargs) -> tuple:
    fig = plt.figure(figsize=plot_kwargs.get("figsize", (10, 10)))
    ax = fig.add_subplot(111, projection="3d")

    ax.scatter(
        df.X,
        df.Y,
        df.Z,
        s=plot_kwargs.get("s", 10),
        c="coral",
    )

    ax.set_xlabel("West-East (m)")
    ax.set_ylabel("South-North (m)")
    ax.set_zlabel("Elevation (m)")
    ax.azim, ax.elev = plot_kwargs.get("azim", -60), plot_kwargs.get("elev", 30)

    plt.title("Global Nodes (3D)")
    if plot_kwargs.get("equal_axes", False):
        set_axes_equal(ax)

    fig.tight_layout()
    return (fig, ax)


def plot_elements_3D(node_data, ele_data, plotting={}) -> tuple:
    # Create a dictionary mapping node tags to coordinates
    node_dict = {row[0]: row[1:] for row in node_data}

    # Create a 3D plot
    fig = plt.figure(figsize=plotting.get("figsize", (10, 10)))
    ax = fig.add_subplot(111, projection="3d")

    # Loop over the elements
    for ele in ele_data:
        # Get the coordinates for each node
        coords = [node_dict[node] for node in ele[1:]]
        # Unzip the coordinates
        x, y, z = zip(*coords)
        # Plot a line between the nodes
        ax.plot(x, y, z, color="coral")
        ax.scatter(x, y, z, s=plotting.get("s", 1), c="purple")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        ax.azim, ax.elev = plotting.get("azim", 30), plotting.get("elev", 30)

    plt.title("Global Elements (3D)")
    if plotting.get("equal_axes", False):
        set_axes_equal(ax)
    fig.tight_layout()
    return (fig, ax)


def check_horizontal_distance(df, spacing, search_key=None) -> pd.DataFrame:
    conditions = [
        df[f"{search_key}-spacing"] > spacing + 1e-6,
        df[f"{search_key}-spacing"] < spacing - 1e-6,
    ]
    results = []
    for condition in conditions:
        results.append(df[condition])

    return results


def set_axes_equal(ax) -> None:
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    plot_radius = 0.5 * max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])


@functools.lru_cache(maxsize=None)
def check_points_on_line(point1, point2, point3, point4) -> tuple:
    if point2[0] - point1[0] != 0:
        slope = (point2[1] - point1[1]) / (point2[0] - point1[0])
    else:
        slope = np.inf

    y_intercept = point1[1] - slope * point1[0] if slope != np.inf else 0

    on_line3 = (
        (point3[1] == slope * point3[0] + y_intercept)
        if slope != np.inf
        else point3[0] == point1[0]
    )
    on_line4 = (
        (point4[1] == slope * point4[0] + y_intercept)
        if slope != np.inf
        else point4[0] == point1[0]
    )

    return (on_line3, on_line4)


def convert_to_range(s):
    parts = list(map(int, s.split("-")))
    if len(parts) == 1:
        return range(parts[0], parts[0] + 1)
    elif len(parts) == 2:
        return range(parts[0], parts[1] + 1)


def poly_area(x, y):
    area = 0.0
    n = len(x)
    j = n - 1
    for i in range(n):
        area += (x[j] + x[i]) * (y[j] - y[i])
        j = i
    return abs(area / 2.0)


def map_list(mapping_dict, lst):
    try:
        return [mapping_dict[item] for item in lst]
    except KeyError as e:
        raise KeyError(f"Item {e.args[0]} not found in mapping dictionary")


def peer_to_2D_array(path) -> tuple:
    try:
        with open(path, "r") as f:
            content = f.readlines()
        counter = 0
        description, row, acc_data = "", "", []
        for x in content:
            if counter == 1:
                description = x
            elif counter == 3:
                row = x
                if row[0][0] == "N":
                    val = row.split()
                    npts = float(val[(val.index("NPTS=")) + 1].rstrip(","))
                    dt = float(val[(val.index("DT=")) + 1])
                else:
                    val = row.split()
                    npts = float(val[0])
                    dt = float(val[1])
            elif counter > 3:
                data = str(x).split()
                for value in data:
                    a = float(value)
                    acc_data.append(a)
                inp_acc = np.asarray([acc_data])
                time = []
                for i in range(0, len(acc_data)):
                    t = i * dt
                    time.append(t)
            counter = counter + 1

        return (description, np.concatenate((np.array([time]), inp_acc), axis=0).T)

    except IOError:
        raise IOError(f"File not found.")


def get_dir(direction):
    if direction in [1, 2, 3]:
        return direction

    elif isinstance(direction, str):
        dir_lower = direction.lower()
        if dir_lower in ["x", "we", "west-east"]:
            return 1
        elif dir_lower in ["y", "sn", "south-north"]:
            return 2
        elif dir_lower in ["z", "elevation", "down-up", "up-down"]:
            return 3
        else:
            raise ValueError(f"Please provide a valid direction.")

    else:
        raise ValueError(f"Please provide a valid direction.")
