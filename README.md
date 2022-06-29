# Spectrogram
> A spectrogram is a visual representation of the spectrum of frequencies of a signal as it varies with time.

[Wikipedia](https://en.wikipedia.org/wiki/Spectrogram)
## Gabor Transform
The convolution used in this project is a Gaussian to create a [Scaled Gabor Transform](https://en.wikipedia.org/wiki/Gabor_transform#Scaled_Gabor_transform).
## Examples

## Usage
### Recommended Usage
```
python song.mp3 -o spectrogram.mp4
```
### Full Usage
```
usage: main.py [-h] -i INPUT [-o OUTPUT] [-p] [-f FPS] [-r RESOLUTION] [-l LOOKAHEAD] [-s SAMPLE_RATE]

Create spectrogram from music

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input audio
  -o OUTPUT, --output OUTPUT
                        output video (default: output.mp4)
  -p, --preview         preview when complete
  -f FPS, --fps FPS     frame rate of video (default: 30)
  -r RESOLUTION, --resolution RESOLUTION
                        video resolution (default: 1920x1080)
  -l LOOKAHEAD, --lookahead LOOKAHEAD
                        number of seconds before each note is played (default: 3)
  -s SAMPLE_RATE, --sample_rate SAMPLE_RATE
                        adjusted sampling rate - approx twice the highest frequency (default: 16000)
```
