#!/usr/bin/env python3

from utils.image import StrideImage
from utils.image_matrix_wrapper import ImageMatrixWrapper
from utils.eye_pattern import BoolEyePattern, BOOL_EYE_PATTERNS


def remove_all_patterns_from_image(image: StrideImage):
    matrix_image = ImageMatrixWrapper(image)
    for pattern in BOOL_EYE_PATTERNS:
        __remove_pattern_from_image(matrix_image, pattern)


def __apply_pattern_removal_at_coordinates(matrix: ImageMatrixWrapper,
                                           pattern: BoolEyePattern,
                                           row_index: int,
                                           col_index: int):

    for pattern_row_index, pattern_row in enumerate(pattern):
        for pattern_col_index, pattern_value in enumerate(pattern_row):
            if not pattern_value:
                continue

            matrix.reduce_red_value_at(row_index+pattern_row_index,
                                       col_index + pattern_col_index)
            # Once we've reduced the red value of a particular pixel,
            # we no longer need to check it in subsequent
            # remove_pattern from_image calls
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


def __remove_pattern_from_image(matrix: ImageMatrixWrapper,
                                pattern: BoolEyePattern):

    removed = True
    while removed:
        removed = False
        # Need to nest two loops because apply_pattern_removal_at_coordinates
        # can modify matrix.red_enough_pixel_positions which would cause issues
        # with the "for x, y in matrix.red_enough_pixel_positions" loop
        # Therefore we restart the loop every single time we remove values
        # from it
        for x, y in matrix.pattern_coordinate_candidates:
            if __does_match_pattern_at_coordinates(matrix, pattern, x, y):
                __apply_pattern_removal_at_coordinates(matrix, pattern, x, y)
                removed = True
                break
