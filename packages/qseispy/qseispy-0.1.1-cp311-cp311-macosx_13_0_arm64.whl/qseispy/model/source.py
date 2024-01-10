import math
import pygmt
import numpy as np
import matplotlib.pyplot as plt

from math import sin, cos, tan, atan2, atan, sqrt, acos
from obspy import UTCDateTime
from obspy.imaging.mopad_wrapper import beach

"""
Source Type:
    1) 'unknown'
    2) 'ep' (explosion)
    3) 'sf' (single force)
    4) 'dc' (double couple)
    5) 'mt' (moment tensor)

Source Time Function Type:
    1) 'trapezoid'

Source Conversion:
    1) strike_dip_rake --> MT
    2) strike_dip_rake --> A/N vector
    3) A/N vector --> strike_dip_rake
    4) A/N vector --> P/T/N vector;
    5) T/P vector --> A/N vector;
    6) MT --> P/T/N vector;
    7) P/T/N vector --> P/T/N vector's stirke and dip;
    8) convertion in different coordinate system: NED, USE, UP/SOUTH/EAST, etc.

             AN
            /  \
           /    \
         DC      TPN  
           \    /
            \  /
             MT
             
Source Plot:
    1) project station to beachball;
    2) Hudson plot;
    3) Lune plot;

Reference:
    1) Aki & Richards (1980)
    2) Bowers & Hudson (1999)  # Hudson, J.A., R.G. Pearce, and R.M.Rogers (1989), "Source type plot for inversion of the moment tensor", J. Geophys. Res., 94, 765?74
    3) Jost & Herrmann (1989)
    4) Tape & Tape (2012)
    
"""


class TrapezoidSTF(object):
    """
    TrapezoidSTF is a class for trapezoid source time function.

    Parameters
    ----------
    dura : float
        Duration of the source time function.
    rise : float
        Rise time of the source time function.
    dt : float
        Sampling interval of the source time function.

    Returns
    -------

    """

    def __init__(self, dura=0.0, rise=0.5, dt=0.1) -> None:
        self.dura = dura
        self.rise = rise
        self.dt = dt

        # generate stf
        ns = int(dura / dt)
        if ns < 2:
            ns = 2
        data = np.zeros(ns + 1, dtype=float)
        nr = int(rise * ns)
        if nr < 1:
            nr = 1
        if 2 * nr > ns:
            nr = ns / 2
        amp = 1.0 / (nr * (ns - nr))
        data[:nr] = amp * np.arange(nr)
        data[nr : ns - nr] = nr * amp
        data[ns - nr :] = (ns - np.arange(ns - nr, ns + 1)) * amp

        self.data = data

    def plot(
        self,
        ax=None,
        figsize=(7, 2),
        show=True,
        save_path=None,
        dpi=100,
    ):
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=figsize)
        times = np.arange(0, len(self.data)) * self.dt
        ax.plot(times, self.data, color="k")
        ax.set_xlim(times.min(), times.max())
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        fig = ax.figure
        if not show:
            plt.close(fig)
        if save_path is not None:
            fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
        else:
            return ax


class EPSource(object):
    def __init__(
        self,
        time=UTCDateTime(0),
        latitude=None,
        longitude=None,
        depth=None,
        mw=None,
        stf=None,
        dt=None,
    ) -> None:
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.depth = depth
        self.mw = mw
        self.stf = stf
        self.type = "ep"

    def __repr__(self) -> str:
        return f"ExplosionSource: time={self.time}, latitude={self.latitude}, longitude={self.longitude}, depth={self.depth}, mw={self.mw}"


class SFSource(object):
    """
    SFSource is a class for single force source.

    Args:
        fx (float): northward component of single force [N]
        fy (float): eastward component of single force [N]
        fz (float): downward component of single force [N]
    """

    def __init__(
        self,
        time=UTCDateTime(0),
        latitude=None,
        longitude=None,
        depth=None,
        fx=None,
        fy=None,
        fz=None,
        stf=None,
        dt=None,
    ) -> None:
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.depth = depth
        self.fx = fx
        self.fy = fy
        self.fz = fz
        self.stf = stf
        self.type = "sf"

    def __repr__(self) -> str:
        return f"SFSource: time={self.time}, latitude={self.latitude}, longitude={self.longitude}, depth={self.depth}, fn={self.fx}, fe={self.fy}, fz={self.fz}"


class DCSource(object):
    """
    Input: fault plane' strike dip and rake in degrees.
        strike : [0, 360)
        dip    : [0, 90]
        rake   : [-180, 180)

    """

    def __init__(
        self,
        time=UTCDateTime(0),
        latitude=None,
        longitude=None,
        depth=None,
        mw=None,
        strike=None,
        dip=None,
        rake=None,
        stf=None,
        dt=None,
    ) -> None:
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.depth = depth
        self.mw = mw
        self.strike = strike
        self.dip = dip
        self.rake = rake
        self.stf = stf
        self.type = "dc"

    def __repr__(self) -> str:
        return f"DCSource: time={self.time}, latitude={self.latitude}, longitude={self.longitude}, depth={self.depth}, mw={self.mw}, strike={self.strike}, dip={self.dip}, rake={self.rake}"

    def to_MT(self):
        mxx, myy, mzz, mxy, mxz, myz = strike_dip_rake2MT(
            self.strike, self.dip, self.rake, m0=self.mw
        )
        source = MTSource(
            time=self.time,
            latitude=self.latitude,
            longitude=self.longitude,
            depth=self.depth,
            mxx=mxx,
            myy=myy,
            mzz=mzz,
            mxy=mxy,
            mxz=mxz,
            myz=myz,
            stf=self.stf,
        )

        return source

    def to_AN(self):
        A, N = strike_dip_rake2AN(self.strike, self.dip, self.rake)

        return A, N

    def to_TPN(self, method=1):
        # method 1
        if method == 1:
            A, N = strike_dip_rake2AN(self.strike, self.dip, self.rake)
            T, P, Null = AN2TPN(A, N)
        elif method == 2:
            mxx, myy, mzz, mxy, mxz, myz = strike_dip_rake2MT(
                self.strike, self.dip, self.rake, m0=self.mw
            )
            T, P, Null = MT2TPN(mxx, myy, mzz, mxy, mxz, myz)
        else:
            raise ValueError("Invalid method.")

        return T, P, Null

    def to_AuxPlane(self):
        # AuxPlane is a class for auxiliary plane.
        T_axis, P_axis, N_axis = self.to_TPN()
        A, N = TP2AN(T_axis, P_axis)
        strike_1, dip_1, rake_1 = AN2strike_dip_rake(A, N)
        strike_2, dip_2, rake_2 = AN2strike_dip_rake(N, A)

        return [strike_1, dip_1, rake_1], [strike_2, dip_2, rake_2]

    def beachball(
        self,
        xy=(0.5, 0.5),
        width=1,
        fontsize=20,
        alpha=1,
        facecolor="r",
        bgcolor="w",
        edgecolor="k",
        nofill=False,
        zorder=100,
        ax=None,
        figsize=(4, 4),
        show=True,
        save_path=None,
        dpi=100,
    ):
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=figsize)
        # beachball
        ball = beach(
            fm=[self.strike, self.dip, self.rake],
            xy=xy,
            width=width,
            alpha=alpha,
            facecolor=facecolor,
            bgcolor=bgcolor,
            edgecolor=edgecolor,
            nofill=nofill,
            zorder=zorder,
            mopad_basis="NED",
        )
        ax.add_collection(ball)
        ax.set_aspect("equal")
        # TPN
        T, P, Null = self.to_TPN()
        T_strike, T_dip = TPNvector2strike_dip(T)
        P_strike, P_dip = TPNvector2strike_dip(P)
        Null_strike, Null_dip = TPNvector2strike_dip(Null)
        T_x, T_y = project_beachball(
            azimuth=T_strike, takeoff=(90 - T_dip), R=width / 2
        )
        P_x, P_y = project_beachball(
            azimuth=P_strike, takeoff=(90 - P_dip), R=width / 2
        )
        Null_x, Null_y = project_beachball(
            azimuth=Null_strike, takeoff=(90 - Null_dip), R=width / 2
        )
        ax.text(
            T_x + xy[0],
            T_y + xy[1],
            "T",
            horizontalalignment="center",
            verticalalignment="center",
            zorder=zorder,
            fontsize=fontsize,
            color="k",
        )
        ax.text(
            P_x + xy[0],
            P_y + xy[1],
            "P",
            horizontalalignment="center",
            verticalalignment="center",
            zorder=zorder,
            fontsize=fontsize,
            color="k",
        )
        ax.text(
            Null_x + xy[0],
            Null_y + xy[1],
            "N",
            horizontalalignment="center",
            verticalalignment="center",
            zorder=zorder,
            fontsize=fontsize,
            color="k",
        )
        # set axis
        ax.set_xlim(xy[0] - 1.05 * width / 2, xy[0] + 1.05 * width / 2)
        ax.set_ylim(xy[1] - 1.05 * width / 2, xy[1] + 1.05 * width / 2)
        ax.set_axis_off()
        fig = ax.figure
        if not show:
            plt.close(fig)
        if save_path is not None:
            fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
        else:
            return ax


