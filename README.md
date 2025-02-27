# HITRAN Parser

A Python tool for parsing HITRAN spectral line files based on molecule and vibrational band criteria.

## Features
- Extracts spectral lines from HITRAN `.par` files.
- Filters data by **molecule, and vibrational band**.
- Currently supports **HCN, H¹³CN, C₂H₂, ¹³CCH₂, CH₄, NH₃, CS** molecules (more to be added).

## Installation

Clone the repository:
```bash
git clone https://github.com/JialLi/HITRAN_Parser.git
cd HITRAN_Parser
```

Ensure you have **Python 2 or 3** and install dependencies (if needed):

```bash
pip install pandas
```

## **Usage**

### **🔹 Show Available Molecules and Bands**

To **print all available molecules and their corresponding vibrational bands**, run:

```python
from parse_hitran import list_available_hitran_selections

# Print available molecules and bands
list_available_hitran_selections()
```

> **Note:** The `"band code"` used in the code will be displayed when listing available molecules and bands. For the corresponding **physical band representations**, see the [Supported Molecules & Bands](#supported-molecules--bands) section.

### **🔹 Extract Data from a HITRAN File**

To extract spectral lines for a specific **molecule and vibrational band**, use the following **example script**:

```python
from parse_hitran import load_hitran_file

# Example HITRAN file path
example_file = "example_HITRAN_CS.par"  # Replace with actual file path

# Load and extract CS v_0 lines from the HITRAN file
cs_data = load_hitran_file(example_file, "CS", "v_0")

print(cs_data.head())  # Display first few lines
```

Make sure to replace `"example_HITRAN.par"` with **your actual HITRAN file**.

## Supported Molecules & Bands

Below is a **list of molecules and their currently supported vibrational bands**.

| Molecule   | Band Code (Used in Code) | Physical Band Representation                      |
| ---------- | ------------------------ | ------------------------------------------------- |
| **HCN**    | v2_0_1                   | ν₂→0                                              |
| **HCN**    | v2_0_2                   | 2ν₂→0                                             |
| **H¹³CN**  | v2_0_1                   | ν₂→0                                              |
| **C₂H₂**   | v5                       | ν₅→0                                              |
| **C₂H₂**   | 2v5^0_v5^1               | 2ν₅<sup>0</sup> → ν₅<sup>1</sup>                  |
| **C₂H₂**   | 2v5^1_v5^1               | 2ν₅<sup>1</sup> → ν₅<sup>1</sup>                  |
| **C₂H₂**   | v4^1+v5^1_v4^1           | ν₄<sup>1</sup> + ν₅<sup>1</sup> → ν₄<sup>1</sup>  |
| **C₂H₂**   | v4^1+v5^-1_v4^1          | ν₄<sup>1</sup> + ν₅<sup>-1</sup> → ν₄<sup>1</sup> |
| **¹³CCH₂** | v5                       | ν₅→0                                              |
| **CH₄**    | v4_0                     | ν₄→0                                              |
| **CH₄**    | 2v4_v4                   | 2ν₄ → ν₄                                          |
| **CH₄**    | 2v4_v2                   | 2ν₄ → ν₂                                          |
| **NH₃**    | v2_0                     | ν₂→0                                              |
| **CS**     | v_0                      | ν→0                                               |
