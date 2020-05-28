import numpy as np
from librosa.util import frame
from scipy.signal.windows import kaiser


class Frames:
    def __init__(self, y, fs, duration=32, hop_size=10):
        """
        :param hop_size: Number of steps to advance between frames (default: 10 ms)
        :param y: audio time series
        :param fs: sampling frequency (Number of samples per second)
        :param duration: Analysis frame duration (in msec)
        """

        self.frame_length = int(duration * (fs / 1000))  # Analysis frame length (in samples)
        # hop_length -> librosa

        self.shift_length = int(float(hop_size) * (fs / 1000))
        # matrix where the rows contains contiguous slice

        self.frames = frame(y, frame_length=self.frame_length, hop_length=self.shift_length, axis=0)
        window = kaiser(M=self.frame_length, beta=0.5)
        self.windowed_frames = np.multiply(self.frames, window)

    def __iter__(self):
        return self.windowed_frames

    def __len__(self):
        return len(self.windowed_frames)
