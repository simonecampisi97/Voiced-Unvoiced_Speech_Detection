import librosa
from librosa.feature import zero_crossing_rate
from librosa.util import frame
from librosa.util import example_audio_file
import wave, struct
from scipy.signal import get_window
from scipy.io import wavfile
import soundfile as sf
import matplotlib.pyplot as plt

import numpy as np


def split_audio(y, fs, duration=30, overlap_rate=0.5, window='hann'):
    """
    :param y: audio time series
    :param fs: sampling frequency (Number of samples per second)
    :param duration: Analysis frame duration (in msec)
    :param overlap_rate: Overlapping rate between successive frame (typically between 50% and 100%)
    :param window: Type of the window to be applied on each frame
    """

    frame_length = int(np.floor(duration * fs / 1000))  # Analysis frame length (in samples)

    shift = 1 - overlap_rate # Shift is the rate of sliding the window

    # shift length in samples -> hop_length
    frame_shift = round(frame_length * shift)
    # matrix where the rows contains contiguous slice
    frames = frame(y, frame_length=frame_length, hop_length=frame_shift, axis=0)
    window = get_window(window=window, Nx=frame_length, fftbins=False)
    windowed_frame = np.multiply(frames, window)

    return windowed_frame


# duration -> msec
# fs -> sampling frequency
# y -> signal
def st_zcr(y, fs, duration=30, overlap_rate=0.5, window='hann'):
    # Analysis frame length (in samples)
    frame_length = int(np.floor(duration * fs / 1000))
    frame_time = []
    st_zcr_ = []
    shift = 1 - overlap_rate
    # shift length in samples -> hop_length
    frame_shift = round(frame_length * shift)
    # matrix where the rows contains contiguous slice
    frames = frame(y, frame_length=frame_length, hop_length=frame_shift, axis=0)
    window = get_window(window=window, Nx=frame_length, fftbins=False)
    windowed_frame = np.multiply(frames, window)

    frame_nb = round(len(y) - frame_length) / frame_shift

    # Ts = 1 / fs
    # k = 0
    for frame_w in windowed_frame:
        # frame_time.append((k*(frame_shift+1))*Ts*1000)
        st_zcr_.append(np.sum(abs(np.diff(np.sign(frame_w - np.mean(frame_w))))) / (2 * frame_length))
        # k += 1

    # plt.plot(frame_time[:200], st_zcr_[:200])
    # print(len(st_zcr_))
    plt.show()

    return st_zcr_


# y, fs = librosa.load(librosa.util.example_audio_file())

# zcr = st_zcr(y=y, fs=fs)


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
