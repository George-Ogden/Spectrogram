import matplotlib.pyplot as plt
import scipy.signal
import soundfile as sf
import numpy as np
import cv2
from ffmpeg import FFmpeg
import asyncio
import time
from tqdm import trange
from halo import Halo

raw, sr = sf.read("music.ogg")
raw = raw.sum(axis=1)
duration = len(raw) / sr

sr = 3000
fps = 10
shape = (1920, 1080)
length = 512
width = 64
lookahead = 5
size = int(lookahead * sr / width / 2)
resampled = scipy.signal.resample(raw, int(duration * sr))
kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])

window = np.arange(-length,length) / length * 2
window = np.exp(-np.pi * window ** 2)

_, _, spectrogram = scipy.signal.spectrogram(np.pad(resampled,length),fs=sr,nperseg=2*length, noverlap=2*length-width, window=window)
spectrogram = np.pad(spectrogram,((0,0), (size,size)))
spectrogram /= spectrogram.max()
spectrogram = np.sqrt(spectrogram)
spectrogram *= 255
spectrogram = np.flipud(spectrogram.astype(np.uint8))

writer = cv2.VideoWriter("video.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, shape, False)

for i in trange(int(duration * fps), message="Creating video"):
    left = int(i * sr / fps / width)
    image = cv2.resize(spectrogram[:,left : left + size * 2], shape)
    image = cv2.filter2D(image, -1, kernel)
    image = cv2.line(image, (shape[0]//2, 0), (shape[0]//2, shape[1]), 255, 1)
    writer.write(image)
    

writer.release()
ffmpeg = FFmpeg().option('y').input(
    "music.ogg"
).input(
    "video.mp4"
).output(
    "output.mp4"
)

with Halo(text="Adding audio", spinner="line"):
    asyncio.run(ffmpeg.execute())