class MTSource(object):
    """
    Input: moment tensor in NED system, which is defined from Aki & Richards (1980), x = North, y = East, z = Down.

    """

    def __init__(
        self,
        time=UTCDateTime(0),
        latitude=None,
        longitude=None,
        depth=None,
        mxx=None,
        myy=None,
        mzz=None,
        mxy=None,
        mxz=None,
        myz=None,
        stf=None,
        dt=None,
    ) -> None:
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.depth = depth
        self.mxx = mxx
        self.myy = myy
        self.mzz = mzz
        self.mxy = mxy
        self.mxz = mxz
        self.myz = myz
        self.stf = stf
        self.type = "mt"

    def __repr__(self) -> str:
        return f"MTSource: time={self.time}, latitude={self.latitude}, longitude={self.longitude}, depth={self.depth}, mxx={self.mxx}, myy={self.myy}, mzz={self.mzz}, mxy={self.mxy}, mxz={self.mxz}, myz={self.myz}"

    @property
    def m0(self):  # probably is wrong, also see self.decompose()
        M = np.array(
            [
                [self.mxx, self.mxy, self.mxz],
                [self.mxy, self.myy, self.myz],
                [self.mxz, self.myz, self.mzz],
            ]
        )
        m0 = np.linalg.norm(M)

        return m0

    def normalize(self):
        M = np.array(
            [
                [self.mxx, self.mxy, self.mxz],
                [self.mxy, self.myy, self.myz],
                [self.mxz, self.myz, self.mzz],
            ]
        )
        return M / np.linalg.norm(M)

    def to_AN(self):
        T, P, Null = MT2TPN(self.mxx, self.myy, self.mzz, self.mxy, self.mxz, self.myz)
        A, N = TP2AN(T, P)

        return A, N

    def to_TPN(self):
        T, P, Null = MT2TPN(self.mxx, self.myy, self.mzz, self.mxy, self.mxz, self.myz)

        return T, P, Null

    def to_AuxPlane(self):
        # AuxPlane is a class for auxiliary plane.
        T, P, Null = self.to_TPN()
        A, N = TP2AN(T, P)
        strike_1, dip_1, rake_1 = AN2strike_dip_rake(A, N)
        strike_2, dip_2, rake_2 = AN2strike_dip_rake(N, A)

        return [strike_1, dip_1, rake_1], [strike_2, dip_2, rake_2]

    def decompose(
        self,
        plot=True,
        show=True,
        ax=None,
        save_path=None,
        dpi=100,
        figsize=(16, 4),
    ):
        """
        Input: moment tensor in NED system.

        Decomposition according Aki & Richards and Jost & Herrmann into: M = isotropic + deviatoric = isotropic + DC + CLVD
        """
        # 1. full-moment
        M_mt = np.array(
            [
                [self.mxx, self.mxy, self.mxz],
                [self.mxy, self.myy, self.myz],
                [self.mxz, self.myz, self.mzz],
            ]
        )

        # 2.isotropic part
        m_ep = 1.0 / 3 * np.trace(M_mt)
        m0_ep = abs(m_ep)
        M_ep = np.diag(np.array([m_ep, m_ep, m_ep]))

        # 3.deviatoric part
        M_devi = M_mt - M_ep

        # 4.eigenvalues and -vectors of M
        eigen_val, eigen_vec = np.linalg.eig(M_mt)

        # 5.eigenvalues in ascending order:
        eigen_val_ord = np.real(np.take(eigen_val, np.argsort(abs(eigen_val))))
        eigen_vec_ord = np.real(np.take(eigen_vec, np.argsort(abs(eigen_val)), 1))

        # 6.named according to Jost & Herrmann:
        # a1 = eigen_vec_ord[:, 0]  # not used
        a2 = eigen_vec_ord[:, 1]
        a3 = eigen_vec_ord[:, 2]
        F = -(eigen_val_ord[0] - m_ep) / (eigen_val_ord[2] - m_ep)

        # 7.decompose
        M_dc = (
            (eigen_val_ord[2] - m_ep)
            * (1 - 2 * F)
            * (np.outer(a3, a3) - np.outer(a2, a2))
        )
        M_clvd = M_devi - M_dc

        # 8.according to Bowers & Hudson:
        M0 = max(abs(eigen_val_ord))  # seismic moment (in N/m)
        Mw = np.log10(M0 * 1.0e7) / 1.5 - 16.1 / 1.5  # moment_magnitude unit is Mw
        ep_percentage = int(round(m0_ep / M0 * 100, 6))
        dc_percentage = int(
            round((1 - 2 * abs(F)) * (1 - ep_percentage / 100.0) * 100, 6)
        )
        clvd_percentage = 100 - ep_percentage - dc_percentage

        # 9. result dictionary
        result = {
            "M_mt": M_mt,
            "M_ep": M_ep,
            "M_dc": M_dc,
            "M_clvd": M_clvd,
            "ep_percentage": ep_percentage,
            "dc_percentage": dc_percentage,
            "clvd_percentage": clvd_percentage,
            "M0": M0,
            "Mw": Mw,
        }

        # 10. plot
        if plot:
            if ax is None:
                _, ax = plt.subplots(1, 1, figsize=figsize)

            # mt
            ax = self.beachball(ax=ax, xy=(0.5, 0.5))

            # dc
            source = MTSource(
                mxx=M_dc[0, 0],
                myy=M_dc[1, 1],
                mzz=M_dc[2, 2],
                mxy=M_dc[0, 1],
                mxz=M_dc[0, 2],
                myz=M_dc[1, 2],
            )
            ax = source.beachball(ax=ax, xy=(2.0, 0.5))

            # clvd
            source = MTSource(
                mxx=M_clvd[0, 0],
                myy=M_clvd[1, 1],
                mzz=M_clvd[2, 2],
                mxy=M_clvd[0, 1],
                mxz=M_clvd[0, 2],
                myz=M_clvd[1, 2],
            )
            ax = source.beachball(ax=ax, xy=(3.5, 0.5))

            # ep
            source = MTSource(
                mxx=M_ep[0, 0],
                myy=M_ep[1, 1],
                mzz=M_ep[2, 2],
                mxy=M_ep[0, 1],
                mxz=M_ep[0, 2],
                myz=M_ep[1, 2],
            )
            ax = source.beachball(ax=ax, xy=(5, 0.5))

            # text
            ax.text(
                0.5,
                -0.2,
                "MT",
                horizontalalignment="center",
                verticalalignment="center",
                fontsize=20,
                color="k",
            )
            ax.text(
                2.0,
                -0.2,
                f"DC: {dc_percentage}%",
                horizontalalignment="center",
                verticalalignment="center",
                fontsize=20,
                color="k",
            )
            ax.text(
                3.5,
                -0.2,
                f"CLVD: {clvd_percentage}%",
                horizontalalignment="center",
                verticalalignment="center",
                fontsize=20,
                color="k",
            )
            ax.text(
                5,
                -0.2,
                f"EP: {ep_percentage}%",
                horizontalalignment="center",
                verticalalignment="center",
                fontsize=20,
                color="k",
            )
            ax.text(
                1.25,
                0.5,
                "=",
                horizontalalignment="center",
                verticalalignment="center",
                fontsize=30,
                color="k",
            )
            ax.text(
                2.75,
                0.5,
                "+",
                horizontalalignment="center",
                verticalalignment="center",
                fontsize=30,
                color="k",
            )
            ax.text(
                4.25,
                0.5,
                "+",
                horizontalalignment="center",
                verticalalignment="center",
                fontsize=30,
                color="k",
            )

            ax.set_xlim(-0.1, 5.6)
            fig = ax.figure
            if not show:
                plt.close(fig)
            if save_path is not None:
                fig.savefig(save_path, dpi=dpi, bbox_inches="tight")

        return result, ax

    def beachball(
        self,
        xy=(0.5, 0.5),
        width=1,
        fontsize=20,
        alpha=1,
        facecolor="r",
        bgcolor="w",
        edgecolor="k",
        nofill=False,
        zorder=100,
        ax=None,
        figsize=(4, 4),
        show=True,
        save_path=None,
        dpi=100,
    ):
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=figsize)
        # beachball
        ball = beach(
            fm=[self.mxx, self.myy, self.mzz, self.mxy, self.mxz, self.myz],
            xy=xy,
            width=width,
            alpha=alpha,
            facecolor=facecolor,
            bgcolor=bgcolor,
            edgecolor=edgecolor,
            nofill=nofill,
            zorder=zorder,
            mopad_basis="NED",  # "NED" is from Aki & Richards (1980), x = North, y = East, z = Down
        )
        ax.add_collection(ball)
        ax.set_aspect("equal")
        # TPN
        T, P, Null = self.to_TPN()
        T_strike, T_dip = TPNvector2strike_dip(T)
        P_strike, P_dip = TPNvector2strike_dip(P)
        Null_strike, Null_dip = TPNvector2strike_dip(Null)
        T_x, T_y = project_beachball(
            azimuth=T_strike, takeoff=(90 - T_dip), R=width / 2
        )
        P_x, P_y = project_beachball(
            azimuth=P_strike, takeoff=(90 - P_dip), R=width / 2
        )
        Null_x, Null_y = project_beachball(
            azimuth=Null_strike, takeoff=(90 - Null_dip), R=width / 2
        )
        ax.text(
            T_x + xy[0],
            T_y + xy[1],
            "T",
            horizontalalignment="center",
            verticalalignment="center",
            zorder=zorder,
            fontsize=fontsize,
            color="k",
        )
        ax.text(
            P_x + xy[0],
            P_y + xy[1],
            "P",
            horizontalalignment="center",
            verticalalignment="center",
            zorder=zorder,
            fontsize=fontsize,
            color="k",
        )
        ax.text(
            Null_x + xy[0],
            Null_y + xy[1],
            "N",
            horizontalalignment="center",
            verticalalignment="center",
            zorder=zorder,
            fontsize=fontsize,
            color="k",
        )
        # set axis
        ax.set_xlim(xy[0] - 1.04 * width / 2, xy[0] + 1.04 * width / 2)
        ax.set_ylim(xy[1] - 1.04 * width / 2, xy[1] + 1.04 * width / 2)
        ax.set_axis_off()
        fig = ax.figure
        if not show:
            plt.close(fig)
        if save_path is not None:
            fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
        else:
            return ax

    def hudson(
        self,
        width=0.15,
        beachball_fontsize=6,
        alpha=1,
        facecolor="r",
        bgcolor="w",
        edgecolor="k",
        nofill=False,
        zorder=100,
        ax=None,
        figsize=(8, 8),
        show=True,
        save_path=None,
        dpi=100,
    ):
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=figsize)

        ax = viz_hudson(ax=ax)
        M = np.array(
            [
                [self.mxx, self.mxy, self.mxz],
                [self.mxy, self.myy, self.myz],
                [self.mxz, self.myz, self.mzz],
            ]
        )
        k, T = M2kT_space(M)
        U, V = kT2UV_space(k, T)
        ax = self.beachball(
            ax=ax,
            xy=(U, V),
            width=width,
            fontsize=beachball_fontsize,
            alpha=alpha,
            facecolor=facecolor,
            bgcolor=bgcolor,
            edgecolor=edgecolor,
            nofill=nofill,
            zorder=zorder,
        )

        ax.set_xlim(-4 / 3 - 0.1, 4 / 3 + 0.1)
        ax.set_ylim(-1 - 0.1, 1 + 0.1)
        ax.set_aspect("equal")
        ax.set_axis_off()
        fig = ax.figure
        if not show:
            plt.close(fig)
        if save_path is not None:
            fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
        else:
            return ax

    def lune(
        self,
        scale="1.0c",
        show=True,
        show_width=300,
        save_path=None,
    ):
        fig = pygmt.Figure()
        with pygmt.config(
            PS_PAGE_ORIENTATION="landscape",
            PROJ_LENGTH_UNIT="inch",
            MAP_FRAME_TYPE="plain",
            MAP_TICK_LENGTH="0.0c",
            MAP_FRAME_PEN="2p",
            FONT_ANNOT_PRIMARY="12p,Helvetica,black",
            FONT_HEADING="18p,Helvetica,black",
            FONT_LABEL="10p,Helvetica,black",
        ):
            # basemap with lune
            fig.basemap(
                region=[-30, 30, -90, 90],
                projection="H0/2.8i",
                frame="wesn+g255/255/252",
            )
            # lon lat in lune sphere. In this step, we use NED system; Actually, it doesn't matter whatever system you use.
            Lsort, Vsort = lune_eig(
                np.array(
                    [
                        [self.mxx, self.mxy, self.mxz],
                        [self.mxy, self.myy, self.myz],
                        [self.mxz, self.myz, self.mzz],
                    ]
                )
            )
            gamma, delta, M0 = lam2lune(Lsort)
            # focal mechanism, 'meca' function use GLOBAL CMT system, which is USE system.
            MT_NED = np.array(
                [self.mxx, self.myy, self.mzz, self.mxy, self.mxz, self.myz]
            )
            MT_USE = MTConverter(MT_NED, old="NED", new="USE")
            FM_USE = {
                "mrr": MT_USE[0],
                "mtt": MT_USE[1],
                "mff": MT_USE[2],
                "mrt": MT_USE[3],
                "mrf": MT_USE[4],
                "mtf": MT_USE[5],
                "exponent": 22,
            }
            fig.meca(
                spec=FM_USE,  # pygmt need USE system
                scale=scale,
                longitude=gamma,
                latitude=delta,
                convention="mt",
                component="full",
                compressionfill="red",
            )
            # lines
            fig.plot(x=lune_arc_1_x, y=lune_arc_1_y, pen="1p,gray,-")
            fig.plot(x=lune_arc_2_x, y=lune_arc_2_y, pen="1p,gray,-")
            fig.plot(x=lune_arc_3_x, y=lune_arc_3_y, pen="1p,gray,-")
            fig.plot(x=lune_arc_4_x, y=lune_arc_4_y, pen="1p,gray,-")
            fig.plot(x=lune_arc_5_x, y=lune_arc_5_y, pen="1p,gray,-")
            fig.plot(x=lune_arc_6_x, y=lune_arc_6_y, pen="1p,gray,-")
            # markers
            for i in range(0, len(lune_marker)):
                text = lune_marker[i][0]
                x = lune_marker[i][1]
                y = lune_marker[i][2]
                offset = lune_marker[i][3]
                fig.text(
                    text=text,
                    x=x,
                    y=y,
                    offset=offset,
                    no_clip=True,
                    font="10p,Helvetica-Bold,black",
                )
                fig.plot(x=x, y=y, no_clip=True, style="c0.2c", fill="black", pen=True)

        if show:
            fig.show(width=show_width)
        if save_path is not None:
            fig.savefig(save_path)
        else:
            return fig


