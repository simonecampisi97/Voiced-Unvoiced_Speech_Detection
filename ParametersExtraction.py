from typing import List

import librosa
from librosa.feature import zero_crossing_rate
from librosa.util import frame
from librosa.util import example_audio_file
import wave, struct
from scipy.signal import get_window
from scipy.io import wavfile
import soundfile as sf
import matplotlib.pyplot as plt
import Frames
import numpy as np
from utils import *
from Signal_Analysis.features.signal import get_HNR


# duration -> msecs
# fs -> sampling frequency
# y -> signal
def st_zcr(Frames):
    """
    :param Frames: Frames object
    :return:
    """
    st_zcr_ = []
    # matrix where the rows contains contiguous slice
    for frame_w in Frames.frames_windowed:
        st_zcr_.append(np.sum(abs(np.diff(np.sign(frame_w - np.mean(frame_w))))) / (2 * Frames.frame_length))
    plt.show()

    return st_zcr_


fs, y = wavfile.read('lar_F02_sa1.wav')

frames = Frames.Frames(y=y, fs=fs, gender='female')

text = open('ref_F02_sa1.f0', 'r')
line = text.readline()
f0_text = []
while line:
    str = line.strip()
    f0_text.append(float(str.split(" ")[0]))
    line = text.readline()
text.close()


def amplitude():
    pass


def st_energy(Frames):
    energy = np.zeros(len(Frames.frames))
    # frame_time = np.zeros(len(Frames.frames))
    for i, windowed_frame in enumerate(Frames.windowed_frames):
        energy[i] = np.mean(windowed_frame ** 2, axis=0)
    return energy


def st_HNR(Frames, time_step=0.01, silence_threshold=0.1):
    hnr = []
    for frame in Frames.windowed_frames:
        hnr.append(get_HNR(signal=frame, rate=Frames.fs, time_step=time_step, silence_threshold=silence_threshold))
    return hnr


# level-crossing rate
def LCR():
    pass


def EGG_to_DEGG():
    pass
