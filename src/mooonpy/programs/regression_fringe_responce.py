# -*- coding: utf-8 -*-
from ..tools.math_utils import compute_fringe_slope, compute_derivative, find_peaks_and_valleys
from ..tools.signals import butter_lowpass, compute_PSD
from .program import ProgramResults

import numpy as np
from numpy.polynomial.polynomial import polyfit
import matplotlib.pyplot as plt


def RFR_tensile_analysis(strain, stress, trans_1=None, trans_2=None, min_xhi=None, max_xhi=None, wn='PSD', order=2,
                         qm='msr', log=None, plots='all') -> ProgramResults:
    try:
        # --------------------------------------------
        # Setup
        results = ProgramResults('RFR_tensile_analysis')
        results.program_version = '1.0: 01-Jul-25'
        if log is None:
            log = ProgramResults.new_log()  # just a list currently

        results.input_settings = {'min_xhi': min_xhi, 'max_xhi': max_xhi, 'wn': wn, 'order': order, 'qm': qm}
        axies = rfr_plotter(plots)

        # --------------------------------------------
        # Filtering
        if wn == 'off':
            stress_filt = stress
            # results.stress_filt = stress
            results.stress_wn = '1.0'
            results.stress_qm = '1,1'
        else:
            stress_filt, stress_wn, stress_qm = butter_lowpass(strain, stress, wn=wn, order=order, quadrant=qm)
            # results.stress_filt = stress_filt
            results.stress_wn = stress_wn
            results.stress_qm = stress_qm

        # --------------------------------------------
        # enable or disable shifting?
        # Shift all data by the "minimum before the maximum" to remove any residual
        # stress. The "minimum before the maximum" allows for fracture to occur where
        # the minimum stress is near zero strain and not maximum strain (in case fracture
        # creates a minimum stress lower than the residual stress).
        max_index = np.min(np.where(stress_filt == np.max(stress_filt))[0])
        min_stress = np.min(stress_filt[:max_index])
        stress_filt -= min_stress
        stress -= min_stress
        results.offset = -min_stress
        results.stress_filt = stress_filt

        if axies['plt_stress'] is not None:
            axies['plt_stress'].plot(strain, stress, alpha=0.25, label='Raw stress')
            axies['plt_stress'].plot(strain, stress_filt, linewidth=2, label='Filtered stress')

        # --------------------------------------------
        # Determine Linear region
        lo, mid, hi, fr2_fringe, fr2_slopes = _forward_backward_forward(strain, stress_filt, min_xhi, max_xhi,
                                                                        _plt_fbf=axies['plt_fbf'])
        results.lox = lo[0]
        results.loy = lo[1]
        results.midx = mid[0]
        results.mixy = mid[1]
        results.hix = hi[0]
        results.hiy = hi[1]

        if axies['plt_stress'] is not None:
            axies['plt_stress'].plot([lo[0], hi[0]], [lo[1], hi[1]], 'go', label='Linear region')

        lo_index = np.argmin(np.abs(strain - lo[0]))
        hi_index = np.argmin(np.abs(strain - hi[0]))
        youngs_modulus_coeffs = polyfit(strain[lo_index:hi_index + 1], stress_filt[lo_index:hi_index + 1], 1)
        youngs_modulus_x = np.array([lo[0], hi[0]])
        youngs_modulus_y = youngs_modulus_coeffs[1] * youngs_modulus_x + youngs_modulus_coeffs[0]

        results.lo_index = lo_index
        results.hi_index = hi_index
        results.y_intercept = youngs_modulus_coeffs[0]
        results.youngs_modulus = youngs_modulus_coeffs[1]

        if axies['plt_stress'] is not None:
            axies['plt_stress'].plot(youngs_modulus_x, youngs_modulus_y, 'g--', label='Linear Fit')

        # --------------------------------------------
        # Find yield
        # Step1: Compute the 2nd derivative from the end of the linear region to the max strain
        fr2_max_index = np.argmax(fr2_slopes)
        reduced_fringe = fr2_fringe[fr2_max_index:-1]
        reduced_slopes = fr2_slopes[fr2_max_index:-1]
        dstrain, dslopes1, dslopes2 = compute_derivative(reduced_fringe, reduced_slopes)

        results.dstrain = dstrain
        results.dslopes1 = dslopes1
        results.dslopes2 = dslopes2

        # Step2: Find peaks and valleys of the 2nd derivative using tuned standard deviations
        prominence = np.std(dslopes2) / 3
        xpeaks, ypeaks, xvalleys, yvalleys = find_peaks_and_valleys(dstrain, dslopes2, prominence=prominence)

        if axies['plt_peaks'] is not None:
            axies['plt_peaks'].plot(dstrain, dslopes2, label='2nd Derivative of Fringe Slopes')

        # Step3: Use first valley with respect to strain as the yield point (if any valleys exist)
        yield_index, x_yield, y_yield, x_yield_d2, y_yield_d2 = None, None, None, None, None
        if np.any(xvalleys) and np.any(yvalleys):
            x_yield_d2 = xvalleys[0]
            y_yield_d2 = yvalleys[0]
            yield_index = np.argmin(np.abs(strain - x_yield_d2))  # equivalent to .index
            x_yield = strain[yield_index]
            y_yield = stress_filt[yield_index]
            # print('{:<50} {}'.format("Computed yield strength: ", y_yield))
            if axies['plt_peaks'] is not None:
                axies['plt_peaks'].plot(xpeaks, ypeaks, 'g^', label='Peaks')
                axies['plt_peaks'].plot(xvalleys, yvalleys, 'rv', label='Valleys')
                axies['plt_peaks'].plot([xvalleys[0], xvalleys[0]], [min(dslopes2), max(dslopes2)], 'r--',
                                        label='Yield strain')

            if axies['plt_stress'] is not None:
                axies['plt_stress'].plot(x_yield, y_yield, 'ro', label='Yield Point')
        else:
            # No yield found with prominence.
            # yield_index = len(strain) - 1
            yield_index = hi_index


        results.yield_index = yield_index
        results.x_yield = x_yield
        results.y_yield = y_yield

        # --------------------------------------------
        # Find Poisson's
        redused_strain = strain[lo_index:yield_index + 1]
        if trans_1 is not None:
            trans_1_filt, wn, qm = butter_lowpass(strain, trans_1)
            reduced_trans_1 = trans_1_filt[lo_index:yield_index + 1]
            trans_1_coeff = polyfit(redused_strain, reduced_trans_1, 1)
            if axies['plt_trans'] is not None:
                axies['plt_trans'].plot(strain, trans_1, 'b-', alpha=0.25, label='Raw Transverse 1')
                axies['plt_trans'].plot(strain, trans_1_filt, 'b-.', label='Filtered Transverse 1')
                trans_1_x = np.array([redused_strain[0], redused_strain[-1]])
                trans_1_y = trans_1_coeff[1] * trans_1_x + trans_1_coeff[0]
                axies['plt_trans'].plot(trans_1_x, trans_1_y, 'bo--', label='Transverse 1 Fit')
        else:
            trans_1_coeff = [None, None]
        results.trans_1_poi = -trans_1_coeff[1]

        if trans_2 is not None:
            trans_2_filt, wn, qm = butter_lowpass(strain, trans_2)
            reduced_trans_2 = trans_2_filt[lo_index:yield_index + 1]
            trans_2_coeff = polyfit(redused_strain, reduced_trans_2, 1)
            if axies['plt_trans'] is not None:
                axies['plt_trans'].plot(strain, trans_2, 'r-', alpha=0.25, label='Raw Transverse 2')
                axies['plt_trans'].plot(strain, trans_2_filt, 'r-.', label='Filtered Transverse 2')
                trans_2_x = np.array([redused_strain[0], redused_strain[-1]])
                trans_2_y = trans_2_coeff[1] * trans_2_x + trans_2_coeff[0]
                axies['plt_trans'].plot(trans_2_x, trans_2_y, 'ro--', label='Transverse 2 Fit')
        else:
            trans_2_coeff = [None, None]
        results.trans_2_poi = -trans_2_coeff[1]

        # --------------------------------------------
        # Cleanup
        rfr_labeler(axies)
        results.log = log
        return results

    except:
        print(log)
        raise Exception('ERROR: RFR_tensile_analysis failed, log printed above')


