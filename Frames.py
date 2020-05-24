import librosa
from librosa.feature import zero_crossing_rate
from librosa.util import frame
from librosa.util import example_audio_file
from scipy.signal import get_window

import numpy as np


class Frames:
    def __init__(self, y, fs, duration=30, overlap_rate=0.5, window='hann'):
        """
        :param y: audio time series
        :param fs: sampling frequency (Number of samples per second)
        :param duration: Analysis frame duration (in msec)
        :param overlap_rate: Overlapping rate between successive frame (typically between 50% and 100%)
        :param window: Type of the window to be applied on each frame
        """

        self.frame_length = int(np.floor(duration * fs / 1000))  # Analysis frame length (in samples)

        shift = 1 - overlap_rate  # Shift is the rate of sliding the window

        # shift length in samples -> hop_length
        frame_shift = round(self.frame_length * shift)
        # matrix where the rows contains contiguous slice
        frames = frame(y, frame_length=self.frame_length, hop_length=frame_shift, axis=0)
        window = get_window(window=window, Nx=self.frame_length, fftbins=False)
        self.windowed_frame = np.multiply(frames, window)

    def __iter__(self):
        return self.windowed_frame
