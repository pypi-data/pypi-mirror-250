# JoyMondalSIG

JoyMondalSIG is a Python package designed to gather system information and check Python installation.

## Installation

You can install the `JoyMondalSIG` package using `pip`. Open your terminal or command prompt and run:

```bash
pip install JoyMondalSIG
```
### Example 
### Retrieving System Information

```bash 
from JoyMondalSIG import get_system_info

# Retrieve system information
system_info = get_system_info()

# Display system information
for key, value in system_info.items():
    print(f"{key}: {value}")

```
### Checking Python Installation
```bash 
from JoyMondalSIG import check_python_installation

# Check if Python is installed and install if not found
check_python_installation()

```
