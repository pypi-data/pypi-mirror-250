import numpy as np
from scipy.stats.stats import _contains_nan


def rankdata(a, method='average', *, axis=None, nan_policy='propagate'):
    """Assign ranks to data, dealing with ties appropriately.

    By default (``axis=None``), the data array is first flattened, and a flat
    array of ranks is returned. Separately reshape the rank array to the
    shape of the data array if desired (see Examples).

    Ranks begin at 1.  The `method` argument controls how ranks are assigned
    to equal values.  See [1]_ for further discussion of ranking methods.

    Parameters
    ----------
    a : array_like
        The array of values to be ranked.
    method : {'average', 'min', 'max', 'dense', 'ordinal'}, optional
        The method used to assign ranks to tied elements.
        The following methods are available (default is 'average'):

          * 'average': The average of the ranks that would have been assigned to
            all the tied values is assigned to each value.
          * 'min': The minimum of the ranks that would have been assigned to all
            the tied values is assigned to each value.  (This is also
            referred to as "competition" ranking.)
          * 'max': The maximum of the ranks that would have been assigned to all
            the tied values is assigned to each value.
          * 'dense': Like 'min', but the rank of the next highest element is
            assigned the rank immediately after those assigned to the tied
            elements.
          * 'ordinal': All values are given a distinct rank, corresponding to
            the order that the values occur in `a`.
    axis : {None, int}, optional
        Axis along which to perform the ranking. If ``None``, the data array
        is first flattened.
    nan_policy : {'propagate', 'omit', 'raise'}, optional
        Defines how to handle when input contains nan.
        The following options are available (default is 'propagate'):

          * 'propagate': propagates nans through the rank calculation
          * 'omit': performs the calculations ignoring nan values
          * 'raise': raises an error

        .. note::

            When `nan_policy` is 'propagate', the output is an array of *all*
            nans because ranks relative to nans in the input are undefined.
            When `nan_policy` is 'omit', nans in `a` are ignored when ranking
            the other values, and the corresponding locations of the output
            are nan.

        .. versionadded:: 1.10

    Returns
    -------
    ranks : ndarray
         An array of size equal to the size of `a`, containing rank
         scores.

    References
    ----------
    .. [1] "Ranking", https://en.wikipedia.org/wiki/Ranking

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.stats import rankdata
    >>> rankdata([0, 2, 3, 2])
    array([ 1. ,  2.5,  4. ,  2.5])
    >>> rankdata([0, 2, 3, 2], method='min')
    array([ 1,  2,  4,  2])
    >>> rankdata([0, 2, 3, 2], method='max')
    array([ 1,  3,  4,  3])
    >>> rankdata([0, 2, 3, 2], method='dense')
    array([ 1,  2,  3,  2])
    >>> rankdata([0, 2, 3, 2], method='ordinal')
    array([ 1,  2,  4,  3])
    >>> rankdata([[0, 2], [3, 2]]).reshape(2,2)
    array([[1. , 2.5],
          [4. , 2.5]])
    >>> rankdata([[0, 2, 2], [3, 2, 5]], axis=1)
    array([[1. , 2.5, 2.5],
           [2. , 1. , 3. ]])
    >>> rankdata([0, 2, 3, np.nan, -2, np.nan], nan_policy="propagate")
    array([nan, nan, nan, nan, nan, nan])
    >>> rankdata([0, 2, 3, np.nan, -2, np.nan], nan_policy="omit")
    array([ 2.,  3.,  4., nan,  1., nan])

    """
    if method not in ('average', 'min', 'max', 'dense', 'ordinal'):
        raise ValueError(f'unknown method "{method}"')

    a = np.asarray(a)

    if axis is not None:
        if a.size == 0:
            # The return values of `normalize_axis_index` are ignored.  The
            # call validates `axis`, even though we won't use it.
            # use scipy._lib._util._normalize_axis_index when available
            np.core.multiarray.normalize_axis_index(axis, a.ndim)
            dt = np.float64 if method == 'average' else np.int_
            return np.empty(a.shape, dtype=dt)
        return np.apply_along_axis(rankdata, axis, a, method,
                                   nan_policy=nan_policy)

    arr = np.ravel(a)
    contains_nan, nan_policy = _contains_nan(arr, nan_policy)
    nan_indexes = None
    if contains_nan:
        if nan_policy == 'omit':
            nan_indexes = np.isnan(arr)
        if nan_policy == 'propagate':
            return np.full_like(arr, np.nan)

    algo = 'mergesort' if method == 'ordinal' else 'quicksort'
    sorter = np.argsort(arr, kind=algo)

    inv = np.empty(sorter.size, dtype=np.intp)
    inv[sorter] = np.arange(sorter.size, dtype=np.intp)

    if method == 'ordinal':
        result = inv + 1
    else:
        arr = arr[sorter]
        obs = np.r_[True, arr[1:] != arr[:-1]]
        dense = obs.cumsum()[inv]

        if method == 'dense':
            result = dense
        else:
            # cumulative counts of each unique value
            count = np.r_[np.nonzero(obs)[0], len(obs)]

            if method == 'max':
                result = count[dense]

            if method == 'min':
                result = count[dense - 1] + 1

            if method == 'average':
                result = .5 * (count[dense] + count[dense - 1] + 1)

    if nan_indexes is not None:
        result = result.astype('float64')
        result[nan_indexes] = np.nan

    return result
