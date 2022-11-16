import numpy as np
import scipy.interpolate
import sklearn
from tqdm import tqdm

import scipy.spatial

from spikeinterface.preprocessing.basepreprocessor import BasePreprocessor, BasePreprocessorSegment
from spikeinterface.preprocessing import get_spatial_interpolation_kernel


# try:
#     import numba
#     HAVE_NUMBA = True
# except ImportError:
#     HAVE_NUMBA = False


def correct_motion_on_peaks(peaks, peak_locations, times,
                            motion, temporal_bins, spatial_bins,
                            direction='y', progress_bar=False):
    """
    Given the output of estimate_motion(), apply inverse motion on peak location.

    Parameters
    ----------
    peaks: np.array
        peaks vector
    peak_locations: np.array
        peaks location vector
    times: np.array
        times vector of recording
    motion: np.array 2D
        motion.shape[0] equal temporal_bins.shape[0]
        motion.shape[1] equal 1 when "rigid" motion
                        equal temporal_bins.shape[0] when "none rigid"
    temporal_bins: np.array
        Temporal bins in second.
    spatial_bins: None or np.array
        Bins for non-rigid motion. If None, rigid motion is used

    Returns
    -------
    corrected_peak_locations: np.array
        Motion-corrected peak locations
    """
    corrected_peak_locations = peak_locations.copy()

    if spatial_bins is None:
        # rigid motion interpolation 1D
        sample_bins = np.searchsorted(times, temporal_bins)
        f = scipy.interpolate.interp1d(sample_bins, motion[:, 0], bounds_error=False, fill_value="extrapolate")
        shift = f(peaks['sample_ind'])
        corrected_peak_locations[direction] -= shift
    else:
        # non rigid motion = interpolation 2D
        f = scipy.interpolate.RegularGridInterpolator((temporal_bins, spatial_bins), motion,
                                                      method='linear', bounds_error=False, fill_value=None)
        spike_times = times[peaks['sample_ind']]
        shift = f(np.c_[spike_times, peak_locations[direction]])
        corrected_peak_locations[direction] -= shift

    return corrected_peak_locations


def correct_motion_on_traces(traces, times, channel_locations, motion, temporal_bins, spatial_bins,
                             direction=1, spatial_interpolation_method='kriging', spatial_interpolation_kwargs={}):
    """
    Apply inverse motion with spatial interpolation on traces.

    Traces can be full traces, but also waveforms snippets.

    Parameters
    ----------
    traces : np.array
        Trace snippet (num_samples, num_channels)
    channel_location: np.array 2d
        Channel location with shape (n, 2) or (n, 3)
    motion: np.array 2D
        motion.shape[0] equal temporal_bins.shape[0]
        motion.shape[1] equal 1 when "rigid" motion
                        equal temporal_bins.shape[0] when "none rigid"
    temporal_bins: np.array
        Temporal bins in second.
    spatial_bins: None or np.array
        Bins for non-rigid motion. If None, rigid motion is used
    direction: int in (0, 1, 2)
        Dimension of shift in channel_locations.
    spatial_interpolation_method: str in ('idw', 'krigging', 
        * idw : Inverse Distance Weighing
        * kriging : kilosort2.5 like
    spatial_interpolation_kwargs:
        * specific option for the interpolation method
    
    Returns
    -------
    channel_motions: np.array
        Shift over time by channel
        Shape (times.shape[0], channel_location.shape[0])
    """
    # assert HAVE_NUMBA
    assert times.shape[0] == traces.shape[0]

    traces_corrected = np.zeros_like(traces)
    # print(traces_corrected.shape)

    
    
    # regroup times by closet temporal_bins
    bin_inds = _get_closest_ind(temporal_bins, times)

    # inperpolation kernel will be the same per temporal bin   
    for bin_ind in np.unique(bin_inds):

        # Step 1 : channel motion
        if spatial_bins is None:
            # rigid motion : same motion for all channels
            channel_motions = motion[bin_ind, 0]
        else:
            # non rigid : interpolation channel motion for this temporal bin
            f = scipy.interpolate.interp1d(spatial_bins, motion[bin_ind, :], kind='linear',
                                           axis=0, bounds_error=False, fill_value="extrapolate")
            locs = channel_locations[:, direction]
            channel_motions = f(locs)
        channel_locations_moved = channel_locations.copy()
        # channel_locations_moved[:, direction] += channel_motions
        channel_locations_moved[:, direction] -= channel_motions

        drift_kernel = get_spatial_interpolation_kernel(channel_locations, channel_locations_moved,
                                                        force_extrapolate=False, dtype='float32',
                                                        method=spatial_interpolation_method, **spatial_interpolation_kwargs)
        
        
        i0 = np.searchsorted(bin_inds, bin_ind, side='left')
        i1 = np.searchsorted(bin_inds, bin_ind, side='right')
        
        # here we use a simple np.matmul even if dirft_kernel can be super sparse.
        # because the speed for a sparse matmul is not so good when we disable multi threaad (due multi processing
        # in ChunkRecordingExecutor)
        traces_corrected[i0:i1] = traces[i0:i1] @ drift_kernel

    return traces_corrected



