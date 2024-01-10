import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


def maskplot(
    stream,
    t_begin=0,
    duration=10,
    t_extra=1,
    beachball_fontsize=6,
    markersize=3,
    markeredgewidth=0.5,
    starttime=None,
    endtime=None,
    starttrace=None,
    endtrace=None,
    norm_method="stream",  # trace or stream
    amp_scale=1,
    time_axis="x",
    invert_x=False,
    invert_y=False,
    time_minticks=5,
    time_maxticks=None,
    timetick_rotation=0,
    timetick_labelsize=10,
    trace_ticks=5,
    tracetick_rotation=0,
    tracetick_labelsize=10,
    trace_label="trace",  # 'trace' or 'distance'
    ax=None,
    color="black",
    linewidth=1,
    linestyle="-",
    alpha=1,
    fillcolors=(None, None),
    fillalpha=0.5,
    grid_color="black",
    grid_linewidth=0.5,
    grid_linestyle=":",
    grid_alpha=1,
    figsize=(10, 5),
    show=True,
    save_path=None,
    dpi=100,
):
    """
    Plot the data in the stream.
    waveform
    wiggles
    """
    # mask data
    trace_num = stream.stats.trace_num
    sampling_rate = stream.stats.sampling_rate
    mask = np.full((trace_num, stream.stats.npts), True)
    t_p = stream.stats.notes["t_p"]
    for i in range(trace_num):
        t_start = t_p[i] + t_begin
        if t_start < 0:
            t_start = 0
        n_mask_start = int(t_start * sampling_rate)
        n_mask_end = int((t_start + t_extra * i + duration) * sampling_rate)
        mask[i, n_mask_start:n_mask_end] = False

    self = stream

    # check starttime and endtime
    if starttime is None:
        starttime = self.stats.starttime
    if starttime < self.stats.starttime:
        raise ValueError("starttime must be greater than or equal to stream starttime.")
    if endtime is None:
        endtime = self.stats.endtime
    if endtime > self.stats.endtime:
        raise ValueError("endtime must be less than or equal to stream endtime.")

    # check starttrace and endtrace
    if starttrace is None:
        starttrace = int(0)
    if starttrace < 0:
        raise ValueError("starttrace must be greater than or equal to 0.")
    if endtrace is None:
        endtrace = int(self.stats.trace_num)
    if endtrace > self.stats.trace_num:
        raise ValueError("endtrace must be less than or equal to stream trace_num.")

    # init win_axis
    if time_axis == "x":
        trace_axis = "y"
    elif time_axis == "y":
        trace_axis = "x"
    else:
        raise ValueError("trace_axis must be 'x' or 'y'")

    # check trace_label
    if trace_label not in ["trace", "interval", "distance"]:
        raise ValueError("trace_label must be 'trace', 'interval' or 'distance'")

    # set times
    total_npts_times = self.times(type="datetime")
    starttime_npts = int((starttime - self.stats.starttime) * self.stats.sampling_rate)
    endtime_npts = int((endtime - self.stats.starttime) * self.stats.sampling_rate)
    npts_times = total_npts_times[starttime_npts:endtime_npts]

    # data
    data = np.ma.masked_array(self.data, mask)[
        starttrace:endtrace, starttime_npts:endtime_npts
    ]
    if norm_method == "trace":
        data = data / (np.max(np.abs(data), axis=1, keepdims=True) * 2)
    elif norm_method == "stream":
        data = data / (np.max(np.abs(data)) * 2)
    else:
        raise ValueError("norm_method must be 'trace' or 'stream'")

    # set ax
    ax = _get_ax(ax, figsize=figsize)

    # plot data
    for i in range(0, endtrace - starttrace):
        shift = i + starttrace
        if time_axis == "x":
            ax.plot(
                npts_times,
                data[i, :] * amp_scale + shift,
                linewidth=linewidth,
                color=color,
                alpha=alpha,
                linestyle=linestyle,
            )
            if fillcolors[0] is not None:
                ax.fill_between(
                    npts_times,
                    data[i, :] * amp_scale + shift,
                    shift,
                    where=data[i, :] * amp_scale + shift > shift,
                    facecolor=fillcolors[0],
                    alpha=fillalpha,
                )
            if fillcolors[1] is not None:
                ax.fill_between(
                    npts_times,
                    data[i, :] * amp_scale + shift,
                    shift,
                    where=data[i, :] * amp_scale + shift < shift,
                    facecolor=fillcolors[1],
                    alpha=fillalpha,
                )
            # plot t_p, t_s
            t_p = stream.stats.notes["t_p"][shift]
            t_s = stream.stats.notes["t_s"][shift]
            tp_npts_n = int(t_p * stream.stats.sampling_rate)
            ts_npts_n = int(t_s * stream.stats.sampling_rate)
            ax.plot(
                total_npts_times[tp_npts_n],
                shift,
                linestyle="none",
                marker="o",
                markersize=markersize,
                markerfacecolor="#ff7f0e",
                markeredgewidth=markeredgewidth,
                markeredgecolor="black",
            )
            ax.plot(
                total_npts_times[ts_npts_n],
                shift,
                linestyle="none",
                marker="o",
                markersize=markersize,
                markerfacecolor="#2ca02c",
                markeredgewidth=markeredgewidth,
                markeredgecolor="black",
            )
        elif time_axis == "y":
            ax.plot(
                data[i, :] * amp_scale + shift,
                npts_times,
                linewidth=linewidth,
                color=color,
                alpha=alpha,
                linestyle=linestyle,
            )
            if fillcolors[0] is not None:
                ax.fill_betweenx(
                    npts_times,
                    data[i, :] * amp_scale + shift,
                    shift,
                    where=data[i, :] * amp_scale + shift > shift,
                    facecolor=fillcolors[0],
                    alpha=fillalpha,
                )
            if fillcolors[1] is not None:
                ax.fill_betweenx(
                    npts_times,
                    data[i, :] * amp_scale + shift,
                    shift,
                    where=data[i, :] * amp_scale + shift < shift,
                    facecolor=fillcolors[1],
                    alpha=fillalpha,
                )
            # plot t_p, t_s
            t_p = stream.stats.notes["t_p"][shift]
            t_s = stream.stats.notes["t_s"][shift]
            tp_npts_n = int(t_p * stream.stats.sampling_rate)
            ts_npts_n = int(t_s * stream.stats.sampling_rate)
            ax.plot(
                shift,
                total_npts_times[tp_npts_n],
                linestyle="none",
                marker="o",
                markersize=markersize,
                markerfacecolor="#ff7f0e",
                markeredgewidth=markeredgewidth,
                markeredgecolor="black",
            )
            ax.plot(
                shift,
                total_npts_times[ts_npts_n],
                linestyle="none",
                marker="o",
                markersize=markersize,
                markerfacecolor="#2ca02c",
                markeredgewidth=markeredgewidth,
                markeredgecolor="black",
            )
        else:
            raise ValueError("time_axis must be 'x' or 'y'")

    # grid
    ax.grid(
        color=grid_color,
        linewidth=grid_linewidth,
        linestyle=grid_linestyle,
        alpha=grid_alpha,
    )

    # format axis
    _format_time_axis(
        ax,
        axis=time_axis,
        tick_rotation=timetick_rotation,
        minticks=time_minticks,
        maxticks=time_maxticks,
        labelsize=timetick_labelsize,
    )
    _format_trace_axis(
        ax,
        trace_label,
        self,
        starttrace,
        endtrace,
        trace_ticks,
        trace_axis,
        tracetick_rotation,
        tracetick_labelsize,
    )

    # legend
    ax.plot(
        [],
        [],
        linestyle="none",
        marker="o",
        markersize=markersize,
        markerfacecolor="#ff7f0e",
        markeredgewidth=markeredgewidth,
        markeredgecolor="black",
        label="t_p",
    )
    ax.plot(
        [],
        [],
        linestyle="none",
        marker="o",
        markersize=markersize,
        markerfacecolor="#2ca02c",
        markeredgewidth=markeredgewidth,
        markeredgecolor="black",
        label="t_s",
    )
    ax.legend(loc="upper right", fontsize=8, shadow=False)

    # label
    if time_axis == "x":
        ax.set_xlim(starttime.datetime, endtime.datetime)
        if trace_label == "trace":
            ax.set_ylabel("Trace")
        elif trace_label == "distance":
            if self.stats.notes["unit"] == "km":
                ax.set_ylabel("Distance(km)")
            elif self.stats.notes["unit"] == "deg":
                ax.set_ylabel("Distance(deg)")
    elif time_axis == "y":
        ax.set_ylim(starttime.datetime, endtime.datetime)
        if trace_label == "trace":
            ax.set_xlabel("Trace")
        elif trace_label == "distance":
            if self.stats.notes["unit"] == "km":
                ax.set_xlabel("Distance(km)")
            elif self.stats.notes["unit"] == "deg":
                ax.set_xlabel("Distance(deg)")

    if invert_x:
        ax.invert_xaxis()
    if invert_y:
        ax.invert_yaxis()

    # beachball
    fig = ax.figure
    width = figsize[0]
    height = figsize[1]
    ax0 = fig.add_subplot(8, int(7 * width / height), 1)
    ax0 = stream.stats.notes["source"].beachball(ax=ax0, fontsize=beachball_fontsize)
    ax0.set_xlim(-0.2, 1.2)
    ax0.set_ylim(-0.2, 1.2)

    if not show:
        plt.close(fig)
    if save_path is not None:
        fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
    else:
        return ax, ax0