def rfr_plotter(plots='all'):
    all_plots = ['plt_stress', 'plt_fbf', 'plt_peaks', 'plt_trans']
    axies = {}
    figs = {}
    if plots in [None, 'off']:
        for plot in all_plots:
            axies[plot] = None
            figs[plot] = None
    elif plots == 'all':
        for plot in all_plots:
            figs[plot], axies[plot] = plt.subplots()
    else:
        for plot in all_plots:
            if plot in plots:  # sub string or list
                figs[plot], axies[plot] = plt.subplots()
            else:
                axies[plot] = None
                figs[plot] = None
    return axies


def rfr_labeler(axies):
    for plot, ax in axies.items():
        try:
            if plot == 'plt_fbf':
                ax.set_xlabel('Fringe')  # load units from rcParams?
                ax.set_ylabel('Slope')
                ax.title.set_text('Forward-Backward-Forward Fringe response')
                ax.legend()
                ax.grid()
            elif plot == 'plt_stress':
                ax.set_xlabel('Strain')  # load units from rcParams?
                ax.set_ylabel('Stress')
                ax.title.set_text('Stress-Strain')
                ax.legend()
                ax.grid()
            elif plot == 'plt_peaks':
                ax.set_xlabel('Fringe')  # load units from rcParams?
                ax.set_ylabel('Slope 2nd Derivative')
                ax.title.set_text('2nd Derivative of Fringe response')
                ax.legend()
                ax.grid()
            elif plot == 'plt_trans':
                ax.set_xlabel('Strain')  # load units from rcParams?
                ax.set_ylabel('Transverse strain')
                ax.title.set_text("Poisson's calculation")
                ax.legend()
                ax.grid()
        except:  # ignore legend errors
            pass


