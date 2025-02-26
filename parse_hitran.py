# MIT License
# 
# Copyright (c) 2025 Jialu Li (https://github.com/JialLi)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is provided
# to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""
HITRAN Parser: A Python tool for parsing HITRAN spectral line files based on molecule and vibrational band criteria.

Author: Jialu Li (https://github.com/JialLi) 
License: MIT License
Version: 1.0
"""

# (Rest of your code starts here)


import pandas as pd

# Define molecule and band-specific parsing rules
HITRAN_RULES = {
    "HCN": {  # Hydrogen cyanide
        "v2_0_1": {
            "wavenumber": 1,  # Wavenumber (cm^-1)
            "wavelength": lambda x: 1e4 / float(x[1]),  # Convert wavenumber to wavelength (um)
            "einstein_A": lambda x: float(x[3][:9]),  # Einstein A (extracting only first 9 characters)
            "energy": lambda x: float(x[4][:-12]),  # Lower state energy (removing last 12 characters)
            "gu": -2,  # Second-to-last column
            "gl": -1,  # Last column
            "band_columns": (5, 13),  # Vibrational band (multi-column)
            "band_criteria": "0 1 1 0 0 0 0 0",  # Required values for v2_0
            "line_name": lambda x: "".join(x[13:15]),  # Transition type (concatenated)
        },
        
        "v2_0_2": {  # Another HCN vibrational band
            "wavenumber": 1,
            "wavelength": lambda x: 1e4 / float(x[1]),
            "einstein_A": lambda x: float(x[3][:9]),
            "energy": lambda x: float(x[4][:-12]),
            "gu": -2,
            "gl": -1,
            "band_columns": (5, 13),
            "band_criteria": "0 2 0 0 0 0 0 0",
            "line_name": lambda x: "".join(x[13:15]),
        }
    },

    "H13CN": {  # Hydrogen cyanide
        "v2_0_1": {
            "wavenumber": 1,  # Wavenumber (cm^-1)
            "wavelength": lambda x: 1e4 / float(x[1]),  # Convert wavenumber to wavelength (um)
            "einstein_A": lambda x: float(x[3][:9]),  # Einstein A (extracting only first 9 characters)
            "energy": lambda x: float(x[4][:-12]),  # Lower state energy (removing last 12 characters)
            "gu": -2,  # Second-to-last column
            "gl": -1,  # Last column
            "band_columns": (5, 13),  # Vibrational band (multi-column)
            "band_criteria": "0 1 1 0 0 0 0 0",  # Required values for v2_0
            "line_name": lambda x: "".join(x[13:15]),  # Transition type (concatenated)
        },
    },
        
    "C2H2": {  # Acetylene
        "v5": {
            "wavenumber": 1,
            "wavelength": lambda x: 1e4 / float(x[1]),
            "einstein_A": lambda x: float(x[3][:9]),
            "energy": lambda x: float(x[4][:-12]),
            "gu": -2,
            "gl": -1,
            "band_columns": (5, 17),
            "band_criteria": "000 0 1 0 1 u 000 0 0 0 0+ g",
            "line_name": lambda x: "".join(x[17:19]),
        },
        "2v5^0_v5^1": {
            "wavenumber": 1,
            "wavelength": lambda x: 1e4 / float(x[1]),
            "einstein_A": lambda x: float(x[3][:9]),
            "energy": lambda x: float(x[4][:-12]),
            "gu": -2,
            "gl": -1,
            "band_columns": (5, 17),
            "band_criteria": "000 0 2 0 0+ g 000 0 1 0 1 u",
            "line_name": lambda x: "".join(x[17:19]),
        },
        "2v5^1_v5^1": {
            "wavenumber": 1,
            "wavelength": lambda x: 1e4 / float(x[1]),
            "einstein_A": lambda x: float(x[3][:9]),
            "energy": lambda x: float(x[4][:-12]),
            "gu": -2,
            "gl": -1,
            "band_columns": (5, 17),
            "band_criteria": "000 0 2 0 2 g 000 0 1 0 1 u",
            "line_name": lambda x: "".join(x[17:19]),
        },
        "v4^1+v5^1_v4^1": {
            "wavenumber": 1,
            "wavelength": lambda x: 1e4 / float(x[1]),
            "einstein_A": lambda x: float(x[3][:9]),
            "energy": lambda x: float(x[4][:-12]),
            "gu": -2,
            "gl": -1,
            "band_columns": (5, 17),
            "band_criteria": "000 1 1 1 1 u 000 1 0 1 0 g",
            "line_name": lambda x: "".join(x[17:19]),
        },
        "v4^1+v5^-1_v4^1": {
            "wavenumber": 1,
            "wavelength": lambda x: 1e4 / float(x[1]),
            "einstein_A": lambda x: float(x[3][:9]),
            "energy": lambda x: float(x[4][:-12]),
            "gu": -2,
            "gl": -1,
            "band_columns": (5, 16),
            "band_criteria": "000 1 1 1-1+ u 000 1 0 1 0 g",
            "line_name": lambda x: "".join(x[16:18]),
        },
    },

    # Add more molecules and bands here
    "13CCH2": { 
        "v5": {
            "wavenumber": 1,
            "wavelength": lambda x: 1e4 / float(x[1]),
            "einstein_A": lambda x: float(x[3][:9]),
            "energy": lambda x: float(x[4][:-12]),
            "gu": -2,
            "gl": -1,
            "band_columns": (5, 17),
            "band_criteria": "000 0 1 0 1 u 000 0 0 0 0+ g",
            "line_name": lambda x: "".join(x[17:19]),
        },
    
    },

    "CH4": { 
        "v4_0": {
            "wavenumber": 1,
            "wavelength": lambda x: 1e4 / float(x[1]),
            "einstein_A": lambda x: float(x[3][:9]),
            "energy": lambda x: float(x[4][:-12]),
            "gu": -2,
            "gl": -1,
            "band_columns": (5, 15),
            "band_criteria": "0 0 0 1 1F2 0 0 0 0 1A1",
            "line_name": lambda x: ",".join(x[15:19]),
        },
        "2v4_v4": {
            "wavenumber": 1,
            "wavelength": lambda x: 1e4 / float(x[1]),
            "einstein_A": lambda x: float(x[3][:9]),
            "energy": lambda x: float(x[4][:-12]),
            "gu": -2,
            "gl": -1,
            "band_columns": (5, 15),
            "band_criteria": "0 0 0 2 1F2 0 0 0 1 1F2",
            "line_name": lambda x: ",".join(x[15:19]),
        },    
        "2v4_v2": {
            "wavenumber": 1,
            "wavelength": lambda x: 1e4 / float(x[1]),
            "einstein_A": lambda x: float(x[3][:9]),
            "energy": lambda x: float(x[4][:-12]),
            "gu": -2,
            "gl": -1,
            "band_columns": (5, 15),
            "band_criteria": [
                "0 0 0 2 1A1 0 1 0 0 1E",
                "0 0 0 2 1F2 0 1 0 0 1E",
                "0 0 0 2 1E 0 1 0 0 1E"
            ],
            "line_name": lambda x: ",".join(x[15:19]),
        },   

    },

    "NH3": { 
        "v2_0": {
            "wavenumber": 1,
            "wavelength": lambda x: 1e4 / float(x[1]),
            "einstein_A": lambda x: float(x[3][:9]),
            "energy": lambda x: float(x[4][:-12]),
            "gu": -2,
            "gl": -1,
            "band_columns": (5, 13),
            "band_criteria": [
                "0100 00 0 A2\" 0000 00 0 A1'",
                "0100 00 0 A1' 0000 00 0 A1'",
                "0100 00 0 A2\" 0000 00 0 A2\"",
                "0100 00 0 A1' 0000 00 0 A2\""
            ],
            "line_name": lambda x: ",".join(x[13:-8]),
        },   

    },

    "CS": { 
        "v_0": {
            "wavenumber": 1,
            "wavelength": lambda x: 1e4 / float(x[1]),
            "einstein_A": lambda x: float(x[3][:9]),
            "energy": lambda x: float(x[4][:-12]),
            "gu": -2,
            "gl": -1,
            "band_columns": (5, 7),
            "band_criteria": "1 0",
            "line_name": lambda x: "".join(x[7:9]),
        },   

    },
            
}

def load_hitran_file(file_path, molecule_name, band_name="default"):
    """
    Parses a HITRAN .par file and extracts spectral line information, following user-defined molecule & band-specific rules.

    Parameters:
    - file_path (str): Path to the HITRAN .par file.
    - molecule_name (str): Name of the molecule (e.g., 'HCN', 'C2H2').
    - band_name (str): Specific vibrational band to apply different rules (e.g., 'v2_0', 'v1_0').

    Returns:
    - DataFrame with columns: ['Wavenumber', 'Wavelength', 'Einstein A', 'Energy', 'Band', 'Line Name', 'gu', 'gl']
    """

    # Check if molecule is defined
    if molecule_name not in HITRAN_RULES:
        raise ValueError("Molecule '{}' is not defined in HITRAN_RULES!".format(molecule_name))

    # Check if the band name exists for the molecule
    if band_name not in HITRAN_RULES[molecule_name]:
        raise ValueError("Band '{}' is not defined for molecule '{}'!".format(band_name, molecule_name))

    # Get the specific rule set for the molecule & band
    col_map = HITRAN_RULES[molecule_name][band_name]

    # Read file line by line
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            x = line.split()

            # Extract band values and convert to a string
            extracted_band_values = " ".join(x[col_map["band_columns"][0]:col_map["band_columns"][1]])

            # Compare extracted band string to the expected criteria
            if extracted_band_values not in col_map["band_criteria"]:
                continue  # Skip lines that do not match the vibrational band criteria

            # Extract required values dynamically based on rules
            wavenumber = float(x[col_map["wavenumber"]])
            wavelength = col_map["wavelength"](x)
            einstein_A = col_map["einstein_A"](x)
            lower_energy = col_map["energy"](x)
            gu = float(x[col_map["gu"]])
            gl = float(x[col_map["gl"]])
            line_name = col_map["line_name"](x)
            vibrational_band = extracted_band_values  # Store matched band

            # Store extracted values
            data.append([wavenumber, wavelength, einstein_A, lower_energy, vibrational_band, line_name, gu, gl])

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=['Wavenumber', 'Wavelength', 'Einstein A', 'Energy_cm', 'Band', 'LineName', 'gu', 'gl'])

    return df



def list_available_hitran_selections():
    """
    Prints all available molecules and their corresponding vibrational bands
    from the HITRAN_RULES dictionary.
    """
    print("\n=== Available HITRAN Selections ===\n")
    for molecule, bands in HITRAN_RULES.items():
        print("Molecule: {}".format(molecule))
        print("  Available Bands:")
        for band in bands.keys():
            print("   - {}".format(band))
        print("")


