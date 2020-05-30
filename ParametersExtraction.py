import librosa
import matplotlib.pyplot as plt
import numpy as np
import python_speech_features
from Signal_Analysis.features.signal import get_HNR

from Frames import Frames


def st_zcr(frames: Frames):
    st_zcr_ = []
    # matrix where the rows contains contiguous slice
    for frame_w in frames.windowed_frames:
        st_zcr_.append(np.sum(abs(np.diff(np.sign(frame_w - np.mean(frame_w))))) / (2 * frames.frame_length))
    plt.show()

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


def MFCC(signal, fs, frame_length, hop, window):
    n_mfcc = 13
    n_mels = 40
    n_fft = 512
    hop_length = hop
    fmin = 0
    fmax = None

    mfcc_librosa = librosa.feature.mfcc(y=signal, sr=fs, n_fft=frame_length,
                                        n_mfcc=n_mfcc, n_mels=n_mels,
                                        hop_length=hop_length,
                                        fmin=fmin, fmax=fmax, htk=False)

    mfcc_speech = python_speech_features.mfcc(signal=signal, samplerate=fs,
                                              winlen=frame_length / fs, winstep=hop_length / fs,
                                              numcep=n_mfcc, nfilt=n_mels, nfft=2048, lowfreq=fmin,
                                              highfreq=fmax, preemph=0.0, ceplifter=0, appendEnergy=False)

    print("shape mfcc(librosa):      ", np.array(mfcc_librosa).shape)
    print("shape mfcc(speech_feature):", np.array(mfcc_speech).shape)
    print()

    return None


def st_HNR(frames: Frames, time_step=0.01, silence_threshold=0.1):
    hnr = []
    for windowed_frame in frames.windowed_frames:
        hnr.append(get_HNR(signal=windowed_frame, rate=frames.fs,
                           time_step=time_step, silence_threshold=silence_threshold))

    return np.array(hnr)