def MTConverter(mt, old=None, new=None):
    """
    Converts from one basis convention to another

    "USE",  [Up, South, East]   Global CMT Catalog, Larson et al. 2010
    "NED",  [North, East, Down]   Jost and Herrmann 1989, Aki and Richards 1980
    "NWU",  [North, West, Up]   Stein and Wysession 2003, Tape and Tape 2012
    "ENU",  [East, North, Up]   Also named by 'XYZ', general formulation, Jost and Herrmann 1989
    "SEU",  [South, East, Up]   Tape and Tape 2013
    """

    mtnew = np.empty(6)
    if old == new:
        mtnew = mt
    elif (old, new) == ("USE", "NED"):
        # up-south-east to north-east-down
        mtnew[0] = mt[1]
        mtnew[1] = mt[2]
        mtnew[2] = mt[0]
        mtnew[3] = -mt[5]
        mtnew[4] = mt[3]
        mtnew[5] = -mt[4]
    elif (old, new) == ("USE", "NWU"):
        # up-south-east to north-west-up
        mtnew[0] = mt[1]
        mtnew[1] = mt[2]
        mtnew[2] = mt[0]
        mtnew[3] = mt[5]
        mtnew[4] = -mt[3]
        mtnew[5] = -mt[4]
    elif (old, new) == ("USE", "ENU"):
        # up-south-east to east-north-up
        mtnew[0] = mt[2]
        mtnew[1] = mt[1]
        mtnew[2] = mt[0]
        mtnew[3] = -mt[5]
        mtnew[4] = mt[4]
        mtnew[5] = -mt[3]
    elif (old, new) == ("USE", "SEU"):
        # up-south-east to south-east-up
        mtnew[0] = mt[1]
        mtnew[1] = mt[2]
        mtnew[2] = mt[0]
        mtnew[3] = mt[5]
        mtnew[4] = mt[3]
        mtnew[5] = mt[4]
    elif (old, new) == ("NED", "USE"):
        # north-east-down to up-south-east
        mtnew[0] = mt[2]
        mtnew[1] = mt[0]
        mtnew[2] = mt[1]
        mtnew[3] = mt[4]
        mtnew[4] = -mt[5]
        mtnew[5] = -mt[3]
    elif (old, new) == ("NED", "NWU"):
        # north-east-down to north-west-up
        mtnew[0] = mt[0]
        mtnew[1] = mt[1]
        mtnew[2] = mt[2]
        mtnew[3] = -mt[3]
        mtnew[4] = -mt[4]
        mtnew[5] = mt[5]
    elif (old, new) == ("NED", "ENU"):
        # north-east-down to east-north-up
        mtnew[0] = mt[1]
        mtnew[1] = mt[0]
        mtnew[2] = mt[2]
        mtnew[3] = mt[3]
        mtnew[4] = -mt[5]
        mtnew[5] = -mt[4]
    elif (old, new) == ("NED", "SEU"):
        # north-east-down to south-east-up
        mtnew[0] = mt[0]
        mtnew[1] = mt[1]
        mtnew[2] = mt[2]
        mtnew[3] = -mt[3]
        mtnew[4] = mt[4]
        mtnew[5] = -mt[5]
    elif (old, new) == ("NWU", "USE"):
        # north-west-up to up-south-east
        mtnew[0] = mt[2]
        mtnew[1] = mt[0]
        mtnew[2] = mt[1]
        mtnew[3] = -mt[4]
        mtnew[4] = -mt[5]
        mtnew[5] = mt[3]
    elif (old, new) == ("NWU", "NED"):
        # north-west-up to north-east-down
        mtnew[0] = mt[0]
        mtnew[1] = mt[1]
        mtnew[2] = mt[2]
        mtnew[3] = -mt[3]
        mtnew[4] = -mt[4]
        mtnew[5] = mt[5]
    elif (old, new) == ("NWU", "ENU"):
        # north-west-up to east-north-up
        mtnew[0] = mt[1]
        mtnew[1] = mt[0]
        mtnew[2] = mt[2]
        mtnew[3] = -mt[3]
        mtnew[4] = -mt[5]
        mtnew[5] = mt[4]
    elif (old, new) == ("NWU", "SEU"):
        # north-west-up to south-east-up
        mtnew[0] = mt[0]
        mtnew[1] = mt[1]
        mtnew[2] = mt[2]
        mtnew[3] = mt[3]
        mtnew[4] = -mt[4]
        mtnew[5] = -mt[5]
    elif (old, new) == ("ENU", "USE"):
        # east-north-up to up-south-east
        mtnew[0] = mt[2]
        mtnew[1] = mt[1]
        mtnew[2] = mt[0]
        mtnew[3] = -mt[5]
        mtnew[4] = mt[4]
        mtnew[5] = -mt[3]
    elif (old, new) == ("ENU", "NED"):
        # east-north-up to north-east-down
        mtnew[0] = mt[1]
        mtnew[1] = mt[0]
        mtnew[2] = mt[2]
        mtnew[3] = mt[3]
        mtnew[4] = -mt[5]
        mtnew[5] = -mt[4]
    elif (old, new) == ("ENU", "NWU"):
        # east-north-up to north-west-up
        mtnew[0] = mt[1]
        mtnew[1] = mt[0]
        mtnew[2] = mt[2]
        mtnew[3] = -mt[3]
        mtnew[4] = mt[5]
        mtnew[5] = -mt[4]
    elif (old, new) == ("ENU", "SEU"):
        # east-north-up to south-east-up
        mtnew[0] = mt[1]
        mtnew[1] = mt[0]
        mtnew[2] = mt[2]
        mtnew[3] = -mt[3]
        mtnew[4] = -mt[5]
        mtnew[5] = mt[4]
    elif (old, new) == ("SEU", "USE"):
        # south-east-up to up-south-east
        mtnew[0] = mt[2]
        mtnew[1] = mt[0]
        mtnew[2] = mt[1]
        mtnew[3] = mt[4]
        mtnew[4] = mt[5]
        mtnew[5] = mt[3]
    elif (old, new) == ("SEU", "NED"):
        # south-east-up to north-east-down
        mtnew[0] = mt[0]
        mtnew[1] = mt[1]
        mtnew[2] = mt[2]
        mtnew[3] = -mt[3]
        mtnew[4] = mt[4]
        mtnew[5] = -mt[5]
    elif (old, new) == ("SEU", "NWU"):
        # south-east-up to north-west-up
        mtnew[0] = mt[0]
        mtnew[1] = mt[1]
        mtnew[2] = mt[2]
        mtnew[3] = mt[3]
        mtnew[4] = -mt[4]
        mtnew[5] = -mt[5]
    elif (old, new) == ("SEU", "ENU"):
        # south-east-up to east-north-up
        mtnew[0] = mt[1]
        mtnew[1] = mt[0]
        mtnew[2] = mt[2]
        mtnew[3] = -mt[3]
        mtnew[4] = mt[5]
        mtnew[5] = -mt[4]
    else:
        raise ValueError("Unknown basis")

    return mtnew


