"""
test_filty
~~~~~~~~~~
"""
import unittest as ut

import numpy as np

from tests.common import (ArrayTestCase, A, F, VIDEO_2_3_3, VIDEO_2_5_5,
                          IMAGE_5_5_LOW_CONTRAST)
from filty import filty as f


# Base test case.
class FilterTestCase(ArrayTestCase):
    def run_test(self, filter, exp, a=None, *args, **kwargs):
        """Run a basic test case for a filter."""
        # Test data and state.
        if a is None:
            a = A.copy()

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


class ContrastTestCase(FilterTestCase):
    def test_filter(self):
        """Given image data, adjust the range of the data to ensure
        the darkest color is black and the lightest is white.
        """
        filter = f.filter_contrast
        exp = np.array([
            [0.0000, 0.2500, 0.5000, 0.7500, 1.0000],
            [0.0000, 0.2500, 0.5000, 0.7500, 1.0000],
            [0.0000, 0.2500, 0.5000, 0.7500, 1.0000],
            [0.0000, 0.2500, 0.5000, 0.7500, 1.0000],
            [0.0000, 0.2500, 0.5000, 0.7500, 1.0000],
        ], dtype=np.float32)
        a = IMAGE_5_5_LOW_CONTRAST.copy()
        self.run_test(filter, exp, a)


class FlipTestCase(FilterTestCase):
    def test_filter(self):
        """Given image data and an axis, flip the image around
        that axis.
        """
        filter = f.filter_flip
        exp = np.array([
            [1.0000, 0.7500, 0.5000, 0.2500, 0.0000],
            [0.7500, 1.0000, 0.7500, 0.5000, 0.2500],
            [0.5000, 0.7500, 1.0000, 0.7500, 0.5000],
            [0.2500, 0.5000, 0.7500, 1.0000, 0.7500],
            [0.0000, 0.2500, 0.5000, 0.7500, 1.0000],
        ], dtype=np.float32)
        kwarg = {
            'axis': f.X,
        }
        self.run_test(filter, exp, **kwarg)

    def test_flip_y_axis(self):
        """Given image data and an axis, flip the image around
        that axis.
        """
        filter = f.filter_flip
        exp = np.array([
            [1.0000, 0.7500, 0.5000, 0.2500, 0.0000],
            [0.7500, 1.0000, 0.7500, 0.5000, 0.2500],
            [0.5000, 0.7500, 1.0000, 0.7500, 0.5000],
            [0.2500, 0.5000, 0.7500, 1.0000, 0.7500],
            [0.0000, 0.2500, 0.5000, 0.7500, 1.0000],
        ], dtype=np.float32)
        kwarg = {
            'axis': f.X,
        }
        self.run_test(filter, exp, **kwarg)

    def test_flip_z_axis(self):
        """Given image data and an axis, flip the image around
        that axis.
        """
        filter = f.filter_flip
        exp = np.array([
            [
                [1.0000, 0.7500, 0.5000, 0.2500, 0.0000],
                [0.7500, 1.0000, 0.7500, 0.5000, 0.2500],
                [0.5000, 0.7500, 1.0000, 0.7500, 0.5000],
                [0.2500, 0.5000, 0.7500, 1.0000, 0.7500],
                [0.0000, 0.2500, 0.5000, 0.7500, 1.0000],
            ],
            [
                [0.0000, 0.2500, 0.5000, 0.7500, 1.0000],
                [0.2500, 0.5000, 0.7500, 1.0000, 0.7500],
                [0.5000, 0.7500, 1.0000, 0.7500, 0.5000],
                [0.7500, 1.0000, 0.7500, 0.5000, 0.2500],
                [1.0000, 0.7500, 0.5000, 0.2500, 0.0000],
            ],
        ], dtype=np.float32)
        a = VIDEO_2_5_5.copy()
        kwarg = {
            'axis': f.Z,
        }
        self.run_test(filter, exp, a, **kwarg)


class GaussianBlurTestCase(FilterTestCase):
    def test_filter(self):
        """Given image data and a sigma, perform a gaussian blur
        on the image data.
        """
        filter = f.filter_gaussian_blur
        exp = np.array([
            [0.1070, 0.3036, 0.5534, 0.7918, 0.9158],
            [0.3036, 0.5002, 0.7442, 0.9046, 0.7918],
            [0.5534, 0.7442, 0.9044, 0.7442, 0.5534],
            [0.7918, 0.9046, 0.7442, 0.5002, 0.3036],
            [0.9158, 0.7918, 0.5534, 0.3036, 0.1070],
        ], dtype=np.float32)
        kwarg = {
            'sigma': 0.5,
        }
        self.run_test(filter, exp, **kwarg)

    def test_blur_video(self):
        """Given image data and a sigma, perform a gaussian blur
        on the image data.
        """
        filter = f.filter_gaussian_blur
        exp = np.array([
            [
                [0.2436, 0.4099, 0.5535, 0.6968, 0.7564],
                [0.3565, 0.5952, 0.7500, 0.8516, 0.6435],
                [0.5000, 0.7499, 0.9465, 0.7499, 0.5000],
                [0.6435, 0.8516, 0.7500, 0.5952, 0.3565],
                [0.7564, 0.6968, 0.5535, 0.4099, 0.2436],
            ],
            [
                [0.7564, 0.6968, 0.5535, 0.4099, 0.2436],
                [0.6435, 0.8516, 0.7500, 0.5952, 0.3565],
                [0.5000, 0.7499, 0.9465, 0.7499, 0.5000],
                [0.3565, 0.5952, 0.7500, 0.8516, 0.6435],
                [0.2436, 0.4099, 0.5535, 0.6968, 0.7564],
            ],
        ], dtype=np.float32)
        a = VIDEO_2_5_5.copy()
        kwarg = {
            'sigma': 0.5,
        }
        self.run_test(filter, exp, a, **kwarg)


