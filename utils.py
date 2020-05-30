import matplotlib.pyplot as plt
import numpy as np


def nextpow2(x):
    return np.ceil(np.log2(abs(x)))


def frame_dft(frames, nfft):
    S = []
    for frame in frames:
        S.append(np.fft.fft(frame, nfft))
    return S


def plot_result(y, Frames, title=''):
    frame_time = []
    for i in range(len(Frames.frames)):
        frame_time.append((i * Frames.frame_length) * (1 / Frames.fs) * 1000)
    plt.figure()
    plt.plot(frame_time, y)
    plt.title(title)
    plt.show()
