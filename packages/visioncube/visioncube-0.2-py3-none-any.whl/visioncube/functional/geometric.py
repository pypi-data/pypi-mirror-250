#!/usr/bin/env python3


import math
from typing import Union

import cv2 as cv
import numpy as np

__all__ = [
    'affine',
    'rotate'
]


def affine(
        image: np.ndarray,
        mat: np.ndarray,
        width: Union[int, None] = None,
        height: Union[int, None] = None,
        cval=127,
        mode='constant'
) -> np.ndarray:
    if not (len(mat.shape) == 2 and mat.shape[0] in {2, 3} and mat.shape[1] == 3):
        raise ValueError('`mat` should be a 3x3 or 2x3 matrix.')
    if mat.shape[0] == 3:
        mat = mat[:2, :]

    original_height, original_width = image.shape[:2]
    if width is None:
        width = original_width
    if height is None:
        height = original_height

    if isinstance(cval, (int, float)):
        cval = (cval, cval, cval)

    border_types = {
        'constant': cv.BORDER_CONSTANT,
        'edge': cv.BORDER_REPLICATE,
        'reflect': cv.BORDER_REFLECT
    }
    assert mode in border_types

    return cv.warpAffine(
        image,
        mat,
        dsize=(width, height),
        borderMode=border_types[mode],
        borderValue=cval
    )


def rotate(
        image: np.ndarray,
        degree: float = 0.0,
        width: Union[int, None] = None,
        height: Union[int, None] = None,
        cval=127,
        mode='constant',
        center=True
) -> np.ndarray:
    original_height, original_width = image.shape[:2]
    if width is None:
        width = original_width
    if height is None:
        height = original_height

    theta = degree / 180 * math.pi
    mat = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ], dtype=np.float32)

    if center:
        m0 = np.array([[1, 0, -original_width * 0.5], [0, 1, -original_height * 0.5], [0, 0, 1]], dtype=np.float32)
        m1 = np.array([[1, 0, width * 0.5], [0, 1, height * 0.5], [0, 0, 1]], dtype=np.float32)
        mat = m1 @ mat @ m0

    return affine(image, mat, width, height, cval, mode)


def rotate90(image: np.ndarray) -> np.ndarray:
    """
    Rotate the image 90 degrees
    """
    return np.rot90(image)
