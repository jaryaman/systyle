import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker
from matplotlib.ticker import FormatStrFormatter
from IPython import get_ipython


def reset_plots():
    """
    Makes axes large, and enables LaTeX for matplotlib plots
    """
    plt.close('all')
    fontsize = 20
    legsize = 15
    plt.rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
    plt.rc('text', usetex=True)
    font = {'size': fontsize}
    plt.rc('font', **font)
    rc = {'axes.labelsize': fontsize,
          'font.size': fontsize,
          'axes.titlesize': fontsize,
          'xtick.labelsize': fontsize,
          'ytick.labelsize': fontsize,
          'legend.fontsize': legsize}
    mpl.rcParams.update(**rc)
    mpl.rc('lines', markersize=10)
    plt.rcParams.update({'axes.labelsize': fontsize})
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}',
                                           r'\usepackage{amsfonts}']


def plot(n_rows=1, n_cols=1, fig_size=5):
    """
    Generate a matplotlib plot and axis handle

    Parameters
    -----------------
    n_rows : An int, number of rows for subplotting
    n_cols : An int, number of columns for subplotting
    fig_size : Numeric or array (xfigsize, yfigsize). The size of each axis.
    """
    if isinstance(fig_size,(list, tuple)):
        xfigsize, yfigsize = fig_size
    elif isinstance(fig_size,(int,float)):
        xfigsize = yfigsize = fig_size
    else:
        raise ValueError
    fig, axs = plt.subplots(n_rows, n_cols, figsize=(n_cols*xfigsize, n_rows*yfigsize))
    if n_rows*n_cols > 1:
        axs = axs.ravel()
    return fig, axs


def remove_tex_axis(ax, xtick_fmt='%d', ytick_fmt='%d', axis_remove='both'):
    """
    Makes axes normal font in matplotlib.

    Parameters
    ---------------
    xtick_fmt : A string, defining the format of the x-axis
    ytick_fmt : A string, defining the format of the y-axis
    axis_remove : A string, which axis to remove. ['x', 'y', 'both']
    """
    if axis_remove not in ['x','y','both']:
        raise Exception('axis_remove value not allowed.')
    fmt = matplotlib.ticker.StrMethodFormatter("{x}")

    if axis_remove == 'both':
        ax.xaxis.set_major_formatter(fmt)
        ax.yaxis.set_major_formatter(fmt)
        ax.xaxis.set_major_formatter(FormatStrFormatter(xtick_fmt))
        ax.yaxis.set_major_formatter(FormatStrFormatter(ytick_fmt))
    elif axis_remove == 'x':
        ax.xaxis.set_major_formatter(fmt)
        ax.xaxis.set_major_formatter(FormatStrFormatter(xtick_fmt))
    else:
        ax.yaxis.set_major_formatter(fmt)
        ax.yaxis.set_major_formatter(FormatStrFormatter(ytick_fmt))



def simpleaxis(ax):
    """
    Remove top and right spines from a plot

    Parameters
    ---------------
    ax : A matplotlib axis
    """
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()


def auto_reload_code():
    """
    Let python functions be updated whilst inside an iPython/Jupyter session
    """
    ipython = get_ipython()
    ipython.magic("reload_ext autoreload")
    ipython.magic("autoreload 2")



def legend_outside(ax, pointers=None, labels=None, size=15, frameon=True):
    """
    Put legend outside the plot area

    Parameters
    ---------------
    ax : A matplotlib axis
    """

    if pointers is None and labels is None:
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
                    prop={'size': size}, frameon=frameon)
    else:
        assert len(pointers) == len(labels)
        ax.legend(pointers, labels, loc='center left', bbox_to_anchor=(1, 0.5),
                    prop={'size': size}, frameon=frameon)


def to_latex(x, dp=1, double_backslash=True):
    """
    Convert a decimal into LaTeX scientific notation

    Parameters
    ---------------
    x : A float, the number to convert to LaTeX notation, e.g. 0.42
    dp : An int, the number of decimal places for the
    double_backslash : A bool, whether to use a double-backslash for LaTeX commands

    Returns
    -----------
    A string where x is cast in LaTeX as scientific notation, e.g. "4.2 \times 10^{-1}"

    """
    fmt = "%.{}e".format(dp)
    s = fmt % x
    arr = s.split('e')
    m = arr[0]
    n = str(int(arr[1]))
    if double_backslash:
        return str(m) + '\\times 10^{' + n + '}'
    else:
        return str(m) + '\times 10^{' + n + '}'
