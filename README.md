# OpenPrintTagDatabase Search
<p align="center">
  <img src="images/main_pic.png" width="800"><br>
  Simple search for f6fb38 (Variant of yellow.)
</p>

## Features
Python Flask script for searching the OpenPrintTag Database by filament color and optional material type.

The script searches through all material YAML files and returns matching:<br>

- Brands<br>
- Filament names<br>
- material types<br>
- color hex values<br>
- Picture of the filament color and webpage link.
  - (Not available for all filaments in the database)
---

## Example
Searching for a substitute for brand Addnorth PETG Grey.
<p align="center">
  <img src="images/addnorth_grey.png" width="800"><br>
  Addnorth PETG Grey
</p>
<br>
Now we have the correct RGB value to search: #6a6c6eff.<br><br>
<p align="center">
  <img src="images/petg_6a6c6e.png" width="800"><br>
  23 Brands for the correct color (cut of the picture to save space.)
</p>

## Installation
```bash
git clone https://github.com/gertlind/OpenPrintTagDatabase-Color-Search.git
cd OpenPrintTagDatabase-Color-Search
git clone https://github.com/OpenPrintTag/openprinttag-database.git
```
### Create virtual environment
```text
- python3 -m venv .venv
- Activate the virtual environment:
  - source .venv/bin/activate
- Install requirements
  - pip install -r requirements.txt
```

run the script:
```bash
python optdsearch.py

 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5001
 * Running on http://192.168.X.X:5001
```
Or as a [service](docs/service.md)