def strike_dip_rake2MT(strike, dip, rake, m0=1):
    """
    Convert strike, dip and rake to moment tensor in NED system, which is defined from Aki & Richards (1980), x = North, y = East, z = Down.

    Parameters
    ----------
    strike : float
        Strike angle in degrees.
    dip : float
        Dip angle in degrees.
    rake : float
        Rake angle in degrees.
    m0 : float
        Scalar moment in N*m.

    Returns
    -------
    mxx : float
        mxx
    myy : float
        myy
    mzz : float
        mzz
    mxy : float
        mxy
    mxz : float
        mxz
    myz : float
        myz
    """
    strike = strike / 180 * np.pi
    dip = dip / 180 * np.pi
    rake = rake / 180 * np.pi

    mxx = -m0 * (
        sin(dip) * cos(rake) * sin(2 * strike)
        + sin(2 * dip) * sin(rake) * sin(strike) ** 2
    )
    myy = m0 * (
        sin(dip) * cos(rake) * sin(2 * strike)
        - sin(2 * dip) * sin(rake) * cos(strike) ** 2
    )
    mzz = m0 * (sin(2 * dip) * sin(rake))
    mxy = m0 * (
        sin(dip) * cos(rake) * cos(2 * strike)
        + 1 / 2 * sin(2 * dip) * sin(rake) * sin(2 * strike)
    )
    mxz = -m0 * (
        cos(dip) * cos(rake) * cos(strike) + cos(2 * dip) * sin(rake) * sin(strike)
    )
    myz = -m0 * (
        cos(dip) * cos(rake) * sin(strike) - cos(2 * dip) * sin(rake) * cos(strike)
    )

    return mxx, myy, mzz, mxy, mxz, myz


