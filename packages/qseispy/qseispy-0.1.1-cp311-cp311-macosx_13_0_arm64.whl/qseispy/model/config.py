import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path


def load_model(model="prem"):
    dir_path = Path(__file__).parent.parent
    model_path = dir_path / "tests" / "data" / "v_model" / f"{model}.nd"

    with open(model_path, "r") as file:
        lines = file.readlines()

    data = []
    for line in lines:
        # check if line contains string
        if any(char.isdigit() for char in line):
            numbers = list(map(float, line.split()))
            data.append(numbers)

    return np.array(data)


class ConfigModel(object):
    """
    Model configuration.

    Example:
    >>> from qseispy import ConfigModel, load_model

    >>> model = load_model("prem")
    >>> model = ConfigModel(model=model,
                            flattening=False,
                            vp_res=0.1,
                            vs_res=0.1,
                            rho_res=0.1)

    >>> model.solution(free_surface=True,
                        penetration_filter=[False, 560.0],
                        phase_filter=[[0.0, 5153.0, 'P_up'],
                                    [0.0, 5153.0, 'P_down'],
                                    [0.0, 5153.0, 'S_up'],
                                    [0.0, 5153.0, 'S_down']])

    >>> model.integration(full_field=True,
                            slowness_window=[0.0, 0.0, 0.0, 0.0],
                            wavenumber_integration_factor=2.0,
                            aliasing_suppression_factor=0.1)
    """

    def __init__(
        self,
        model=None,
        ss_model=None,
        rr_model=None,
        flattening=False,
        vp_res=-1,
        vs_res=-1,
        rho_res=-1,
    ) -> None:
        # layer model
        if model is not None and ss_model is None and rr_model is None:
            pass
        elif model is None and ss_model is not None and rr_model is not None:
            pass
        else:
            raise ValueError("Invalid model configuration.")

        if model is not None:
            self.model = model.astype(float)
        else:
            self.model = None

        if ss_model is not None:
            self.ss_model = ss_model.astype(float)
        else:
            self.ss_model = None

        if rr_model is not None:
            self.rr_model = rr_model.astype(float)
        else:
            self.rr_model = None

        self.flattening = flattening
        self.vp_res = float(vp_res)
        self.vs_res = float(vs_res)
        self.rho_res = float(rho_res)

        # solution
        self.free_surface = True
        self.penetration_filter = [False, 0.0]
        self.phase_filter = []

        # integration
        self.full_field = True
        self.slowness_window = [0.0, 0.0, 0.0, 0.0]
        self.wavenumber_integration_factor = 2.0
        self.aliasing_suppression_factor = 0.1

    def __repr__(self) -> str:
        return f"ConfigModel: model={self.model}, ss_model={self.ss_model}, rr_model={self.rr_model}, flattening={self.flattening}, vp_res={self.vp_res}, vs_res={self.vs_res}, rho_res={self.rho_res}"

    def solution(
        self,
        free_surface=True,
        penetration_filter=[False, 0.0],
        phase_filter=[],
    ) -> None:
        if free_surface not in [0, 1, 2]:
            raise ValueError(
                "Invalid solution configuration, free_surface must be 0, 1 or 2."
            )

        for i in range(len(phase_filter)):
            if phase_filter[i][2] not in ["P_up", "P_down", "S_up", "S_down"]:
                raise ValueError(
                    "Invalid solution configuration, phase_filter must be 'P_up', 'P_down', 'S_up' or 'S_down'."
                )

        self.free_surface = free_surface
        self.penetration_filter = penetration_filter
        self.phase_filter = phase_filter

    def integration(
        self,
        full_field=True,
        slowness_window=[0.0, 0.0, 0.0, 0.0],
        wavenumber_integration_factor=2.0,
        aliasing_suppression_factor=0.1,
    ) -> None:
        if full_field not in [0, 1, 2]:
            raise ValueError(
                "Invalid integration configuration, full_field must be 0, 1 or 2."
            )

        self.full_field = full_field
        self.slowness_window = slowness_window
        self.wavenumber_integration_factor = wavenumber_integration_factor
        self.aliasing_suppression_factor = aliasing_suppression_factor

    def plot(
        self,
        fig=["v", "rho", "q"],
        legend_loc="upper right",
        grid=True,
        figsize=(12, 6),
        show=True,
        save_path=None,
        dpi=100,
    ):
        fig_num = len(fig)
        _, ax = plt.subplots(1, fig_num, figsize=figsize)
        if fig_num == 1:
            ax = [ax]

        # plot
        for i in range(0, fig_num):
            # plot model
            if self.model is not None:
                depth_min = self.model[:, 0].min()
                depth_max = self.model[:, 0].max()
                if fig[i] == "v":
                    ax[i].plot(
                        self.model[:, 1], self.model[:, 0], color="#ff7f0e", label="Vp"
                    )
                    ax[i].plot(
                        self.model[:, 2], self.model[:, 0], color="#2ca02c", label="Vs"
                    )
                    ax[i].set_xlabel("V (km/s)")
                    ax[i].set_ylim([depth_min, depth_max])
                    ax[i].invert_yaxis()
                elif fig[i] == "rho":
                    ax[i].plot(
                        self.model[:, 3], self.model[:, 0], color="#7f7f7f", label="Rho"
                    )
                    ax[i].set_xlabel("Density (g/cm^3)")
                    ax[i].set_ylim([depth_min, depth_max])
                    ax[i].invert_yaxis()
                elif fig[i] == "q":
                    ax[i].plot(
                        self.model[:, 4], self.model[:, 0], color="#ff7f0e", label="Qp"
                    )
                    ax[i].plot(
                        self.model[:, 5], self.model[:, 0], color="#2ca02c", label="Qs"
                    )
                    ax[i].set_xlabel("Q")
                    ax[i].set_ylim([depth_min, depth_max])
                    ax[i].invert_yaxis()
                else:
                    raise ValueError("Invalid figure type.")
            elif self.ss_model is not None and self.rr_model is not None:
                depth_min = self.ss_model[:, 0].min()
                depth_max = self.ss_model[:, 0].max()
                if fig[i] == "v":
                    ax[i].plot(
                        self.ss_model[:, 1],
                        self.ss_model[:, 0],
                        color="#ff7f0e",
                        label="SS Vp",
                    )
                    ax[i].plot(
                        self.ss_model[:, 2],
                        self.ss_model[:, 0],
                        color="#2ca02c",
                        label="SS Vs",
                    )
                    ax[i].plot(
                        self.rr_model[:, 1],
                        self.rr_model[:, 0],
                        color="#1f77b4",
                        label="RR Vp",
                    )
                    ax[i].plot(
                        self.rr_model[:, 2],
                        self.rr_model[:, 0],
                        color="#d62728",
                        label="RR Vs",
                    )
                    ax[i].set_xlabel("V (km/s)")
                    ax[i].set_ylim([depth_min, depth_max])
                    ax[i].invert_yaxis()
                elif fig[i] == "rho":
                    ax[i].plot(
                        self.ss_model[:, 3],
                        self.ss_model[:, 0],
                        color="#7f7f7f",
                        label="SS Rho",
                    )
                    ax[i].plot(
                        self.rr_model[:, 3],
                        self.rr_model[:, 0],
                        color="#9467bd",
                        label="RR Rho",
                    )
                    ax[i].set_xlabel("Density (g/cm^3)")
                    ax[i].set_ylim([depth_min, depth_max])
                    ax[i].invert_yaxis()
                elif fig[i] == "q":
                    ax[i].plot(
                        self.ss_model[:, 4],
                        self.ss_model[:, 0],
                        color="#ff7f0e",
                        label="SS Qp",
                    )
                    ax[i].plot(
                        self.ss_model[:, 5],
                        self.ss_model[:, 0],
                        color="#2ca02c",
                        label="SS Qs",
                    )
                    ax[i].plot(
                        self.rr_model[:, 4],
                        self.rr_model[:, 0],
                        color="#1f77b4",
                        label="RR Qp",
                    )
                    ax[i].plot(
                        self.rr_model[:, 5],
                        self.rr_model[:, 0],
                        color="#d62728",
                        label="RR Qs",
                    )
                    ax[i].set_xlabel("Q")
                    ax[i].set_ylim([depth_min, depth_max])
                    ax[i].invert_yaxis()
                else:
                    raise ValueError("Invalid figure type.")

            # plot configuration
            if self.penetration_filter[0]:
                ax[i].axhline(
                    self.penetration_filter[1],
                    color="k",
                    linestyle="--",
                    label="Penetration",
                )

            # legend, grid
            ax[i].legend(loc=legend_loc, fontsize=8, shadow=True)
            if grid:
                ax[i].grid()

        # label
        ax[0].set_ylabel("Depth (km)")

        # show or save
        if not show:
            plt.close(fig)
        if save_path is not None:
            fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
        else:
            return ax
