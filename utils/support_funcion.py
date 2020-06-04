import numpy as np
import matplotlib.pyplot as plt
import DataLoader as dl
import librosa
import os
from Frames import Frames


def nextpow2(x):
    return np.ceil(np.log2(abs(x)))


def plot_result(signal, Frames, ax):
    frame_time = []
    for i in range(len(Frames.windowed_frames)):
        frame_time.append((i * Frames.frame_length) * (1 / Frames.fs) * 1000)

    ax.plot(frame_time, signal)


def plot_segments(time, frames, prediction):
    for i, frame_labeled in enumerate(prediction):
        idx = i * frames.shift_length
        if frame_labeled == 1:
            plt.axvspan(xmin=time[idx], xmax=time[idx + frames.frame_length - 1], ymin=-1000, ymax=1000,
                        alpha=0.2, zorder=-100, facecolor='g', label='Voiced-Region')


# root: folder dataset SPEECH_DATA
def get_pitch(absolute_audio_path, root):
    filename = absolute_audio_path.split('\\')[-1]
    filename_splitted = filename.split('_')
    M_F = filename_splitted[1][0]
    filename_ref = 'ref_' + filename_splitted[1] + '_' + filename_splitted[2].split('.')[0] + '.f0'
    if M_F == 'M':
        gender = 'MALE'
    else:
        gender = 'FEMALE'

    path_ref = os.path.join(root, gender, 'REF', filename_splitted[1], filename_ref)

    with open(path_ref) as f:
        pitches = [(line.rstrip().split(" ")[0]) for line in f]

    return np.array(pitches).astype(np.float32)


def plot_pitches_pred(time, frames, pitches, prediction):
    f0_time = []
    for i in range(len(frames.windowed_frames[:-3])):
        f0_time.append((i * frames.shift_length + 1) * 1000 / frames.fs)
    plt.plot(f0_time, pitches, label='Pitches')

    plot_segments(time=time, frames=frames, prediction=prediction)


def plot_model_prediction(path_file, data_root, model):
    y, fs = librosa.core.load(path_file, sr=48000)
    frames = Frames(y=y, fs=fs)
    new_data = dl.features_extraction(fs, y, gender_id=1)
    prediction = model.predict_classes(new_data)
    prediction = prediction.reshape((-1,))
    pitches = get_pitch(path_file, data_root)

    time = np.arange(len(y)) * 1000 / fs
    plot_segments(time, frames, prediction)
    plt.plot(time, y, label='Signal')
    plt.legend(['Signal', 'Voiced-Region'])
    plt.show()

    plt.figure()
    plt.legend()
    plot_pitches_pred(time, frames, pitches, prediction)
    plt.legend(['Pitches', 'Voiced-Region'])
    plt.show()