def strike_dip_rake2AN(strike, dip, rake):
    """
    Convert strike, dip and rake to slip vector(A) and fault plane direction vector(N) in NED system.

    Parameters
    ----------
    strike : float
        Strike angle in degrees. [0, 360)
    dip : float
        Dip angle in degrees. [0, 90]
    rake : float
        Rake angle in degrees. [-180, 180)

    Returns
    -------
    A : array
        Slip vector in NED system.
    N : array
        Fault plane direction vector in NED system.
    """
    strike = strike / 180 * np.pi
    dip = dip / 180 * np.pi
    rake = rake / 180 * np.pi

    A = np.array(
        [
            cos(rake) * cos(strike) + sin(rake) * cos(dip) * sin(strike),
            cos(rake) * sin(strike) - sin(rake) * cos(dip) * cos(strike),
            -sin(rake) * sin(dip),
        ]
    )

    N = np.array([-sin(strike) * sin(dip), cos(strike) * sin(dip), -cos(dip)])

    return A, N


def AN2strike_dip_rake(A, N):
    """
    Convert slip vector(A) and fault plane direction vector(N) in NED system to strike, dip and rake.

    Parameters
    ----------
    A : array
        Slip vector in NED system.
    N : array
        Fault plane direction vector in NED system.

    Returns
    -------
    strike : float
        Strike angle in degrees. [0, 360)
    dip : float
        Dip angle in degrees. [0, 90]
    rake : float
        Rake angle in degrees. [-180, 180)
    """

    if abs(N[2] + 1) < 0.00001:  # nz=-1: the fault plane is horizontal
        strike = atan2(
            A[1], A[0]
        )  # The direction of slip is also the strike, because the fault plane is horizontal
        dip = 0.0
    else:
        strike = atan2(-N[0], N[1])
        if abs(N[2] - 0) < 0.00001:  # nz=-1: the fault plane is vertical
            dip = np.pi / 2
        elif abs(sin(strike)) > abs(cos(strike)):
            dip = atan((N[0] / sin(strike)) / N[2])
        else:
            dip = atan((-N[1] / cos(strike)) / N[2])

    cos_rake = A[0] * cos(strike) + A[1] * sin(strike)

    if abs(A[2] - 0) > 0.0000001:  # az!=0: consider the effect of dip
        if abs(dip - 0) > 0.000001:
            rake = atan2(-A[2] / sin(dip), cos_rake)
        else:
            rake = atan2(-100000000.0 * A[2], cos_rake)
    else:  # az=0: don't consider the effect of dip
        if cos_rake > 1:
            cos_rake = 1
        if cos_rake < -1:
            cos_rake = -1
        rake = acos(cos_rake)

    if dip < 0:
        dip = -dip
        strike = strike + np.pi  # strike need to be in the opposite direction

    if strike >= 2 * np.pi:
        strike = strike - 2 * np.pi
    if strike < 0:
        strike = strike + 2 * np.pi

    strike = strike * 180 / np.pi
    dip = dip * 180 / np.pi
    rake = rake * 180 / np.pi

    return strike, dip, rake


def AN2TPN(A, N):
    """
    Convert slip vector(A) and fault plane direction vector(N) in NED system to T-axis, P-axis and N-axis.

    Parameters
    ----------
    A : array
        Slip vector in NED system.
    N : array
        Fault plane direction vector in NED system.

    Returns
    -------
    T : array
        Tension-axis vector in NED system.
    P : array
        Pressure-axis vector in NED system.
    Null : array
        Null-axis vector in NED system.
    """
    T = sqrt(2) / 2 * (A + N)
    P = sqrt(2) / 2 * (A - N)
    Null = np.cross(P, T)

    return T, P, Null


def TP2AN(T, P):
    """
    Convert T-axis and P-axis to slip vector(A) and fault plane direction vector(N) in NED system.

    Parameters
    ----------
    T : array
        Tension-axis vector in NED system.
    P : array
        Pressure-axis vector in NED system.

    Returns
    -------
    A : array
        Slip vector in NED system.
    N : array
        Fault plane direction vector in NED system.
    """
    A = sqrt(2) / 2 * (T + P)
    N = sqrt(2) / 2 * (T - P)

    return A, N


def MT2TPN(mxx, myy, mzz, mxy, mxz, myz):
    """
    Convert moment tensor in NED system to T-axis, P-axis and N-axis.

    Parameters
    ----------
    mxx : float
        mxx
    myy : float
        myy
    mzz : float
        mzz
    mxy : float
        mxy
    mxz : float
        mxz
    myz : float
        myz

    Returns
    -------
    T : array
        Tension-axis vector in NED system.
    P : array
        Pressure-axis vector in NED system.
    Null : array
        Null-axis vector in NED system.
    """

    M = np.array(
        [
            [mxx, mxy, mxz],
            [mxy, myy, myz],
            [mxz, myz, mzz],
        ]
    )
    eigen_val, eigen_vec = np.linalg.eig(M)
    # The TNP axis should be arranged in order of eigenvalues from largest to smallest
    eigen_vec_ord_axis = np.real(np.take(eigen_vec, np.argsort(-eigen_val), 1))

    T = eigen_vec_ord_axis[:, 0]
    Null = eigen_vec_ord_axis[:, 1]
    P = eigen_vec_ord_axis[:, 2]

    return T, P, Null


def TPNvector2strike_dip(vector):
    """
    Convert P/T/N vector to P/T/N vector's stirke and dip.

    Parameters
    ----------
    vector : array
        P/T/N vector(only one vector) in NED system, such as eigenvectors P/T/N of the moment tensor object.

    Returns
    -------
    strike : float
        Strike angle in degrees. [0, 360)
    dip : float
        Dip angle in degrees. [0, 90]
    """
    x = vector[0]
    y = vector[1]
    z = vector[2]

    strike = atan2(y, x) * 180 / np.pi
    r = sqrt(x**2 + y**2)
    dip = atan2(z, r) * 180 / np.pi

    if dip < 0.0:
        dip = -dip
        strike = strike - 180
    if strike < 0:
        strike = strike + 360
    if strike > 360:
        strike = strike - 360

    return strike, dip


