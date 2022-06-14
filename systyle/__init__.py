import matplotlib.pyplot as plt
from IPython import get_ipython

from .style import Style


def plot(n_rows=1, n_cols=1, fig_size=5):
    """Generate a matplotlib plot and axis handle

    Parameters
    ----------
    n_rows:
        An int, number of rows for subplotting
    n_cols:
        An int, number of columns for subplotting
    fig_size:
        Numeric or array (xfigsize, yfigsize). The size of each axis.
    """
    if isinstance(fig_size, (list, tuple)):
        xfigsize, yfigsize = fig_size
    elif isinstance(fig_size, (int, float)):
        xfigsize = yfigsize = fig_size
    else:
        raise ValueError
    fig, axs = plt.subplots(n_rows, n_cols, figsize=(n_cols * xfigsize, n_rows * yfigsize))
    if n_rows * n_cols > 1:
        axs = axs.ravel()
    return fig, axs


def simpleaxis(ax):
    """Remove top and right spines from a plot

    Parameters
    ----------
    ax :
        A matplotlib axis
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
    ----------
    ax :
        A matplotlib axis
    pointers:
        List of pointers to artists
    labels:
        List of labels corresponding to pointers
    size:
        Size of the legend
    frameon:
        Display legend with frame
    """

    if pointers is None and labels is None:
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
                  prop={'size': size}, frameon=frameon)
    else:
        assert len(pointers) == len(labels)
        ax.legend(pointers, labels, loc='center left', bbox_to_anchor=(1, 0.5),
                  prop={'size': size}, frameon=frameon)
