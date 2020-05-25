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


def vuv_ceptrum(Frames, f0min=50, f0max=500, threshold=0.1):
    index_f0min = round(fs / f0min)  # Index of f0 min
    index_f0max = round(fs / f0max)  # Index of f0 max
    nfft = 2 ** nextpow2( Frames.frame_length)
    f0 = np.zeros(len(Frames.frames))
    vuv_cep = np.zeros(len(Frames.frames))
    for i, frame in enumerate(Frames.frames):

        S = np.fft.fft(frame, int(nfft))
        S_mag_log = np.log((abs(S)))# log(Magnitude) spectrum

        cep = np.real(np.fft.ifft(S_mag_log))  # The real cepstrum = real(inverseDFT(lof(magnitude(DFT))))
        cep_shift = np.fft.fftshift(cep)  # centered ceptrum
        cep2 = cep_shift[index_f0max >= 0]
        print(cep2)

        cep_max = np.amax(cep2)
        print(cep_max)
        ind_cep_max = np.argmax(cep2)
        print(ind_cep_max)
        f0[i] = Frames.fs / (index_f0max + ind_cep_max)  # potential f0 value

        if cep_max > threshold:
            vuv_cep[i] = 1
        else:
            vuv_cep[i] = 0
        f0[i] = f0[i] * vuv_cep[i] # final f0
    return f0


fs, y = wavfile.read('lar_F02_sa1.wav')

frames = Frames.Frames(y=y, fs=fs, gender='female')

f0 = vuv_ceptrum(Frames=frames)

#print(f0)
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
