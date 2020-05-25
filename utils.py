import numpy as np


def nextpow2(x):
    return np.ceil(np.log2(abs(x)))


def frame_dft(frames, nfft):
    S = []
    for frame in frames:
        S.append(np.fft.fft(frame, nfft))
    return S
