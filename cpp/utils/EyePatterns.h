#ifndef UTILS_EYEPATTERNS_H_
#define UTILS_EYEPATTERNS_H_

#include <array>
#include <string>

//NOTE: don't forget that some symbols need to be escaped
constexpr int32_t EYE_PATTERN_COL_SIZE = 5;
using EyePattern = std::array<const char*, EYE_PATTERN_COL_SIZE>;
using BoolEyePattern = std::array<std::array<bool, EYE_PATTERN_COL_SIZE>, EYE_PATTERN_COL_SIZE>;

constexpr EyePattern EYE_PATTERN_1 {
  "/---\\",
  "|   |",
  "|-o-|",
  "|   |",
  "\\---/"
};

constexpr EyePattern EYE_PATTERN_2 {
  "/---\\",
  "| | |",
  "| 0 |",
  "| | |",
  "\\---/"
};

constexpr EyePattern EYE_PATTERN_3 {
  "/---\\",
  "| | |",
  "|-q-|",
  "| | |",
  "\\---/"
};

constexpr EyePattern EYE_PATTERN_4 {
  "/---\\",
  "|\\ /|",
  "| w |",
  "|/ \\|",
  "\\---/"
};

constexpr int32_t EYE_PATTERNS_COUNT = 4;
constexpr std::array<EyePattern, EYE_PATTERNS_COUNT> EYE_PATTERNS {
  EYE_PATTERN_1, EYE_PATTERN_2, EYE_PATTERN_3, EYE_PATTERN_4
};

constexpr BoolEyePattern convertEyePatternToBoolPattern(EyePattern input) {
  BoolEyePattern pattern{};
  int currentPatternLineIndex = 0;
  for (const auto line : input) {
    for (int i = 0; i < EYE_PATTERN_COL_SIZE; i++) {
      char c = *(line+i);
      if (c == ' ') {
        pattern[currentPatternLineIndex][i] = false;
      } else {
        pattern[currentPatternLineIndex][i] = true;
      }
    }
    ++currentPatternLineIndex;
  }
  return pattern;
}

constexpr std::array<BoolEyePattern, EYE_PATTERNS_COUNT> BOOL_EYE_PATTERNS {
  convertEyePatternToBoolPattern(EYE_PATTERN_4),
  convertEyePatternToBoolPattern(EYE_PATTERN_3),
  convertEyePatternToBoolPattern(EYE_PATTERN_2),
  convertEyePatternToBoolPattern(EYE_PATTERN_1),
};

#endif /* UTILS_EYEPATTERNS_H_ */
