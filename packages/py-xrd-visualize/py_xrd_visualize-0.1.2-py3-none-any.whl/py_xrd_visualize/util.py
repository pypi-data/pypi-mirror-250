import traceback
import sys
import io
import pathlib

import numpy as np
import scipy

import xrd_xy_parser.xy as xrdxy
from py_xrd_visualize.visualize import XY


def read_xy(target_file: io.TextIOBase | str | pathlib.Path) -> XY:
    """
    read file from `target_filename` ,and return x-y data.
    Parameters
    ---
    target_filename:xy-styled file name.

    Return
    ---
    x,y:
        x,y:np.ndarray

    Error
    ---
       If file not found, exit program.
    """
    try:
        return XY(*(xrdxy.read2xy(target_file)))
    except xrdxy.ParseError as e:
        traceback.print_exception(e)
        sys.exit(1)


def slide_XYs_linear(xys: list[XY], slide: float):
    for i, xy in enumerate(xys):
        xy.y += slide * i


def slide_XYs_log(xys: list[XY], slide: float, base: float = 1.0):
    for i, xy in enumerate(xys):
        xy.y = (xy.y + 1) * base * 10 ** (slide * i)


def gauss(x, amp, center, sigma):
    """
    parameter order:
        [amp, center, sigma]
    """
    return amp * np.exp(-((x - center) ** 2) / (2 * sigma**2))


def gauss_const_bg(x, amp, center, sigma, const_):
    """
    parameter order:
        [amp, center, sigma]
        const_:constant background
    """
    return amp * np.exp(-((x - center) ** 2) / (2 * sigma**2)) + const_


def __voigt(x, amp, center, gw, lw):
    """
    https://qiita.com/yamadasuzaku/items/4fccdc90fa13746af1e1

    Parameters:
        `amp` : amplitude
        `center `: center of Lorentzian line
        `gw` : sigma of the gaussian
        `lw` : FWHM of Lorentzian

    """

    z = (x - center + 1j * lw) / (gw * np.sqrt(2.0))
    w = scipy.special.wofz(z)
    y = amp * (w.real) / (gw * np.sqrt(2.0 * np.pi))
    return y