def _get_ax(ax, figsize=None, **kwargs):
    """Get an axis if ax is None"""
    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=figsize, **kwargs)
    return ax


def _format_time_axis(
    ax, axis="x", tick_rotation=0, minticks=5, maxticks=None, labelsize=10
):
    locator = mdates.AutoDateLocator(tz="UTC", minticks=minticks, maxticks=maxticks)
    formatter = mdates.ConciseDateFormatter(locator)
    formatter.formats = [
        "%y",  # ticks are mostly years
        "%b",  # ticks are mostly months
        "%d",  # ticks are mostly days
        "%H:%M",  # hrs
        "%H:%M",  # min
        "%H:%M:%S.%f",
    ]  # secs

    formatter.zero_formats = [
        "",
        "%Y",
        "%b",
        "%b-%d",
        "%H:%M",
        "%H:%M:%S.%f",
    ]

    formatter.offset_formats = [
        "",
        "%Y",
        "%Y-%m",
        "%Y-%m-%d",
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
    ]
    if axis.lower() == "x":
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
    elif axis.lower() == "y":
        ax.yaxis.set_major_locator(locator)
        ax.yaxis.set_major_formatter(formatter)
    ax.tick_params(axis=axis.lower(), rotation=tick_rotation, labelsize=labelsize)


