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


# duration -> msecs
# fs -> sampling frequency
# y -> signal
def st_zcr(frames_windowed, frame_length):

    st_zcr_ = []
    # matrix where the rows contains contiguous slice
    for frame_w in frames_windowed:
        st_zcr_.append(np.sum(abs(np.diff(np.sign(frame_w - np.mean(frame_w))))) / (2 * frame_length))
    plt.show()

    return st_zcr_


fs, y = wavfile.read('lar_F02_sa1.wav')

frames = Frames.Frames(y=y, fs=fs)




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
