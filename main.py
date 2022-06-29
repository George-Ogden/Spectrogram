import scipy.signal
import numpy as np
import cv2

from ffmpeg import FFmpeg
import soundfile as sf
import asyncio

from pydub.utils import get_array_type
from pydub import AudioSegment

from argparse import ArgumentParser
import shutil
import os

from tqdm import trange
from halo import Halo


def parse_args():
    parser = ArgumentParser(description="Create spectrogram from music")
    parser.add_argument("-f", "--fps", type=float, default=30,
                        help="frame rate of video (default: 30)")
    parser.add_argument("-r", "--resolution", type=lambda x: tuple(map(int, x.lower().split("x"))),
                        default=(1920, 1080), help="video resolution (default: 1920x1080)")
    parser.add_argument("-l", "--lookahead", type=float, default=3,
                        help="number of seconds before each note is played (default: 3)")
    parser.add_argument("-i", "--input", required=True, help="input audio")
    parser.add_argument("-o", "--output", default="output.mp4",
                        help="output video (default: output.mp4)")
    parser.add_argument("-s", "--sampling_rate", type=int, default=16000,
                        help="adjusted sampling rate - approx twice the highest frequency (default: 16000)")
    parser.add_argument("-p", "--preview", action="store_true",
                        help="preview when complete")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    try:
        if not os.path.exists("tmp"):
            os.mkdir("tmp")

        # set parameters
        fps = args.fps
        shape = args.resolution
        lookahead = args.lookahead
        infile = args.input
        outfile = args.output
        sr = args.sampling_rate
        length = 1024
        width = 64
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

        # change format of input audio
        AudioSegment.from_file(infile).export("tmp/music.wav", format="wav")
        # load file
        raw, rate = sf.read("tmp/music.wav")
        if raw.ndim > 1:
            raw = raw.sum(axis=1)
        duration = len(raw) / rate

        # resample to lower sample rate
        resampled = scipy.signal.resample(raw, int(duration * sr))
        padding = int(lookahead * sr / width / 2)

        # create Gaussian window
        window = np.arange(-length, length) / length * 2
        window = np.exp(-np.pi * 2 * window ** 2)

        # calculate spectrogram
        spinner = Halo(text="Creating spectrogram", spinner="line")
        spinner.start()
        _, _, spectrogram = scipy.signal.spectrogram(np.pad(
            resampled, length), fs=sr, nperseg=2*length, noverlap=2*length-width, window=window)
        spinner.succeed()

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
            image = cv2.line(
                image, (shape[0]//2, 0), (shape[0]//2, shape[1]), 255, 1)
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

        # preview file
        if args.preview:
            os.startfile(outfile)

    except Exception as e:
        print(f"{type(e).__name__}: {e}")
    finally:
        # delete working directory
        if os.path.exists("tmp"):
            shutil.rmtree("tmp")