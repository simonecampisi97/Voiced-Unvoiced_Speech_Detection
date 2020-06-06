import os

import librosa
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import utils.VisualizeNN as VisNN

import DataLoader
from Frames import Frames


def nextpow2(x):
    return np.ceil(np.log2(abs(x)))


def plot_result(signal, Frames, ax):
    frame_time = []
    for i in range(len(Frames.windowed_frames)):
        frame_time.append((i * Frames.frame_length) * (1 / Frames.fs) * 1000)

    ax.plot(frame_time, signal)


def plot_segments(time, frames, prediction, ax):
    for i, frame_labeled in enumerate(prediction):
        idx = i * frames.shift_length
        if frame_labeled == 1:
            ax.axvspan(xmin=time[idx], xmax=time[idx + frames.frame_length - 1], ymin=-1000, ymax=1000,
                       alpha=0.2, zorder=-100, facecolor='green')
        else:
            ax.axvspan(xmin=time[idx], xmax=time[idx + frames.frame_length - 1], ymin=-1000, ymax=1000,
                       alpha=0.2, zorder=-100, facecolor='red')


# root: folder dataset
def get_pitch(absolute_audio_path, root):
    filename = absolute_audio_path.split('/')[-1]
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


def plot_pitches_prediction(time, frames, pitches, prediction, ax):
    f0_time = []
    for i in range(len(frames.windowed_frames[:-3])):
        f0_time.append((i * frames.shift_length + 1) * 1000 / frames.fs)
    ax.plot(f0_time, pitches, label='Pitches')

    plot_segments(time=time, frames=frames, prediction=prediction, ax=ax)


# compute the class prediction given the path of the new file audio,
# the path of dataset (if is available)
# and plot the results
def plot_model_prediction(path_file, model, gender, data_root=None):
    figure = plt.Figure(figsize=(9, 6), dpi=90)
    figure.suptitle('VUV predicion', fontsize=15)
    if data_root is not None:
        ax_1 = figure.add_subplot(211)
    else:
        ax_1 = figure.add_subplot(111)

    y, fs = librosa.core.load(path_file, sr=48000)
    frames = Frames(y=y, fs=fs)

    new_data = DataLoader.features_extraction(fs, y, gender_id=gender)
    prediction = model.predict_classes(new_data)
    prediction = prediction.reshape((-1,))

    time = np.arange(len(y)) * 1000 / fs
    plot_segments(time, frames, prediction, ax=ax_1)
    ax_1.plot(time, y, c='b')
    blue_line = mlines.Line2D([], [], color='blue',
                              markersize=15, label='Signal')

    legend = [blue_line, mpatches.Patch(label='Voiced-Prediction', color='green', alpha=.2),
              mpatches.Patch(label='Unvoiced-Prediction', color='red', alpha=.2)]

    ax_1.legend(handles=legend, loc='best')
    # ax_1.legend(['Signal', 'Voiced-Prediction', 'Unvoiced-Prediction'], loc='best')

    if data_root is not None:
        pitches = get_pitch(path_file, data_root)
        ax_2 = figure.add_subplot(212)
        plot_pitches_prediction(time, frames, pitches, prediction, ax=ax_2)
        blue_line = mlines.Line2D([], [], color='blue',
                                  markersize=15, label='Pitches')
        legend2 = [blue_line, mpatches.Patch(label='Voiced-Prediction', color='green', alpha=.2),
                   mpatches.Patch(label='Unvoiced-Prediction', color='red', alpha=.2)]

        ax_2.legend(handles=legend2, loc='best')

    return figure


# Standardizing the data
def standardize_dataset(X, mean=None, std=None):
    if mean is None:
        mean = np.mean(X, axis=0)  # Computing the dataset mean

    if std is None:
        std = np.std(X, axis=0)  # Computing the dataset standard deviation

    X_std = (X - mean) / std

    return X_std, mean, std


def butter_highpass(cutoff, fs, order=4):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False, output='ba')
    return b, a


def butter_highpass_filter(data, cutoff, fs, order=4):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y


def visualizeNN(ax,model, input_shape):
    network_structure = [[input_shape]]

    for layer in model.layers:
        network_structure.append([layer.output_shape[1]])

    network_structure = np.concatenate(network_structure)

    weights_list = []
    for layer in model.layers:
        weights = layer.get_weights()[0]
        weights_list.append(weights)

    feature_name = ['E', 'MG', 'ZRC', 'MFCC\n(1)', 'MFCC\n(2)', 'MFCC\n(3)', 'MFCC\n(4)', 'MFCC\n(5)', 'MFCC\n(6)',
                    'MFCC\n(7)',
                    'MFCC\n(8)', 'MFCC\n(9)', 'MFCC\n(10)', 'MFCC\n(11)', 'MFCC\n(12)', 'MFCC\n(13)', 'FEMALE', 'MALE']

    network = VisNN.DrawNN(network_structure, weights_list, feature_name)
    network.draw(ax=ax)

