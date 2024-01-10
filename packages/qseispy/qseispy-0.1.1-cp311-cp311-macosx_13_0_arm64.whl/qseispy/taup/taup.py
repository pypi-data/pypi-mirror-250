import numpy as np

from pathlib import Path
from obspy.taup import TauPyModel
from obspy.taup.taup_create import build_taup_model


def build_taup(model, output_folder="./.qseispy_cache", flag=True) -> None:
    # create output_folder
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    # write nd_model
    nd_model_path = Path(output_folder) / "model.nd"
    np.savetxt(nd_model_path, model)

    # add mantle, outer-core and inner-core boundary
    if model[-1, 0] < 2891:
        text = """mantle
 2891.00    13.71660   7.26466   5.56645     826.0     312.0
outer-core
 2891.00     8.06482   0.00000   9.90349   57822.0       0.0
 5149.50    10.35568   0.00000  12.16634   57822.0       0.0
inner-core
 5149.50    11.02827   3.50432  12.76360     445.0      85.0
 6371.00    11.26220   3.66780  13.08848     431.0      85.0
"""

        with open(nd_model_path, "a") as file:
            file.write("\n" + text)
    else:
        raise ValueError("only support model with depth < 2891 km (mantle boundary)")

    # build npz_model
    npz_model_path = Path(output_folder) / "model.npz"
    if not npz_model_path.exists():
        build_taup_model(
            str(nd_model_path.resolve()), output_folder=output_folder, verbose=flag
        )
    else:
        if flag:
            print(f"model.npz already exists in {output_folder}")


def taup(
    model_path,
    depth,
    distance,
    plot=False,
    plot_type="cartesian",  # 'spherical'  'cartesian'
):
    """
    Calculate travel time, ray parameter and incident angle.

    Parameters
    ----------
    model : str
        Path to the model file.
    depth : float
        Source depth in km.
    distance : float
        Source-receiver distance in km.

    Returns
    -------
    Ray_p : float
    """
    model = TauPyModel(model=model_path)

    time_p = model.get_travel_times(
        source_depth_in_km=depth,
        distance_in_degree=distance / 119.19,
        phase_list=["p", "P"],
    )
    time_s = model.get_travel_times(
        source_depth_in_km=depth,
        distance_in_degree=distance / 119.19,
        phase_list=["s", "S"],
    )

    ray_p = time_p[0].ray_param
    t_p = time_p[0].time
    angle_p = time_p[0].incident_angle

    ray_s = time_s[0].ray_param
    t_s = time_s[0].time
    angle_s = time_s[0].incident_angle

    if plot:
        path_p = model.get_ray_paths(
            source_depth_in_km=depth,
            distance_in_degree=distance / 111.19,
            phase_list=["p", "P", "s", "S"],
        )
        path_p[0].path.dtype
        path_p.plot_rays(plot_type=plot_type, legend=True)

    return ray_p, t_p, angle_p, ray_s, t_s, angle_s