def _forward_backward_forward(strain, stress, min_xhi, max_xhi, _plt_fbf=None,maximize=True):
    # --------------------------------------------------------
    # Compute the forward-backwards-forwards fringe response
    # --------------------------------------------------------
    # Step1: First forward response (fr1 - applying minxhi and maxxhi accordingly)
    min_strain_fr1 = min(strain)
    max_strain_fr1 = max(strain)
    if min_xhi is not None: min_strain_fr1 = min_xhi
    if max_xhi is not None: max_strain_fr1 = max_xhi
    fr1_fringe, fr1_slopes = compute_fringe_slope(strain, stress, min_strain=min_strain_fr1,
                                                  max_strain=max_strain_fr1, direction='forward')
    if maximize:
        fr1_max_index = np.argmax(fr1_slopes)
    else:
        fr1_max_index = np.argmin(fr1_slopes)
    fr1_max_slope = fr1_slopes[fr1_max_index]
    fr1_max_fringe = fr1_fringe[fr1_max_index]

    if _plt_fbf:
        _plt_fbf.plot(fr1_fringe, fr1_slopes, label='Forward 1')
        _plt_fbf.scatter(fr1_max_fringe, fr1_max_slope)

    # Step2: First backwards response (br1 - applying minxhi and maxxhi accordingly)
    min_strain_br1 = min(strain)
    max_strain_br1 = fr1_max_fringe  # changed
    fr1_max_index_absolute = np.argmin(np.abs(strain - fr1_max_fringe))  # equivalent to .index
    reduced_strain = strain[0:fr1_max_index_absolute]
    reduced_stress = stress[0:fr1_max_index_absolute]

    br1_fringe, br1_slopes = compute_fringe_slope(reduced_strain, reduced_stress, min_strain=min_strain_br1,
                                                  max_strain=max_strain_br1, direction='reverse')
    if maximize:
        br1_max_index = np.argmax(br1_slopes)
    else:
        br1_max_index = np.argmin(br1_slopes)
    br1_max_slope = br1_slopes[br1_max_index]
    br1_max_fringe = br1_fringe[br1_max_index]
    br1_max_index_absolute = np.argmin(np.abs(strain - br1_max_fringe))  # equivalent to .index

    if _plt_fbf:
        _plt_fbf.plot(br1_fringe, br1_slopes, label='Backward 1')
        _plt_fbf.scatter(br1_max_fringe, br1_max_slope)

    # Step3: Second forward response (fr2 - applying minxhi and maxxhi accordingly)
    min_strain_fr2 = min_strain_fr1 + br1_max_fringe
    max_strain_fr2 = max_strain_fr1 + br1_max_fringe
    reduced_strain = strain[br1_max_index_absolute:-1]
    reduced_stress = stress[br1_max_index_absolute:-1]
    fr2_fringe, fr2_slopes = compute_fringe_slope(reduced_strain, reduced_stress, min_strain=min_strain_fr2,
                                                  max_strain=max_strain_fr2, direction='forward')
    if maximize:
        fr2_max_index = np.argmax(fr2_slopes)
    else:
        fr2_max_index = np.argmin(fr2_slopes)
    fr2_max_slope = fr2_slopes[fr2_max_index]
    fr2_max_fringe = fr2_fringe[fr2_max_index]
    fr2_max_index_absolute = np.argmin(np.abs(strain - fr2_max_fringe))  # equivalent to .index

    if _plt_fbf:
        _plt_fbf.plot(fr2_fringe, fr2_slopes, label='Forward 2')
        _plt_fbf.scatter(fr2_max_fringe, fr2_max_slope)

    # Set linear region bounds xlo and xhi from the 3 step FBF method
    xlo = br1_max_fringe
    ylo = stress[br1_max_index_absolute]
    xmid = fr1_max_fringe
    ymid = stress[fr1_max_index_absolute]
    xhi = fr2_max_fringe
    yhi = stress[fr2_max_index_absolute]
    return (xlo, ylo), (xmid, ymid), (xhi, yhi), fr2_fringe, fr2_slopes
