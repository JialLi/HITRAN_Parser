# MIT License
#
# Copyright (c) 2025 Jialu Li (https://github.com/JialLi)
#
# This example script is distributed under the MIT License.
# See the LICENSE file for details.

"""
Example usage of the HITRAN Parser.

This script demonstrates how to extract spectral lines for a specific
molecule and vibrational band from a HITRAN .par file.

Author: Jialu Li (https://github.com/JialLi)
"""

from parse_hitran import load_hitran_file, list_available_hitran_selections

# Show available molecules and bands
list_available_hitran_selections()

# Example HITRAN file path
example_file = "example_HITRAN_CS.par"  # Replace with actual file; CS from 728 to 1285 cm-1 here.

# Extract CS lines
cs_data = load_hitran_file(example_file, "CS", "v_0")

print(cs_data.head())  # Display first few lines

