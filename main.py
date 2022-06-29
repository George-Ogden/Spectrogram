import scipy.signal
import numpy as np
import cv2
import os

from pydub.utils import get_array_type
from pydub import AudioSegment
from ffmpeg import FFmpeg
import soundfile as sf
import asyncio
import array

from tqdm import trange
from halo import Halo

fps = 30
shape = (1920, 1080)
lookahead = 3
infile = "Fur Elise.mp3"
outfile = "Fur Elise.mp4"

if not os.path.exists("tmp"):
    os.mkdir("tmp")

AudioSegment.from_file(infile).export("tmp/music.wav", format="wav")

# load file
raw, sr = sf.read("tmp/music.wav")
raw = raw.sum(axis=1)

duration = len(raw) / sr

# set parameters
sr = 8000
length = 1024
width = 64
kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

# resample to lower sample rate
resampled = scipy.signal.resample(raw, int(duration * sr))
padding = int(lookahead * sr / width / 2)

# create Gaussian window
window = np.arange(-length, length) / length * 2
window = np.exp(-np.pi * 2 * window ** 2)

# calculate spectrogram
_, _, spectrogram = scipy.signal.spectrogram(np.pad(resampled, length), fs=sr, nperseg=2*length, noverlap=2*length-width, window=window)
# process spectrogram for better display
spectrogram = np.pad(spectrogram, ((0, 0), (padding, padding)))
spectrogram /= spectrogram.max()
spectrogram = 1 - (1 - np.minimum(1, np.sqrt(spectrogram))) ** 4
spectrogram *= 255
spectrogram = np.flipud(spectrogram.astype(np.uint8))

# open video
writer = cv2.VideoWriter(
    "tmp/video.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, shape, False)

# add each frame to video
for i in trange(int(duration * fps), desc="Creating video"):
    # take a slice of the entire spectrogram
    left = int(i * sr / fps / width)
    image = cv2.resize(spectrogram[:, left:left + padding * 2], shape)
    # sharpen
    image = cv2.filter2D(image, -1, kernel)
    # add a line down the centre
    image = cv2.line(image, (shape[0]//2, 0), (shape[0]//2, shape[1]), 255, 1)
    # save image to video
    writer.write(image)
writer.release()

# dub music
ffmpeg = FFmpeg().option('y').input(
    infile
).input(
    "tmp/video.mp4"
).output(
    outfile
)
# add spinner as this takes a while
spinner = Halo(text="Adding audio", spinner="line")
spinner.start()
asyncio.run(ffmpeg.execute())
spinner.succeed()
