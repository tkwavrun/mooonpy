# -*- coding: utf-8 -*-
import numpy as np
import scipy as sp

from numbers import Number
from typing import Union, Tuple, Optional

Array1D = Union[np.ndarray, list]


def aggregate_fun(fun_name: str, vector: Array1D) -> Number:
    """
    Apply generic aggregate functions to a vector, similar to the bottom row of a spreadsheet.
    Modes control values to be ignored in operation, by slicing the vector before the operation.

    Note that operating on an empty sclice will return a np.nan.

    **Currently supported Operators: fun_name must start with one of these substrings**
        - sum: Summation
        - avg: Arithmetic mean
        - std: Standard Deviation

    **Currently supported Modes: if fun_name ends with one of these substrings, the rule is applied**
        -0: Ignores 0's
        -None: Ignores None or nan

    :param fun_name: Selection of Function and Mode.
    :type fun_name: str
    :param vector: row or column vector to operate on.
    :type vector: list or numpy array
    :return: Result of operation.
    :rtype: Number

    :Example:
        >>> from mooonpy.tools import aggregate_fun
        >>> MyVect = [0,1,2]
        >>> avg_no0 = aggregate_fun('avg0', MyVect)
        1.5
        >>> avg_all = aggregate_fun('avg', MyVect)
        1.0
    """
    # Do sclicing for Mode rules
    if fun_name.endswith('0'):
        slice_ = np.nonzero(vector)
        if len(slice_) == 0:
            return np.nan
    elif fun_name.endswith('None'):
        slice_ = np.logical_not(np.isnan(vector))
        if len(slice_) == 0:
            return np.nan
    else:
        slice_ = True

    # Compute aggregate
    if fun_name.startswith('sum'):
        return np.sum(vector[slice_])
    elif fun_name.startswith('avg'):
        return np.mean(vector[slice_])
    elif fun_name.startswith('std'):
        return np.std(vector[slice_])
    else:
        raise Exception(f'ERROR: fun_name {fun_name} not recognized')


def compute_PSD(xdata: Array1D, ydata: Array1D) -> Tuple[Array1D, Array1D]:
    """
    Compute the Power Spectral Density (PSD) with the X-values being the normalized frequencies.

    Returns the normalized frequencies (Omega N / Wn) and power spectral density (PSD) as a tuple of arrays.

    :param xdata: Array of x values.
    :type xdata: Array1D
    :param ydata: Array of y values.
    :type ydata: Array1D
    :return: Wnss, PDS's
    :rtype: Tuple(Array1D, Array1D)
    """
    # Define sampling rate and number of data points
    dx = np.mean(np.abs(np.diff(xdata)))
    if dx != 0:
        fs = 1 / dx  # sampling rate
    else:
        fs = xdata.shape[0] / (np.max(xdata) - np.min(xdata))
    N = xdata.shape[0]  # number of data points
    d = 1 / fs  # sampling space

    # Perform one sided FFT
    fft_response = np.fft.rfft(ydata, axis=0, norm='backward')
    x_fft = np.fft.rfftfreq(N, d=d)
    y_fft = fft_response

    # Compute the final PSD and normalized cutoff frequencies
    psd = np.real((y_fft * np.conjugate(y_fft)) / N)
    wns = x_fft / (0.5 * fs)
    return wns, psd


def power_to_db(power: Array1D, ref_power: Number = 1) -> np.ndarray:
    """
    Convert power to decibels (dB).

    :param power: Power to convert.
    :type power: Array1D
    :param ref_power: Reference power.
    :type ref_power: Number
    :return: Converted power.
    :rtype: Array1D
    """
    power_in_dB = 10 * np.log10(power / ref_power)
    return power_in_dB


