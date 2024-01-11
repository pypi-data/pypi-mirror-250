from tempfile import NamedTemporaryFile
from typing import Any, Optional
from speedup import speedup
from io import BytesIO
import os

try:
	from flask import Flask, request
	import soundfile as sf
except ModuleNotFoundError:
	from sys import stderr
	print('''
		Either the `soundfile` or `flask` modules were not found.
		Did you install `speedup.py` with the optional dependency group `[server]`?
		If not, run `pip install speedup.py[server]`.
	''', file=stderr)
	exit(1)

app = Flask(__name__)

def get_qp_value(*names: str, type: Optional[type] = None) -> Optional[Any]:
	for name in names:
		value = request.args.get(name, type=type)
		if value is not None:
			return value

@app.route('/speedup', methods=['GET', 'POST'])
def handle_speedup():
	try:
		# Get audio format from Content-Type
		content_type = request.headers['Content-Type']
		if 'audio' not in content_type:
			return 'Invalid content type. Only audio files are allowed.', 400
		input_format = content_type.split('/')[1].strip()

		# soundfile doesn't like reading from memory buffers so this is the workaround!
		with NamedTemporaryFile(suffix=f'.{input_format}', delete=False) as temp_audio_file:
			temp_audio_file.write(request.data)
		audio, samplerate = sf.read(temp_audio_file.name)
		os.remove(temp_audio_file.name)

		# Query params
		multiplier = get_qp_value('m', 'multiplier', type=float)
		if multiplier is None:
			return 'Multiplier not provided. Supply it using the `multiplier` or `m` query parameter.', 400
		output_format = get_qp_value('f', 'format') or 'mp3'

		# Speedup and send it back
		spedup_audio = speedup(audio, multiplier)
		with BytesIO() as output_buffer:
			sf.write(output_buffer, spedup_audio, samplerate, format=output_format)
			return output_buffer.getvalue(), 200, {'Content-Type': 'audio/mpeg'}
	except Exception as e:
		return str(e), 500

if __name__ == '__main__':
	app.run(port=8000)
