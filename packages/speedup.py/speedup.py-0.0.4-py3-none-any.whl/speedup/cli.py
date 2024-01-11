import os
from speedup import speedup
from argparse import ArgumentParser
from sys import stdout, stdin, stderr
from tempfile import NamedTemporaryFile

try:
	from sounddevice import play
	import soundfile as sf
except ModuleNotFoundError:
	print('''Either the `soundfile` or `sounddevice` modules were not found.
Did you install `speedup.py` with the optional dependency group `[cli]`?
If not, run `pip install speedup.py[cli]`.''', file=stderr)
	exit(1)

arg_parser = ArgumentParser(description='Speed up (or slow down) audio.')
arg_parser.add_argument('input_file', help='An audio file')
arg_parser.add_argument('multiplier', type=float, help='Audio speed multiplier')
arg_parser.add_argument('--format', default='mp3', help='Output file format')
mutually_exclusive = arg_parser.add_mutually_exclusive_group()
mutually_exclusive.add_argument('--output-file', help='Where to save the sped up audio')
mutually_exclusive.add_argument('--play', action='store_true', help='Play the spedup audio instead of saving it')

def highest_index(s: str, target: str) -> int:
	for i in range(len(s) - 1, -1, -1):
		if s[i] == target:
			return i
	return -1

def main() -> None:
	args = arg_parser.parse_args()

	if args.multiplier == 1 and not args.play:
		# Don't waste time
		return

	if args.format is None:	# Default to MP3 format
		args.format = 'mp3'

	if args.input_file == "-": # Handle `-` as stdin
		# soundfile doesn't like memory buffers so use tempfiles instead
		with NamedTemporaryFile(delete=False) as tf:
			tf.write(stdin.buffer.read())
		audio, samplerate = sf.read(tf.name)
		os.remove(tf.name)
		if args.output_file is None and not args.play:
			print("--output-file or --play is required when input_file is `-` (stdin)")
			exit(1)
	else: # Read from input_file
		# Create output filename if not already provided
		if args.output_file is None:
			input_filename = args.input_file[highest_index(args.input_file, '/') + 1 : highest_index(args.input_file, '.')]
			args.output_file = f'{input_filename}-{args.multiplier}x.{args.format}'
		audio, samplerate = sf.read(args.input_file)

	if args.play: # Play the spedup audio instead of saving
		play(audio, samplerate * args.multiplier, blocking=True)
		return

	spedup_audio = speedup(audio, args.multiplier)

	if args.output_file == '-': # Handle `-` as stdout
		# Default to WAV for compatibility with other programs
		sf.write(stdout.buffer, spedup_audio, samplerate, format="wav")
	else: # Save to output_file
		sf.write(args.output_file, spedup_audio, samplerate)

if __name__ == '__main__':
	main()
