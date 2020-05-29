import librosa
import matplotlib.pyplot as plt
from Signal_Analysis.features.signal import get_HNR
from scipy.io import wavfile

from utils import *


def st_zcr(frames):
    st_zcr_ = []
    # matrix where the rows contains contiguous slice
    for frame_w in frames.windowed_frames:
        st_zcr_.append(np.sum(abs(np.diff(np.sign(frame_w - np.mean(frame_w))))) / (2 * frames.frame_length))
    plt.show()

    return np.array(st_zcr_)


def st_magnitude(frames):
    st_mag = []
    i = 0
    for windowed_frame in frames.windowed_frames:
        st_mag.append(np.sum(abs(windowed_frame)))
        i += 1
    return np.array(st_mag)


def st_energy(frames):
    energy = np.zeros(len(frames.frames))
    for i, windowed_frame in enumerate(frames.windowed_frames):
        energy[i] = np.mean(windowed_frame ** 2, axis=0)
    return energy


def MFCC(frames):
    # TODO da sistemare
    mfcc = []
    for frame in frames.windowed_frames:
        t = librosa.feature.mfcc(frame, frames.fs, n_mfcc=13)
    return mfcc


def st_HNR(frames, time_step=0.01, silence_threshold=0.1):
    hnr = []
    for windowed_frame in frames.windowed_frames:
        hnr.append(
            get_HNR(signal=windowed_frame, rate=frames.fs, time_step=time_step, silence_threshold=silence_threshold))

    return np.array(hnr)
