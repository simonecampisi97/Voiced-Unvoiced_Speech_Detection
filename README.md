# Voiced/Unvoiced Speech Detection

We present an algorithm for automatically classifying speech into two categories: voiced and unvoiced speech. 
The algorithm uses a Neural Network fitted with audio files which contain sentences spoken from both female, and male people. 
Each file audio is subjected to the short-time analysis for features extraction, and the extracted features are 18: short-time energy, 
short-time magnitude, short-time zero-crossing rate, the first 13 parameters of MFCC, and the gender of the speaker. 
The model computes a binary classification, predicting voiced/unvoiced speech with an overall accuracy of about 95.67 % on the test set.
