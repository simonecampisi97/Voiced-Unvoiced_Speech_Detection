import os

import numpy as np
from scipy.io import wavfile
from torchvision import datasets


def label_extraction(file_name):
    with open(file_name) as f:
        voicing = [int(line.rstrip().split(" ")[1]) for line in f]
    voicing = np.array(voicing)

    return voicing


def features_extraction(rate, data):
    feature = []
    # TODO add feature extraction

    return np.array(feature)


class DataLoader(datasets.VisionDataset):

    def __init__(self, root):
        self.root = root
        self.genders = ['FEMALE', 'MALE']

        self.file_names = []
        self.file_per_gender = []
        self.speaker_per_gender = []
        self.file_per_speaker = 0
        self.total_number = 0

        for gender_dir in [os.path.join(root, gender) for gender in self.genders]:
            gender_fileName = []
            speech_dir = os.path.join(gender_dir, "MIC")

            for speaker in os.listdir(speech_dir):
                speaker_dir = os.path.join(speech_dir, speaker)
                speech_list = os.listdir(speaker_dir)

                gender_fileName.append(speech_list)
                self.total_number += len(speech_list)

            gender_fileName = np.array(gender_fileName)
            self.file_names.append(gender_fileName)

        # test
        # print("Len file_names(2):", len(self.file_names))
        # print("Type file_names[0]", type(self.file_names[0]))
        # print("Type file_names[0][8]", type(self.file_names[0][8]))
        # print("Shape file_names[0](10,236):", self.file_names[0].shape)
        # print()
        # end test

        self.file_names = np.array(self.file_names)
        self.file_per_gender = [self.file_names[idx].size for idx in range(len(self.genders))]
        self.speaker_per_gender = [self.file_names[idx].shape[0] for idx in range(len(self.genders))]
        self.file_per_speaker = self.file_names.shape[2]

        # test
        # print("File_name shape(2, 10, 234):", self.file_names.shape)
        # print("File_name size(2680):", self.file_names.size)
        # print("File per gender(2360):", self.file_per_gender)
        # print("File per speaker(234):", self.file_per_speaker)
        # print("Speaker per gender(10):", self.speaker_per_gender)
        # print()
        # end test

    def __len__(self):
        return self.total_number

    def get_genders(self):
        return self.genders

    def item_per_gender(self, gender):
        idx = self.genders.index(gender)
        return self.file_per_gender[idx]

    def __getitem__(self, index):
        # Retrieve the position of the file from the index
        gender_idx = 0 if index < self.item_per_gender("FEMALE") else 1
        index = index if gender_idx == 0 else index - self.item_per_gender(self.genders[gender_idx])
        speaker_idx = int(index / (self.file_per_gender[gender_idx] / self.speaker_per_gender[gender_idx]))
        audio_id = int(index % (self.file_per_gender[gender_idx] / self.speaker_per_gender[gender_idx]))

        file_name = self.file_names[gender_idx, speaker_idx, audio_id]

        # Build the path of the file required and the label associated
        wav_path = self.get_mic_path(file_name, gender_idx, speaker_idx)
        label_path = self.get_ref_path(file_name, gender_idx, speaker_idx)

        # Load and process the data
        fs, x = wavfile.read(wav_path)
        y = label_extraction(label_path)

        features = features_extraction(rate=fs, data=x)

        # test
        print("{}  pos:({}, {}, {})".format(file_name, gender_idx, speaker_idx, audio_id))
        print(wav_path, " -  SampleRate:", fs)
        print(label_path, " -  Frame_num:", len(y))
        print()
        # end test

        return features, y

    def get_ref_path(self, file_name, gender_idx, speaker_idx):
        return os.path.join(self.root,
                            self.genders[gender_idx],
                            "REF",
                            self.genders[gender_idx][0] + "{:02d}".format(speaker_idx + 1),
                            "ref" + file_name[3:])[:-4] + ".f0"

    def get_mic_path(self, file_name, gender_idx, speaker_idx):
        return os.path.join(self.root,
                            self.genders[gender_idx],
                            "MIC",
                            self.genders[gender_idx][0] + "{:02d}".format(speaker_idx + 1),
                            file_name)
