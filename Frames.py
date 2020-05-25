import librosa
from librosa.feature import zero_crossing_rate
from librosa.util import frame
from librosa.util import example_audio_file
from scipy.signal import get_window, kaiser
import pysptk
from utils import *
import numpy as np
import io


class Frames:
    def __init__(self, y, fs, gender, duration=32, hop_size=10):
        """
        :param hop_size: default: 10 ms
        :param y: audio time series
        :param fs: sampling frequency (Number of samples per second)
        :param duration: Analysis frame duration (in msec)
        :param overlap_rate: Overlapping rate between successive frame (typically between 50% and 100%)
        """
        self.freq_female = 25  # Hz
        self.fre_male = 15  # Hz

        self.frame_length = int(duration * (fs / 1000))  # Analysis frame length (in samples)
        # hop_length -> librosa

        shift_length = int(float(hop_size) * (fs / 1000))
        # matrix where the rows contains contiguous slice

        frames = frame(y, frame_length=self.frame_length, hop_length=shift_length, axis=0)
        print('Frames', frames.shape[0])
        window = kaiser(M=self.frame_length, beta=0.5)  # get_window(window=window, Nx=self.frame_length, fftbins=False)
        self.windowed_frame = np.multiply(frames, window)

        # pitch = pysptk.swipe(x=y.astype(np.float64), fs=fs, hopsize=shift_length)
        nfft = 2 ** nextpow2(self.frame_length)
        S = np.array(frame_dft(frames, int(nfft)))
        pitches, _ = librosa.core.piptrack(y=y, sr=fs, S=S, n_fft=int(nfft), window='hann', hop_length=shift_length)
        # vuv = np.where()
        file = open('pitches.txt', mode='w')
        vuv = []

        for pitch in pitches:
            vuv.append(np.sum(pitch))
            file.write(str(np.sum(pitch))+'\n')
        vuv= np.array(vuv)
        print(vuv)
        print(vuv[581])
        file.close()

    def __iter__(self):
        return self.windowed_frame
