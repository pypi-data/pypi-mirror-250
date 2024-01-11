from typing import Callable
from numpy.typing import ArrayLike
from scipy.signal import resample
from numpy import size

speedup: Callable[[ArrayLike, float], ArrayLike]
'''
Speed up a NumPy array of audio data `audio` by `multiplier`.
This is a simple wrapper around `scipy.signal.resample`.
'''
speedup = lambda audio, multiplier: resample(audio, int(size(audio, axis=0) * (1 / multiplier)))
