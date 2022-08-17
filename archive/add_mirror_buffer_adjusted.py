import xarray as xr
import numpy as np
from ptsa.data.timeseries import TimeSeries
# from ptsa.data import timeseries

# class TimeSeries(xr.DataArray):
#     """A thin wrapper around :class:`xr.DataArray` for dealing with time series
#     data.
#     Note that xarray internals prevent us from overriding the constructor which
#     leads to some awkwardness: you must pass coords as a dict with a
#     ``samplerate`` entry.
#     Parameters
#     ----------
#     data : array-like
#         Time series data
#     coords : dict-like
#         Coordinate arrays. This must contain at least a ``samplerate``
#         coordinate.
#     dims : array-like
#         Dimension labels
#     name : str
#         Name of the time series
#     attrs : dict
#         Dictionary of arbitrary metadata
#     fastpath : bool
#         Not used, but required when subclassing :class:`xr.DataArray`.
#     Raises
#     ------
#     AssertionError
#         When ``samplerate`` is not present in ``coords``.
#     See also
#     --------
#     xr.DataArray : Base class
#     """

#     __slots__ = ()
    
#     def __init__(self, data, coords, dims=None, name=None, attrs=None,
#             fastpath=False, **kwargs):
#         assert 'samplerate' in coords
#         super(TimeSeries, self).__init__(
#             data=data, coords=coords, dims=dims, name=name, attrs=attrs,
#             fastpath=fastpath, **kwargs)

def add_mirror_buffer_adjusted(eeg_ptsa, duration):
    """
    Return a time series with mirrored data added to both ends of this
    time series (up to specified length/duration).
    The new series total time duration is:
        ``original duration + 2 * duration * samplerate``
    Parameters
    ----------
    duration : float
        Buffer duration in seconds.
    Returns
    -------
    New time series with added mirrored buffer.
    """
    samplerate = float(eeg_ptsa['samplerate'])
    samples = int(np.ceil(float(eeg_ptsa['samplerate']) * duration))   

    if samples > len(eeg_ptsa['time']):
        raise ValueError("Requested buffer time is longer than the data")

    data = eeg_ptsa.data

    mirrored_data = np.concatenate(
        (data[..., 1:samples + 1][..., ::-1], data,
         data[..., -samples - 1:-1][..., ::-1]), axis=-1)

    start_time = eeg_ptsa['time'].data[0] - (duration*1000) # Noa's edit
    t_axis = (np.arange(mirrored_data.shape[-1]) * (1000 / samplerate))+start_time #Noa's edit
#     t_axis = (np.arange(mirrored_data.shape[-1]) *
#               (1.0 / samplerate)) + start_time
    # coords = [self.coords[dim_name] for dim_name in self.dims[:-1]] +[t_axis]
    coords = {dim_name:eeg_ptsa.coords[dim_name]
              for dim_name in eeg_ptsa.dims[:-1]}
    coords['time'] = t_axis
    coords['samplerate'] = float(eeg_ptsa['samplerate'])

    return TimeSeries(mirrored_data, dims=eeg_ptsa.dims, coords=coords)