def project_beachball(azimuth, takeoff, R=1, menthod="schmidt"):
    """
    Project the station to the beachball.

    Parameters
    ----------
    azimuth : float
        azimuth in degrees. (strike)
    takeoff : float
        takeoff angle in degrees.  (takeoff = pi/2 - dip)
    R : float
        beachball radius that you want to plot.
    menthod : str, optional
        projection menthod, by default "schmidt"
        "schmidt" (Lambert, equal-area) default
        "wulff" (Stereographic, equal-angle) not recommmended

    Returns
    -------
    X : float
        X coordinates in E direction. Note: the center of the beachball circle is the origin.
    Y : float
        Y coordinates in N direction.
    """

    azimuth = azimuth / 180 * np.pi
    takeoff = takeoff / 180 * np.pi

    if menthod == "schmidt":
        r = math.sqrt(2) * sin(takeoff / 2)

    elif menthod == "wulff":
        r = tan(takeoff / 2)
    else:
        raise ValueError("projection error!")

    X = R * r * sin(azimuth)
    Y = R * r * cos(azimuth)

    return X, Y


def M2kT_space(MT):
    """
    Convert moment tensor in NED system to [k,T] space.

    Parameters
    ----------
    MT : array
        moment tensor in NED system, for example,
        MT = np.array(
            [
                [mxx, mxy, mxz],
                [mxy, myy, myz],
                [mxz, myz, mzz],
            ]
        )

    Returns
    -------
    k : float
        k
    T : float
        T
    """
    # 1. full-moment
    M = MT

    # 2.isotropic part
    m_iso = 1.0 / 3 * np.trace(M)
    M_iso = np.diag(np.array([m_iso, m_iso, m_iso]))

    # 3.deviatoric part
    M_devi = M - M_iso

    # 4.eigenvalues and vectors of M
    devi_eigen_val, devi_eigen_vec = np.linalg.eig(M_devi)

    # 5.eigenvalues in ascending order:
    devi_eigen_val_ord = np.real(
        np.take(devi_eigen_val, np.argsort(-devi_eigen_val))
    )  # descend order

    if (abs(m_iso) + max(abs(devi_eigen_val_ord[0]), abs(devi_eigen_val_ord[2]))) == 0:
        raise TypeError("MomentTensor cannot be translated into [k,T] space.")
    else:
        k = m_iso / (
            abs(m_iso) + max(abs(devi_eigen_val_ord[0]), abs(devi_eigen_val_ord[2]))
        )

    if max(abs(devi_eigen_val_ord[0]), abs(devi_eigen_val_ord[2])) == 0:
        T = 0
    else:
        T = (
            2
            * devi_eigen_val_ord[1]
            / max(abs(devi_eigen_val_ord[0]), abs(devi_eigen_val_ord[2]))
        )

    return k, T


def kT2UV_space(k, T):
    """
    Convert [k,T] space to [U,V] space.

    Parameters
    ----------
    k : float
        k
    T : float
        T

    Returns
    -------
    U : float
        U
    V : float
        V
    """
    tau = T * (1 - abs(k))
    if ((tau > 0) & (k < 0)) | ((tau < 0) & (k > 0)):
        # 2nd and 4th quadrants
        U = tau
        V = k
    elif (tau < (4 * k)) & ((tau >= 0) & (k >= 0)):
        # First quadrant, Region A
        U = tau / (1 - tau / 2)
        V = k / (1 - tau / 2)
    elif (tau >= (4 * k)) & ((tau >= 0) & (k >= 0)):
        # First quadrant, Region B
        U = tau / (1 - 2 * k)
        V = k / (1 - 2 * k)
    elif (tau >= (4 * k)) & ((tau <= 0) & (k <= 0)):
        # Third quadrant, Region A
        U = tau / (1 + tau / 2)
        V = k / (1 + tau / 2)
    elif (tau < (4 * k)) & ((tau <= 0) & (k <= 0)):
        # Third quadrant, Region B
        U = tau / (1 + 2 * k)
        V = k / (1 + 2 * k)
    else:
        raise TypeError("def: kT2UV_space(k,T)")

    return U, V


def viz_hudson(
    ax=None,
    ms=3,
    marker_ms="o",
    color_ms="k",
    alpha_ms=0.5,
    alpha_text=0.9,
    fontsize=8,
):
    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=(4, 4))

    ######################
    ## 1. Fill and draw the border
    ax.fill_between(
        x=[-1, 0], y1=[0, 0], y2=[0, 1], color="k", alpha=0.05
    )  # fill the second quadrant
    ax.fill_between(
        x=[0, 1], y1=[0, 0], y2=[-1, 0], color="k", alpha=0.05
    )  # fill the fourth quadrant
    ax.plot(
        [0, 4 / 3, 0, -4 / 3, 0],
        [1, 1 / 3, -1, -1 / 3, 1],
        linestyle="-",
        color="k",
        lw=1,
        alpha=0.6,
    )
    ax.plot([-1, 1], [0, 0], linestyle="-", color="k", lw=1, alpha=0.6)
    ax.plot([0, 0], [-1, 1], linestyle="-", color="k", lw=1, alpha=0.6)

    ######################
    ## 2. Draw the inner dotted line
    U_vector = []
    V_vector = []
    for i in np.linspace(-1, 1, num=100):
        k = i
        T = 0.5
        U, V = kT2UV_space(k=k, T=T)
        U_vector.append(U)
        V_vector.append(V)
    ax.plot(U_vector, V_vector, linestyle="--", color="k", lw=1, alpha=0.6)

    U_vector = []
    V_vector = []
    for i in np.linspace(-1, 1, num=100):
        k = i
        T = -0.5
        U, V = kT2UV_space(k=k, T=T)
        U_vector.append(U)
        V_vector.append(V)
    ax.plot(U_vector, V_vector, linestyle="--", color="k", lw=1, alpha=0.6)

    U_vector = []
    V_vector = []
    for i in np.linspace(-1, 1, num=100):
        k = 0.5
        T = i
        U, V = kT2UV_space(k=k, T=T)
        U_vector.append(U)
        V_vector.append(V)
    ax.plot(U_vector, V_vector, linestyle="--", color="k", lw=1, alpha=0.6)

    U_vector = []
    V_vector = []
    for i in np.linspace(-1, 1, num=100):
        k = -0.5
        T = i
        U, V = kT2UV_space(k=k, T=T)
        U_vector.append(U)
        V_vector.append(V)
    ax.plot(U_vector, V_vector, linestyle="--", color="k", lw=1, alpha=0.6)

    ######################
    ## 3. Draw marker points and text
    U, V = kT2UV_space(k=1, T=1)
    ax.plot(U, V, marker=marker_ms, color=color_ms, ms=ms, alpha=alpha_ms)
    ax.text(
        U,
        V,
        "ISO+ (Explosion)",
        horizontalalignment="center",
        verticalalignment="bottom",
        fontsize=fontsize,
        color="k",
        alpha=alpha_text,
    )

    U, V = kT2UV_space(k=-1, T=1)
    ax.plot(U, V, marker=marker_ms, color=color_ms, ms=ms, alpha=alpha_ms)
    ax.text(
        U,
        V,
        "ISO- (Implosion)",
        horizontalalignment="center",
        verticalalignment="top",
        fontsize=fontsize,
        color="k",
        alpha=alpha_text,
    )

    U, V = kT2UV_space(k=0, T=1)
    ax.plot(U, V, marker=marker_ms, color=color_ms, ms=ms, alpha=alpha_ms)
    ax.text(
        U,
        V,
        "CLVD (-)",
        horizontalalignment="left",
        verticalalignment="top",
        fontsize=fontsize,
        color="k",
        alpha=alpha_text,
    )

    U, V = kT2UV_space(k=-5 / 9, T=1)
    ax.plot(U, V, marker=marker_ms, color=color_ms, ms=ms, alpha=alpha_ms)
    ax.text(
        U,
        V,
        "Anticrack",
        horizontalalignment="left",
        verticalalignment="top",
        fontsize=fontsize,
        color="k",
        alpha=alpha_text,
    )

    U, V = kT2UV_space(k=0, T=-1)
    ax.plot(U, V, marker=marker_ms, color=color_ms, ms=ms, alpha=alpha_ms)
    ax.text(
        U,
        V,
        "CLVD (+)",
        horizontalalignment="right",
        verticalalignment="bottom",
        fontsize=fontsize,
        color="k",
        alpha=alpha_text,
    )

    U, V = kT2UV_space(k=5 / 9, T=-1)
    ax.plot(U, V, marker=marker_ms, color=color_ms, ms=ms, alpha=alpha_ms)
    ax.text(
        U,
        V,
        "Tensile Crack",
        horizontalalignment="right",
        verticalalignment="bottom",
        fontsize=fontsize,
        color="k",
        alpha=alpha_text,
    )

    U, V = kT2UV_space(k=0, T=0)
    ax.plot(U, V, marker=marker_ms, color=color_ms, ms=ms, alpha=alpha_ms)
    ax.text(
        U,
        V,
        "DC",
        horizontalalignment="center",
        verticalalignment="bottom",
        fontsize=fontsize,
        color="k",
        alpha=alpha_text,
    )

    U, V = kT2UV_space(k=1 / 3, T=-1)
    ax.plot(U, V, marker=marker_ms, color=color_ms, ms=ms, alpha=alpha_ms)
    ax.text(
        U,
        V,
        "LVD (+)",
        horizontalalignment="right",
        verticalalignment="bottom",
        fontsize=fontsize,
        color="k",
        alpha=alpha_text,
    )

    U, V = kT2UV_space(k=-1 / 3, T=1)
    ax.plot(U, V, marker=marker_ms, color=color_ms, ms=ms, alpha=alpha_ms)
    ax.text(
        U,
        V,
        "LVD (-)",
        horizontalalignment="left",
        verticalalignment="top",
        fontsize=fontsize,
        color="k",
        alpha=alpha_text,
    )

    ######################
    ## 4. Set the axes
    ax.set_xlim(-4 / 3 - 0.1, 4 / 3 + 0.1)
    ax.set_ylim(-1 - 0.1, 1 + 0.1)
    ax.set_aspect("equal")
    ax.set_axis_off()

    return ax


