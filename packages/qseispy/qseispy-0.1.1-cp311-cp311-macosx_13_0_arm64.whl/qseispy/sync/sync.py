import sys
import numpy as np

from qseispy.taup.taup import taup

sys.path.append("/Users/yinfu/ohmyshake/shakecore")
from shakecore import Stream


def calculate_sync(gf, source, azimuth, taup_model_path=None):
    # check gf and source type
    if gf.stats.notes["source_type"] == "dc" and source.type == "mt":
        pass  # moment tensor also use dc gf
    elif gf.stats.notes["source_type"] != source.type:
        raise ValueError("Source type mismatch")

    # check gf and source depth
    if source.depth != None and source.depth != gf.stats.notes["source_depth"]:
        Warning("Source depth mismatch")
    else:
        source.depth = gf.stats.notes["source_depth"]

    # check stf dt and gf dt
    if source.stf.dt != gf.stats.delta:
        raise ValueError("GF dt and STF dt mismatch")

    # sync
    npts = gf.stats.npts
    if source.type == "ep":  # only z and r component
        GFr = gf.data[0, :]
        GFz = gf.data[1, :]
        Ur = np.convolve(source.stf.data, GFr)[:npts]
        Ut = np.zeros_like(Ur)
        Uz = np.convolve(source.stf.data, GFz)[:npts]
    elif source.type == "sf":
        F = np.array(
            [
                source.fx,
                source.fy,
                source.fz,
            ]
        ).reshape(1, 3)
        GFr = radiat_gf_sf(gf, azimuth, component="r")
        GFt = radiat_gf_sf(gf, azimuth, component="t")
        GFz = radiat_gf_sf(gf, azimuth, component="z")
        Ur = np.convolve(source.stf.data, (F @ GFr).reshape(-1))[:npts]
        Ut = np.convolve(source.stf.data, (F @ GFt).reshape(-1))[:npts]
        Uz = np.convolve(source.stf.data, (F @ GFz).reshape(-1))[:npts]
    elif source.type == "dc":
        mt_source = source.to_mt()
        M = np.array(
            [
                mt_source.mxx,
                mt_source.myy,
                mt_source.mzz,
                mt_source.mxy,
                mt_source.mxz,
                mt_source.myz,
            ]
        ).reshape(1, 6)
        GFz = radiat_gf_dc(gf, azimuth, component="z")
        GFr = radiat_gf_dc(gf, azimuth, component="r")
        GFt = radiat_gf_dc(gf, azimuth, component="t")
        Uz = np.convolve(source.stf.data, (M @ GFz).reshape(-1))[:npts]
        Ur = np.convolve(source.stf.data, (M @ GFr).reshape(-1))[:npts]
        Ut = np.convolve(source.stf.data, (M @ GFt).reshape(-1))[:npts]
    elif source.type == "mt":
        M = np.array(
            [
                source.mxx,
                source.myy,
                source.mzz,
                source.mxy,
                source.mxz,
                source.myz,
            ]
        ).reshape(1, 6)
        GFz = radiat_gf_dc(gf, azimuth, component="z")
        GFr = radiat_gf_dc(gf, azimuth, component="r")
        GFt = radiat_gf_dc(gf, azimuth, component="t")
        Uz = np.convolve(source.stf.data, (M @ GFz).reshape(-1))[:npts]
        Ur = np.convolve(source.stf.data, (M @ GFr).reshape(-1))[:npts]
        Ut = np.convolve(source.stf.data, (M @ GFt).reshape(-1))[:npts]
    else:
        raise ValueError("Unknown source type")

    # stream
    data = np.array([Ur, Ut, Uz])
    header = {
        "sampling_rate": gf.stats.sampling_rate,
        "type": "velocity",
        "station": ["syn"] * 3,
        "channel": ["r", "t", "z"],
        "notes": {
            "azimuth": azimuth,
            "source": source,
            "receiver": gf.stats.notes["receiver"],
        },
    }
    stream = Stream(data, header)
    if (
        gf.stats.notes["ray_p"] is not None
    ):  # copy ray_p, t_p, angle_p, ray_s, t_s, angle_s from gf to stream
        try:
            stream.stats.notes["ray_p"] = gf.stats.notes["ray_p"]
            stream.stats.notes["t_p"] = gf.stats.notes["t_p"]
            stream.stats.notes["angle_p"] = gf.stats.notes["angle_p"]
            stream.stats.notes["ray_s"] = gf.stats.notes["ray_s"]
            stream.stats.notes["t_s"] = gf.stats.notes["t_s"]
            stream.stats.notes["angle_s"] = gf.stats.notes["angle_s"]
        except:
            Warning(
                "Failed to copy ray_p, t_p, angle_p, ray_s, t_s, angle_s from gf to stream"
            )

    # taup
    if taup_model_path is not None:
        try:
            ray_p, t_p, angle_p, ray_s, t_s, angle_s = taup(
                taup_model_path,
                gf.stats.notes["source_depth"],
                gf.stats.notes["receiver"].distances[0][0],
            )
            stream.stats.notes["ray_p"] = ray_p
            stream.stats.notes["t_p"] = t_p
            stream.stats.notes["angle_p"] = angle_p
            stream.stats.notes["ray_s"] = ray_s
            stream.stats.notes["t_s"] = t_s
            stream.stats.notes["angle_s"] = angle_s
        except Exception as e:
            Warning(
                f"Failed to calculate ray_p, t_p, angle_p, ray_s, t_s, angle_s: {e}"
            )

    return stream


