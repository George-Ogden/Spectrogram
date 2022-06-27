import matplotlib.pyplot as plt
import scipy.signal
import soundfile as sf
import numpy as np
import cv2
from tqdm import trange
from ffmpeg import FFmpeg
import asyncio
import time

raw, sr = sf.read("music.ogg")
raw = raw.sum(axis=1)
duration = len(raw) / sr

sr = 5000
resampled = scipy.signal.resample(raw, int(duration * sr))

length = 512
window = np.arange(-length,length) / length * 2
window = np.exp(-np.pi * window ** 2)

width = 64
lookahead = 5
resampled.resize(len(resampled) + lookahead * sr)
f, t, Sxx = scipy.signal.spectrogram(np.pad(resampled,length),fs=sr,nperseg=2*length, noverlap=2*length-width)
Sxx /= Sxx.max()
Sxx = np.sqrt(Sxx)
Sxx *= 255
Sxx = np.flipud(Sxx.astype(np.uint8))

fps = 10
shape = (1920, 1080)
writer = cv2.VideoWriter("video.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, shape, False)

for i in trange(int(duration * fps)):
    position = int(i * sr / fps / width)
    image = cv2.resize(Sxx[:,position : int(position + lookahead * sr / width)], shape)
    writer.write(image)
    

writer.release()
ffmpeg = FFmpeg().option('y').input(
    "music.ogg"
).input(
    "video.mp4"
).output(
    "output.mp4"
)

asyncio.run(ffmpeg.execute())
