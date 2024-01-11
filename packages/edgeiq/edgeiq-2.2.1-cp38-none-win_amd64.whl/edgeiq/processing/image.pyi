import numpy as np
from typing import Tuple

__all__ = ['get_image_blob']

def get_image_blob(image: np.ndarray, scalefactor: float, size: Tuple[int, int], mean: Tuple[float, float, float], swaprb: bool, crop: bool) -> np.ndarray: ...
