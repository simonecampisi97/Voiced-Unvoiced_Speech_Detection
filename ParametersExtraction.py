from scipy.io import wavfile
from Frames import Frames
import numpy as np
from utils import *
from Signal_Analysis.features.signal import get_HNR
import torch


def st_zcr(Frames):
    st_zcr_ = []
    # matrix where the rows contains contiguous slice
    for frame_w in Frames.frames_windowed:
        st_zcr_.append(np.sum(abs(np.diff(np.sign(frame_w - np.mean(frame_w))))) / (2 * Frames.frame_length))
    plt.show()

    return np.array(st_zcr_)

fs, y = wavfile.read('lar_F02_sa1.wav')

frames = Frames(y=y, fs=fs, gender='female')



def st_magnitude(Frames):
    st_mag = []
    i = 0
    for windowed_frame in Frames.windowed_frames:
        st_mag.append(np.sum(abs(windowed_frame)))
        i += 1
    return np.array(st_mag)


mag = st_magnitude(frames)

plot_result(Frames=frames, y=mag, title='st_mag')


def st_energy(Frames):
    energy = np.zeros(len(Frames.frames))
    for i, windowed_frame in enumerate(Frames.windowed_frames):
        energy[i] = np.mean(windowed_frame ** 2, axis=0)
    return energy



plot_result(Frames=frames, y=st_energy(frames), title='st_energy')


def st_HNR(Frames, time_step=0.01, silence_threshold=0.1):
    hnr = []
    for windowed_frame in Frames.windowed_frames:
        hnr.append(
            get_HNR(signal=windowed_frame, rate=Frames.fs, time_step=time_step, silence_threshold=silence_threshold))

    return np.array(hnr)

plot_result(Frames=frames, y=st_HNR(frames), title='st_HNR')
