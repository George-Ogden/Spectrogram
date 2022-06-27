import matplotlib.pyplot as plt
import scipy.signal
import soundfile as sf
import numpy as np
import cv2
from tqdm import trange

raw, sr = sf.read("music.ogg")
duration = len(raw) / sr
raw = raw.sum(axis=1)

sr = 3000
resampled = scipy.signal.resample(raw, int(duration * sr))

length = 512
window = np.arange(-length,length) / length * 2
window = np.exp(-np.pi * window ** 2)

f, t, Sxx = scipy.signal.spectrogram(np.pad(resampled,length),fs=sr,nperseg=len(window),window=window)
max = Sxx.max()

fps = 10
shape = (1920, 1080)
writer = cv2.VideoWriter("video.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, shape)
lookahead = 5

for i in trange(int(duration * fps)):
    position = int(i * sr / fps)
    signal = resampled[position : position + lookahead * sr]
    signal = np.pad(signal, length)
    f, t, Sxx  = scipy.signal.spectrogram(signal,fs=sr,nperseg=len(window),window=window)
    image = cv2.resize(Sxx, shape) * 255 / max
    writer.write(image.astype(np.uint8))

writer.release()