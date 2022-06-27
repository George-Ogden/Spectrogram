import matplotlib.pyplot as plt
import scipy.signal
import soundfile as sf
import numpy as np
import cv2

signal, sr = sf.read("music.ogg")
length = 10
signal = signal.sum(axis=1)[sr * 5:sr * (5 + length)]
sr = 3000
signal = scipy.signal.resample(signal, sr * length)
sf.write("music.wav", np.expand_dims(signal, 1), sr)

length = 512
window = np.arange(-length,length) / length * 2
window = np.exp(-np.pi * window ** 2)
signal = np.pad(signal, length * 2)

f, t, Sxx  = scipy.signal.spectrogram(signal,fs=sr,nperseg=len(window),window=window)
plt.pcolormesh(t, f, Sxx, shading='gouraud')
plt.show()