def radiat_gf_sf(gf, azimuth, component):
    """
    Calculate radiation pattern for single-force source.

    Parameters
    ----------
    gf : Stream
        Green's function.
    azimuth : float
        Azimuth of the source.
    component : str
        Component of the Green's function.

    Returns
    -------
    data : array
        Radiation pattern of the Green's function, 3 components for [fx, fy, fz], x=north, y=east, z=down
    """
    az = np.deg2rad(azimuth)
    data = np.empty([3, gf.stats.npts])
    if component == "z":
        ZHF = gf.data[2, :]
        ZVF = gf.data[4, :]
        data[0, :] = ZHF * np.cos(az)  # fx
        data[1, :] = ZHF * np.sin(az)  # fy
        data[2, :] = ZVF  # fz
    elif component == "r":
        RHF = gf.data[0, :]
        RVF = gf.data[3, :]
        data[0, :] = RHF * np.cos(az)  # fx
        data[1, :] = RHF * np.sin(az)  # fy
        data[2, :] = RVF  # fz
    elif component == "t":
        THF = gf.data[1, :]
        data[0, :] = THF * np.sin(az)
        data[1, :] = -THF * np.cos(az)
        data[2, :] = 0
    else:
        raise ValueError("Unknown component")

    return data


def radiat_gf_dc(gf, azimuth, component):
    """
    Calculate radiation pattern for double-couple source.

    Parameters
    ----------
    gf : Stream
        Green's function.
    azimuth : float
        Azimuth of the source.
    component : str
        Component of the Green's function.

    Returns
    -------
    data : array
        Radiation pattern of the Green's function, 6 components for [mxx, myy, mzz, mxy, mxz, myz], x=north, y=east, z=down
    """
    az = np.deg2rad(azimuth)
    data = np.empty([6, gf.stats.npts])
    if component == "z":
        ZEP = gf.data[6, :]
        ZSS = gf.data[9, :]
        ZDS = gf.data[4, :]
        ZDD = gf.data[1, :]
        data[0, :] = ZSS / 2 * np.cos(2 * az) - ZDD / 6 + ZEP / 3  # mxx
        data[1, :] = -ZSS / 2 * np.cos(2 * az) - ZDD / 6 + ZEP / 3  # myy
        data[2, :] = ZDD / 3 + ZEP / 3  # mzz
        data[3, :] = ZSS * np.sin(2 * az)  # mxy
        data[4, :] = ZDS * np.cos(az)  # mxz
        data[5, :] = ZDS * np.sin(az)  # myz
    elif component == "r":
        REP = gf.data[5, :]
        RSS = gf.data[7, :]
        RDS = gf.data[2, :]
        RDD = gf.data[0, :]
        data[0, :] = RSS / 2 * np.cos(2 * az) - RDD / 6 + REP / 3  # mxx
        data[1, :] = -RSS / 2 * np.cos(2 * az) - RDD / 6 + REP / 3  # myy
        data[2, :] = RDD / 3 + REP / 3  # mzz
        data[3, :] = RSS * np.sin(2 * az)  # mxy
        data[4, :] = RDS * np.cos(az)  # mxz
        data[5, :] = RDS * np.sin(az)  # myz
    elif component == "t":
        TSS = gf.data[8, :]
        TDS = gf.data[3, :]
        data[0, :] = TSS / 2 * np.sin(2 * az)  # mxx
        data[1, :] = -TSS / 2 * np.sin(2 * az)  # myy
        data[2, :] = 0  # mzz
        data[3, :] = -TSS * np.cos(2 * az)  # mxy
        data[4, :] = TDS * np.sin(az)  # mxz
        data[5, :] = -TDS * np.cos(az)  # myz
    else:
        raise ValueError("Unknown component")

    return data
