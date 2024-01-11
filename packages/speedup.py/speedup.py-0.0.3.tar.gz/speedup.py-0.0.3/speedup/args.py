from argparse import ArgumentParser

arg_parser = ArgumentParser(description='Speed up (or slow down) your audio.')

ARGUMENTS = {
	'input_file': {
		'help': 'An audio file'
	},

	'multiplier': {
		'type': float,
		'help': 'Audio speed multiplier'
	},

	'--format': {
		'help': 'The audio format (and file extension) for the output file',
		'default': 'mp3',
	}
}

for key, value in ARGUMENTS.items():
	arg_parser.add_argument(key, **value)

MUTUALLY_EXCLUSIVE = {
	'--output-file': {
		'help': 'Where to save the sped up audio'
	},

	'--play': {
		'help': 'Play the spedup audio instead of saving it',
		'action': 'store_true'
	}
}

group = arg_parser.add_mutually_exclusive_group()
for key, value in MUTUALLY_EXCLUSIVE.items():
	group.add_argument(key, **value) # type: ignore
