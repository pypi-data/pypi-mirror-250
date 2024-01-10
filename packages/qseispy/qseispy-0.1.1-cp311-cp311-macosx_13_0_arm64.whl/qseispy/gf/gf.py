import sys
import shutil
import subprocess
import numpy as np

from tqdm import tqdm
from mpi4py import MPI
from joblib import Parallel, delayed
from pathlib import Path
from qseispy.taup.taup import taup
from qseispy.model.receiver import ReceiverModel

sys.path.append("/Users/yinfu/ohmyshake/shakecore")
from shakecore import Stream, Pool


def calculate_gf(
    config,
    receiver,
    source_depth,
    source_type="dc",
    taup_model_path=None,
    flag=True,
    jobs=1,
    cache_path="./.qseispy_cache",
    rm_cache=True,  # remove cache after calculation
):
    # check source_depth
    source_depth = [float(item) for item in source_depth]

    # check source type
    if source_type not in ["ep", "sf", "dc"]:
        raise ValueError(f"Unknown source type {source_type}.")

    # check rank
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    # create rank cache folder
    rank_path = Path(cache_path) / f"rank_{rank}"
    if rank_path.exists():
        shutil.rmtree(rank_path)
    rank_path.mkdir(parents=True, exist_ok=True)

    # initialize pbar
    task_num = len(source_depth) * len(receiver.depths)
    if flag:
        pbar = tqdm(range(0, task_num), desc=f"Calculating {task_num} tasks...")
    else:
        pbar = range(0, task_num)

    # serial processing
    if jobs == 1:
        for i in pbar:
            process_job(
                i,
                config=config,
                receiver=receiver,
                source_depth=source_depth,
                source_type=source_type,
                rank_path=rank_path,
            )
    # parallel processing
    elif jobs > 1:
        Parallel(n_jobs=jobs, backend="loky")(
            delayed(process_job)(
                i,
                config=config,
                receiver=receiver,
                source_depth=source_depth,
                source_type=source_type,
                rank_path=rank_path,
            )
            for i in pbar
        )
    else:
        raise ValueError(f"jobs={jobs} must be larger than 0.")

    # close pbar
    if flag:
        pbar.close()

    # return gfs, 1 station -> 1 stream, 1 source -> 1 pool, all source -> 1 list of pool
    gfs = []
    for i in range(len(source_depth)):
        streams = []
        for j in range(len(receiver.depths)):
            dir_path = (
                rank_path / f"ss_{source_depth[i]:.6f}km_rr_{receiver.depths[j]:.6f}km"
            )
            files = [file for file in dir_path.glob("*-2.t[rtz]") if file.is_file()]
            n_channel_num = len(files)
            n_receiver_num = len(receiver.distances[j])
            station = np.empty(n_receiver_num * n_channel_num, dtype="U2")  # ss_type
            channel = np.empty(n_receiver_num * n_channel_num, dtype="U1")  # component
            data = np.empty((n_receiver_num * n_channel_num, receiver.npts))
            for k in range(n_channel_num):
                data[n_receiver_num * k : n_receiver_num * (k + 1), :] = np.loadtxt(
                    files[k], skiprows=1
                )[:, 1:].T
                ss_type = files[k].name[:2]
                component = files[k].name[-1:]
                if ss_type == "cl":  # clvd correction
                    ss_type = "dd"
                    data[n_receiver_num * k : n_receiver_num * (k + 1), :] *= 2
                if ss_type == "ex":  # explosion correction
                    ss_type = "ep"
                station[n_receiver_num * k : n_receiver_num * (k + 1)] = ss_type
                channel[n_receiver_num * k : n_receiver_num * (k + 1)] = component

            # organize data into each station
            for s in range(n_receiver_num):
                index = np.arange(0, n_channel_num * n_receiver_num, n_receiver_num) + s
                data_s = data[index, :]
                network_s = n_channel_num * ["GF"]
                station_s = station[index].tolist()
                channel_s = channel[index].tolist()
                receiver_s = ReceiverModel(dt=receiver.dt, npts=receiver.npts)
                receiver_s.add(
                    distance=[receiver.distances[j][s]],
                    depth=receiver.depths[j],
                    unit=receiver.units[j],
                )
                # create stream
                header = {
                    "sampling_rate": 1 / float(receiver.dt),
                    "type": "velocity",
                    "network": network_s,
                    "station": station_s,
                    "channel": channel_s,
                    "notes": {
                        "source_depth": source_depth[i],
                        "source_type": source_type,
                        "receiver": receiver_s,
                    },
                }
                stream = Stream(data_s, header)
                stream.sort(keys=["network", "station", "channel"])
                # taup stream
                if taup_model_path is not None:
                    try:
                        ray_p, t_p, angle_p, ray_s, t_s, angle_s = taup(
                            taup_model_path,
                            source_depth[i],
                            receiver.distances[j][s],
                        )
                        stream.stats.notes["ray_p"] = ray_p
                        stream.stats.notes["t_p"] = t_p
                        stream.stats.notes["angle_p"] = angle_p
                        stream.stats.notes["ray_s"] = ray_s
                        stream.stats.notes["t_s"] = t_s
                        stream.stats.notes["angle_s"] = angle_s
                    except:
                        pass
                # append stream
                streams.append(stream)

        gfs.append(Pool(streams))

    # delete rank cache
    if rm_cache:
        shutil.rmtree(rank_path)

    return gfs


