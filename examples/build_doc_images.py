"""
build_doc_images
~~~~~~~~~~~~~~~~

Build the documentation images for :mod:`imgfilt`.
"""
from argparse import ArgumentParser
from copy import deepcopy
from pathlib import Path
from typing import Callable

import imggen as ig
import imgwriter as iw
import numpy as np

import imgfilt as ift


# Constants.
X, Y, Z = -1, -2, -3


# Make the example images.
def make_base_image(size: ig.Size) -> ig.ImgAry:
    """Make the base image to run filters on."""
    source = ig.Hexes(radius=51)
    text = ig.Text(
        'SPAM',
        font='Menlo',
        size=525,
        face=1,
        origin=(0, 60),
        fill_color=0.25,
        bg_color=0.0,
        align='center'
    )
    a = source.fill(size)
    a += text.fill(size)
    a /= 2
    a += 0.25
    return a


def make_image(
    a: ig.ImgAry,
    filter: Callable,
    kwargs: dict,
    size: ig.Size,
    color: bool = False
) -> ig.ImgAry:
    """Make an example image for a filter."""
    # Filter the image data.
    filtered = filter(a, **kwargs)
    
    # Because we are putting the filtered data back into the bottom half
    # of the original data, work needs to be done to make sure the shape
    # of the filtered data matches the shape of the bottom half of the
    # original data.
    if color:
        a = ift.filter_colorize(a)
        
    if filtered.shape != a.shape and not color:
        mshape = tuple(max(a, b) for a, b in zip(a.shape, filtered.shape))
        m = np.zeros(mshape, dtype=filtered.dtype)
        mstarts = [(mn - fn) // 2 for mn, fn in zip(mshape, filtered.shape)]
        mstops = [ms + fn for ms, fn in zip(mstarts, filtered.shape)]
        m[
            mstarts[Z]:mstops[Z], mstarts[Y]:mstops[Y], mstarts[X]:mstops[X]
        ] = filtered
        fstarts = [(mn - an) // 2 for mn, an in zip(mshape, a.shape)]
        fstops = [sn + an for sn, an in zip(fstarts, a.shape)]
        filtered = m[
            fstarts[Z]:fstops[Z], fstarts[Y]:fstops[Y], fstarts[X]:fstops[X]
        ]
    
    # Replace the bottom half of the image data with the filtered data.
    midheight = size[Y] // 2
    a[:, midheight:, :] = filtered[:, midheight:, :]
    
    # Add the label.
    label, ystart, ystop = make_label(size)
    if color:
        label = ift.filter_colorize(label)
    a[:, ystart:ystop, :] = label
    return a


def make_images(path: Path, size: ig.Size, ext: str = 'jpg') -> None:
    """Make the example images."""
    filters = [
        (ift.filter_box_blur, {'size': size[X] // 32,}, False),
        (ift.filter_colorize, {'colorkey': 'g',}, True),
        (ift.filter_contrast, {}, False),
        (ift.filter_flip, {'axis': X,}, False),
        (ift.filter_gaussian_blur, {'sigma': 12.0,}, False),
        (ift.filter_glow, {'sigma': 3,}, False),
        (ift.filter_grow, {'factor': 2,}, False),
        (ift.filter_inverse, {}, False),
        (ift.filter_linear_to_polar, {}, False),
        (ift.filter_motion_blur, {'amount': size[X] // 32, 'axis': X}, False),
        (ift.filter_pinch, {
            'amount': 0.5,
            'radius': size[X] // 3,
            'scale': (0, 0.5, 0.5),
            'offset': (0, 0, 0)
        }, False),
        (ift.filter_polar_to_linear, {}, False),
        (ift.filter_ripple, {
            'wave': (0, size[Y] // 5, size[Y] // 5),
            'amp': (0, size[Y] // 80, size[Y] // 80),
            'distaxis': (Z, Y, X),
        }, False),
        (ift.filter_rotate_90, {}, False),
        (ift.filter_skew, {'slope': 0.25,}, False),
        (ift.filter_twirl, {
            'radius': size[X],
            'strength': 3,
        }, False),
    ]
    for item in filters:
        a = make_base_image(size)
        filter, kwargs, color = item
        fname = f'{filter.__name__}.{ext}'
        print(f'Making {fname}...')
        a = make_image(a, filter, kwargs, size, color)
        iw.write(path / fname, a)
        print(f'{fname} made.')


def make_label(size: ig.Size) -> tuple[ig.ImgAry, int, int]:
    """Make the label to insert between the halves of the example image."""
    # Original side.
    oheight = int(size[Y] * 1.1 // 12)
    origin = (size[X] // 10, oheight // 20)
    text_orig = ig.Text(
        '\u25b2 ORIGINAL \u25b2',
        font='Menlo',
        size=size[Y] // 30,
        origin=origin
    )
    height = int(size[Y] * 1.1 // 24)
    label = text_orig.fill((size[Z], height, size[X]))
    
    # Filtered side.
    origin = (size[X] * 8 // 10, oheight // 20)
    text_filt = ig.Text(
        '\u25bc FILTER \u25bc',
        font='Menlo',
        size=size[Y] // 30,
        origin=origin
    )
    height = int(size[Y] * 1.1 // 24)
    label += text_filt.fill((size[Z], height, size[X]))

    # Cap the color values.
    label[label > 1.0] = 1.0
    label[label < 0.0] = 0.0
    
    # Locate the label in the image.
    ystart = size[Y] // 2 - height // 2
    ystop = ystart + height
    return label, ystart, ystop
    

# Mainline.
if __name__ == '__main__':
    p = ArgumentParser(
        description='Generate images for the documentation for imggen.',
        prog='imggen'
    )
    p.add_argument(
        '--outdir', '-o',
        action='store',
        default=Path('docs/source/images'),
        help='The directory to save the images.',
        type=Path
    )
    p.add_argument(
        '--size', '-s',
        action='store',
        default=(1280, 720),
        help='The height and width dimensions of the images.',
        nargs=2,
        type=int
    )
    args = p.parse_args()

    size = (1, args.size[1], args.size[0])
    path = args.outdir
    make_images(path, size)
    