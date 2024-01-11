# speedup.py
A simple Python module to speed up (or slow down) audio. It also comes with a commandline interface and a Flask server.

## Installation
To install `speedup.py` run:
```
pip install speedup.py
```

The `speedup.py` module has optional dependencies required for the CLI and API modules. Run one of the three lines below to:
```
pip install speedup.py[cli]			# Only install CLI dependencies
pip install speecup.py[server]		# Only install server dependencies
pip install speedup.py[cli,server]	# Install dependencies for both
```

## Usage
Assuming you have `soundfile` for reading in audio files, speeding up audio from a file called `audio.mp3` by a factor of 1.5 takes four lines of Python code:
```py
from speedup import speedup
import soundfile as sf
audio, samplerate = sf.read("audio.mp3")
spedup_audio = speedup(audio, 1.5)
```

The `speedup` function returns the sped up audio as a NumPy array, which you can then save to a file like so:
```py
sf.write("spedup-audio.mp3", spedup_audio, samplerate)
```

### CLI usage
The CLI abstracts everything in the previous section away.

To speed up `audio.mp3` by a factor of `1.5`, run:
```
speedup audio.mp3 1.5
```

Despite the project's name, **multipliers below 1 work as well.** The audio will be slowed down in this case:
```
speedup audio.mp3 0.75
```

In this case, the sped up audio is saved to `audio-1.5x.mp3` by default. You can specify the output file using `--output-file`:
```
speedup audio.mp3 1.5 --output-file spedup.mp3
```

Since the resample operation takes some time, the `--play` option lets you hear your spedup audio without resampling:
```
speedup audio.mp3 1.5 --play
```
Using `--play` prevents saving the audio to a file, since the exact same file would be created, except the sample rate would be multiplied. This is because compressed audio formats (especially MPEG-3) don't support custom sample rates.

The `--output-file` and `--play` options are mutually exclusive.

## Running the Flask server
You can run the Flask development server with:
```
python -m speedup.api
```
For production environments however, you should use a WSGI server like `gunicorn`:
```
pip install gunicorn
gunicorn -w 4 speedup.api:app
```

## Building
To build the Python package, run the below commands in your terminal:
```
git clone https://github.com/trustytrojan/speedup.py
cd speedup.py
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m build
```
