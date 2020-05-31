import matplotlib.pyplot as plt
import numpy as np


def nextpow2(x):
    return np.ceil(np.log2(abs(x)))


def frame_dft(frames, nfft):
    S = []
    for frame in frames:
        S.append(np.fft.fft(frame, nfft))
    return S


def plot_result(signal, Frames, ax):
    frame_time = []
    for i in range(len(Frames.windowed_frames)):
        frame_time.append((i * Frames.frame_length) * (1 / Frames.fs) * 1000)

    ax.plot(frame_time, signal)