def process_job(
    i,
    config,
    receiver,
    source_depth,
    source_type,
    rank_path,
):
    # 1. initialize receiver
    receiver_distance = receiver.distances[i % len(receiver.depths)]
    receiver_depth = float(receiver.depths[i % len(receiver.depths)])
    receiver_unit = receiver.units[i % len(receiver.depths)]

    # 2. initialize source_depth
    source_depth_job = float(source_depth[i // len(receiver.depths)])

    # 3. output path
    output_path = rank_path / f"ss_{source_depth_job:.6f}km_rr_{receiver_depth:.6f}km"
    output_path.mkdir(parents=True, exist_ok=True)

    # 4. write input file
    write_input_file(
        config,
        receiver,
        receiver_distance,
        receiver_depth,
        receiver_unit,
        source_depth_job,
        source_type,
        output_path,
    )

    # 5. run qseis
    dir_path = Path(__file__).parent.parent
    Qseis06a = dir_path / "Qseis06a"
    if not Qseis06a.exists():
        raise FileNotFoundError(f"Qseis06a not found at {Qseis06a}.")

    try:
        cmd = subprocess.Popen(
            [Qseis06a],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=output_path,
        )
        stdout, stderr = cmd.communicate("input.txt\n".encode())
        if cmd.returncode != 0 or (
            len(stderr.decode()) > 0 and stderr.decode()[0:4] == "STOP"
        ):  # Qseis06a executed unsuccessfully
            print(f"Qseis06a returned an error with exit code {cmd.returncode}:\n")
            print(f"stderr: {stderr.decode()}")
            print(f"stdout: {stdout.decode()}")
            sys.exit(1)
    except subprocess.SubprocessError as e:
        print(f"Subprocess error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def write_input_file(
    config,
    receiver,
    receiver_distance,
    receiver_depth,
    receiver_unit,
    source_depth_job,
    source_type,
    output_path,
):
    # source
    source_depth = source_depth_job  # km

    # receiver
    sw_equidistant = 0  # 1/0 = equidistant/irregular
    if receiver_unit == "km":
        sw_distance_unit = 1  # 1/0 = km/deg
    elif receiver_unit == "deg":
        sw_distance_unit = 0
    else:
        raise ValueError(f"Unknown unit {receiver_unit}.")
    n_distances = len(receiver_distance)
    str_distances = " ".join(str(float(d)) for d in receiver_distance)
    time_start = 0.0  # sec
    time_window = receiver.npts * receiver.dt - receiver.dt  # sec
    nsamples = int(receiver.npts)
    sw_t_reduce = 1  # 1 = velocity [km/sec], 0 = slowness [sec/deg]
    time_reduction_velocity = 0.0  # align time window with first arrival

    # wavenumber integration
    if config.full_field is True:
        sw_algorithm = int(0)  # 0 = suggested for full wave-field modelling;
    else:
        sw_algorithm = int(
            2
        )  # 1 or 2 = suggested when using a slowness window with narrow taper range - a technique for suppressing space-domain aliasing
    str_slowness_window = " ".join(str(d) for d in config.slowness_window)
    wavenumber_integration_factor = float(config.wavenumber_integration_factor)
    aliasing_suppression_factor = float(config.aliasing_suppression_factor)

    # partial solutions
    if config.free_surface is True:
        filter_surface_effects = int(
            0
        )  # 0 = with free surface, i.e., do not select this filter
    else:
        filter_surface_effects = int(
            1
        )  # 1 = without free surface; 2 = without free surface but with correction on amplitude and wave form. Note switch 2 can only be used for receivers at the surface
    filter_shallow_paths = 1 if config.penetration_filter[0] is True else 0
    filter_shallow_paths_depth = float(config.penetration_filter[1])
    n_depth_ranges = len(config.phase_filter)
    if n_depth_ranges == 0:
        str_depth_ranges = "# "
    else:
        str_depth_ranges = ""
        for i in range(n_depth_ranges):
            upper = float(config.phase_filter[i][0])
            lower = float(config.phase_filter[i][1])
            if config.phase_filter[i][2] == "P_up":
                phase = 1
            elif config.phase_filter[i][2] == "P_down":
                phase = 2
            elif config.phase_filter[i][2] == "S_up":
                phase = 3
            elif config.phase_filter[i][2] == "S_down":
                phase = 4
            else:
                raise ValueError(f"Unknown phase {phase}.")

            if i < n_depth_ranges - 1:
                str_depth_ranges += f"{upper} {lower} {phase}\n"
            else:
                str_depth_ranges += f"{upper} {lower} {phase}"

    # source time function
    wavelet_duration_samples = float(2.0)
    wavelet_type = int(1)
    no_w_samples = "# "
    str_w_samples = "# "

    # instrument response
    str_constant_factor = (
        f"({float(receiver.constant_factor[0])},{float(receiver.constant_factor[1])})"
    )

    num_roots = len(receiver.root_positions)
    if num_roots == 0:
        str_root_positions = "# "
    else:
        str_root_positions = ""
        for i in range(num_roots):
            str_root_positions += f"({float(receiver.root_positions[i][0])},{float(receiver.root_positions[i][1])})"
            if i != num_roots - 1:
                str_root_positions += ", "

    num_poles = len(receiver.pole_positions)
    if num_poles == 0:
        str_pole_positions = "# "
    else:
        str_pole_positions = ""
        for i in range(num_poles):
            str_pole_positions += f"({float(receiver.pole_positions[i][0])},{float(receiver.pole_positions[i][1])})"
            if i != num_poles - 1:
                str_pole_positions += ", "

    # output files for Green's functions
    str_gf_filenames = "'ex-2'  'ss-2'  'ds-2'  'cl-2'  'fz-2'  'fh-2'"
    if source_type == "ep":
        str_gf_sw_source_types = "1  0  0  0  0  0"
    elif source_type == "sf":
        str_gf_sw_source_types = "0  0  0  0  1  1"
    elif source_type == "dc":
        str_gf_sw_source_types = "1  1  1  1  0  0"
    else:
        raise ValueError(f"Unknown source type {source_type}.")

    # output files for an arbitrary point dislocation source
    str_source = "0  0.0  0.0  0.0  0.0  0.0  0.0  'seis-2'"
    sw_irregular_azimuths = 0
    str_azimuths = "0.0"

    # global model parameters
    sw_flat_earth_transform = 1 if config.flattening is True else 0
    gradient_resolution_vp = float(config.vp_res)
    gradient_resolution_vs = float(config.vs_res)
    gradient_resolution_density = float(config.rho_res)

    # layered earth model
    if config.model is not None:
        n_model_lines = len(config.model)
        model_lines = ""
        for i in range(n_model_lines):
            if i < n_model_lines - 1:
                model_lines += f"{i+1}  {config.model[i][0]}  {config.model[i][1]}  {config.model[i][2]}  {config.model[i][3]}  {config.model[i][4]}  {config.model[i][5]}\n"
            else:
                model_lines += f"{i+1}  {config.model[i][0]}  {config.model[i][1]}  {config.model[i][2]}  {config.model[i][3]}  {config.model[i][4]}  {config.model[i][5]}"

        n_model_receiver_lines = 0
        model_receiver_lines = "1  0.000  2.900  1.676  2.600  92.00  41.00"
    elif (
        config.model is None
        and config.ss_model is not None
        and config.rr_model is not None
    ):
        n_model_lines = len(config.ss_model)
        model_lines = ""
        for i in range(n_model_lines):
            if i < n_model_lines - 1:
                model_lines += f"{i+1}  {config.ss_model[i][0]}  {config.ss_model[i][1]}  {config.ss_model[i][2]}  {config.ss_model[i][3]}  {config.ss_model[i][4]}  {config.ss_model[i][5]}\n"
            else:
                model_lines += f"{i+1}  {config.ss_model[i][0]}  {config.ss_model[i][1]}  {config.ss_model[i][2]}  {config.ss_model[i][3]}  {config.ss_model[i][4]}  {config.ss_model[i][5]}"

        n_model_receiver_lines = len(config.rr_model)
        model_receiver_lines = ""
        for i in range(n_model_receiver_lines):
            model_receiver_lines += f"{i+1}  {config.rr_model[i][0]}  {config.rr_model[i][1]}  {config.rr_model[i][2]}  {config.rr_model[i][3]}  {config.rr_model[i][4]}  {config.rr_model[i][5]}\n"
    else:
        raise ValueError("Model setting is wrong.")

    # TEMPLATE
    template = f"""# This is the input file of FORTRAN77 program "qseis06" for calculation of
# synthetic seismograms based on a layered halfspace earth model.
#
# by
# Rongjiang  Wang <wang@gfz-potsdam.de>
# GeoForschungsZentrum Potsdam
# Telegrafenberg, D-14473 Potsdam, Germany
#
# Last modified: Potsdam, Nov., 2006
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# If not specified, SI Unit System is used overall!
#
# Coordinate systems:
# cylindrical (z,r,t) with z = downward,
#                          r = from source outward,
#                          t = azmuth angle from north to east;
# cartesian (x,y,z) with   x = north,
#                          y = east,
#                          z = downward;
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
#	SOURCE PARAMETERS
#	=================
# 1. source depth [km]
#------------------------------------------------------------------------------
{source_depth}                    |dble: source_depth;
#------------------------------------------------------------------------------
#
#	RECEIVER PARAMETERS
#	===================
# 1. receiver depth [km]
# 2. switch for distance sampling role (1/0 = equidistant/irregular); switch
#    for unit used (1/0 = km/deg)
# 3. number of distance samples
# 4. if equidistant, then start and end trace distance (> 0); else distance
#    list (please order the receiver distances from small to large)
# 5. (reduced) time begin [sec] & length of time window [sec], number of time
#    samples (<= 2*nfmax in qsglobal.h)
# 6. switch for unit of the following time reduction parameter: 1 = velocity
#    [km/sec], 0 = slowness [sec/deg]; time reduction parameter
#------------------------------------------------------------------------------
{receiver_depth}                         |dble: receiver_depth;
{sw_equidistant}  {sw_distance_unit}   |int: sw_equidistant, sw_d_unit;
{n_distances}                            |int: no_distances;
{str_distances}                          |dble: d_1,d_n; or d_1,d_2, ...(no comments in between!);
{time_start} {time_window} {nsamples}  |dble: t_start,t_window; int: no_t_samples;
{sw_t_reduce} {time_reduction_velocity}  |int: sw_t_reduce; dble: t_reduce;
#------------------------------------------------------------------------------
#
#	WAVENUMBER INTEGRATION PARAMETERS
#	=================================
# 1. select slowness integration algorithm (0 = suggested for full wave-field
#    modelling; 1 or 2 = suggested when using a slowness window with narrow
#    taper range - a technique for suppressing space-domain aliasing);
# 2. 4 parameters for low and high slowness (Note 1) cut-offs [s/km] with
#    tapering: 0 < slw1 < slw2 defining cosine taper at the lower end, and 0 <
#    slw3 < slw4 defining the cosine taper at the higher end. default values
#    will be used in case of inconsistent input of the cut-offs (possibly with
#    much more computational effort);
# 3. parameter for sampling rate of the wavenumber integration (1 = sampled
#    with the spatial Nyquist frequency, 2 = sampled with twice higher than
#    the Nyquist, and so on: the larger this parameter, the smaller the space-
#    domain aliasing effect, but also the more computation effort);
# 4. the factor for suppressing time domain aliasing (> 0 and <= 1) (Note 2).
#------------------------------------------------------------------------------
{sw_algorithm}                   |int: sw_algorithm;
{str_slowness_window}             |dble: slw(1-4);
{wavenumber_integration_factor}             |dble: sample_rate;
{aliasing_suppression_factor}     |dble: supp_factor;%(str_source_disk_radius)s
#------------------------------------------------------------------------------
#
#	        OPTIONS FOR PARTIAL SOLUTIONS
#       (only applied to the source-site structure)
#	    ===========================================
#
# 1. switch for filtering free surface effects (0 = with free surface, i.e.,
#    do not select this filter; 1 = without free surface; 2 = without free
#    surface but with correction on amplitude and wave form. Note switch 2
#    can only be used for receivers at the surface)
# 2. switch for filtering waves with a shallow penetration depth (concerning
#    their whole trace from source to receiver), penetration depth limit [km]
#
#    if this option is selected, waves whose travel path never exceeds the
#    given depth limit will be filtered ("seismic nuting"). the condition for
#    selecting this filter is that the given shallow path depth limit should
#    be larger than both source and receiver depth.
#
# 3. number of depth ranges where the following selected up/down-sp2oing P or
#    SV waves should be filtered
# 4. the 1. depth range: upper and lower depth [km], switch for filtering P
#    or SV wave in this depth range:
#
#    switch no:              1      2        3       4         other
#    filtered phase:         P(up)  P(down)  SV(up)  SV(down)  Error
#
# 5. the 2. ...
#
#    The partial solution options are useful tools to increase the numerical
#    significance of desired wave phases. Especially when the desired phases
#    are smaller than the undesired phases, these options should be selected
#    and carefully combined.
#------------------------------------------------------------------------------
{filter_surface_effects}                  |int: isurf;
{filter_shallow_paths}   {filter_shallow_paths_depth}  |int: sw_path_filter; dble:shallow_depth_limit;
{n_depth_ranges} 
{str_depth_ranges}
#------------------------------------------------------------------------------
#
#	SOURCE TIME FUNCTION (WAVELET) PARAMETERS (Note 3)
#	==================================================
# 1. wavelet duration [unit = time sample rather than sec!], that is about
#    equal to the half-amplitude cut-off period of the wavelet (> 0. if <= 0,
#    then default value = 2 time samples will be used), and switch for the
#    wavelet form (0 = user's own wavelet; 1 = default wavelet: normalized
#    square half-sinusoid for simulating a physical delta impulse; 2 = tapered
#    Heaviside wavelet, i.e. integral of wavelet 1)
# 2. IF user's own wavelet is selected, then number of the wavelet time samples
#    (<= 1024), and followed by
# 3. equidistant wavelet time samples
# 4  ...(continue) (! no comment lines allowed between the time sample list!)
#    IF default, delete line 2, 3, 4 ... or comment them out!
#------------------------------------------------------------------------------
{wavelet_duration_samples} {wavelet_type} 
{no_w_samples}       |int: no_w_samples;
{str_w_samples}        |dble: w_samples;
# 100
#  0.000  0.063  0.127  0.189  0.251  0.312  0.372  0.430  0.486  0.541
#  0.593  0.643  0.690  0.735  0.776  0.815  0.850  0.881  0.910  0.934
#------------------------------------------------------------------------------
#
#	 FILTER PARAMETERS OF RECEIVERS (SEISMOMETERS OR HYDROPHONES)
#	 ============================================================
# 1. constant coefficient (normalization factor)
# 2. number of roots (<= nrootmax in qsglobal.h)
# 3. list of the root positions in the complex format (Re,Im). If no roots,
#    comment out this line
# 4. number of poles (<= npolemax in qsglobal.h)
# 5. list of the pole positions in the complex format (Re,Im). If no poles,
#    comment out this line
#------------------------------------------------------------------------------
{str_constant_factor}    |dble: constant_factor;
{num_roots}            |int: no_roots;
{str_root_positions}    |dble: root_positions; eg: (0.0, 0.0), (0.0, 0.0)
{num_poles}            |int: no_poles;
{str_pole_positions}    |dble: pole_positions; eg: (-4.35425, 4.44222), (-4.35425,-4.44222)
#------------------------------------------------------------------------------
#
#	OUTPUT FILES FOR GREEN'S FUNCTIONS (Note 4)
#	===========================================
# 1. selections of source types (yes/no = 1/0)
# 2. file names of Green's functions (please give the names without extensions,
#    which will be appended by the program automatically: *.tz, *.tr, *.tt
#    and *.tv are for the vertical, radial, tangential, and volume change (for
#    hydrophones) components, respectively)
#------------------------------------------------------------------------------
#  explosion   strike-slip dip-slip   clvd       single_f_v  single_f_h
#------------------------------------------------------------------------------
{str_gf_sw_source_types}
{str_gf_filenames}
#------------------------------------------------------------------------------
#	OUTPUT FILES FOR AN ARBITRARY POINT DISLOCATION SOURCE
#               (for applications to earthquakes)
#	======================================================
# 1. selection (0 = not selected; 1 or 2 = selected), if (selection = 1), then
#    the 6 moment tensor elements [N*m]: Mxx, Myy, Mzz, Mxy, Myz, Mzx (x is
#    northward, y is eastward and z is downard); else if (selection = 2), then
#    Mis [N*m] = isotropic moment part = (MT+MN+MP)/3, Mcl = CLVD moment part
#    = (2/3)(MT+MP-2*MN), Mdc = double-couple moment part = MT-MN, Strike [deg],
#    Dip [deg] and Rake [deg].
#
#    Note: to use this option, the Green's functions above should be computed
#          (selection = 1) if they do not exist already.
#
#                 north(x)
#                  /
#                 /\ strike
#                *----------------------->  east(y)
#                |\                       \
#                |-\                       \
#                |  \     fault plane       \
#                |90 \                       \
#                |-dip\                       \
#                |     \                       \
#                |      \                       \
#           downward(z)  \-----------------------\\
#
# 2. switch for azimuth distribution of the stations (0 = uniform azimuth,
#    else = irregular azimuth angles)
# 3. list of the azimuth angles [deg] for all stations given above (if the
#    uniform azimuth is selected, then only one azimuth angle is required)
#
#------------------------------------------------------------------------------
#     Mis        Mcl        Mdc        Strike     Dip        Rake      File
#------------------------------------------------------------------------------
#  2   0.00       1.00       6.0E+19    120.0      30.0       25.0      'seis'
#------------------------------------------------------------------------------
#     Mxx        Myy        Mzz        Mxy        Myz        Mzx       File
#------------------------------------------------------------------------------
{str_source}
{sw_irregular_azimuths}
{str_azimuths}
#------------------------------------------------------------------------------
#
#	GLOBAL MODEL PARAMETERS (Note 5)
#	================================
# 1. switch for flat-earth-transform
# 2. gradient resolution [%%] of vp, vs, and ro (density), if <= 0, then default
#    values (depending on wave length at cut-off frequency) will be used
#------------------------------------------------------------------------------
{sw_flat_earth_transform}     |int: sw_flat_earth_transform;
{gradient_resolution_vp} {gradient_resolution_vs} {gradient_resolution_density}   |dble: vp_res, vs_res, ro_res;
#------------------------------------------------------------------------------
#
#	                LAYERED EARTH MODEL
#       (SHALLOW SOURCE + UNIFORM DEEP SOURCE/RECEIVER STRUCTURE)
#	=========================================================
# 1. number of data lines of the layered model (source site)
#------------------------------------------------------------------------------
{n_model_lines}                  |int: no_model_lines;
#------------------------------------------------------------------------------
#
#	MULTILAYERED MODEL PARAMETERS (source site)
#	===========================================
# no  depth[km]  vp[km/s]  vs[km/s]  ro[g/cm^3] qp      qs
#------------------------------------------------------------------------------
{model_lines}
#------------------------------------------------------------------------------
#
#	          LAYERED EARTH MODEL
#       (ONLY THE SHALLOW RECEIVER STRUCTURE)
#       =====================================
# 1. number of data lines of the layered model
#
#    Note: if the number = 0, then the receiver site is the same as the
#          source site, else different receiver-site structure is considered.
#          please be sure that the lowest interface of the receiver-site
#          structure given given below can be found within the source-site
#          structure, too.
#
#------------------------------------------------------------------------------
{n_model_receiver_lines}                               |int: no_model_lines;
#------------------------------------------------------------------------------
#
#	MULTILAYERED MODEL PARAMETERS (shallow receiver-site structure)
#	===============================================================
# no  depth[km]    vp[km/s]    vs[km/s]   ro[g/cm^3]   qp      qs
#------------------------------------------------------------------------------
{model_receiver_lines}
#---------------------------------end of all inputs----------------------------


Note 1:

The slowness is defined by inverse value of apparent wave velocity = sin(i)/v
with i = incident angle and v = true wave velocity.

Note 2:

The suppression of the time domain aliasing is achieved by using the complex
frequency technique. The suppression factor should be a value between 0 and 1.
If this factor is set to 0.1, for example, the aliasing phase at the reduced
time begin is suppressed to 10%%.

Note 3:

The default basic wavelet function (option 1) is (2/tau)*sin^2(pi*t/tau),
for 0 < t < tau, simulating physical delta impuls. Its half-amplitude cut-off
frequency is 1/tau. To avoid high-frequency noise, tau should not be smaller
than 4-5 time samples.

Note 4:

  Double-Couple   m11/ m22/ m33/ m12/ m23/ m31  Azimuth_Factor_(tz,tr,tv)/(tt)
  ============================================================================
  explosion       1.0/ 1.0/ 1.0/ -- / -- / --       1.0         /   0.0
  strike-slip     -- / -- / -- / 1.0/ -- / --       sin(2*azi)  /   cos(2*azi)
                  1.0/-1.0/ -- / -- / -- / --       cos(2*azi)  /  -sin(2*azi)
  dip-slip        -- / -- / -- / -- / -- / 1.0      cos(azi)    /   sin(azi)
                  -- / -- / -- / -- / 1.0/ --       sin(azi)    /  -cos(azi)
  clvd           -0.5/-0.5/ 1.0/ -- / -- / --       1.0         /   0.0
  ============================================================================
  Single-Force    fx / fy / fz                  Azimuth_Factor_(tz,tr,tv)/(tt)
  ============================================================================
  fz              -- / -- / 1.0                        1.0      /   0.0
  fx              1.0/ -- / --                         cos(azi) /   sin(azi)
  fy              -- / 1.0/ --                         sin(azi) /  -cos(azi)
  ============================================================================

Note 5:

Layers with a constant gradient will be discretized with a number of homogeneous
sublayers. The gradient resolutions are then used to determine the maximum
allowed thickness of the sublayers. If the resolutions of Vp, Vs and Rho
(density) require different thicknesses, the smallest is first chosen. If this
is even smaller than 1%% of the characteristic wavelength, then the latter is
taken finally for the sublayer thickness.
"""
    with open(output_path / "input.txt", "w") as f:
        f.write(template)