def lam2lune(lam):
    """
    Converts moment tensor eigenvalues to lune coordinates

    input
    : lam: vector with shape [3]

    output
    : gamma: angle from DC meridian to lune point (-30 <= gamma <= 30)
    : delta: angle from deviatoric plane to lune point (-90 <= delta <= 90)
    : M0: seismic moment, M0 = ||lam|| / sqrt(2)
    """
    PI = np.pi
    DEG = 180.0 / PI

    # descending sort
    lam = np.sort(lam)[::-1]

    # magnitude of lambda vector (rho of TapeTape2012a p.490)
    lammag = np.linalg.norm(lam)

    # seismic moment
    M0 = lammag / np.sqrt(2.0)

    # TapeTape2012a, eqs.21a,23
    # numerical safety 1: if trace(M) = 0, delta = 0
    # numerical safety 2: is abs(bdot) > 1, adjust bdot to +1 or -1
    if np.sum(lam) != 0.0:
        bdot = np.sum(lam) / (np.sqrt(3) * lammag)
        np.clip(bdot, -1, 1)
        delta = 90.0 - np.arccos(bdot) * DEG
    else:
        delta = 0.0

    # TapeTape2012a, eq.21a
    # note: we set gamma=0 for (1,1,1) and (-1,-1,-1)
    if lam[0] != lam[2]:
        gamma = (
            np.arctan(
                (-lam[0] + 2.0 * lam[1] - lam[2]) / (np.sqrt(3) * (lam[0] - lam[2]))
            )
            * DEG
        )
    else:
        gamma = 0.0

    return (
        gamma,
        delta,
        M0,
    )


def lune2lam(gamma, delta, M0):
    """
    Converts lune coordinates to moment tensor eigenvalues
    """
    PI = np.pi
    DEG = 180.0 / PI
    beta = 90.0 - delta

    # magnitude of lambda vectors (TT2012, p.490)
    rho = M0 * np.sqrt(2)

    # convert to eigenvalues (TT2012, Eq.20)
    # matrix to rotate points such that delta = 90 is (1,1,1) and delta = -90 is (-1,-1,-1)
    R = (
        np.array(
            [
                [3.0**0.5, 0.0, -(3.0**0.5)],
                [-1.0, 2.0, -1.0],
                [2.0**0.5, 2.0**0.5, 2.0**0.5],
            ]
        )
        / 6.0**0.5
    )

    # Cartesian points as 3 x n unit vectors (TT2012, Eq.20)
    # Pxyz = latlon2xyz(delta,gamma,ones(n,1))
    Pxyz = np.array(
        [
            np.cos(gamma / DEG) * np.sin(beta / DEG),
            np.sin(gamma / DEG) * np.sin(beta / DEG),
            np.cos(beta / DEG),
        ]
    )

    # rotate points and apply magnitudes
    lamhat = np.dot(R.T, Pxyz)
    lam = rho * lamhat

    return rho * lamhat


def lune_eig(M, sort_type=1):
    """
    Calculates eigenvalues and eigenvectors of matrix

    sorting of eigenvalues
    1: highest to lowest, algebraic: lam1 >= lam2 >= lam3
    2: lowest to highest, algebraic: lam1 <= lam2 <= lam3
    3: highest to lowest, absolute : | lam1 | >= | lam2 | >= | lam3 |
    4: lowest to highest, absolute : | lam1 | <= | lam2 | <= | lam3 |
    """
    if sort_type not in [1, 2, 3, 4]:
        raise ValueError

    lam, V = np.linalg.eigh(M)

    if sort_type == 1:
        idx = np.argsort(lam)[::-1]
    elif sort_type == 2:
        idx = np.argsort(lam)
    elif sort_type == 3:
        idx = np.argsort(np.abs(lam))[::-1]
    elif sort_type == 4:
        idx = np.argsort(np.abs(lam))
    lsort = lam[idx]
    Vsort = V[:, idx]

    return lsort, Vsort


lune_marker = [
    ["DC", 0, 0, "0.4c/0.4c"],
    ["CLVD", -30, 0, "-0.6c/0c"],
    ["CLVD", 30, 0, "0.6c/0c"],
    ["ISO", 0, -90, "0.0c/-0.3c"],
    ["ISO", 0, 90, "0.0c/0.3c"],
    ["LVD", -30, 35, "-0.5c/0c"],
    ["LVD", 30, -35, "0.5c/0c"],
    ["_", -30, -55, "-0.3c/0c"],
    ["_", 30, 55, "0.3c/0c"],
    ["C(nu=0.25)", -30, 60, "-1.1c/0c"],
    ["C(nu=0.25)", 30, -60, "1.1c/0c"],
]

lune_arc_1_x = np.array(
    [
        -30.0,
        -28.78,
        -27.55,
        -26.33,
        -25.1,
        -23.88,
        -22.65,
        -21.43,
        -20.2,
        -18.98,
        -17.76,
        -16.53,
        -15.31,
        -14.08,
        -12.86,
        -11.63,
        -10.41,
        -9.18,
        -7.96,
        -6.73,
        -5.51,
        -4.29,
        -3.06,
        -1.84,
        -0.61,
        0.61,
        1.84,
        3.06,
        4.29,
        5.51,
        6.73,
        7.96,
        9.18,
        10.41,
        11.63,
        12.86,
        14.08,
        15.31,
        16.53,
        17.76,
        18.98,
        20.2,
        21.43,
        22.65,
        23.88,
        25.1,
        26.33,
        27.55,
        28.78,
        30.0,
    ]
)

lune_arc_1_y = np.array(
    [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ]
)

lune_arc_2_x = np.array(
    [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ]
)

