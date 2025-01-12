#!/usr/bin/env python3

from utils.image import StrideImage
from utils.image_matrix_wrapper import ImageMatrixWrapper
from utils.eye_pattern import BoolEyePattern, BOOL_EYE_PATTERNS


def remove_all_patterns_from_image(image: StrideImage):
    matrix = ImageMatrixWrapper(image)
    while matrix.pattern_coordinate_candidates:
        x, y = matrix.pattern_coordinate_candidates.pop()
        for pattern in BOOL_EYE_PATTERNS:
            if __does_match_pattern_at_coordinates(matrix, pattern, x, y):
                __apply_pattern_removal_at_coordinates(
                    matrix, pattern, x, y)
                break


def __apply_pattern_removal_at_coordinates(matrix: ImageMatrixWrapper,
                                           pattern: BoolEyePattern,
                                           row_index: int,
                                           col_index: int):
    '''
    Reduces red pixel values in the image wrapped by matrix.
    The reduced values match the shape of the pattern argument.
    The pattern is overlayed such that its top left pixel matches
    the (x, y) pixel location of (row_index, col_index) in the
    image wrapped by matrix.

    NOTE: mutates the matrix object. The pixel coordinates that
    match the pattern are removed from the pattern candidates set
    stored by the matrix argument.
    '''

    for pattern_row_index, pattern_row in enumerate(pattern):
        for pattern_col_index, pattern_value in enumerate(pattern_row):
            if not pattern_value:
                continue

            matrix.reduce_red_value_at(row_index+pattern_row_index,
                                       col_index + pattern_col_index)
            # Once we've reduced the red value of a particular pixel,
            # we no longer need to check it in subsequent
            # remove_pattern from_image calls. Therefore, we discard it
            # from the pattern candidates set
            # NOTE: this makes the assumptions that patterns don't overlap
            # if patterns overlap, this optimization will lead to incorrect
            # results
            matrix.discard_candidate((row_index+pattern_row_index,
                                      col_index + pattern_col_index))


def __does_match_pattern_at_coordinates(
        matrix: ImageMatrixWrapper,
        pattern: BoolEyePattern,
        row_index: int,
        col_index: int) -> bool:
    '''
    Checks whether the provided pattern is found in the image
    wrapped by the matrix argument.
    The pattern is considered found if all locations in it
    which are True are overlayed over red pixel values greater
    than or equal to 200.
    The pattern is overlayed such that its top left pixel matches
    the (x, y) pixel location of (row_index, col_index) in the
    image wrapped by matrix.
    '''

    pattern_width = len(pattern[0])
    pattern_height = len(pattern)
    if col_index + pattern_width > matrix.resolution.width:
        return False
    if row_index + pattern_height > matrix.resolution.height:
        return False

    for pattern_row_index, krow in enumerate(pattern):
        for pattern_col_index, pattern_value in enumerate(krow):
            if not pattern_value:
                continue

            row_to_test = pattern_row_index + row_index
            col_to_test = col_index + pattern_col_index
            if not matrix.is_pixel_red_enough(row_to_test, col_to_test):
                return False

    return True
