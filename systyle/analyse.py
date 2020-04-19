import numpy as np
import scipy.stats as stats


def bootstrap_lr(x, y, x_sp = None, q_low = 2.5, q_high = 100-2.5, B=1000):
    """
    Bootstrap linear regression

    Parameters
    -------------

    x : An array of floats, the independent variable
    y : An array of floats, the dependent variable

    x_sp : An array of floats, the space over the independent variable to evaluate the bootstrap
    q_low : The lower quantile for the bootstrap
    q_high : The upper quantile for the bootstrap

    Returns
    -------------
    y_ql : An array of floats, the lower bootstrapped quantile of the dependent variable under linear regression over x_sp
    y_qh : An array of floats, the upper bootstrapped quantile of the dependent variable under linear regression over x_sp
    """
    x_sp_defined = 1
    if x_sp is None:
        x_sp = np.linspace(min(x), max(x))
        x_sp_defined = 0
    y_arr = np.zeros((B, len(x_sp)))
    for i in range(B):
        idxs = np.random.choice(len(x),size=len(x),replace=True)
        xb = x[idxs]
        yb = y[idxs]
        lr = stats.linregress(xb, yb)
        y_arr[i,:] = lr.slope * x_sp + lr.intercept
    y_ql = np.percentile(y_arr, q_low, axis = 0)
    y_qh = np.percentile(y_arr, q_high, axis = 0)

    if x_sp_defined == 0:
        return x_sp, y_ql, y_qh
    else:
        return y_ql, y_qh
