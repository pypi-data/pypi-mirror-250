from typing import Callable
from numpy.typing import ArrayLike
import numpy as np
import scipy.signal

speedup: Callable[[ArrayLike, float], ArrayLike]
speedup = lambda audio, multiplier: scipy.signal.resample(audio, int(np.size(audio, axis=0) * (1 / multiplier)))
