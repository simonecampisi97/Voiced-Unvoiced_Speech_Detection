import librosa
from librosa.feature import zero_crossing_rate
from librosa.util import frame
from librosa.util import example_audio_file
from scipy.signal import get_window, kaiser

import numpy as np


class Frames:
    def __init__(self, y, fs, gender, duration=32, hop_size=10):
        """
        :param hop_size: default: 10 ms
        :param y: audio time series
        :param fs: sampling frequency (Number of samples per second)
        :param duration: Analysis frame duration (in msec)
        :param overlap_rate: Overlapping rate between successive frame (typically between 50% and 100%)
        :param window: Type of the window to be applied on each frame
        """
        self.freq_female = 25  # Hz
        self.fre_male = 15  # Hz
        self.frame_length = 2400  # int((duration * fs) / 1000)  # Analysis frame length (in samples)
        # hop_length -> librosa
        print('aaaaaa', (48000 * 7) / self.frame_length)
        frame_shift = int((hop_size * fs) / 1000)
        # matrix where the rows contains contiguous slice
        frames = frame(y, frame_length=self.frame_length, hop_length=frame_shift, axis=0)
        print('Frames', len(frames))
        window = kaiser(M=2400, beta=0.5)  # get_window(window=window, Nx=self.frame_length, fftbins=False)
        self.windowed_frame = np.multiply(frames, window)

    def __iter__(self):
        return self.windowed_frame