class GrowTestCase(FilterTestCase):
    def test_filter(self):
        """Given image data and a size factor, zoom into the image
        by the size factor.
        """
        filter = f.filter_grow
        exp = np.array([
            [
                [1.0000, 0.7500, 0.5000, 0.2500, 0.0000, 0.0000],
                [0.7500, 0.5000, 0.2500, 0.2500, 0.2500, 0.2500],
                [0.5000, 0.2500, 0.0000, 0.2500, 0.5000, 0.5000],
                [0.2500, 0.2500, 0.2500, 0.5000, 0.7500, 0.7500],
                [0.0000, 0.2500, 0.5000, 0.7500, 1.0000, 1.0000],
                [0.0000, 0.2500, 0.5000, 0.7500, 1.0000, 1.0000],
            ],
            [
                [1.0000, 0.7500, 0.5000, 0.2500, 0.0000, 0.0000],
                [0.7500, 0.5000, 0.2500, 0.2500, 0.2500, 0.2500],
                [0.5000, 0.2500, 0.0000, 0.2500, 0.5000, 0.5000],
                [0.2500, 0.2500, 0.2500, 0.5000, 0.7500, 0.7500],
                [0.0000, 0.2500, 0.5000, 0.7500, 1.0000, 1.0000],
                [0.0000, 0.2500, 0.5000, 0.7500, 1.0000, 1.0000],
            ],
            [
                [1.0000, 0.7500, 0.5000, 0.2500, 0.0000, 0.0000],
                [0.7500, 0.5000, 0.2500, 0.2500, 0.2500, 0.2500],
                [0.5000, 0.2500, 0.0000, 0.2500, 0.5000, 0.5000],
                [0.2500, 0.2500, 0.2500, 0.5000, 0.7500, 0.7500],
                [0.0000, 0.2500, 0.5000, 0.7500, 1.0000, 1.0000],
                [0.0000, 0.2500, 0.5000, 0.7500, 1.0000, 1.0000],
            ],
            [
                [1.0000, 0.7500, 0.5000, 0.2500, 0.0000, 0.0000],
                [0.7500, 0.5000, 0.2500, 0.2500, 0.2500, 0.2500],
                [0.5000, 0.2500, 0.0000, 0.2500, 0.5000, 0.5000],
                [0.2500, 0.2500, 0.2500, 0.5000, 0.7500, 0.7500],
                [0.0000, 0.2500, 0.5000, 0.7500, 1.0000, 1.0000],
                [0.0000, 0.2500, 0.5000, 0.7500, 1.0000, 1.0000],
            ],
        ], dtype=np.float32)
        a = VIDEO_2_3_3.copy()
        kwarg = {
            'factor': 2,
        }
        self.run_test(filter, exp, a, **kwarg)

    def test_two_dimensional_grow(self):
        """Given image data and a size factor, zoom into the image
        by the size factor. This should work on still image data.
        """
        filter = f.filter_grow
        exp = np.array([
            [1.0000, 0.7500, 0.5000, 0.2500, 0.0000, 0.0000],
            [0.7500, 0.5000, 0.2500, 0.2500, 0.2500, 0.2500],
            [0.5000, 0.2500, 0.0000, 0.2500, 0.5000, 0.5000],
            [0.2500, 0.2500, 0.2500, 0.5000, 0.7500, 0.7500],
            [0.0000, 0.2500, 0.5000, 0.7500, 1.0000, 1.0000],
            [0.0000, 0.2500, 0.5000, 0.7500, 1.0000, 1.0000],
        ], dtype=np.float32)
        a = F.copy()
        kwarg = {
            'factor': 2,
        }
        self.run_test(filter, exp, a, **kwarg)


class InverseTestCase(FilterTestCase):
    def test_filter(self):
        """Given image data, invert the colors of the image data."""
        filter = f.filter_inverse
        exp = np.array([
            [1.0000, 0.7500, 0.5000, 0.2500, 0.0000],
            [0.7500, 0.5000, 0.2500, 0.0000, 0.2500],
            [0.5000, 0.2500, 0.0000, 0.2500, 0.5000],
            [0.2500, 0.0000, 0.2500, 0.5000, 0.7500],
            [0.0000, 0.2500, 0.5000, 0.7500, 1.0000],
        ], dtype=np.float32)
        self.run_test(filter, exp)


class LinearToPolarTestCase(FilterTestCase):
    def test_filter(self):
        """Given image data, invert the colors of the image data."""
        filter = f.filter_linear_to_polar
        exp = np.array([
            [0.0000, 0.2500, 0.0000, 0.0000, 0.0000],
            [0.2500, 0.5000, 0.7500, 0.5000, 0.2500],
            [0.2500, 0.7500, 1.0000, 0.7500, 0.5000],
            [0.5000, 1.0000, 0.7500, 0.5000, 0.5000],
            [0.5000, 0.7500, 1.0000, 0.7500, 1.0000],
        ], dtype=np.float32)
        self.run_test(filter, exp)
