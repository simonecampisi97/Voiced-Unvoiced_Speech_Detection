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


def vuv_ceptrum(Frames, f0min=50, f0max=500, threshold=0.05):
    """
    :param Frames: Frames Object
    :param f0min: minimum f0 value
    :param f0max: maximun f0 value
    :param threshold: Threshold that will used to decide about voicing activity
    :return: array of f0 final value
    """
    index_f0max = round(fs / f0max)  # Index of f0 max
    nfft = int(2 ** nextpow2(Frames.frame_length))
    f0_ = np.zeros(len(Frames.frames))
    vuv_cep = np.zeros(len(Frames.frames))
    # to plot
    f0_time = np.zeros(len(Frames.frames))

    for i, frame in enumerate(Frames.frames):

        S = np.fft.fft(frame, int(nfft))

        S_mag_log = np.log((abs(S)))  # log(Magnitude) spectrum

        cep_real = np.real(np.fft.ifft(S_mag_log))  # The real cepstrum = real(inverseDFT(lof(magnitude(DFT))))

        index_cep = np.arange(len(cep_real))  # The time indexes of the cepstrum (the quefrencies)
        index_cep_shift = index_cep - np.floor(len(cep_real) / 2)  # The zero-centered quefrencies
        cep_shift = np.fft.fftshift(cep_real)  # centered ceptrum
        cep = cep_shift[index_cep_shift >= 0]  # The part of the centred cepstrum located in the positive quefrencies

        # Search for the local maximum of the cepstrum located beyond index_f0_max
        cep_max = np.amax(cep[index_f0max: len(cep) - 1])
        ind_cep_max = np.argmax(cep[index_f0max: len(cep) - 1])
        # print(ind_cep_max)
        f0_[i] = Frames.fs / (index_f0max + ind_cep_max)  # potential f0 value
        f0_time[i] = (i * Frames.shift_length + 1) * (1000 / fs)
        if cep_max > threshold:
            vuv_cep[i] = 1
        else:
            vuv_cep[i] = 0
        f0_[i] = f0_[i] * vuv_cep[i]  # final f0
    # plot signal
    plt.figure()
    plt.plot(np.arange(len(Frames.y)), Frames.y)
    # plt.plot(f0_time[:30],f0_[:30])
    plt.show()
    return f0_


fs, y = wavfile.read('lar_F02_sa1.wav')

frames = Frames.Frames(y=y, fs=fs, gender='female')

f0 = vuv_ceptrum(Frames=frames)


# print(f0)
# print(len(frames.frames))


def amplitude():
    pass


def st_energy(Frames):
    energy = np.zeros(len(Frames.frames))
    # frame_time = np.zeros(len(Frames.frames))
    for i, windowed_frame in enumerate(Frames.windowed_frames):
        energy[i] = np.mean(windowed_frame ** 2, axis=0)
        # frame_time[i] = (i * Frames.shift_length) * (1 / fs) * 1000
    # plt.figure()
    # plt.plot(frame_time, energy)
    # plt.show()

    return energy


e = st_energy(frames)


def EMFCC():
    pass


def pitch():
    pass


# level-crossing rate
def LCR():
    pass


def EGG_to_DEGG():
    pass
