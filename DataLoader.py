import os

import numpy as np
from torchvision import datasets


class DataLoader(datasets.VisionDataset):
    def __init__(self, root):
        self.genders = ['FEMALE', 'MALE']

        self.file_names = []
        self.file_per_gender = []
        self.speaker_per_gender = []
        self.file_per_speaker = 0
        self.total_number = 0

        for gender_dir in [os.path.join(root, gender) for gender in self.genders]:
            gender_fileName = []
            self.speech_dir = os.path.join(gender_dir, "MIC")

            for speaker_dir in os.listdir(self.speech_dir):
                speech_list = os.listdir(speaker_dir)

                gender_fileName.append(speech_list)
                self.total_number += len(speech_list)

            gender_fileName = np.array(gender_fileName)
            self.file_names.append(gender_fileName)

        # test
        print("Len file_names(2):", len(self.file_names))
        print("Shape file_names[0](10,236):", self.file_names[0].shape)
        print()
        # end test

        self.file_names = np.array(self.file_names)
        self.file_per_gender = [self.file_names[idx] for idx in range(len(self.genders))]
        self.speaker_per_gender = [self.file_names[idx].shape[0] for idx in range(len(self.genders))]
        self.file_per_speaker = self.file_names.shape[2]

        # test
        print("File per gender(2360):", self.file_per_gender)
        print("File per speaker(236):", self.file_per_speaker)
        print("File_name shape(2, 10, 236):", self.file_names.shape)
        print("Speaker per gender(10):", self.speaker_per_gender)
        print()
        # end test

    def __len__(self):
        return self.total_number

    def get_genders(self):
        return self.genders

    def item_per_gender(self, gender):
        idx = self.genders.index(gender)
        return self.file_per_gender[idx]

    def __getitem__(self, index):
        gender_idx = 0 if index < self.item_per_gender("FEMALE") else 1
        index = index if gender_idx == 0 else index - self.item_per_gender(gender_idx)
        speaker_idx = index % self.speaker_per_gender[gender_idx]
        audio_id = index / self.speaker_per_gender[gender_idx]
        file_name = ""  # self.file_names[gender_idx, speaker_idx, audio_id]

        # test
        print(gender_idx, speaker_idx, audio_id)
        print(file_name)
        # end test

        return 0
