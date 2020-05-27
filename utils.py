import numpy as np
from scipy import signal


def nextpow2(x):
    return np.ceil(np.log2(abs(x)))


def frame_dft(frames, nfft):
    S = []
    for frame in frames:
        S.append(np.fft.fft(frame, nfft))
    return S


def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a


def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y