lune_arc_2_y = np.array(
    [
        -90.0,
        -86.33,
        -82.65,
        -78.98,
        -75.31,
        -71.63,
        -67.96,
        -64.29,
        -60.61,
        -56.94,
        -53.27,
        -49.59,
        -45.92,
        -42.24,
        -38.57,
        -34.9,
        -31.22,
        -27.55,
        -23.88,
        -20.2,
        -16.53,
        -12.86,
        -9.18,
        -5.51,
        -1.84,
        1.84,
        5.51,
        9.18,
        12.86,
        16.53,
        20.2,
        23.88,
        27.55,
        31.22,
        34.9,
        38.57,
        42.24,
        45.92,
        49.59,
        53.27,
        56.94,
        60.61,
        64.29,
        67.96,
        71.63,
        75.31,
        78.98,
        82.65,
        86.33,
        90.0,
    ]
)

lune_arc_3_x = np.array(
    [
        -30.0,
        -29.2,
        -28.38,
        -27.55,
        -26.71,
        -25.86,
        -24.98,
        -24.1,
        -23.19,
        -22.27,
        -21.34,
        -20.39,
        -19.42,
        -18.43,
        -17.42,
        -16.4,
        -15.35,
        -14.29,
        -13.21,
        -12.1,
        -10.98,
        -9.83,
        -8.67,
        -7.48,
        -6.27,
        -5.04,
        -3.79,
        -2.51,
        -1.22,
        0.1,
        1.44,
        2.79,
        4.17,
        5.57,
        6.99,
        8.43,
        9.89,
        11.36,
        12.85,
        14.36,
        15.88,
        17.41,
        18.96,
        20.51,
        22.08,
        23.65,
        25.24,
        26.82,
        28.41,
        30.0,
    ]
)


lune_arc_3_y = np.array(
    [
        35.26,
        35.91,
        36.55,
        37.19,
        37.82,
        38.44,
        39.06,
        39.67,
        40.27,
        40.87,
        41.46,
        42.04,
        42.62,
        43.18,
        43.74,
        44.28,
        44.82,
        45.35,
        45.87,
        46.38,
        46.88,
        47.36,
        47.84,
        48.3,
        48.75,
        49.19,
        49.61,
        50.02,
        50.41,
        50.8,
        51.16,
        51.51,
        51.85,
        52.17,
        52.47,
        52.75,
        53.02,
        53.27,
        53.5,
        53.71,
        53.9,
        54.08,
        54.23,
        54.36,
        54.48,
        54.57,
        54.64,
        54.69,
        54.73,
        54.74,
    ]
)

lune_arc_4_x = np.array(
    [
        -30.0,
        -28.41,
        -26.82,
        -25.24,
        -23.65,
        -22.08,
        -20.51,
        -18.96,
        -17.41,
        -15.88,
        -14.36,
        -12.85,
        -11.36,
        -9.89,
        -8.43,
        -6.99,
        -5.57,
        -4.17,
        -2.79,
        -1.44,
        -0.1,
        1.22,
        2.51,
        3.79,
        5.04,
        6.27,
        7.48,
        8.67,
        9.83,
        10.98,
        12.1,
        13.21,
        14.29,
        15.35,
        16.4,
        17.42,
        18.43,
        19.42,
        20.39,
        21.34,
        22.27,
        23.19,
        24.1,
        24.98,
        25.86,
        26.71,
        27.55,
        28.38,
        29.2,
        30.0,
    ]
)


lune_arc_4_y = np.array(
    [
        -54.74,
        -54.73,
        -54.69,
        -54.64,
        -54.57,
        -54.48,
        -54.36,
        -54.23,
        -54.08,
        -53.9,
        -53.71,
        -53.5,
        -53.27,
        -53.02,
        -52.75,
        -52.47,
        -52.17,
        -51.85,
        -51.51,
        -51.16,
        -50.8,
        -50.41,
        -50.02,
        -49.61,
        -49.19,
        -48.75,
        -48.3,
        -47.84,
        -47.36,
        -46.88,
        -46.38,
        -45.87,
        -45.35,
        -44.82,
        -44.28,
        -43.74,
        -43.18,
        -42.62,
        -42.04,
        -41.46,
        -40.87,
        -40.27,
        -39.67,
        -39.06,
        -38.44,
        -37.82,
        -37.19,
        -36.55,
        -35.91,
        -35.26,
    ]
)


lune_arc_5_x = np.array(
    [
        -30.0,
        -27.22,
        -24.78,
        -22.61,
        -20.67,
        -18.92,
        -17.33,
        -15.87,
        -14.54,
        -13.3,
        -12.14,
        -11.06,
        -10.04,
        -9.07,
        -8.15,
        -7.27,
        -6.42,
        -5.6,
        -4.81,
        -4.04,
        -3.28,
        -2.54,
        -1.81,
        -1.08,
        -0.36,
        0.36,
        1.08,
        1.81,
        2.54,
        3.28,
        4.04,
        4.81,
        5.6,
        6.42,
        7.27,
        8.15,
        9.07,
        10.04,
        11.06,
        12.14,
        13.3,
        14.54,
        15.87,
        17.33,
        18.92,
        20.67,
        22.61,
        24.78,
        27.22,
        30.0,
    ]
)


lune_arc_5_y = np.array(
    [
        60.5,
        58.27,
        55.98,
        53.65,
        51.29,
        48.9,
        46.48,
        44.04,
        41.59,
        39.12,
        36.64,
        34.15,
        31.65,
        29.14,
        26.62,
        24.1,
        21.58,
        19.05,
        16.51,
        13.98,
        11.44,
        8.9,
        6.36,
        3.82,
        1.27,
        -1.27,
        -3.82,
        -6.36,
        -8.9,
        -11.44,
        -13.98,
        -16.51,
        -19.05,
        -21.58,
        -24.1,
        -26.62,
        -29.14,
        -31.65,
        -34.15,
        -36.64,
        -39.12,
        -41.59,
        -44.04,
        -46.48,
        -48.9,
        -51.29,
        -53.65,
        -55.98,
        -58.27,
        -60.5,
    ]
)


lune_arc_6_x = np.array(
    [
        -30.0,
        -28.43,
        -26.92,
        -25.44,
        -24.01,
        -22.62,
        -21.26,
        -19.94,
        -18.65,
        -17.38,
        -16.15,
        -14.93,
        -13.74,
        -12.57,
        -11.42,
        -10.29,
        -9.16,
        -8.06,
        -6.96,
        -5.87,
        -4.79,
        -3.72,
        -2.65,
        -1.59,
        -0.53,
        0.53,
        1.59,
        2.65,
        3.72,
        4.79,
        5.87,
        6.96,
        8.06,
        9.16,
        10.29,
        11.42,
        12.57,
        13.74,
        14.93,
        16.15,
        17.38,
        18.65,
        19.94,
        21.26,
        22.62,
        24.01,
        25.44,
        26.92,
        28.43,
        30.0,
    ]
)


lune_arc_6_y = np.array(
    [
        35.26,
        33.96,
        32.63,
        31.28,
        29.92,
        28.54,
        27.15,
        25.75,
        24.33,
        22.91,
        21.47,
        20.02,
        18.57,
        17.11,
        15.64,
        14.17,
        12.69,
        11.21,
        9.72,
        8.23,
        6.74,
        5.25,
        3.75,
        2.25,
        0.75,
        -0.75,
        -2.25,
        -3.75,
        -5.25,
        -6.74,
        -8.23,
        -9.72,
        -11.21,
        -12.69,
        -14.17,
        -15.64,
        -17.11,
        -18.57,
        -20.02,
        -21.47,
        -22.91,
        -24.33,
        -25.75,
        -27.15,
        -28.54,
        -29.92,
        -31.28,
        -32.63,
        -33.96,
        -35.26,
    ]
)