def _format_trace_axis(
    ax,
    trace_label,
    self,
    starttrace,
    endtrace,
    trace_ticks,
    trace_axis,
    tracetick_rotation,
    tracetick_labelsize,
):
    if trace_ticks > (endtrace - starttrace - 1):
        trace_ticks = round(endtrace - starttrace - 1)
    ticks = np.linspace(starttrace, endtrace - 1, num=trace_ticks)

    if trace_label == "trace":
        labels = np.round(
            np.linspace(starttrace, endtrace - 1, num=trace_ticks)
        ).astype(int)
    elif trace_label == "distance":
        index = np.round(np.linspace(starttrace, endtrace - 1, num=trace_ticks)).astype(
            int
        )
        labels = np.array(self.stats.notes["distance"])[index]
    else:
        raise ValueError("trace_label must be 'trace', 'interval', or 'distance'")

    if trace_axis == "x":
        ax.set_xticks(ticks)
        ax.set_xticklabels(labels)
    elif trace_axis == "y":
        ax.set_yticks(ticks)
        ax.set_yticklabels(labels)
    else:
        raise ValueError("trace_axis must be 'x' or 'y'")

    ax.tick_params(
        axis=trace_axis, rotation=tracetick_rotation, labelsize=tracetick_labelsize
    )
