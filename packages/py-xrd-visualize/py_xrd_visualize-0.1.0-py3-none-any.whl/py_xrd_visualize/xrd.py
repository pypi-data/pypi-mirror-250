from dataclasses import dataclass
from io import TextIOBase
from pathlib import Path
from typing import Callable

from matplotlib import ticker
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import numpy as np

from scipy.optimize import curve_fit

from py_xrd_visualize import util, visualize
from py_xrd_visualize.visualize import (
    XY,
    ax_conf_pass,
    ax_default_legends,
    axis_conf_func,
    fig_conf_func,
    fig_conf_pass,
    fig_conf_show,
    fig_func_label,
    multi_ax_func,
    multi_fig_func,
)


@dataclass()
class Scaned:
    path: Path
    legend: str
    scantime_s: float

    # paths: list[Union[str, Path]],


def fig_2θ_ω_1axis(
    paths: list[TextIOBase | str | Path],
    scantimes_sec: list[float],
    range_: tuple[float, float],
    ax_func: axis_conf_func = ax_conf_pass,
    fig_conf: fig_conf_func = fig_conf_pass,
    xlabel: str = "2θ(deg.)",
    ylabel: str = "Intensity(arb. unit)",
    legends: list[str] = [],
    legend_title: str = "",
    legend_reverse: bool = False,
    slide_exp: float = 2,
    slide_base: float = 1.0,
) -> Figure:
    xys: list[XY] = []
    for p in paths:
        xys.append(util.read_xy(p))

    # y unit: count per sec
    for xy, st in zip(xys, scantimes_sec):
        xy.y /= st

    # slide after reverse
    util.slide_XYs_log(xys, slide_exp, slide_base)

    def ax_func_xrd(ax: Axes):
        # y axis: log scale
        ax.yaxis.set_major_locator(ticker.LogLocator(10))
        # don't show y value
        ax.yaxis.set_major_formatter(ticker.NullFormatter())

    fig = visualize.arrange_row_1axis_nxy(
        xys=xys,
        ax_legends=ax_default_legends(legends, legend_title, legend_reverse),
        ax_func=multi_ax_func(
            visualize.arrange_row_default_conf(range_, xscale="linear", yscale="log"),
            ax_func_xrd,
            ax_func,
        ),
        fig_func=multi_fig_func(
            fig_func_label(xlabel, ylabel),
            fig_conf,
        ),
    )

    return fig


def fig_ω_scan_1axis(
    paths: list[TextIOBase | str | Path],
    amps: list[float],
    range_: tuple[float, float],
    ax_func: axis_conf_func = ax_conf_pass,
    fig_conf: fig_conf_func = fig_conf_pass,
    xlabel: str = "ω(deg.)",
    ylabel: str = "Intensity(arb. unit)",
    legends: list[str] = [],
    legend_title: str = "",
    legend_reverse: bool = False,
    optimize_func: Callable = util.gauss,
    show_optparam: bool = False,
) -> Figure:
    xys: list[XY] = []
    for p in paths:
        xys.append(util.read_xy(p))

    # shift x-axis to center roughly
    for xy in xys:
        x = xy.x
        x -= (x[0] + x[-1]) / 2.0

    # fitting
    p0s = []
    if optimize_func == util.gauss:
        for amp in amps:
            p0s.append([amp, 0, 1])

    popts = []
    for xy, p0 in zip(xys, p0s):
        popt, _ = curve_fit(optimize_func, xdata=xy.x, ydata=xy.y, p0=p0)
        [amp, center, sigma] = popt[0:3]

        xy.x -= center
        xy.y /= optimize_func(center, *popt)

        popts.append(popt)

    def ax_func_format(ax: Axes):
        # show range includes amp(=1.0),
        ax.set_ylim(ymin=0, ymax=2)

        # y axis: linear scale
        ax.yaxis.set_major_locator(ticker.LinearLocator())
        ax.yaxis.set_minor_locator(ticker.LinearLocator(21))

        # don't show y value
        ax.yaxis.set_major_formatter(ticker.NullFormatter())

    def fig_func_opt(fig: Figure):
        if not show_optparam:
            return

        ax = fig.axes[0]
        for popt, legend in zip(popts, legends):
            x = np.linspace(*range_)
            # center(x)=0
            y = np.vectorize(optimize_func)(x, popt[0], 0, *popt[2:])
            # y=1 on x=0
            y /= np.max(y)

            # plot fit curve
            ax.plot(x, y)

            [amp, center, sigma] = popt[0:3]
            annote = "{}::amp:{:#.3g},center:{:#.3g},sigma:{:#.3g},HWFM:{:#.3g}".format(
                legend, amp, center, sigma, sigma * 2.355
            )
            ax.annotate(
                annote,
                xy=(sigma, 0.3 + 0.3 * sigma),
                horizontalalignment="left",
                verticalalignment="baseline",
            )
        print("optimized param")
        for popt, legend in zip(popts, legends):
            print(f"{legend}:{popt}")

        fig.suptitle("fit:{}".format(optimize_func.__name__))

    fig = visualize.arrange_row_1axis_nxy(
        xys=xys,
        ax_legends=ax_default_legends(legends, legend_title, legend_reverse),
        ax_func=multi_ax_func(
            visualize.arrange_row_default_conf(
                range_, xscale="linear", yscale="linear"
            ),
            ax_func_format,
            ax_func,
        ),
        fig_func=multi_fig_func(
            fig_conf,
            fig_func_label(xlabel, ylabel),
            fig_func_opt,
            fig_conf_show(),
        ),
    )

    return fig
