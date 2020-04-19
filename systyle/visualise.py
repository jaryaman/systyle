import matplotlib.pyplot as plt
from systyle import remove_tex_axis
from systyle.analyse import bootstrap_lr
import scipy.stats as stats

import os
from matplotlib import cm
import numpy as np


def make_heatmap(matrix, xlabel, ylabel, zlabel, xticklabels, yticklabels, plotextensions=('svg', 'png'),
                 colorbar_heatmap=cm.jet, figname=None, vmin=None, vmax=None, out_dir=os.getcwd()):
    """
    Make a heatmap of a matrix where rows are plotted on the vertical axis, and columns plotted along the horizontal

    Parameters
    ---------------
    matrix : A numpy matrix, intensities for heatmap. Expect a square matrix of dimension (n_points x n_points)
    zlabel : A string, colorbar label of heatmap
    figname : A string, prefix to figure name. If none, do not write to file
    xlabel : A string, x-label of heatmap
    ylabel : A string, y-label of heatmap
    xticklabels : A list of strings, x tick labels
    yticklabels : A list of strings, y tick labels
    vmin : A float, minimum value for colorbar
    vmax : A float, maximum value for colorbar
    plotextensions :  A list of strings, default extensions for plotting
    colorbar_heatmap : The colormap for the heatmap
    out_dir : A string, the output directory for the plot
    """
    plt.close('all')
    nan_col = 0.4
    nan_rgb = nan_col * np.ones(3)
    colorbar_heatmap.set_bad(nan_rgb)

    fig, ax = plt.subplots(1, 1, figsize=(9, 9))
    im = ax.imshow(np.flipud(matrix), cmap=colorbar_heatmap, vmin=vmin, vmax=vmax)
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label=zlabel)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks(np.arange(len(xticklabels)))
    ax.set_yticks(np.arange(len(yticklabels)))
    ax.set_xticklabels(xticklabels)
    ax.set_yticklabels(yticklabels[::-1])

    if figname is not None:
        for p in plotextensions:
            plt.savefig(out_dir + '/' + figname + '.' + p, bbox_inches='tight')


def get_non_null_and_jitter(data, name, dx, offset):
    """
    Strip out null values from a dataframe and return jittered x with y-values

    Parameters
    ---------------
    data : A pandas dataframe, contains numeric values in the column `name`
    name : A string, the name of the column to be plotted
    dx : A float, width of the jitter
    offset : A float, offset of the jitter

    Returns
    ----------
    datax : A pandas series, containing non-null values of the column to plot
    x : A numpy array, jittered x-values
    """
    datax = data[name]
    datax = datax[~datax.isnull()]
    x = np.ones(len(datax)) + offset + np.random.uniform(-dx, dx, size=len(datax))
    return datax, x


def make_jitter_plots(data, names, ylabel, dx=0.1, offset=0.0, ytick_fmt=None,
                      xlabels=None, ax_handle=None, alpha=1, color=None,
                      marker=None, markersize=12, return_plot_pointer=False):
    """
    Make a jitter plot of columns from a pandas dataframe

    Parameters
    ---------------
    data : A pandas dataframe, contains numeric values in the columns `names`
    names: An array of strings, the name of the columns to be plotted
    dx : A float, width of the jitter
    offset : A float, offset of the jitter
    ylabel : A string, the y-label for the plot
    ax_handle : A matplotlib axis handle. When defined, the function will add a jitter plot to an ax object
    xlabels : A list of strings, the names along the x-axis
    alpha : A float, transparency on data points
    color : A string or a list of strings, the color of the points
    marker : A string or a list of strings, the marker of the points
    ytick_fmt : A string, the format of the y-ticks
    markersize : An int, the marker size

    Returns
    --------
    fig : A matplotlib figure handle (only if ax_handle is None)
    ax : A matplotlib axis handle (only if ax_handle is None)
    p[0] : A matplotlib.lines.Line2D object corresponding to the marker used in
            the jitter plot (only if return_plot_pointer is True)
    """

    if isinstance(marker, (list, tuple)):
        assert len(marker) == len(names)
    if isinstance(color, (list, tuple)):
        assert len(color) == len(names)

    yx_tuples = []
    for name in names:
        yx_tuples.append(get_non_null_and_jitter(data, name, dx, offset))

    if ax_handle is None:
        fig, ax = plt.subplots(1, 1)
    else:
        ax = ax_handle

    for i in range(len(names)):
        if isinstance(marker, (list, tuple)):
            marker_i = marker[i]
        elif isinstance(marker, str):
            marker_i = marker
        else:
            marker_i = '.'
        if isinstance(color, (list, tuple)):
            color_i = color[i]
        elif isinstance(color, str):
            color_i = color
        else:
            color_i = 'k'

        yi = yx_tuples[i][0]
        xi = yx_tuples[i][1]
        p=ax.plot(i + xi, yi, marker_i, color=color_i, alpha=alpha,
                markersize=markersize, markeredgecolor='k')

    if ytick_fmt is not None:
        remove_tex_axis(ax, ytick_fmt=ytick_fmt)

    ax.set_xticks(1 + np.arange(len(names)))
    if xlabels is None:
        names = [s.replace('_', '-') for s in names]  # underscores make LaTeX unhappy
        ax.set_xticklabels(names)
    else:
        ax.set_xticklabels(xlabels)
    for t in ax.get_xticklabels():
        t.set_rotation(90)
    ax.set_ylabel(ylabel)

    if ax_handle is None:
        if return_plot_pointer:
            return fig, ax, p[0]
        else:
            return fig, ax

    if return_plot_pointer:
        return p[0]


def plot_bootstrapped_lr(x, y, q_low=2.5, q_high=97.5, ax_handle=None, B=1000,
                        legend=True, alpha=0.5):
    """
    Plot bootstrapped linear regression trend line

    Parameters
    --------------
    x : A numpy array, x-values
    y : A numpy array, x-values
    q_low : A float, lower quantile on the steady state line fit
    q_high : A float, upper quantile on the steady state line fit
    ax_handle : A matplotlib axis handle, for adding onto an existing plot
    B : Number of bootstrap iterations
    legend : A bool, if True add to legend.

    Returns
    -------------
    fig : A matplotlib figure handle (if ax_handle is None)
    ax : A matplotlib axis handle (if ax_handle is None)
    summary_stats : A list containing the variables [slope_ml, intercept_ml, pval, r_sq], see mystyle.ana.bootstrap_lfc

    Note
    -------------
    Should remove NaN values first
    """
    x_sp, y_ql, y_qh = bootstrap_lr(x, y, x_sp=None, q_low=q_low, q_high=q_high, B=B)
    lr_ml = stats.linregress(x, y)
    slope_ml = lr_ml.slope
    intercept_ml = lr_ml.intercept
    pval = lr_ml.pvalue
    r_sq = lr_ml.rvalue**2

    summary_stats = {'slope_ml':slope_ml, 'intercept_ml':intercept_ml,
        'pval':pval, 'r_sq':r_sq}


    if ax_handle is None:
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    else:
        ax = ax_handle

    if legend:
        ax.plot(x_sp, x_sp * slope_ml + intercept_ml, '-r', label='LR')
        ax.fill_between(x_sp, y_ql, y_qh, color='red', alpha=alpha, label='95\% Boot. C.I.')
    else:
        ax.plot(x_sp, x_sp * slope_ml + intercept_ml, '-r')
        ax.fill_between(x_sp, y_ql, y_qh, color='red', alpha=alpha)

    if ax_handle is None:
        return fig, ax, summary_stats, x_sp
    else:
        return summary_stats