# if HAVE_NUMBA:
#     # @numba.jit(parallel=False)
#     @numba.jit(parallel=True)
#     def my_sparse_dot(data_in, data_out, sparse_chans, weights):
#         """
#         Experimental home made sparse dot.
#         Faster when use prange but with multiprocessing it is not a good idea.
#         Custum sparse dot
#         data_in: num_sample, num_chan_in
#         data_out: num_sample, num_chan_out
#         sparse_chans: num_chan_out, num_sparse
#         weights: num_chan_out, num_sparse
#         """
#         num_samples = data_in.shape[0]
#         num_chan_out = data_out.shape[1]
#         num_sparse = sparse_chans.shape[1]
#         # for sample_ind in range(num_samples):
#         for sample_ind in numba.prange(num_samples):
#             for out_chan in range(num_chan_out):
#                 v = 0
#                 for i in range(num_sparse):
#                     in_chan = sparse_chans[out_chan, i]
#                     v +=  weights[out_chan, i] * data_in[sample_ind, in_chan]
#                 data_out[sample_ind, out_chan] = v


def _get_closest_ind(array, values):
    # https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array

    # get insert positions
    idxs = np.searchsorted(array, values, side="left")

    # find indexes where previous index is closer
    prev_idx_is_less = ((idxs == len(array)) | (np.fabs(values - array[np.maximum(idxs-1, 0)]) <
                                                np.fabs(values - array[np.minimum(idxs, len(array)-1)])))
    idxs[prev_idx_is_less] -= 1

    return idxs


# TODO:
#  * add option for interpolation mode
#  * add option to handle the borders

class CorrectMotionRecording(BasePreprocessor):
    """
    Recording that corrects motion on-the-fly given a rigid or non-rigid
    motion vector estimation.
    This internally applies for every time bin an inverse weighted distance interpolation
    on the original after reverse the motion.
    `estimate_motion()` must be call before this to get the motion vector.

    Parameters
    ----------
    recording: Recording
        The parent recording.
    motion: np.array 2D
        motion.shape[0] equal temporal_bins.shape[0]
        motion.shape[1] equal 1 when "rigid" motion
                        equal temporal_bins.shape[0] when "none rigid"
    temporal_bins: np.array
        Temporal bins in second.
    spatial_bins: None or np.array
        Bins for non-rigid motion. If None, rigid motion is used
    direction: int in (0, 1, 2)
        Dimension of shift in channel_locations.

    Returns
    -------
    Corrected_recording: CorrectMotionRecording
        Recording after motion correction
    """
    name = 'correct_motion'

    def __init__(self, recording, motion, temporal_bins, spatial_bins, direction=1):
        assert recording.get_num_segments() == 1, 'correct is handle only for one segment for the moment'
        BasePreprocessor.__init__(self, recording)

        channel_locations = recording.get_channel_locations()

        for parent_segment in recording._recording_segments:
            rec_segment = CorrectMotionRecordingSegment(parent_segment, channel_locations,
                                                        motion, temporal_bins, spatial_bins, direction)
            self.add_recording_segment(rec_segment)

        self._kwargs = dict(recording=recording.to_dict(), motion=motion, temporal_bins=temporal_bins,
                            spatial_bins=spatial_bins, direction=direction)
        # self.is_dumpable= False


class CorrectMotionRecordingSegment(BasePreprocessorSegment):
    def __init__(self, parent_recording_segment, channel_locations, motion, temporal_bins, spatial_bins, direction):
        BasePreprocessorSegment.__init__(self, parent_recording_segment)
        self.channel_locations = channel_locations
        self.motion = motion
        self.temporal_bins = temporal_bins
        self.spatial_bins = spatial_bins
        self.direction = direction

    def get_traces(self, start_frame, end_frame, channel_indices):
        if self.time_vector is not None:
            raise NotImplementedError('time_vector for CorrectMotionRecording do not work because temporal_bins start from 0')
            # times = np.asarray(self.time_vector[start_frame:end_frame])
        else:
            times = np.arange((end_frame or self.get_num_samples()) - (start_frame or 0), dtype='float64')
            times /= self.sampling_frequency
            t0 = start_frame / self.sampling_frequency
            # if self.t_start is not None:
            #     t0 = t0 + self.t_start
            times += t0

        traces = self.parent_recording_segment.get_traces(start_frame, end_frame, channel_indices=None)

        # print(traces.shape, times.shape, self.channel_locations, self.motion, self.temporal_bins, self.spatial_bins)
        trace2 = correct_motion_on_traces(traces, times, self.channel_locations, self.motion,
                                          self.temporal_bins, self.spatial_bins, direction=self.direction)

        if trace2 is not None:
            trace2 = trace2[:, channel_indices]

        return trace2
