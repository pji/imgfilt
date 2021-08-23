"""
test_filty
~~~~~~~~~~
"""
import unittest as ut

import numpy as np

from tests.common import ArrayTestCase, A, F, VIDEO_2_3_3, VIDEO_2_5_5
from filty import filty as f


# Base test case.
class FilterTestCase(ArrayTestCase):
    def run_test(self, filter, exp, a=None, *args, **kwargs):
        """Run a basic test case for a filter."""
        # Test data and state.
        if a is None:
            a = A

        # Run test.
        act = filter(a, *args, **kwargs)

        # Determine test result.
        self.assertArrayEqual(exp, act, round_=True)


# Test cases.
class BoxBlurTestCase(FilterTestCase):
    def test_filter(self):
        """Given image data and a box size, perform a box blur on the
        image data.
        """
        filter = f.filter_box_blur
        exp = np.array([
            [0.2500, 0.2500, 0.5000, 0.7500, 0.8750],
            [0.2500, 0.2500, 0.5000, 0.7500, 0.8750],
            [0.5000, 0.5000, 0.7500, 0.8750, 0.7500],
            [0.7500, 0.7500, 0.8750, 0.7500, 0.5000],
            [0.8750, 0.8750, 0.7500, 0.5000, 0.2500],
        ], dtype=np.float32)
        kwargs = {
            'size': 2,
        }
        self.run_test(filter, exp, **kwargs)

    def test_filter_on_video(self):
        """Given three dimensional image data, the blur should be
        performed on all frames of the image data.
        """
        filter = f.filter_box_blur
        exp = np.array([
            [
                [0.2500, 0.2500, 0.5000, 0.7500, 0.8750],
                [0.2500, 0.2500, 0.5000, 0.7500, 0.8750],
                [0.5000, 0.5000, 0.7500, 0.8750, 0.7500],
                [0.7500, 0.7500, 0.8750, 0.7500, 0.5000],
                [0.8750, 0.8750, 0.7500, 0.5000, 0.2500],
            ],
            [
                [0.8750, 0.8750, 0.7500, 0.5000, 0.2500],
                [0.8750, 0.8750, 0.7500, 0.5000, 0.2500],
                [0.7500, 0.7500, 0.8750, 0.7500, 0.5000],
                [0.5000, 0.5000, 0.7500, 0.8750, 0.7500],
                [0.2500, 0.2500, 0.5000, 0.7500, 0.8750],
            ],
        ], dtype=np.float32)
        a = VIDEO_2_5_5.copy()
        kwargs = {
            'size': 2,
        }
        self.run_test(filter, exp, a, **kwargs)


class ColorizeTestCase(FilterTestCase):
    def test_filter(self):
        """Given an RGB color and grayscale image data, the color is
        applied to the image data.
        """
        filter = f.filter_colorize
        exp = np.array([
            [
                [1.0000, 0.0000, 0.1686],
                [0.4980, 0.0000, 0.0824],
                [0.0000, 0.0000, 0.0000],
            ],
            [
                [0.4980, 0.0000, 0.0824],
                [0.0000, 0.0000, 0.0000],
                [0.4980, 0.0000, 0.0824],
            ],
            [
                [0.0000, 0.0000, 0.0000],
                [0.4980, 0.0000, 0.0824],
                [1.0000, 0.0000, 0.1686],
            ],
        ], dtype=np.float32)
        a = F.copy()
        kwargs = {
            'white': 'hsv(350, 100%, 100%)',
            'black': 'hsv(10, 100%, 0%)',
        }
        self.run_test(filter, exp, a, **kwargs)

    def test_filter_by_colorkey(self):
        """Given an RGB color and grayscale image data, the color is
        applied to the image data.
        """
        filter = f.filter_colorize
        exp = np.array([
            [
                [1.0000, 0.0000, 0.1686],
                [0.4980, 0.0000, 0.0824],
                [0.0000, 0.0000, 0.0000],
            ],
            [
                [0.4980, 0.0000, 0.0824],
                [0.0000, 0.0000, 0.0000],
                [0.4980, 0.0000, 0.0824],
            ],
            [
                [0.0000, 0.0000, 0.0000],
                [0.4980, 0.0000, 0.0824],
                [1.0000, 0.0000, 0.1686],
            ],
        ], dtype=np.float32)
        a = F.copy()
        kwargs = {
            'colorkey': 's',
        }
        self.run_test(filter, exp, a, **kwargs)

    def test_filter_on_video(self):
        """Given three-dimensional image data, the filter should
        colorize every frame of the data.
        """
        filter = f.filter_colorize
        exp = np.array([
            [
                [
                    [1.0000, 0.0000, 0.1686],
                    [0.4980, 0.0000, 0.0824],
                    [0.0000, 0.0000, 0.0000],
                ],
                [
                    [0.4980, 0.0000, 0.0824],
                    [0.0000, 0.0000, 0.0000],
                    [0.4980, 0.0000, 0.0824],
                ],
                [
                    [0.0000, 0.0000, 0.0000],
                    [0.4980, 0.0000, 0.0824],
                    [1.0000, 0.0000, 0.1686],
                ],
            ],
            [
                [
                    [1.0000, 0.0000, 0.1686],
                    [0.4980, 0.0000, 0.0824],
                    [0.0000, 0.0000, 0.0000],
                ],
                [
                    [0.4980, 0.0000, 0.0824],
                    [0.0000, 0.0000, 0.0000],
                    [0.4980, 0.0000, 0.0824],
                ],
                [
                    [0.0000, 0.0000, 0.0000],
                    [0.4980, 0.0000, 0.0824],
                    [1.0000, 0.0000, 0.1686],
                ],
            ],
        ], dtype=np.float32)
        a = VIDEO_2_3_3.copy()
        kwargs = {
            'colorkey': 's',
        }
        self.run_test(filter, exp, a, **kwargs)
