# -*- coding: utf-8 -*-
"""
This module shows a few doc string examples for how
to write doc strings for automatic Sphinx documentation.

This module will eventually be deleted once all developers
understand doc strings and the syntax for sphinx.

The following is a good resources
    https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html
    
    https://thomas-cokelaer.info/tutorials/sphinx/docstring_python.html
"""





def add(a: [float, int], b: [float, int]) -> float:
    """
    This function adds two values a and b.

    :param a: value a
    :type a: float, int
    :param b: value b
    :type b: float, int
    :return: a + b
    :rtype: float
    
    
    :Example:
        
    >>> import mooonpy
    >>> c = mooonpy.doc_examples.add(a: float 1.123, b: int 10)
    >>> print(c)
    11.123
    
    .. note:: can be useful to emphasize
        important feature
        
    .. seealso:: :func:`subtract`, :func:`multiply`, :func:`divide`
    
    .. warning:: a and b must be floats or ints.
    
    .. todo::
        - check that a and b are floats or ints.
        - add raises examples.
    """
    return float(a + b)


def subtract(a: [float, int], b: [float, int]) -> float:
    """
    This function subtracts two values a and b.

    :param a: value a
    :type a: float, int
    :param b: value b
    :type b: float, int
    :return: a - b
    :rtype: float
    
    :Example:
        
    >>> import mooonpy
    >>> c = mooonpy.doc_examples.subtract(a: float 1.123, b: int 10)
    >>> print(c)
    -8.877
    
    .. note:: can be useful to emphasize
        important feature
        
    .. seealso:: :func:`add`, :func:`multiply`, :func:`divide`
    
    .. warning:: a and b must be floats or ints.
    
    .. todo:: 
        - check that a and b are floats or ints.
        - add raises examples.
    """
    return float(a - b)


def multiply(a: [float, int], b: [float, int]) -> float:
    """
    This function multiplies two values a and b.

    :param a: value a
    :type a: float, int
    :param b: value b
    :type b: float, int
    :raises TypeError: If a or b are not of type float or int.
    :return: a*b
    :rtype: float
    
    **Bullet list**:
        - This section might be useful
        - But who knows what to put here
        
    :Example:
        
    >>> import mooonpy
    >>> c = mooonpy.doc_examples.multiply(a: float 1.123, b: int 10)
    >>> print(c)
    11.23
    
    .. note:: can be useful to emphasize
        important feature
        
    .. seealso:: :func:`subtract` :func:`add` :func:`divide`
    """
    if not isinstance(a, (int, float)):
        raise TypeError(f' a={a} is not of type int or float')
        
    if not isinstance(b, (int, float)):
        raise TypeError(f' b={b} is not of type int or float')
    return float(a*b)


def divide(a: [float, int], b: [float, int]) -> float:
    """
    This function divides two values a and b.

    :param a: a parameter
    :type a: float, int
    :param b: b parameter
    :type b: float, int
    :raises TypeError: If a or b are not of type float or int.
    :raises ZeroDivisionError: if b = 0.
    :return: a/b
    :rtype: float
    
    **Bullet list**:
        - This section might be useful
        - But who knows what to put here
        
    :Example:
        
    >>> import mooonpy
    >>> c = mooonpy.doc_examples.divide(a: float 1.123, b: int 10)
    >>> print(c)
    0.1123
    
    .. note:: can be useful to emphasize
        important feature
        
    .. seealso:: :func:`subtract` :func:`add` :func:`multiply`
    """
    if not isinstance(a, (int, float)):
        raise TypeError(f' a={a} is not of type int or float')
        
    if not isinstance(b, (int, float)):
        raise TypeError(f' b={b} is not of type int or float')
        
    if b == 0:
        raise ZeroDivisionError(' b={b}. Can not divide by zero')
    return float(a*b)

def latex(alpha: str) -> None:
    """
    This function prints the alpha (:math:`\\alpha`) parameter and shows how to use latex symbols.

    :param alpha: alpha parameter
    :type alpha: str
    :return: None
    :rtype: None
    """
    print(alpha)
    return None


