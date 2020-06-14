import librosa
import matplotlib.pyplot as plt
import numpy as np
from Signal_Analysis.features.signal import get_HNR
import utils.support_funcion as sf

from Frames import Frames


def st_zcr(frames: Frames):
    st_zcr_ = []
    # matrix where the rows contains contiguous slice
    for frame_w in frames.windowed_frames:
        st_zcr_.append(np.sum(abs(np.diff(np.sign(frame_w - np.mean(frame_w))))) / (2 * frames.frame_length))

    return np.array(st_zcr_)


def st_magnitude(frames: Frames):
    st_mag = []
    i = 0
    for windowed_frame in frames.windowed_frames:
        st_mag.append(np.sum(abs(windowed_frame)))
        i += 1
    return np.array(st_mag)


def st_energy(frames: Frames):
    energy = np.zeros(len(frames))
    for i, windowed_frame in enumerate(frames.windowed_frames):
        energy[i] = np.mean(windowed_frame ** 2, axis=0)
    return energy


def MFCC(signal, frames: Frames, n_mfcc=13):
    n_fft = int(2 ** sf.nextpow2(frames.frame_length))

    mfcc = librosa.feature.mfcc(y=signal, sr=frames.fs, n_mfcc=n_mfcc, hop_length=frames.shift_length,
                                htk=False, win_length=frames.frame_length, window=frames.window, n_fft=n_fft)

    diff = mfcc.shape[1] - len(frames.windowed_frames)

    mfcc_truncated = mfcc.T[:-diff]

    return mfcc_truncated.T


def st_HNR(frames: Frames, time_step=0.01, silence_threshold=0.1):
    hnr = []
    for windowed_frame in frames.windowed_frames:
        hnr.append(get_HNR(signal=windowed_frame, rate=frames.fs,
                           time_step=time_step, silence_threshold=silence_threshold))

    return np.array(hnr)
