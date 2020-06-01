import torchvision.transforms as transforms
from ParametersExtraction import *
from scipy.io import wavfile
from librosa.core import load

from DataLoader import DataLoader

if __name__ == "__main__":
    dataset_dir = "C:\\Users\\simoc\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"
    # dataset_dir = "C:\\Users\\carot\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"

    transform = transforms.Compose(
        [transforms.ToTensor()])

    dl = DataLoader(dataset_dir, transform)

    _, feature, label = dl[0]

    print("Type feature:", type(feature))
    print("Type labels:", (type(label)))
    print()

    print("Size feature:", feature.shape)
    print("Size labels:", label.shape)
    print()

    print(type(label[0]), label[0])

    y, fs = load(path='TestData/lar_M08_si1794.wav', sr=48000)
    frames = Frames(y=y, fs=fs)

    print('Number of Frame of the signal: ', len(frames.windowed_frames))

    MFCC(signal=y.astype('float'), fs=fs, frame_length=frames.frame_length, hop=frames.shift_length, window='hann')