def useful_docstring() -> None:    
    """
    This is a longer explanation, which may include math with latex syntax
    :math:`\\alpha`.
    Then, you need to provide optional subsection in this order (just to be
    consistent and have a uniform documentation. Nothing prevent you to
    switch the order):

      - parameters using ``:param <name>: <description>``
      - type of the parameters ``:type <name>: <description>``
      - returns using ``:returns: <description>``
      - examples (doctest)
      - seealso using ``.. seealso:: text``
      - notes using ``.. note:: text``
      - warning using ``.. warning:: text``
      - todo ``.. todo:: text``
    """
    return None

def butter(N, Wn, btype='low', analog=False, output='ba', fs=None):
    """
    Butterworth digital and analog filter design.

    Design an Nth-order digital or analog Butterworth filter and return
    the filter coefficients.

    Parameters
    ----------
    N : int
        The order of the filter. For 'bandpass' and 'bandstop' filters,
        the resulting order of the final second-order sections ('sos')
        matrix is ``2*N``, with `N` the number of biquad sections
        of the desired system.
    Wn : array_like
        The critical frequency or frequencies. For lowpass and highpass
        filters, Wn is a scalar; for bandpass and bandstop filters,
        Wn is a length-2 sequence.

        For a Butterworth filter, this is the point at which the gain
        drops to 1/sqrt(2) that of the passband (the "-3 dB point").

        For digital filters, if `fs` is not specified, `Wn` units are
        normalized from 0 to 1, where 1 is the Nyquist frequency (`Wn` is
        thus in half cycles / sample and defined as 2*critical frequencies
        / `fs`). If `fs` is specified, `Wn` is in the same units as `fs`.

        For analog filters, `Wn` is an angular frequency (e.g. rad/s).
    btype : {'lowpass', 'highpass', 'bandpass', 'bandstop'}, optional
        The type of filter.  Default is 'lowpass'.
    analog : bool, optional
        When True, return an analog filter, otherwise a digital filter is
        returned.
    output : {'ba', 'zpk', 'sos'}, optional
        Type of output:  numerator/denominator ('ba'), pole-zero ('zpk'), or
        second-order sections ('sos'). Default is 'ba' for backwards
        compatibility, but 'sos' should be used for general-purpose filtering.
    fs : float, optional
        The sampling frequency of the digital system.

        .. versionadded:: 1.2.0

    Returns
    -------
    b, a : ndarray, ndarray
        Numerator (`b`) and denominator (`a`) polynomials of the IIR filter.
        Only returned if ``output='ba'``.
    z, p, k : ndarray, ndarray, float
        Zeros, poles, and system gain of the IIR filter transfer
        function.  Only returned if ``output='zpk'``.
    sos : ndarray
        Second-order sections representation of the IIR filter.
        Only returned if ``output='sos'``.

    See Also
    --------
    buttord, buttap

    Notes
    -----
    The Butterworth filter has maximally flat frequency response in the
    passband.

    The ``'sos'`` output parameter was added in 0.16.0.

    If the transfer function form ``[b, a]`` is requested, numerical
    problems can occur since the conversion between roots and
    the polynomial coefficients is a numerically sensitive operation,
    even for N >= 4. It is recommended to work with the SOS
    representation.

    .. warning::
        Designing high-order and narrowband IIR filters in TF form can
        result in unstable or incorrect filtering due to floating point
        numerical precision issues. Consider inspecting output filter
        characteristics `freqz` or designing the filters with second-order
        sections via ``output='sos'``.

    Examples
    --------
    Design an analog filter and plot its frequency response, showing the
    critical points:

    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np

    >>> b, a = signal.butter(4, 100, 'low', analog=True)
    >>> w, h = signal.freqs(b, a)
    >>> plt.semilogx(w, 20 * np.log10(abs(h)))
    >>> plt.title('Butterworth filter frequency response')
    >>> plt.xlabel('Frequency [rad/s]')
    >>> plt.ylabel('Amplitude [dB]')
    >>> plt.margins(0, 0.1)
    >>> plt.grid(which='both', axis='both')
    >>> plt.axvline(100, color='green') # cutoff frequency
    >>> plt.show()

    Generate a signal made up of 10 Hz and 20 Hz, sampled at 1 kHz

    >>> t = np.linspace(0, 1, 1000, False)  # 1 second
    >>> sig = np.sin(2*np.pi*10*t) + np.sin(2*np.pi*20*t)
    >>> fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    >>> ax1.plot(t, sig)
    >>> ax1.set_title('10 Hz and 20 Hz sinusoids')
    >>> ax1.axis([0, 1, -2, 2])

    Design a digital high-pass filter at 15 Hz to remove the 10 Hz tone, and
    apply it to the signal. (It's recommended to use second-order sections
    format when filtering, to avoid numerical error with transfer function
    (``ba``) format):

    >>> sos = signal.butter(10, 15, 'hp', fs=1000, output='sos')
    >>> filtered = signal.sosfilt(sos, sig)
    >>> ax2.plot(t, filtered)
    >>> ax2.set_title('After 15 Hz high-pass filter')
    >>> ax2.axis([0, 1, -2, 2])
    >>> ax2.set_xlabel('Time [s]')
    >>> plt.tight_layout()
    >>> plt.show()
    """
    return None


