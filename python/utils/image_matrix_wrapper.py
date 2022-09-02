#!/usr/bin/env python3

from utils.image import StrideImage
from typing import Set, Tuple


class ImageMatrixWrapper:
    '''
    Provides row and column accessor helpers for an image with contiguous
    pixel values.
    E.g. a 2x2 matrix which looks like this
    A = [[1, 2],
         [3, 4]]

    would look like this if represented in a contiguous manner:
    B = [1, 2, 3, 4]

    If we wanted to get the value 3 from A we would do something like A[1][0].
    ImageMatrixWrapper allows us to access the value 3 from B in the same
    manner via a    red_pixel_at(1, 0) call, even though the matrix is
    represented as a 1D list.
    [1,0] gets translated into the 1D index value of 2.

    It also adds some helper methods for checking the redness of pixels at
    location [i, j] and reducing the redness of pixels at location [i, j]
    '''

    SMOOTHING_REDUCTION = 150
    RED_THRESHOLD = 200

    def __init__(self, image: StrideImage):
        self._image = image
        self._resolution = image.resolution
        # Holds the coordinates of all indexes which contain a red
        # pixel value of over 200. We don't need to check all
        # pixels in the image to remove a pattern. We only need to
        # check the 'viable' candidates
        self._pattern_coordinate_candidates =\
            self._init_pattern_coordinate_candidates()

    @property
    def resolution(self):
        return self._resolution

    @property
    def image(self):
        return self._image

    @property
    def pattern_coordinate_candidates(self):
        return self._pattern_coordinate_candidates

    def discard_candidate(self, coordinates):
        self._pattern_coordinate_candidates.discard(coordinates)

    def _identify_index_given_row_and_col(self, row: int, col: int) -> int:
        offset = row * self.resolution.width
        return offset + col

    def red_pixel_at(self, row: int, col: int) -> int:
        index = self._identify_index_given_row_and_col(row, col)
        return self._image.pixels_red[index]

    def reduce_red_value_at(self, row: int, col: int):
        index = self._identify_index_given_row_and_col(row, col)
        self._image.pixels_red[index] -= ImageMatrixWrapper.SMOOTHING_REDUCTION

    def is_pixel_red_enough(self, row: int, col: int) -> bool:
        index = self._identify_index_given_row_and_col(row, col)
        red_pixel_value = self._image.pixels_red[index]
        return red_pixel_value >= ImageMatrixWrapper.RED_THRESHOLD

    def _init_pattern_coordinate_candidates(self) -> Set[Tuple[int, int]]:
        '''
        Builds a set of all index locations which are candidates (red >= 200)
        for a starting point of an eye pattern.
        '''
        def to_matrix_coordinates(index) -> Tuple[int, int]:
            x = index // self.resolution.width
            y = index % self.resolution.width
            return (x, y)

        red_enough_indexes = (i
                              for i, p in enumerate(self._image.pixels_red)
                              if p >= ImageMatrixWrapper.RED_THRESHOLD)
        return set(to_matrix_coordinates(i) for i in red_enough_indexes)
