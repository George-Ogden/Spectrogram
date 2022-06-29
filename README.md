# Spectrogram
> A spectrogram is a visual representation of the spectrum of frequencies of a signal as it varies with time.

[Wikipedia](https://en.wikipedia.org/wiki/Spectrogram)
## Gabor Transform
The convolution used in this project is a Gaussian to create a [Scaled Gabor Transform](https://en.wikipedia.org/wiki/Gabor_transform#Scaled_Gabor_transform).
## Examples
### The Chain
[![The Chain Spectrogram](http://img.youtube.com/vi/W_m7tK5T9-I/0.jpg)](http://www.youtube.com/watch?v=W_m7tK5T9-I "The Chain Spectrogram")
### Smoke on the Water
[![Smoke on the Water Spectrogram](http://img.youtube.com/vi/VQ4pzRnL0TA/0.jpg)](http://www.youtube.com/watch?v=VQ4pzRnL0TA "Smoke on the Water Spectrogram")
### 7 Nation Army
[![7 Nation Army Spectrogram](http://img.youtube.com/vi/BVsp23B8dWo/0.jpg)](http://www.youtube.com/watch?v=BVsp23B8dWo "7 Nation Army Spectrogram")
### Für Elise
[![Für Elise Spectrogram](http://img.youtube.com/vi/a5Or6Bafqug/0.jpg)](http://www.youtube.com/watch?v=a5Or6Bafqug "Für Elise Spectrogram")  
### Full Playlist
[https://www.youtube.com/watch?v=W_m7tK5T9-I&list=PL1_riyn9sOjc3FAxJN3EPs8b6vM4ArGfp](https://www.youtube.com/watch?v=W_m7tK5T9-I&list=PL1_riyn9sOjc3FAxJN3EPs8b6vM4ArGfp)
## Install
You will need to install [ffmpeg](https://ffmpeg.org/download.html) as well as downloading Python dependencies
```
pip install -r requirements.txt
```
## Usage
### Recommended Usage
```
python -i song.mp3 -o spectrogram.mp4
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
