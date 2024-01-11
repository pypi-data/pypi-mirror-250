import os
from sounddevice import play
from speedup import speedup
from speedup.args import arg_parser
import soundfile as sf
from sys import stdout, stdin
from tempfile import NamedTemporaryFile

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