class MainClass1(object):
    """This class docstring shows how to use sphinx and rst syntax

    The first line is brief explanation, which may be completed with 
    a longer one. For instance to discuss about its methods. The only
    method here is :func:`function1`'s. The main idea is to document
    the class and methods's arguments with 

    - **parameters**, **types**, **return** and **return types**::

          :param arg1: description
          :param arg2: description
          :type arg1: type description
          :type arg1: type description
          :return: return description
          :rtype: the return type description

    - and to provide sections such as **Example** using the double commas syntax::

          :Example:

          followed by a blank line !

      which appears as follow:

      :Example:

      followed by a blank line

    - Finally special sections such as **See Also**, **Warnings**, **Notes**
      use the sphinx syntax (*paragraph directives*)::

          .. seealso:: blabla
          .. warnings also:: blabla
          .. note:: blabla
          .. todo:: blabla

    .. note::
        There are many other Info fields but they may be redundant:
            * param, parameter, arg, argument, key, keyword: Description of a
              parameter.
            * type: Type of a parameter.
            * raises, raise, except, exception: That (and when) a specific
              exception is raised.
            * var, ivar, cvar: Description of a variable.
            * returns, return: Description of the return value.
            * rtype: Return type.

    .. note::
        There are many other directives such as versionadded, versionchanged,
        rubric, centered, ... See the sphinx documentation for more details.

    Here below is the results of the :func:`function1` docstring.

    """

    def function1(self, arg1, arg2, arg3):
        """returns (arg1 / arg2) + arg3

        This is a longer explanation, which may include math with latex syntax
        :math:`\\alpha`.
        Then, you need to provide optional subsection in this order (just to be
        consistent and have a uniform documentation. Nothing prevent you to
        switch the order):

          - parameters using ``:param <name>: <description>``
          - type of the parameters ``:type <name>: <description>``
          - returns using ``:returns: <description>``
          - examples (doctest)
          - seealso using ``.. seealso:: text``
          - notes using ``.. note:: text``
          - warning using ``.. warning:: text``
          - todo ``.. todo:: text``

        **Advantages**:
         - Uses sphinx markups, which will certainly be improved in future
           version
         - Nice HTML output with the See Also, Note, Warnings directives


        **Drawbacks**:
         - Just looking at the docstring, the parameter, type and  return
           sections do not appear nicely

        :param arg1: the first value
        :param arg2: the first value
        :param arg3: the first value
        :type arg1: int, float,...
        :type arg2: int, float,...
        :type arg3: int, float,...
        :returns: arg1/arg2 +arg3
        :rtype: int, float

        :Example:

        >>> import template
        >>> a = template.MainClass1()
        >>> a.function1(1,1,1)
        2

        .. note:: can be useful to emphasize
            important feature
        .. seealso:: :class:`MainClass2`
        .. warning:: arg2 must be non-zero.
        .. todo:: check that arg2 is non zero.
        """
        return arg1/arg2 + arg3
