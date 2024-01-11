#!/usr/bin/env python3


from typing import Union

import cv2 as cv
import numpy as np

__all__ = [
    'resize',
    'pad',
    'pad_to_square',
]


def resize(
        image: np.ndarray,
        width: Union[int, float, None] = None,
        height: Union[int, float, None] = None,
        longer_side: Union[int, float, None] = None,
        shorter_side: Union[int, float, None] = None,
        interpolation='cubic'
) -> np.ndarray:
    original_height, original_width = image.shape[:2]

    wh_mode = width is not None or height is not None
    ls_mode = longer_side is not None or shorter_side is not None

    if wh_mode and ls_mode:
        raise RuntimeError('Only one of `width-height` or `longer-shorter` mode should be chosen.')

    if ls_mode:
        if original_width >= original_height:
            width = longer_side
            height = shorter_side
        else:
            width = shorter_side
            height = longer_side

    if width is None and height is None:
        return image

    if isinstance(width, float):
        width = int(width * original_width)
    if isinstance(height, float):
        height = int(height * original_height)

    if width is None:
        width = int(height * (original_width / original_height))
    if height is None:
        height = int(width * (original_height / original_width))

    cv_inter = {
        'cubic': cv.INTER_CUBIC,
        'linear': cv.INTER_LINEAR,
        'area': cv.INTER_AREA,
        'nearest': cv.INTER_NEAREST
    }
    assert interpolation in cv_inter

    return cv.resize(
        image,
        dsize=(width, height),
        interpolation=cv_inter[interpolation]
    )


def pad(
        image: np.ndarray,
        top: Union[int, float] = 0,
        right: Union[int, float] = 0,
        bottom: Union[int, float] = 0,
        left: Union[int, float] = 0,
        cval=127,
        mode='constant'
) -> np.ndarray:
    height, width = image.shape[:2]
    if isinstance(top, float):
        top = int(height * top)
    if isinstance(right, float):
        right = int(width * right)
    if isinstance(bottom, float):
        bottom = int(height * bottom)
    if isinstance(left, float):
        left = int(width * left)

    if isinstance(cval, (int, float)):
        cval = (cval, cval, cval)

    border_types = {
        'constant': cv.BORDER_CONSTANT,
        'edge': cv.BORDER_REPLICATE,
        'reflect': cv.BORDER_REFLECT
    }
    assert mode in border_types

    return cv.copyMakeBorder(
        image,
        top=top,
        bottom=bottom,
        left=left,
        right=right,
        borderType=border_types[mode],
        value=cval
    )


def pad_to_square(
        image: np.ndarray,
        size: Union[int, None] = None,
        cval=127,
        mode='constant'
) -> np.ndarray:
    height, width = image.shape[:2]
    longer_side = max(width, height)
    if size is None:
        size = longer_side
    else:
        if size < longer_side:
            raise ValueError(f'`size={size}` should not smaller than the longer side ({longer_side}) of the image.')
    top = (size - height) // 2
    right = (size - width) // 2
    bottom = size - height - top
    left = size - width - right

    return pad(image, top, right, bottom, left, cval, mode)
