from librosa.feature import zero_crossing_rate
from librosa.util import frame
import wave, struct
from scipy.signal import get_window
from scipy.io import wavfile
import soundfile as sf

import numpy as np


def split_audio():
    pass


# duration -> msec
# fs -> sampling frequency
# y -> signal
def st_zcr(y, fs, duration=30, overlap_rate=0.5, window='hann'):
    # Analysis frame length (in samples)
    frame_length = np.floor(duration * fs / 1000)
    shift = 1 - overlap_rate
    # shift length in samples -> hop_length
    frame_shift = round(frame_length * shift)

    # matrix where the rows contains contiguous slice
    frames = frame(y, frame_length=frame_length, hop_length=frame_shift, axis=0)
    window = get_window(window=window)
    return frames


def amplitude():
    pass


def energy():
    pass


def EMFCC():
    pass


def pitch():
    pass


# level-crossing rate
def LCR():
    pass


def EGG_to_DEGG():
    pass