def find_peaks_and_valleys(xdata: Array1D, ydata: Array1D, prominence: Optional[Number] = None) -> Tuple[
    np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute the peaks and valleys of a curve using a specified prominence for cutoff.

    :param xdata: Array of x values. Must be increasing monotonically.
    :type xdata: Array1D
    :param ydata: Array of y values.
    :type ydata: Array1D
    :param prominence: Prominence for cutoff
    :type prominence: Number or None

    :return: X peaks, Y peaks, X valleys, Y valleys
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]

    .. TODO::
        make an example image
    """
    # Find peaks
    peaks, properties = find_peaks(ydata, prominence=prominence)
    xpeaks = xdata[peaks];
    ypeaks = ydata[peaks]

    # Find valleys
    xvalleys, yvalleys = [], []
    if len(xpeaks) >= 2 and len(ypeaks) >= 2:
        for i in range(len(peaks) - 1):
            lo = peaks[i];
            hi = peaks[i + 1];
            between_peaksx = xdata[lo:hi]
            between_peaksy = ydata[lo:hi]
            minimum_index = np.min(np.where(between_peaksy == between_peaksy.min())[0])
            xvalleys.append(between_peaksx[minimum_index])
            yvalleys.append(between_peaksy[minimum_index])
    xvalleys = np.array(xvalleys)
    yvalleys = np.array(yvalleys)
    return xpeaks, ypeaks, xvalleys, yvalleys


def compute_derivative(xdata: Array1D, ydata: Array1D) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Function to compute the 1st and 2nd order central derivatives. Edges are not considered, and trimmed x array is returned.

    :param xdata: Array of x values.
    :type xdata: Array1D
    :param ydata: Array of y values.
    :type ydata: Array1D
    :return: Trimmed x, 1st derivative, 2nd derivative
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray

    .. TODO::
        make an example image
    """
    dxn = xdata[1:-1]  # ignore first and last point
    dy1 = np.zeros_like(dxn)
    dy2 = np.zeros_like(dxn)
    if len(xdata) == len(ydata):
        for i in range(1, len(xdata) - 1):
            dx = (xdata[i + 1] - xdata[i - 1]) / 2
            if dx == 0:
                print(
                    'WARNING finite difference dx was zero at x={}. Derivative was set to zero to avoid infinite derivative.'.format(
                        xdata[i]))
            else:
                dy1[i - 1] = (ydata[i + 1] - ydata[i - 1]) / (2 * dx)
                dy2[i - 1] = (ydata[i + 1] - 2 * ydata[i] + ydata[i - 1]) / (dx * dx)
    else:
        print('ERROR (compute_derivative) inconsistent number of data points between X and Y arrays')
    return dxn, dy1, dy2


def compute_fringe_slope(strain: Array1D, stress: Array1D, min_strain: Optional[Number] = None,
                         max_strain: Optional[Number] = None, direction: str = 'forward'):
    """
    Compute fringe slope

    .. TODO::
        Most concice writeup and a link to the paper

    :param strain: Strain
    :type strain: Array1D
    :param stress: Stress
    :type stress: Array1D
    :param min_strain: Minimum strain, defaults to None to use minimum index
    :type min_strain: Optional(Number)
    :param max_strain: Maximum strain, defaults to None to use maximum index
    :type max_strain: Optional(Number)
    :param direction: Direction, Must be 'forward' or 'backward', flips both vectors, defaults to 'forward'.
    :type direction: str
    """
    # Set direction
    if direction == 'forward':
        strain = strain.copy()
        stress = stress.copy()
    elif direction == 'reverse':
        strain = np.flip(strain.copy())
        stress = np.flip(stress.copy())
    else:
        raise Exception(
            f'ERROR direction={direction} is not supported. Supported directions are "forward" or "reverse"')

    # Set defaults if min_strain or max_strain are None
    if min_strain is None: min_strain = min(strain)
    if max_strain is None: max_strain = max(strain)

    # Start the walked linear regression method
    slopes, fringe = [], []
    sum_xi, sum_yi, sum_xi_2, sum_yi_2, sum_xi_yi, n = 0, 0, 0, 0, 0, 0
    for x, y in zip(strain, stress):
        # Compute cumulative linear regression parameters
        sum_xi += x
        sum_yi += y
        n += 1
        sum_xi_2 += x * x
        sum_yi_2 += y * y
        sum_xi_yi += x * y

        # Need at least 2 points to perform linear regression
        if n <= 3: continue

        # Only compute outputs if x is in the desired range
        if min_strain <= x <= max_strain:
            SSxy = sum_xi_yi - (sum_xi * sum_yi / n)
            SSxx = sum_xi_2 - (sum_xi * sum_xi / n)
            b1 = SSxy / SSxx

            slopes.append(b1)
            fringe.append(x)
    return np.array(fringe), np.array(slopes)
